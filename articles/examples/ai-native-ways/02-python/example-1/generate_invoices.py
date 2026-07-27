#!/usr/bin/env python3
"""100 個のサンプル請求書 PDF を生成する。

各 PDF: A4 1 枚、宛名・明細・合計を含む。WeasyPrint で HTML → PDF。
これをあとで pypdf でテキスト抽出 → 金額集計し、所要時間を測る。
"""
from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

from weasyprint import HTML

random.seed(42)
OUT = Path(__file__).parent / "pdf"
OUT.mkdir(exist_ok=True)

CUSTOMERS = [
    "山田農園", "鈴木商店", "高橋食品", "佐藤畜産", "田中株式会社",
    "渡辺青果", "中村製作所", "小林技研", "斎藤運輸", "加藤建設",
    "吉田出版", "山本印刷", "松本物流", "井上工業", "木村電機",
    "林産業", "清水運送", "山崎商会", "森精密", "池田化学",
]

ITEMS = [
    ("コンサルティング業務", 80000, 250000),
    ("月額保守料", 30000, 120000),
    ("システム開発(時間単価)", 8000, 15000),
    ("出張費", 5000, 50000),
    ("資料制作", 20000, 100000),
    ("研修実施", 50000, 200000),
]

CSS = """
@page { size: A4; margin: 18mm; @bottom-center { content: counter(page); font-size: 8pt; color: #888; } }
body { font-family: 'Noto Serif CJK JP', serif; font-size: 10pt; color: #1a1a1a; }
h1 { font-size: 24pt; border-bottom: 2pt solid #1a1a1a; padding-bottom: 6pt; margin-bottom: 12pt; }
.meta { display: flex; justify-content: space-between; margin-bottom: 18pt; }
.meta div { font-size: 9pt; line-height: 1.7; }
table { width: 100%; border-collapse: collapse; margin: 18pt 0; }
th, td { border: 1pt solid #888; padding: 6pt 8pt; }
th { background: #ebe6d8; text-align: left; }
td.num { text-align: right; }
.totals { width: 50%; margin-left: auto; margin-top: 12pt; }
.totals td { border: none; padding: 4pt 6pt; }
.totals .label { text-align: right; }
.totals .num { text-align: right; }
.totals .grand { font-size: 14pt; font-weight: bold; border-top: 2pt solid #1a1a1a; padding-top: 8pt; }
.footer { margin-top: 36pt; font-size: 9pt; color: #666; border-top: 1pt solid #ccc; padding-top: 8pt; }
"""


def make_invoice(invoice_no: int) -> tuple[str, int]:
    customer = random.choice(CUSTOMERS)
    issue = date(2026, 4, 1) + timedelta(days=random.randint(0, 27))
    due = issue + timedelta(days=30)

    rows = []
    subtotal = 0
    n_items = random.randint(2, 5)
    for _ in range(n_items):
        name, lo, hi = random.choice(ITEMS)
        qty = random.randint(1, 6)
        unit = random.randint(lo, hi)
        amt = qty * unit
        subtotal += amt
        rows.append(
            f"<tr><td>{name}</td><td class='num'>{qty}</td>"
            f"<td class='num'>{unit:,} 円</td><td class='num'>{amt:,} 円</td></tr>"
        )

    tax = subtotal // 10
    total = subtotal + tax

    html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>
<h1>請求書 №{invoice_no:04d}</h1>
<div class='meta'>
  <div><strong>請求先:</strong><br>{customer} 御中</div>
  <div>
    請求日: {issue.isoformat()}<br>
    支払期限: {due.isoformat()}<br>
    請求番号: INV-2026-{invoice_no:04d}
  </div>
</div>
<table>
  <thead><tr><th>品目</th><th>数量</th><th>単価</th><th>金額</th></tr></thead>
  <tbody>{''.join(rows)}</tbody>
</table>
<table class='totals'>
  <tr><td class='label'>小計:</td><td class='num'>{subtotal:,} 円</td></tr>
  <tr><td class='label'>消費税(10%):</td><td class='num'>{tax:,} 円</td></tr>
  <tr><td class='label grand'>合計金額:</td><td class='num grand'>{total:,} 円</td></tr>
</table>
<div class='footer'>
  株式会社 aiseed.dev / 〒770-0000 徳島県徳島市 / inquiry@aiseed.dev<br>
  振込先: 〇〇銀行 普通 1234567 アイシード(カ
</div>
</body></html>"""
    return html, total


def main():
    grand_total = 0
    for n in range(1, 101):
        html, total = make_invoice(n)
        path = OUT / f"INV-2026-{n:04d}.pdf"
        HTML(string=html).write_pdf(path)
        grand_total += total
    files = sorted(OUT.glob("*.pdf"))
    size = sum(p.stat().st_size for p in files)
    print(f"  生成完了: {len(files)} ファイル / 合計サイズ {size / 1024:.1f} KB")
    print(f"  全請求書の合計金額(正解): {grand_total:,} 円")


if __name__ == "__main__":
    main()
