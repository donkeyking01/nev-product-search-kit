# 07 Generate Deliverables

输出最终交付物。必要时先读 `../references/deliverables.md`。

## 默认交付物

```text
07_market_brief.md
08_competitor_matrix.md
09_user_insight_report.md
10_prd_draft.md
11_final_report.md
```

如果用户需要正式报告，再基于 `11_final_report.md` 导出 `final_report.pdf`。

## 目标

把前面阶段形成的证据、模型和机会诊断，整理成产品经理可复核、可继续使用的文档。

## 强制规则

- 所有关键判断都带 `Evidence Trace`。
- `10_prd_draft.md` 必须来自 `06_opportunity_cards.md`。
- 对没有充分证据的内容标注 `Assumption` 或 `Evidence Gap`。
- 最终报告保留证据附录、假设和缺口。

## 完成检查

- 是否回答了最初的研究问题？
- 是否明确展示了竞品差异？
- 是否把用户洞察连接到了具体机会？
- 是否让 PRD 与机会卡片一一对应？
- 是否保留了证据边界，而不是写成确定性宣传稿？

## PDF

在当前目录或目标输出目录中运行：

```bash
python scripts/md_to_pdf.py 11_final_report.md --pdf final_report.pdf
```
