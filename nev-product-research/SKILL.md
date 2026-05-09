---
name: nev-product-research
description: 面向新能源乘用车产品研究的结构化 Skill。用于把市场资料、车型参数、竞品信息、用户评论、车主反馈和访谈材料，转化为可追溯的产品研究交付物。适用于用户要求做产品研究、竞品分析、用户洞察、机会诊断、PRD 前置研究、研究报告、机会卡片或证据驱动的产品判断时。尤其适合“研究某个细分市场”“比较几款车”“从用户声音里提炼产品机会”“输出 final report / pdf 报告”这类请求；不适用于泛泛行业摘要、单纯参数查询、纯营销文案或无证据支撑的观点输出。
---

# NEV Product Research

按“先证据，后判断”的顺序推进研究。不要从零散搜索结果直接跳到产品结论。

## 执行顺序

按以下顺序阅读和执行 workflow：

1. `workflows/01_define_scope.md`
2. `workflows/02_collect_evidence.md`
3. `workflows/03_normalize_evidence.md`
4. `workflows/04_build_product_model.md`
5. `workflows/05_build_user_model.md`
6. `workflows/06_diagnose_opportunity.md`
7. `workflows/07_generate_deliverables.md`

除非用户明确只要其中一个阶段，否则不要跳步。后续阶段必须引用前序产物。

## 先读什么

- 先读当前 workflow。
- 需要统一口径时，再读 `references/evidence-rules.md`。
- 需要确认交付结构时，再读 `references/deliverables.md`。
- 需要导出 PDF 时，使用 `scripts/md_to_pdf.py`。

## 核心约束

- 区分 `Evidence`、`Inference`、`Assumption`、`Evidence Gap`。
- 不要把用户原话直接写成产品结论。
- 不要把参数事实直接写成产品优势。
- 不要在证据不足时给出确定性判断。
- 不要从原始搜索结果直接生成 PRD。
- 默认用中文输出；仅在用户明确要求英文时切换。

## 文件约定

在研究输出目录中按顺序产出：

```text
01_research_scope.md
02_evidence_collection.md
03_normalized_evidence_pack.md
04_product_model.md
05_user_model.md
06_opportunity_cards.md
07_market_brief.md
08_competitor_matrix.md
09_user_insight_report.md
10_prd_draft.md
11_final_report.md
final_report.pdf
```

如果用户只要部分交付物，仍然保持编号和证据链完整。

## 质量门槛

- 让每条关键判断都能追溯到来源。
- 明确写出缺失信息和待验证假设。
- 优先服务产品经理决策，而不是写成泛行业综述。
- 在最终报告中保留证据附录、关键假设和证据缺口。
