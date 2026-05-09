"""
EV PM DSS - Chainlit Frontend Application
电动汽车产品管理决策支持系统 - Chainlit 前端

Author: EV PM DSS Team
Date: 2026-02-15
"""

import chainlit as cl
from chainlit.input_widget import Select, Slider
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to enable imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import RAG tools
from rag.tools import (
    VectorRetriever,
    GraphRetriever,
    HybridRetriever,
    QueryAnalyzer,
    format_ugc_context,
    format_vehicle_comparison,
    format_ipa_scores
)
from rag.config import get_deepseek_client

# Load environment variables from offline-pipeline/.env by default.
ENV_FILE = current_dir.parent / ".env"
load_dotenv(dotenv_path=ENV_FILE)

# ==================== Configuration ====================
APP_TITLE = "EV PM DSS | 电动汽车 PM 决策支持系统"
APP_DESCRIPTION = """
欢迎使用 **EV PM DSS** - 基于知识图谱和向量数据库的智能决策支持系统。

### 核心功能
- 📊 **User Insights**: 深度用户画像分析
- ⚔️ **Competitor Analysis**: 智能竞品对比
- 📝 **PRD Writer**: AI 辅助需求文档撰写

请从左侧菜单选择功能模块开始使用。
"""

# Initialize tools (lazy loading)
vector_retriever = None
graph_retriever = None
hybrid_retriever = None
query_analyzer = None
llm_client = None


def get_tools():
    """获取工具实例（延迟加载）"""
    global vector_retriever, graph_retriever, hybrid_retriever, query_analyzer, llm_client
    
    if llm_client is None:
        llm_client = get_deepseek_client()
    
    if vector_retriever is None:
        vector_retriever = VectorRetriever()
    if graph_retriever is None:
        graph_retriever = GraphRetriever()
    if hybrid_retriever is None:
        hybrid_retriever = HybridRetriever()
    if query_analyzer is None:
        query_analyzer = QueryAnalyzer(llm_client)
    
    return vector_retriever, graph_retriever, hybrid_retriever, query_analyzer, llm_client


# ==================== Chat Profiles (侧边栏模块选择) ====================
@cl.set_chat_profiles
async def chat_profile():
    """定义聊天配置文件（侧边栏显示）"""
    return [
        cl.ChatProfile(
            name="User Insights",
            markdown_description="📊 **用户洞察分析**\n\n基于知识图谱的 8 个权威用户画像，深度分析用户需求和痛点。",
            icon="https://api.dicebear.com/7.x/shapes/svg?seed=user"
        ),
        cl.ChatProfile(
            name="Competitor Analysis",
            markdown_description="⚔️ **竞品对比分析**\n\n混合检索车型参数和用户评论，生成专业竞品分析报告。",
            icon="https://api.dicebear.com/7.x/shapes/svg?seed=comp"
        ),
        cl.ChatProfile(
            name="PRD Writer",
            markdown_description="📝 **PRD 文档撰写**\n\n全栈数据驱动，自动生成结构化产品需求文档。",
            icon="https://api.dicebear.com/7.x/shapes/svg?seed=prd"
        ),
    ]


# ==================== Startup ====================
@cl.on_chat_start
async def start():
    """应用启动时的初始化"""
    
    import time
    session_id = id(cl.user_session)
    
    # 检查是否已经初始化过（避免重复显示欢迎消息）
    already_initialized = cl.user_session.get("initialized", False)
    
    if already_initialized:
        print(f"\n⚠️ [会话 {session_id}] 检测到重新初始化，跳过欢迎消息\n")
        return
    
    print(f"\n{'='*80}")
    print(f"🚀 [新会话 {session_id}] 开始")
    print(f"   时间: {time.strftime('%H:%M:%S')}")
    print(f"{'='*80}\n")
    
    # 标记已初始化
    cl.user_session.set("initialized", True)
    
    # 获取当前选择的模块
    chat_profile = cl.user_session.get("chat_profile")
    module_name = chat_profile if chat_profile else "User Insights"
    
    # 初始化会话历史
    cl.user_session.set("chat_history", [])
    cl.user_session.set("current_module", module_name)
    
    # 发送欢迎消息
    welcome_msg = f"""**欢迎使用 EV PM DSS** 🚗

当前模块: **{module_name}**

您可以随时从左侧切换到其他模块。每个模块都有独立的对话历史。

---
{APP_DESCRIPTION}
"""
    
    await cl.Message(
        content=welcome_msg,
        author="System"
    ).send()
    
    # 初始化工具
    try:
        get_tools()
        await cl.Message(
            content="✅ 系统初始化完成，向量库和图数据库已连接。",
            author="System"
        ).send()
    except Exception as e:
        await cl.Message(
            content=f"⚠️ 系统初始化警告：{str(e)}\n部分功能可能不可用，请检查 offline-pipeline/.env 配置。",
            author="System"
        ).send()


def _build_history_text(max_rounds: int = 3) -> str:
    """构建最近 N 轮对话历史文本，用于注入 LLM prompt。
    
    每条消息截断到 300 字符，避免历史过长占用 token。
    如果没有历史（第一轮对话），返回空字符串。
    """
    chat_history = cl.user_session.get("chat_history", [])
    # 排除最后一条（即当前用户消息，已经作为 user_query 传入 prompt）
    history = chat_history[:-1] if chat_history else []
    if not history:
        return ""
    
    # 取最近 max_rounds 轮（每轮 = 1 user + 1 assistant = 2 条）
    recent = history[-(max_rounds * 2):]
    
    lines = []
    for msg in recent:
        role = "用户" if msg["role"] == "user" else "助手"
        content = msg["content"]
        if len(content) > 300:
            content = content[:300] + "..."
        lines.append(f"{role}: {content}")
    
    return "\n【对话历史（最近 {} 轮）】\n{}\n".format(
        min(max_rounds, len(recent) // 2 + 1),
        "\n".join(lines)
    )


def _save_assistant_reply(answer_text: str):
    """将 assistant 回复保存到 chat_history。"""
    chat_history = cl.user_session.get("chat_history", [])
    # 截断保存，避免历史膨胀
    chat_history.append({"role": "assistant", "content": answer_text[:500]})
    cl.user_session.set("chat_history", chat_history)


# ==================== Message Handler ====================
@cl.on_message
async def main(message: cl.Message):
    """处理用户消息"""
    
    import time
    start_time = time.time()
    session_id = id(cl.user_session)
    
    print(f"\n{'='*80}")
    print(f"📨 [会话 {session_id}] 收到新消息")
    print(f"   时间: {time.strftime('%H:%M:%S')}")
    print(f"   内容: {message.content[:50]}...")
    print(f"{'='*80}\n")
    
    # 获取当前模块（从 chat profile）
    current_module = cl.user_session.get("chat_profile", "User Insights")
    
    # 获取对话历史
    chat_history = cl.user_session.get("chat_history", [])
    
    # 添加用户消息到历史
    chat_history.append({"role": "user", "content": message.content})
    cl.user_session.set("chat_history", chat_history)
    
    # 根据模块路由
    if current_module == "User Insights":
        await handle_user_insights(message)
    elif current_module == "Competitor Analysis":
        await handle_competitor_analysis(message)
    elif current_module == "PRD Writer":
        await handle_prd_writer(message)
    else:
        # Fallback to User Insights
        await handle_user_insights(message)


async def handle_user_insights(message: cl.Message):
    """User Insights 模块 - 用户洞察分析（智能检索版）"""
    import time
    start_time = time.time()
    
    user_query = message.content
    
    # 创建消息并立即发送，后续用 update
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        v_retriever, g_retriever, hybrid, analyzer, llm = get_tools()
        
        # ==================== Step 0: 查询路由（判断是否需要检索）====================
        async with cl.Step(name="🎯 查询路由", type="tool") as step:
            step.output = "正在判断问题类型..."
            
            # 关键修复：用 make_async 包装同步调用，避免阻塞事件循环
            routing_result = await cl.make_async(analyzer.needs_retrieval)(user_query, "User Insights")
            
            if not routing_result["requires_retrieval"]:
                # 不需要检索，直接返回
                step.output = f"""✅ 路由完成

**问题类型**: {routing_result['query_category']}
**需要检索**: 否
**理由**: {routing_result['reasoning']}

直接返回预设回复，无需查询数据库。"""
                
                msg.content = f"**{routing_result['query_category'].title()} Response**\n\n{routing_result['direct_response']}"
                await msg.update()
                return
            
            # 需要检索，继续流程
            step.output = f"""✅ 路由完成

**问题类型**: {routing_result['query_category']}
**需要检索**: 是
**理由**: {routing_result['reasoning']}

继续执行完整检索流程..."""
        
        # ==================== Step 1: 问题分析 ====================
        async with cl.Step(name="🧠 问题分析", type="tool") as step:
            step.output = "正在分析问题复杂度和检索策略..."
            
            analysis = await cl.make_async(analyzer.analyze_query)(user_query, "User Insights")
            
            step.output = f"""✅ 问题分析完成

**复杂度**: {analysis['complexity']}
**问题类型**: {analysis['query_type']}
**检索策略**: {', '.join(analysis['data_sources'])}
**检索数量**: {analysis['n_results']} 条
**分析理由**: {analysis['reasoning']}
"""
        
        # ==================== Step 2: 智能分层检索 ====================
        async with cl.Step(name="🔍 智能混合检索", type="retrieval") as step:
            step.output = "正在执行分层检索（质量优先）..."
            
            # 使用 retrieve_for_user_insights（内部已集成分层检索）
            retrieval_result = await cl.make_async(hybrid.retrieve_for_user_insights)(user_query)
            personas = retrieval_result["personas"]
            ugc_result = retrieval_result["ugc_result"]
            ugc_docs = ugc_result["docs"]
            quality_result = ugc_result["quality_result"]
            layer = ugc_result["layer"]
            context = retrieval_result["context"]
            
            layer_names = {1: "快速", 2: "标准", 3: "深度"}
            step.output = f"""✅ 混合检索完成

**知识图谱数据**:
- 用户画像: {len(personas)} 个（权威数据源）

**向量库数据**:
- 检索层级: Layer {layer} ({layer_names[layer]}检索)
- 相关评论: {len(ugc_docs)} 条
"""
        
        # ==================== Step 3: LLM 分析（优化 Prompt）====================
        async with cl.Step(name="🤖 AI 深度分析", type="llm") as step:
            step.output = "正在调用 DeepSeek R1 进行深度分析..."
            
            # 构建对话历史
            history_text = _build_history_text(max_rounds=3)
            
            # 强化约束的 Prompt（防止幻觉）
            prompt = f"""你是一位资深的电动汽车产品经理，擅长从用户评论和用户画像中提取关键洞察。

**重要格式要求**: 请将你的思考过程放在<think></think>标签中，最终答案放在标签之外。

【严格要求 - 必须遵守】
1. **仅基于提供的数据回答**: 严禁使用任何外部知识、常识或假设
2. **数据不足时必须明确说明**: 如果提供的数据不足以回答问题，请明确指出，不要编造
3. **强制引用来源**: 每个论述都必须引用具体数据来源（格式: [画像X]、[评论Y]）
4. **禁止推测**: 不要使用"可能"、"一般来说"、"通常"等推测性表述
{history_text}
【数据来源】
{context}

【用户问题】
{user_query}

【回答格式】
## 核心发现
- [基于数据的关键洞察，必须引用来源]
- [关键洞察 2，必须引用来源]

## 详细分析
[每个论点都必须引用数据，格式: [画像X] 或 [评论Y] 具体内容]

## 数据覆盖度说明
- 能够回答的方面: [列出哪些方面有数据支持]
- 数据不足的方面: [列出哪些方面数据不足，无法回答]

请严格基于上述数据回答，不要添加任何推测或外部知识。"""
            
            print(f"\n{'='*60}")
            print(f"🔍 开始 LLM 分析")
            print(f"Context 长度: {len(context)} 字符")
            print(f"{'='*60}\n")
            
            response = await cl.make_async(llm.chat)(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            
            print(f"\n{'='*60}")
            print(f"✅ LLM 响应成功")
            print(f"Response type: {type(response)}")
            if hasattr(response, 'choices') and len(response.choices) > 0:
                print(f"Content length: {len(response.choices[0].message.content)}")
                print(f"Content preview: {response.choices[0].message.content[:200]}...")
            print(f"{'='*60}\n")
            
            raw_output = response.choices[0].message.content
            print(f"\n✅ 获取原始输出，长度: {len(raw_output)}")
            step.output = f"✅ 分析完成（Token: ~{response.usage.total_tokens if hasattr(response, 'usage') else 'N/A'}）"
        
        # 格式化最终输出 - 简化的健壮处理
        print(f"\n{'='*60}")
        print(f"📝 开始格式化输出")
        print(f"Raw output 长度: {len(raw_output)}")
        print(f"{'='*60}\n")
        
        try:
            # 尝试提取思考链（如果存在），但不强制要求
            thought_chain = None
            final_answer = raw_output  # 默认使用全部内容
            
            # 如果包含 </think> 标签，尝试分离思考过程和最终答案
            if "</think>" in raw_output:
                # 查找结束标签位置
                think_end = raw_output.find("</think>")
                
                # 尝试查找开始标签
                think_start = 0
                if "<think>" in raw_output:
                    think_start = raw_output.find("<think>") + 7  # 跳过 <think>
                
                potential_thought = raw_output[think_start:think_end].strip()
                potential_answer = raw_output[think_end + 8:].strip()  # 跳过 </think>
                
                # 验证提取结果
                if potential_answer:  # 只要有答案就可以
                    if potential_thought:
                        thought_chain = potential_thought
                    final_answer = potential_answer
                    print(f"✅ 成功分离内容 - 思考链: {len(thought_chain or '')} 字符, 答案: {len(final_answer)} 字符")
                else:
                    print(f"⚠️ 未找到答案部分，使用全部内容")
                    final_answer = raw_output
            else:
                print(f"⚠️ 未检测到 </think> 标签，直接使用全部内容")
            
            # 构建最终消息（确保一定有内容）
            
            print(f"\n📝 准备发送回复:")
            print(f"   答案长度: {len(final_answer)} 字符")
            print(f"   答案预览: {final_answer[:100]}...")
            
            # 构建可折叠的数据溯源区域
            source_sections = []
            
            # 用户画像溯源
            if personas:
                persona_lines = []
                for i, p in enumerate(personas, 1):
                    dims = ', '.join([d['dimension'] for d in p.get('top_dimensions', [])])
                    persona_lines.append(
                        f"**[画像 {i}] {p.get('persona_name', 'Unknown')}** — "
                        f"评论数: {p.get('review_count', 0)} | 优先维度: {dims}"
                    )
                source_sections.append(
                    f"<details><summary>📊 知识图谱 · 用户画像（{len(personas)} 个）</summary>\n\n"
                    + "\n\n".join(persona_lines)
                    + "\n\n</details>"
                )
            
            # 评论溯源
            if ugc_docs:
                review_lines = []
                for i, doc in enumerate(ugc_docs[:15], 1):
                    meta = doc.get('metadata', {})
                    brand = meta.get('brand', '')
                    series = meta.get('series', '')
                    model = meta.get('model', '')
                    dim = meta.get('dimension', '')
                    text = doc.get('text', '')
                    # 截断过长的评论
                    if len(text) > 200:
                        text = text[:200] + "..."
                    review_lines.append(
                        f"**[评论 {i}]** {brand} {series} {model} · {dim}\n> {text}"
                    )
                source_sections.append(
                    f"<details><summary>💬 向量检索 · 用户评论（{len(ugc_docs)} 条）</summary>\n\n"
                    + "\n\n".join(review_lines)
                    + "\n\n</details>"
                )
            
            source_block = "\n\n".join(source_sections)
            
            msg.content = f"""**📊 用户洞察分析**

{final_answer}

---

{source_block}

<sub>数据来源: 知识图谱 + 向量库 | 画像: {len(personas)} 个 · 评论: {len(ugc_docs)} 条</sub>"""
            
            # 如果成功提取思考链，添加到消息的 elements 中（不创建新消息）
            if thought_chain:
                msg.elements = [
                    cl.Text(name="💭 思考过程", content=thought_chain, display="side")
                ]
            
            print(f"✅ 消息格式化成功，最终内容长度: {len(msg.content)}")
            
            # 一次性发送完整消息（而不是先 send 再 update）
            await msg.send()
            
            # 保存 assistant 回复到对话历史
            _save_assistant_reply(final_answer)
            
            # 记录发送后状态
            elapsed = time.time() - start_time
            print(f"✅ 消息已发送")
            print(f"⏱️  总耗时: {elapsed:.1f}秒")
            print(f"\n{'='*80}\n")
            
        except Exception as e:
            # 捕获格式化/发送异常
            print(f"\n❌ 格式化或发送失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 使用原始内容
            try:
                fallback_msg = f"**📊 用户洞察分析**\n\n{raw_output}\n\n---\n*数据来源: 知识图谱 + 向量库*"
                msg.content = fallback_msg
                await msg.send()
            except:
                pass
        
    except Exception as e:
        # 最外层异常处理
        print(f"❌ 分析出错: {e}")
        try:
            msg.content = f"❌ 分析出错: {str(e)}"
            await msg.send()
        except:
            pass


async def handle_competitor_analysis(message: cl.Message):
    """Competitor Analysis 模块 - 竞品分析（智能检索版）"""
    user_query = message.content
    
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        v_retriever, g_retriever, hybrid, analyzer, llm = get_tools()
        
        # ==================== Step 0: 查询路由 ====================
        async with cl.Step(name="🎯 查询路由", type="tool") as step:
            step.output = "正在判断问题类型..."
            
            routing_result = await cl.make_async(analyzer.needs_retrieval)(user_query, "Competitor Analysis")
            
            if not routing_result["requires_retrieval"]:
                step.output = f"""✅ 路由完成

**问题类型**: {routing_result['query_category']}
**需要检索**: 否
**理由**: {routing_result['reasoning']}

直接返回预设回复。"""
                
                msg.content = f"**{routing_result['query_category'].title()} Response**\n\n{routing_result['direct_response']}"
                await msg.update()
                return
            
            step.output = f"""✅ 路由完成

**问题类型**: {routing_result['query_category']}
**需要检索**: 是
**理由**: {routing_result['reasoning']}

继续执行竞品分析流程..."""
        
        # ==================== Step 1: 问题分析 ====================
        async with cl.Step(name="🧠 问题分析", type="tool") as step:
            step.output = "正在分析竞品分析需求..."
            
            analysis = await cl.make_async(analyzer.analyze_query)(user_query, "Competitor Analysis")
            
            step.output = f"""✅ 分析完成

**复杂度**: {analysis['complexity']}
**问题类型**: {analysis['query_type']}
**检索策略**: {', '.join(analysis['data_sources'])}
**检索数量**: {analysis['n_results']} 条
"""
        
        # ==================== Step 1.5: 实体提取 ====================
        async with cl.Step(name="🏷️ 实体提取", type="tool") as step:
            step.output = "正在从问题中提取品牌和车型..."
            
            entities = await cl.make_async(analyzer.extract_entities)(user_query, "Competitor Analysis")
            extracted_brands = entities["brands"]
            extracted_models = entities["models"]
            
            step.output = f"""✅ 实体提取完成

**提取的品牌**: {', '.join(extracted_brands) if extracted_brands else '无'}
**提取的车型**: {', '.join(extracted_models) if extracted_models else '无'}
**置信度**: {entities['extraction_confidence']:.0%}
"""
        
        # ==================== Step 2: 智能分层检索 ====================
        async with cl.Step(name="🔍 智能混合检索", type="retrieval") as step:
            step.output = "正在执行分层检索（质量优先）..."
            
            # 使用 retrieve_for_competitor_analysis（内部已集成分层检索）
            retrieval_result = await cl.make_async(hybrid.retrieve_for_competitor_analysis)(user_query, brands=extracted_brands)
            vehicles = retrieval_result["vehicles"]
            ugc_result = retrieval_result["ugc_result"]
            ugc_docs = ugc_result["docs"]
            quality_result = ugc_result["quality_result"]
            layer = ugc_result["layer"]
            spec_docs = retrieval_result["spec_docs"]
            context = retrieval_result["context"]
            
            layer_names = {1: "快速", 2: "标准", 3: "深度"}
            step.output = f"""✅ 混合检索完成

**知识图谱数据**:
- 车型参数: {len(vehicles)} 个

**向量库数据**:
- 检索层级: Layer {layer} ({layer_names[layer]}检索)
- 相关评论: {len(ugc_docs)} 条
- 规格文档: {len(spec_docs)} 个
"""
        
        # ==================== Step 3: LLM 竞品分析 ====================
        async with cl.Step(name="⚔️ 竞品对比分析", type="llm") as step:
            step.output = "正在生成竞品分析报告..."
            
            # 构建对话历史
            history_text = _build_history_text(max_rounds=3)
            
            prompt = f"""你是一位资深的电动汽车产品分析师，擅长竞品对比和市场洞察。

【严格要求 - 必须遵守】
1. **仅基于提供的数据**: 严禁使用外部知识或市场常识
2. **数据不足时明确说明**: 如果某方面数据缺失，请明确指出而非推测
3. **强制引用来源**: 每个参数、评价都必须标注来源
4. **避免主观描述**: 使用客观的数据对比，不要使用"更好"、"优秀"等主观词汇（除非有数据支持）
{history_text}
【数据来源】
{context}

【用户需求】
{user_query}

【分析框架】
## 1. 核心参数对比
[仅列出数据中有的参数，标注来源]

## 2. 用户评价对比
[基于真实评论，引用格式: [评论X] 具体内容]

## 3. 优劣势分析
- 优势: [基于数据的客观对比]
- 劣势: [基于数据的客观对比]

## 4. 数据覆盖说明
- 数据完整的方面: [列出]
- 数据缺失的方面: [明确指出无法对比的部分]

请严格基于上述数据生成报告，不要添加推测。"""
            
            response = await cl.make_async(llm.chat)(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # 降低温度提高确定性
                max_tokens=2000
            )
            
            raw_output = response.choices[0].message.content
            step.output = "✅ 分析报告生成完成"
        
        # ==================== 格式化输出（简化健壮处理）====================
        try:
            # 尝试提取思考链
            thought_chain = None
            final_answer = raw_output
            
            if "</think>" in raw_output:
                think_end = raw_output.find("</think>")
                potential_thought = raw_output[:think_end].strip()
                potential_answer = raw_output[think_end + 8:].strip()
                
                if potential_thought and potential_answer:
                    thought_chain = potential_thought
                    final_answer = potential_answer
            
            # 展示思考链（如有）- 附加到消息 elements 上，不创建新消息
            if thought_chain:
                msg.elements = [cl.Text(name="💭 分析思路", content=thought_chain, display="side")]
            
            # 构建最终消息
            data_note = f"{len(vehicles)} 个车型参数 + " if vehicles else ""
            
            # 构建可折叠的数据溯源区域
            source_sections = []
            
            # 车型参数溯源
            if vehicles:
                vehicle_lines = []
                for v in vehicles:
                    vehicle_lines.append(
                        f"**{v.get('brand', '')} {v.get('series', '')} {v.get('model', '')}** — "
                        f"价格: {v.get('price', 'N/A')}万 | 续航: {v.get('range_cltc', 'N/A')}km | "
                        f"加速: {v.get('acceleration', 'N/A')}s | 座位: {v.get('seats', 'N/A')}"
                    )
                source_sections.append(
                    f"<details><summary>🚗 知识图谱 · 车型参数（{len(vehicles)} 个）</summary>\n\n"
                    + "\n\n".join(vehicle_lines)
                    + "\n\n</details>"
                )
            
            # 评论溯源
            if ugc_docs:
                review_lines = []
                for i, doc in enumerate(ugc_docs[:15], 1):
                    meta = doc.get('metadata', {})
                    brand = meta.get('brand', '')
                    series = meta.get('series', '')
                    model = meta.get('model', '')
                    dim = meta.get('dimension', '')
                    text = doc.get('text', '')
                    if len(text) > 200:
                        text = text[:200] + "..."
                    review_lines.append(
                        f"**[评论 {i}]** {brand} {series} {model} · {dim}\n> {text}"
                    )
                source_sections.append(
                    f"<details><summary>💬 向量检索 · 用户评论（{len(ugc_docs)} 条）</summary>\n\n"
                    + "\n\n".join(review_lines)
                    + "\n\n</details>"
                )
            
            # 规格文档溯源
            if spec_docs:
                spec_lines = []
                for i, doc in enumerate(spec_docs[:10], 1):
                    meta = doc.get('metadata', {})
                    text = doc.get('text', '')
                    if len(text) > 200:
                        text = text[:200] + "..."
                    spec_lines.append(
                        f"**[规格 {i}]** {meta.get('brand', '')} {meta.get('series', '')} {meta.get('model', '')}\n> {text}"
                    )
                source_sections.append(
                    f"<details><summary>📋 向量检索 · 车型规格（{len(spec_docs)} 个）</summary>\n\n"
                    + "\n\n".join(spec_lines)
                    + "\n\n</details>"
                )
            
            source_block = "\n\n".join(source_sections)
            
            msg.content = f"""**⚔️ 竞品分析报告**

{final_answer}

---

{source_block}

<sub>数据来源: 知识图谱 + 向量库 | 车型: {len(vehicles)} 个 · 评论: {len(ugc_docs)} 条 · 规格: {len(spec_docs)} 个</sub>"""
            
            await msg.update()
            
            # 保存 assistant 回复到对话历史
            _save_assistant_reply(final_answer)
        except Exception as e:
            # 降级显示
            data_note = f"{len(vehicles)} 个车型参数 + " if vehicles else ""
            msg.content = f"""**⚔️ 竞品分析报告**

{raw_output}

---
*基于 {data_note}{len(ugc_docs)} 条评论和 {len(spec_docs)} 个车型数据*"""
            await msg.update()
        
    except Exception as e:
        msg.content = f"❌ 分析出错: {str(e)}"
        await msg.update()


async def handle_prd_writer(message: cl.Message):
    """PRD Writer 模块 - PRD 文档撰写（智能检索版）"""
    user_query = message.content
    
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        v_retriever, g_retriever, hybrid, analyzer, llm = get_tools()
        
        # ==================== Step 0: 查询路由 ====================
        async with cl.Step(name="🎯 查询路由", type="tool") as step:
            step.output = "正在判断问题类型..."
            
            routing_result = await cl.make_async(analyzer.needs_retrieval)(user_query, "User Insights")
            
            if not routing_result["requires_retrieval"]:
                step.output = f"""✅ 路由完成

**问题类型**: {routing_result['query_category']}
**需要检索**: 否

直接返回预设回复。"""
                
                msg.content = f"**{routing_result['query_category'].title()} Response**\n\n{routing_result['direct_response']}"
                await msg.update()
                return
            
            step.output = f"""✅ 路由完成

**问题类型**: {routing_result['query_category']}
**需要检索**: 是

继续执行 PRD 撰写流程..."""
        
        # ==================== Step 1: 问题分析 ====================
        async with cl.Step(name="🧠 问题分析", type="tool") as step:
            step.output = "正在分析 PRD 撰写需求..."
            
            analysis = await cl.make_async(analyzer.analyze_query)(user_query, "PRD Writer")
            
            step.output = f"""✅ 分析完成

**复杂度**: {analysis['complexity']}
**问题类型**: {analysis['query_type']}
**检索数量**: {analysis['n_results']} 条（PRD 需要更多数据）
"""
        
        # ==================== Step 1.5: 实体提取 ====================
        async with cl.Step(name="🏷️ 实体提取", type="tool") as step:
            step.output = "正在从问题中提取品牌和车型..."
            
            entities = await cl.make_async(analyzer.extract_entities)(user_query, "PRD Writer")
            extracted_brands = entities["brands"]
            extracted_models = entities["models"]
            
            step.output = f"""✅ 实体提取完成

**提取的品牌**: {', '.join(extracted_brands) if extracted_brands else '无'}
**提取的车型**: {', '.join(extracted_models) if extracted_models else '无'}
**置信度**: {entities['extraction_confidence']:.0%}
"""
        
        # ==================== Step 2: 智能分层检索 ====================
        async with cl.Step(name="🔍 全栈数据检索", type="retrieval") as step:
            step.output = "正在执行分层检索（质量优先）..."
            
            # 使用 retrieve_for_prd（内部已集成分层检索）
            retrieval_result = await cl.make_async(hybrid.retrieve_for_prd)(user_query, brands=extracted_brands)
            personas = retrieval_result["personas"]
            vehicles = retrieval_result["vehicles"]
            ugc_result = retrieval_result["ugc_result"]
            ugc_docs = ugc_result["docs"]
            quality_result = ugc_result["quality_result"]
            layer = ugc_result["layer"]
            spec_docs = retrieval_result["spec_docs"]
            context = retrieval_result["context"]
            
            layer_names = {1: "快速", 2: "标准", 3: "深度"}
            step.output = f"""✅ 全栈检索完成

**知识图谱数据**:
- 用户画像: {len(personas)} 个
- 车型参数: {len(vehicles)} 个

**向量库数据**:
- 检索层级: Layer {layer} ({layer_names[layer]}检索)
- 用户评论: {len(ugc_docs)} 条
- 规格文档: {len(spec_docs)} 个
"""
        
        # ==================== Step 5: PRD 生成 ====================
        async with cl.Step(name="📝 生成 PRD 文档", type="llm") as step:
            step.output = "正在使用 DeepSeek R1 生成产品需求文档..."
            
            # 构建对话历史
            history_text = _build_history_text(max_rounds=3)
            
            prompt = f"""你是一位资深的电动汽车产品经理，擅长撰写专业的产品需求文档（PRD）。

【严格要求 - 防止幻觉】
1. **仅基于提供数据**: 严禁使用行业常识、预训练知识或假设
2. **数据不足时务必说明**: 如果某个PRD章节缺乏数据支持，请明确说明
3. **所有需求必须溯源**: 每个功能需求都必须引用具体数据来源
4. **禁止臆造用户画像**: 只使用提供的权威画像数据，不要创造新的用户类型
5. **禁止臆造竞品信息**: 只对比提供的车型数据
{history_text}
【数据来源】
{context}

【用户需求】
{user_query}

【PRD 结构要求】

## 1. 项目背景
[基于提供的评论和画像数据分析市场机会，标注来源]

## 2. 目标用户
[仅使用提供的权威用户画像，引用格式: [画像X]]

## 3. 市场分析
[基于提供的评论和车型数据，引用具体来源]

## 4. 核心功能需求
[每个需求必须标注来源，格式: 需求X - 来源: [评论Y]]
- P0: [核心需求，引用数据]
- P1: [重要需求，引用数据]
- P2: [可选需求，引用数据]

## 5. 数据覆盖度说明
- 数据完整的部分: [哪些需求有充分数据支持]
- 需要补充调研的部分: [哪些方面数据不足，需进一步研究]

## 6. 成功指标
[基于数据中的用户期望和痛点，设定可量化指标]

【重要】所有内容必须基于提供的数据，不要添加任何推测。如果数据不足，请明确说明哪些部分需要补充调研。"""
            
            response = await cl.make_async(llm.chat)(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # 降低温度提高确定性
                max_tokens=3000
            )
            
            raw_output = response.choices[0].message.content
            step.output = f"✅ PRD 生成完成（Token: ~{response.usage.total_tokens if hasattr(response, 'usage') else 'N/A'}）"
        
        # ==================== 解析思考链 ====================
        if "<think>" in raw_output and "</think>" in raw_output:
            think_start = raw_output.find("<think>") + 7
            think_end = raw_output.find("</think>")
            thought_chain = raw_output[think_start:think_end].strip()
            final_prd = raw_output[think_end + 8:].strip()
            
            msg.elements = [
                cl.Text(name="💭 PRD 撰写思路（可展开）", content=thought_chain, display="side")
            ]
            
            prd_content = final_prd
        else:
            prd_content = raw_output
        
        # ==================== 显示 PRD ====================
        # 构建可折叠的数据溯源区域
        source_sections = []
        
        # 用户画像溯源
        if personas:
            persona_lines = []
            for i, p in enumerate(personas, 1):
                dims = ', '.join([d['dimension'] for d in p.get('top_dimensions', [])])
                persona_lines.append(
                    f"**[画像 {i}] {p.get('persona_name', 'Unknown')}** — "
                    f"评论数: {p.get('review_count', 0)} | 优先维度: {dims}"
                )
            source_sections.append(
                f"<details><summary>📊 知识图谱 · 用户画像（{len(personas)} 个）</summary>\n\n"
                + "\n\n".join(persona_lines)
                + "\n\n</details>"
            )
        
        # 评论溯源
        if ugc_docs:
            review_lines = []
            for i, doc in enumerate(ugc_docs[:20], 1):
                meta = doc.get('metadata', {})
                brand = meta.get('brand', '')
                series = meta.get('series', '')
                model = meta.get('model', '')
                dim = meta.get('dimension', '')
                text = doc.get('text', '')
                if len(text) > 200:
                    text = text[:200] + "..."
                review_lines.append(
                    f"**[评论 {i}]** {brand} {series} {model} · {dim}\n> {text}"
                )
            source_sections.append(
                f"<details><summary>💬 向量检索 · 用户评论（{len(ugc_docs)} 条）</summary>\n\n"
                + "\n\n".join(review_lines)
                + "\n\n</details>"
            )
        
        source_block = "\n\n".join(source_sections)
        
        msg.content = f"""**📝 产品需求文档（PRD）**

{prd_content}

---

{source_block}

<sub>数据来源: 知识图谱 + 向量库 | 画像: {len(personas)} 个 · 车型: {len(vehicles)} 个 · 评论: {len(ugc_docs)} 条</sub>

💡 **提示**: 您可以复制上述内容保存为 Markdown 文件，或直接用于产品规划。
"""
        
        await msg.update()
        
        # 保存 assistant 回复到对话历史
        _save_assistant_reply(prd_content)
        
        # ==================== 可选：提供导出功能 ====================
        actions = [
            cl.Action(name="export_prd", payload={"content": prd_content[:3000]}, label="📥 导出为 Markdown 文件")
        ]
        await cl.Message(content="", actions=actions).send()
        
    except Exception as e:
        msg.content = f"❌ PRD 生成出错: {str(e)}"
        await msg.update()


@cl.action_callback("export_prd")
async def on_export_prd(action: cl.Action):
    """处理 PRD 导出"""
    prd_content = action.payload.get("content", "")
    
    # 创建文本元素供下载
    elements = [
        cl.Text(name="PRD.md", content=prd_content, display="inline")
    ]
    
    await cl.Message(
        content="✅ PRD 文档已准备好，您可以复制上方内容。",
        elements=elements
    ).send()


if __name__ == "__main__":
    # Chainlit will handle the server startup
    pass
