#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 Markdown 研究报告转换为带样式的 HTML，并在可用时导出 PDF。

用法：
    python md_to_pdf.py input.md [--html output.html] [--pdf output.pdf]
                            [--title "报告标题"] [--author "作者"]
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

try:
    import markdown
except ImportError as exc:  # pragma: no cover
    raise SystemExit("缺少依赖，请先安装：pip install markdown") from exc


DEFAULT_TITLE = "新能源产品研究报告"
DEFAULT_SUBTITLE = "基于证据的产品研究报告"
DEFAULT_AUTHOR = "DonkeyKing01"

CSS_TEMPLATE = """
@page {
  size: A4;
  margin: 25mm 20mm 20mm 20mm;

  @top-center {
    content: "HEADER_TEXT";
    font-family: "Source Han Sans SC", "Noto Sans SC", "Microsoft YaHei", Arial, sans-serif;
    font-size: 8pt;
    color: #95a5a6;
    border-bottom: 0.5pt solid #ecf0f1;
    padding-bottom: 3mm;
  }

  @bottom-center {
    content: "第 " counter(page) " 页";
    font-family: "Source Han Sans SC", "Noto Sans SC", "Microsoft YaHei", Arial, sans-serif;
    font-size: 8pt;
    color: #95a5a6;
    border-top: 0.8pt solid #1a5276;
    padding-top: 2mm;
  }
}

@page :first {
  @top-center { content: none; }
  @bottom-center { content: none; }
}

body {
  font-family: "Source Han Sans SC", "Noto Sans SC", "Microsoft YaHei", Arial, sans-serif;
  font-size: 10.5pt;
  line-height: 1.75;
  color: #2c3e50;
  text-align: justify;
}

.cover {
  page-break-after: always;
  text-align: center;
  padding-top: 45%;
}

.cover h1 {
  font-size: 28pt;
  color: #1a5276;
  margin-bottom: 8mm;
  font-weight: bold;
  letter-spacing: 1pt;
}

.cover .subtitle {
  font-size: 14pt;
  color: #7f8c8d;
  margin-bottom: 6mm;
}

.cover .meta {
  font-size: 11pt;
  color: #95a5a6;
  margin-bottom: 4mm;
}

.cover .divider {
  width: 60%;
  margin: 8mm auto;
  border: none;
  border-top: 1.5pt solid #1a5276;
}

h1 {
  font-size: 20pt;
  color: #1a5276;
  margin-top: 16mm;
  margin-bottom: 6mm;
  padding-bottom: 3mm;
  border-bottom: 2pt solid #1a5276;
  page-break-before: always;
  font-weight: bold;
}

h2 {
  font-size: 14pt;
  color: #1e8449;
  margin-top: 10mm;
  margin-bottom: 5mm;
  font-weight: bold;
}

h3 {
  font-size: 12pt;
  color: #2e86c1;
  margin-top: 6mm;
  margin-bottom: 3mm;
  font-weight: bold;
}

h4 {
  font-size: 11pt;
  color: #5b2c6f;
  margin-top: 5mm;
  margin-bottom: 2mm;
  font-weight: bold;
}

p {
  margin-top: 1.5mm;
  margin-bottom: 1.5mm;
  orphans: 3;
  widows: 3;
}

blockquote {
  margin: 4mm 0;
  padding: 4mm 4mm 4mm 10mm;
  background: #f8f9fa;
  border-left: 3pt solid #1a5276;
  color: #5d6d7e;
  font-size: 10pt;
}

blockquote p {
  margin: 1mm 0;
}

strong, b {
  font-weight: bold;
  color: #1a252f;
}

code {
  font-family: "Courier New", Courier, monospace;
  background: #fdf2e9;
  color: #c0392b;
  padding: 0.5mm 1.5mm;
  border-radius: 2pt;
  font-size: 9.5pt;
}

pre {
  background: #f8f9fa;
  padding: 4mm;
  overflow-x: auto;
  border-radius: 4pt;
}

pre code {
  display: block;
  padding: 0;
  background: transparent;
  color: #2c3e50;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 4mm 0;
  font-size: 9.5pt;
}

thead th {
  background: #1a5276;
  color: #ffffff;
  padding: 3mm;
  text-align: left;
  font-weight: bold;
}

tbody td {
  padding: 2.5mm 3mm;
  border-bottom: 0.5pt solid #bdc3c7;
  vertical-align: top;
}

tbody tr:nth-child(even) {
  background: #f8f9fa;
}

hr {
  border: none;
  border-top: 0.5pt solid #bdc3c7;
  margin: 4mm 0;
}

ul, ol {
  margin: 2mm 0;
  padding-left: 8mm;
}

li {
  margin-bottom: 1mm;
}

a {
  color: #2e86c1;
  text-decoration: none;
}
"""


def extract_title(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip() or fallback
    return fallback


def extract_meta_line(markdown_text: str) -> str:
    english_patterns = ("research time", "domain", "object type")
    chinese_patterns = ("研究时间", "所属领域", "研究对象类型")

    for line in markdown_text.splitlines():
        stripped = line.strip().lstrip(">").strip()
        lowered = stripped.lower()
        if any(pattern in lowered for pattern in english_patterns) or any(pattern in stripped for pattern in chinese_patterns):
            return stripped
    return ""


def build_cover_html(title: str, subtitle: str, meta_line: str, author: str) -> str:
    meta_html = f"<div class=\"meta\">{html.escape(meta_line)}</div>" if meta_line else ""
    return f"""
<div class="cover">
  <h1 style="page-break-before: avoid; border: none;">{html.escape(title)}</h1>
  <div class="subtitle">{html.escape(subtitle)}</div>
  {meta_html}
  <hr class="divider">
  <div class="meta">作者：{html.escape(author)}</div>
</div>
"""


def markdown_to_html(markdown_text: str, title: str, subtitle: str, meta_line: str, author: str) -> str:
    html_body = markdown.markdown(
        markdown_text,
        extensions=["tables", "fenced_code", "nl2br", "toc"],
        output_format="html5",
    )

    first_h1_match = re.search(r"<h1.*?>(.*?)</h1>", html_body, flags=re.DOTALL)
    if first_h1_match:
        html_body = html_body.replace(first_h1_match.group(0), "", 1)

    header_text = f"{title} | 新能源产品研究报告"
    css = CSS_TEMPLATE.replace("HEADER_TEXT", header_text.replace('"', "'"))
    cover_html = build_cover_html(title=title, subtitle=subtitle, meta_line=meta_line, author=author)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <style>{css}</style>
</head>
<body>
{cover_html}
{html_body}
</body>
</html>"""


def try_export_pdf(html_content: str, pdf_path: Path) -> bool:
    try:
        from weasyprint import HTML
    except ImportError:
        return False

    HTML(string=html_content).write_pdf(str(pdf_path))
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将 Markdown 报告导出为 HTML 和 PDF。")
    parser.add_argument("input", help="输入 Markdown 文件路径")
    parser.add_argument("--html", help="输出 HTML 文件路径")
    parser.add_argument("--pdf", help="输出 PDF 文件路径")
    parser.add_argument("--title", default=None, help="覆盖报告标题")
    parser.add_argument("--author", default=DEFAULT_AUTHOR, help="封面展示的作者名")
    parser.add_argument("--subtitle", default=DEFAULT_SUBTITLE, help="封面展示的副标题")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise SystemExit(f"输入文件不存在：{input_path}")

    html_path = Path(args.html).resolve() if args.html else input_path.with_suffix(".html")
    pdf_path = Path(args.pdf).resolve() if args.pdf else input_path.with_suffix(".pdf")

    markdown_text = input_path.read_text(encoding="utf-8")
    title = args.title or extract_title(markdown_text, input_path.stem or DEFAULT_TITLE)
    meta_line = extract_meta_line(markdown_text)

    html_content = markdown_to_html(
        markdown_text=markdown_text,
        title=title,
        subtitle=args.subtitle,
        meta_line=meta_line,
        author=args.author,
    )
    html_path.write_text(html_content, encoding="utf-8")
    print(f"已生成 HTML：{html_path}")

    if try_export_pdf(html_content, pdf_path):
        print(f"已生成 PDF：{pdf_path}")
    else:
        print("未检测到 WeasyPrint，已跳过 PDF 导出。")
        print("如需导出 PDF，请先安装：pip install weasyprint")


if __name__ == "__main__":
    main()
