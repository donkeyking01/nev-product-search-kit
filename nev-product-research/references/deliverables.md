# Deliverables

最终交付物默认包括以下文件：

- `07_market_brief.md`
- `08_competitor_matrix.md`
- `09_user_insight_report.md`
- `10_prd_draft.md`
- `11_final_report.md`

## 输出要求

### 07 Market Brief

- 回答研究问题
- 总结市场范围、主要玩家、关键变化
- 保留证据边界，不写成泛行业综述

### 08 Competitor Matrix

- 列出主要竞品
- 对比关键产品维度、用户认知、优势、弱项
- 标明信息来源或依据

### 09 User Insight Report

- 总结用户分群、使用场景、痛点、隐性需求
- 给出代表性原话或证据摘要

### 10 PRD Draft

- 仅基于 `06_opportunity_cards.md` 进入需求定义
- 写清目标用户、场景、功能、非目标、指标、约束
- 无证据支撑的功能写为 `Assumption` 或不纳入

### 11 Final Report

至少包含：

- Research Scope
- Evidence Summary
- Product Model
- User Model
- Opportunity Cards
- Market Brief
- Competitor Matrix
- User Insight Report
- Evidence-backed PRD Draft
- Evidence Appendix
- Assumptions
- Evidence Gaps

## PDF

当 `11_final_report.md` 完成且用户需要正式报告时，运行：

```bash
python scripts/md_to_pdf.py 11_final_report.md --pdf final_report.pdf
```
