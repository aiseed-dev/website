#!/usr/bin/env python3
"""差し込み印刷を Python で。

Word の「差し込み印刷ウィザード」が「Markdown テンプレ + CSV + Python」に置き換わる。

入力:
  - data/recipients.csv  (顧客 10 件)
  - template.md          (Jinja2 テンプレ、{{ var }} で差し込み)

出力:
  - out/letters/<id>.md   (Markdown のお手紙、10 件)
  - out/letters/<id>.pdf  (印刷用 PDF、10 件)
  - out/letters/<id>.txt  (メール本文用テキスト、10 件)
"""
from __future__ import annotations

import csv
import time
from pathlib import Path

from jinja2 import Template
from markdown_it import MarkdownIt
from weasyprint import HTML

HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = HERE / "out" / "letters"
OUT.mkdir(parents=True, exist_ok=True)

md = MarkdownIt("commonmark", {"html": True}).enable("table")

PDF_CSS = """
@page { size: A4; margin: 22mm; @bottom-center { content: counter(page); font-size: 8pt; color: #888; } }
body { font-family: 'Noto Serif CJK JP', serif; font-size: 11pt; line-height: 1.7; color: #1a1a1a; }
h1 { font-size: 22pt; border-bottom: 2pt solid #1a1a1a; padding-bottom: 6pt; margin-bottom: 18pt; }
h2 { font-size: 15pt; margin-top: 24pt; margin-bottom: 10pt; color: #2f5f3f; }
table { width: 100%; border-collapse: collapse; margin: 12pt 0; }
th, td { border: 1pt solid #888; padding: 6pt 10pt; }
th { background: #ebe6d8; }
strong { background: #f7e9c8; padding: 0 2pt; }
hr { margin: 24pt 0; border: none; border-top: 1pt solid #ccc; }
"""


def render_one(row: dict) -> dict:
    """1 顧客あたり 3 形式 (md / pdf / txt) を生成。"""
    # 数値整形
    row = {**row}
    row["monthly_yen_fmt"] = f"{int(row['monthly_yen']):,}"
    row["balance_yen_fmt"] = f"{int(row['balance_yen']):,}"

    # 1) Markdown
    md_src = (HERE / "template.md").read_text()
    md_filled = Template(md_src).render(**row)
    cid = row["customer_id"]
    (OUT / f"{cid}.md").write_text(md_filled)

    # 2) PDF
    html_body = md.render(md_filled)
    full_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>更新案内 {cid}</title><style>{PDF_CSS}</style></head>
<body>{html_body}</body></html>"""
    HTML(string=full_html).write_pdf(OUT / f"{cid}.pdf")

    # 3) プレーンテキスト(メール本文用)
    plain = md_filled
    # Markdown のマークアップを軽く除去
    for repl in [("**", ""), ("---", "----"), ("# ", ""), ("## ", "")]:
        plain = plain.replace(repl[0], repl[1])
    (OUT / f"{cid}.txt").write_text(plain)

    return {
        "id": cid,
        "company": row["company"],
        "md_size": (OUT / f"{cid}.md").stat().st_size,
        "pdf_size": (OUT / f"{cid}.pdf").stat().st_size,
        "txt_size": (OUT / f"{cid}.txt").stat().st_size,
    }


def main():
    with (DATA / "recipients.csv").open() as f:
        rows = list(csv.DictReader(f))

    t0 = time.perf_counter()
    results = [render_one(r) for r in rows]
    elapsed = time.perf_counter() - t0

    md_total = sum(r["md_size"] for r in results)
    pdf_total = sum(r["pdf_size"] for r in results)
    txt_total = sum(r["txt_size"] for r in results)

    print(f"\n=== 差し込み印刷結果 ===")
    print(f"  対象 : {len(rows)} 件")
    print(f"  実行時間: {elapsed:.2f} 秒  (1 件あたり {elapsed/len(rows)*1000:.0f} ms)")
    print()
    print(f"  Markdown 合計: {md_total/1024:.1f} KB")
    print(f"  PDF 合計     : {pdf_total/1024:.1f} KB")
    print(f"  TEXT 合計    : {txt_total/1024:.1f} KB")
    print()
    print("  出力例:")
    for r in results[:3]:
        print(f"    out/letters/{r['id']}.{{md,pdf,txt}}  ({r['company']})")
    print(f"    ... 計 {len(rows)} 件")


if __name__ == "__main__":
    main()
