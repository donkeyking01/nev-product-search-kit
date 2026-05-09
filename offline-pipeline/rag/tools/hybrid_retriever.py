"""
Hybrid Retriever - 混合检索器
结合向量检索和图数据库查询，提供更准确的结果

Author: EV PM DSS Team
Date: 2026-02-15
"""

from typing import List, Dict, Optional
from rag.tools.vector_tool import VectorRetriever, format_ugc_context
from rag.tools.graph_tool import GraphRetriever, format_ipa_scores


class HybridRetriever:
    """混合检索器 - 向量 + 图谱"""
    
    def __init__(self):
        self.vector = VectorRetriever()
        self.graph = GraphRetriever()
    
    def retrieve_for_user_insights(self, query: str) -> Dict:
        """
        用户洞察专用检索
        
        策略:
        1. 从图数据库获取所有 Persona 节点（权威数据源）
        2. 分层检索相关 UGC 评论（质量自动把控）
        3. 结合 Persona 的优先维度
        
        Returns:
            Dict with personas, ugc_result, context
        """
        # 1. 从图数据库获取所有用户画像（权威数据）
        print("=== 开始检索用户画像 ===")
        personas = self.graph.get_all_personas()
        print(f"=== 检索到 {len(personas)} 个用户画像 ===")
        
        # 2. 分层检索相关评论（自动质量把控）
        ugc_result = self.layered_retrieve_ugc(query)
        ugc_docs = ugc_result["docs"]
        print(f"=== 检索到 {len(ugc_docs)} 条评论（Layer {ugc_result['layer']}，质量 {ugc_result['quality']:.0%}）===")
        
        # 3. 构建上下文
        context = self._build_persona_context(personas, ugc_docs)
        
        return {
            "personas": personas,
            "ugc_reviews": ugc_docs,
            "ugc_result": ugc_result,
            "context": context,
            "retrieval_strategy": "Hybrid: Graph Personas + Vector UGC (Layered)"
        }
    
    def layered_retrieve_ugc(self, query: str, min_quality: float = 0.4, llm_client=None) -> Dict:
        """
        分层检索：从少到多，基于向量距离快速判断是否需要扩大范围，
        最终用 LLM 评估检索质量（仅后台日志，不暴露给前端）。
        
        策略：
        - Layer 1: 检索 15 条，距离达标直接返回
        - Layer 2: 扩大到 50 条
        - Layer 3: 扩大到 100 条
        - 确定最终层后，LLM 评估一次质量（打日志）
        
        Args:
            query: 查询问题
            min_quality: 距离判断的最小质量阈值（默认 0.4）
            llm_client: LLM 客户端（用于最终质量评估日志）
        
        Returns:
            {
                "docs": List[Dict],
                "quality": float,         # 距离质量分数 0~1
                "avg_distance": float,    # top-k 平均距离
                "quality_result": Dict,   # 详细质量信息
                "layer": int,
                "n_results": int,
                "warning": Optional[str]
            }
        """
        layers = [
            {"n_results": 15, "name": "快速检索"},
            {"n_results": 50, "name": "标准检索"},
            {"n_results": 100, "name": "深度检索"}
        ]
        
        print(f"\n🔍 [分层检索] 开始")
        
        final_docs = []
        final_layer = 1
        final_quality = 0.0
        final_avg_distance = 1.5
        final_quality_result = {}
        
        for i, layer in enumerate(layers, 1):
            n = layer["n_results"]
            print(f"\n   Layer {i}: {layer['name']}（{n} 条）...")
            
            docs = self.vector.search_ugc_reviews(query, n_results=n)
            
            if not docs:
                print(f"   ⚠️ 未检索到任何文档")
                continue
            
            # 基于向量距离快速计算质量分数
            distances = [doc.get('distance', 1.0) for doc in docs]
            avg_distance = sum(distances) / len(distances)
            min_distance = min(distances)
            
            # 统计各相关度区间的文档数
            high_relevant = sum(1 for d in distances if d < 0.5)
            mid_relevant = sum(1 for d in distances if 0.5 <= d < 1.0)
            low_relevant = sum(1 for d in distances if d >= 1.0)
            
            # 用 top-k 平均距离计算质量（不被总检索量稀释）
            top_k = min(10, len(distances))
            top_distances = sorted(distances)[:top_k]
            top_avg_distance = sum(top_distances) / len(top_distances)
            
            # 归一化：distance=0 → quality=1, distance≥1.5 → quality=0
            quality = max(0.0, min(1.0, 1.0 - top_avg_distance / 1.5))
            
            print(f"   Top-{top_k} 平均距离: {top_avg_distance:.3f}, 质量分数: {quality:.0%}")
            print(f"   分布: 高相关={high_relevant}, 中相关={mid_relevant}, 低相关={low_relevant}")
            
            quality_result = {
                "is_sufficient": quality >= min_quality,
                "relevant_count": high_relevant + mid_relevant,
                "total_count": len(docs),
                "relevance_ratio": quality,
                "avg_distance": avg_distance,
                "top_avg_distance": top_avg_distance,
                "min_distance": min_distance,
                "distribution": {"high": high_relevant, "mid": mid_relevant, "low": low_relevant}
            }
            
            final_docs = docs
            final_layer = i
            final_quality = quality
            final_avg_distance = top_avg_distance
            final_quality_result = quality_result
            
            # 如果距离质量达标，停止扩大
            if quality >= min_quality:
                print(f"   ✅ 距离质量达标，使用 Layer {i}")
                break
        
        if not final_docs:
            print(f"   ⚠️ 所有层级均未检索到文档")
            return {
                "docs": [], "quality": 0.0, "avg_distance": 1.5,
                "quality_result": {"is_sufficient": False, "relevant_count": 0, "total_count": 0, "relevance_ratio": 0.0},
                "layer": len(layers), "n_results": 0, "warning": None
            }
        
        print(f"   ✅ 最终使用 Layer {final_layer}，共 {len(final_docs)} 条文档\n")
        
        # ==================== LLM 质量评估（仅后台日志） ====================
        self._log_quality_with_llm(query, final_docs, llm_client)
        
        return {
            "docs": final_docs,
            "quality": final_quality,
            "avg_distance": final_avg_distance,
            "quality_result": final_quality_result,
            "layer": final_layer,
            "n_results": len(final_docs),
            "warning": None  # 不再向前端传递警告
        }
    
    def _log_quality_with_llm(self, query: str, docs: List[Dict], llm_client=None):
        """
        用 LLM 评估检索质量，仅打印到后台日志，不影响前端。
        评估意图匹配度而非纯语义距离。
        """
        if llm_client is None:
            try:
                from rag.config import get_deepseek_client
                llm_client = get_deepseek_client()
            except Exception:
                print("   ⚠️ [LLM质量评估] 无法获取 LLM 客户端，跳过")
                return
        
        # 取前 10 条文档的摘要
        docs_preview = "\n".join([
            f"文档{i+1}: {doc.get('text', '')[:150]}..."
            for i, doc in enumerate(docs[:10])
        ])
        
        prompt = f"""评估以下检索结果对回答用户问题的帮助程度。

用户问题: {query}

检索到的文档:
{docs_preview}

返回 JSON:
{{
    "score": 0-10,
    "useful_count": 0-10,
    "reason": "简短说明"
}}

评分标准:
- 9-10: 文档高度相关，可以直接回答问题
- 6-8: 大部分文档有用，能辅助回答
- 3-5: 部分相关，需要补充其他数据源
- 0-2: 几乎无关，无法回答问题

只返回 JSON。"""
        
        try:
            response = llm_client.chat(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=150,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            score = result.get("score", 0)
            useful = result.get("useful_count", 0)
            reason = result.get("reason", "")
            
            # 只打日志
            emoji = "✅" if score >= 6 else "⚠️" if score >= 3 else "❌"
            print(f"\n📋 [LLM质量评估] {emoji} 评分: {score}/10 | 有用文档: {useful}/10 | {reason}")
            
        except Exception as e:
            print(f"\n📋 [LLM质量评估] ⚠️ 评估失败: {e}")
    
    def retrieve_for_competitor_analysis(self, query: str, brands: Optional[List[str]] = None) -> Dict:
        """
        竞品分析专用检索
        
        策略:
        1. 从图数据库获取车型参数（结构化对比）- 仅当指定品牌时
        2. 分层检索相关 UGC 评论（质量自动把控）
        3. 向量检索规格文档
        
        Returns:
            Dict with vehicles, ugc_result, spec_docs, context
        """
        print(f"\n{'='*60}")
        print(f"🔍 [竞品分析检索] 开始...")
        print(f"   用户查询: {query}")
        print(f"   提取的品牌: {brands}")
        print(f"{'='*60}")
        
        # 1. 图数据库查询车型（仅当指定品牌时）
        vehicles = []
        
        if brands:
            print(f"\n📊 [图谱检索] 检测到 {len(brands)} 个品牌，开始查询车型参数...")
            for brand in brands:
                print(f"   查询品牌: {brand}")
                vehicle_list = self.graph.get_vehicle_by_filters(brand=brand, limit=5)
                vehicles.extend(vehicle_list)
            print(f"   ✅ 图谱检索完成: 共 {len(vehicles)} 个车型")
        else:
            print(f"\n⚠️ [图谱检索] 未提取到品牌，跳过图数据库查询")
        
        # 2. 分层检索评论（质量自动把控）
        print(f"\n🔎 [向量检索] 开始分层检索评论...")
        ugc_result = self.layered_retrieve_ugc(query)
        ugc_docs = ugc_result["docs"]
        
        # 3. 向量检索规格文档
        spec_docs = self.vector.search_vehicle_specs(query, n_results=10)
        print(f"   ✅ 向量检索完成: {len(ugc_docs)} 条评论 (Layer {ugc_result['layer']}), {len(spec_docs)} 个规格文档")
        
        # 4. 构建上下文
        context = self._build_competitor_context(vehicles, ugc_docs, spec_docs)
        
        print(f"\n{'='*60}")
        print(f"✅ [竞品分析检索] 完成")
        print(f"   车型参数: {len(vehicles)} 个")
        print(f"   用户评论: {len(ugc_docs)} 条（质量 {ugc_result['quality']:.0%}）")
        print(f"   规格文档: {len(spec_docs)} 个")
        print(f"{'='*60}\n")
        
        return {
            "vehicles": vehicles,
            "ugc_reviews": ugc_docs,
            "ugc_result": ugc_result,
            "spec_docs": spec_docs,
            "context": context,
            "retrieval_strategy": "Hybrid: Graph Vehicles + Vector UGC/Specs (Layered)" if vehicles else "Vector Only: UGC/Specs (Layered)"
        }
    
    def retrieve_for_prd(self, query: str, brands: Optional[List[str]] = None) -> Dict:
        """
        PRD 撰写专用检索
        
        策略:
        1. 获取相关 Persona（目标用户）
        2. 获取竞品参数（仅当指定品牌）
        3. 分层检索相关评论（需求洞察，质量自动把控）
        
        Returns:
            Dict with all relevant data
        """
        print(f"\n{'='*60}")
        print(f"📝 [PRD 检索] 开始...")
        print(f"   用户查询: {query}")
        print(f"   提取的品牌: {brands}")
        print(f"{'='*60}")
        
        # 1. 获取用户画像
        print(f"\n📊 [图谱检索] 开始检索用户画像...")
        personas = self.graph.get_all_personas()
        print(f"   ✅ 用户画像检索完成: {len(personas)} 个")
        
        # 2. 获取车型数据（仅当指定品牌时）
        vehicles = []
        if brands:
            print(f"\n📊 [图谱检索] 检测到 {len(brands)} 个品牌，开始查询车型...")
            for brand in brands:
                vehicle_list = self.graph.get_vehicle_by_filters(brand=brand, limit=5)
                vehicles.extend(vehicle_list)
            print(f"   ✅ 车型检索完成: {len(vehicles)} 个")
        else:
            print(f"\n⚠️ [图谱检索] 未提取到品牌，跳过车型查询")
        
        # 3. 分层检索评论（质量自动把控）
        print(f"\n🔎 [向量检索] 开始分层检索评论和规格...")
        ugc_result = self.layered_retrieve_ugc(query)
        ugc_docs = ugc_result["docs"]
        
        # 4. 向量检索规格
        spec_docs = self.vector.search_vehicle_specs(query, n_results=15)
        print(f"   ✅ 向量检索完成: {len(ugc_docs)} 条评论 (Layer {ugc_result['layer']}), {len(spec_docs)} 个规格")
        
        context = self._build_prd_context(personas, ugc_docs, spec_docs)
        
        print(f"\n{'='*60}")
        print(f"✅ [PRD 检索] 完成")
        print(f"   用户画像: {len(personas)} 个")
        print(f"   车型参数: {len(vehicles)} 个")
        print(f"   用户评论: {len(ugc_docs)} 条（质量 {ugc_result['quality']:.0%}）")
        print(f"   规格文档: {len(spec_docs)} 个")
        print(f"{'='*60}\n")
        
        return {
            "personas": personas,
            "vehicles": vehicles,
            "ugc_reviews": ugc_docs,
            "ugc_result": ugc_result,
            "spec_docs": spec_docs,
            "context": context,
            "retrieval_strategy": "Hybrid: Full Stack (Graph + Vector, Layered)"
        }
    
    # ==================== Context Builders ====================
    def _build_persona_context(self, personas: List[Dict], ugc_docs: List[Dict]) -> str:
        """构建用户洞察上下文"""
        context_parts = []
        
        # Part 1: 权威的用户画像数据（明确标注）
        context_parts.append("=== 📊 权威用户画像数据（来自知识图谱，准确可信） ===\n")
        context_parts.append("**重要说明**: 以下用户画像数据来自经过验证的知识图谱，是权威数据源。\n\n")
        for i, p in enumerate(personas, 1):
            context_parts.append(f"""
**[画像 {i}]: {p.get('persona_name', 'Unknown')}** [权威来源]
- 描述: {p.get('description', 'N/A')}
- 评论数: {p.get('review_count', 0)}
- 优先维度: {', '.join([d['dimension'] for d in p.get('top_dimensions', [])])}
""")
        
        # Part 2: 相关评论（明确标注为参考）
        context_parts.append("\n=== 💬 用户评论（仅供参考，可能存在主观性和偏见） ===\n")
        context_parts.append("**重要说明**: 以下是用户个人评论，仅作为辅助参考，请结合权威画像数据分析。\n\n")
        context_parts.append(format_ugc_context(ugc_docs, max_docs=15))  # 显示更多评论
        
        return "\n".join(context_parts)
    
    def _build_competitor_context(self, vehicles: List[Dict], ugc_docs: List[Dict], spec_docs: List[Dict]) -> str:
        """构建竞品分析上下文"""
        context_parts = []
        
        # Part 1: 车型参数（如有）
        if vehicles:
            context_parts.append("=== 车型参数对比（来自知识图谱）===\n")
            for v in vehicles[:5]:
                context_parts.append(f"""
**{v.get('brand')} {v.get('series')} {v.get('model')}**
- 价格: {v.get('price', 'N/A')} 万
- 续航: {v.get('range_cltc', 'N/A')} km
- 加速: {v.get('acceleration', 'N/A')} s
- 座位: {v.get('seats', 'N/A')}
""")
        
        # Part 2: 用户评论
        context_parts.append("\n=== 用户评论 ===\n")
        context_parts.append(format_ugc_context(ugc_docs, max_docs=15))  # 显示更多评论
        
        return "\n".join(context_parts)
    
    def _build_prd_context(self, personas: List[Dict], ugc_docs: List[Dict], spec_docs: List[Dict]) -> str:
        """构建 PRD 上下文"""
        context_parts = []
        
        context_parts.append("=== 📊 目标用户画像（权威数据） ===\n")
        context_parts.append("**数据来源**: 经过验证的知识图谱\n\n")
        for p in personas[:3]:
            context_parts.append(f"- **[画像]** {p.get('persona_name')}: {p.get('description')}\n")
        
        context_parts.append("\n=== 💬 用户需求洞察（基于真实评论） ===\n")
        context_parts.append("**数据来源**: 用户评论（仅供参考）\n\n")
        context_parts.append(format_ugc_context(ugc_docs, max_docs=20))  # PRD需要更多数据
        
        return "\n".join(context_parts)
