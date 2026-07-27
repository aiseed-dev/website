#!/usr/bin/env python3
"""個人事業主の 1 ヶ月クローズ ── 1 コマンドで全部生成。

入力(月初〜月末を CSV に貯めるだけ):
  - data/clients.csv     顧客マスタ
  - data/work_log.csv    時間 × 単価 で売上(複数顧客)
  - data/expenses.csv    経費

出力(`out/2026-04/` 配下):
  - 顧客ごとの請求書 PDF (3 件)
  - 顧客ごとの請求書 Markdown
  - 月次サマリ Markdown(売上・経費・利益)
  - 確定申告用の経費 CSV(国税庁仕訳に近い形)
  - 月次レポート PDF
  - 全部の状況を 1 つの index.md にまとめる

これが「個人事業主 + AI」の月次フロー。
"""
from __future__ import annotations

import csv
import time
from collections import defaultdict
from datetime import date
from pathlib import Path

import pandas as pd
from jinja2 import Environment
from markdown_it import MarkdownIt
from weasyprint import HTML

HERE = Path(__file__).parent
DATA = HERE / "data"
PERIOD = "2026-04"
OUT = HERE / "out" / PERIOD
INVOICES_DIR = OUT / "invoices"
INVOICES_DIR.mkdir(parents=True, exist_ok=True)

md = MarkdownIt("commonmark", {"html": True}).enable("table")

CSS = """
@page { size: A4; margin: 22mm; @bottom-center { content: counter(page); font-size: 8pt; color: #888; } }
body { font-family: 'Noto Serif CJK JP', serif; font-size: 11pt; line-height: 1.7; color: #1a1a1a; }
h1 { font-size: 22pt; border-bottom: 2pt solid #1a1a1a; padding-bottom: 6pt; margin-bottom: 18pt; }
h2 { font-size: 15pt; margin-top: 22pt; margin-bottom: 10pt; color: #2f5f3f; border-left: 4pt solid #2f5f3f; padding-left: 8pt; }
table { width: 100%; border-collapse: collapse; margin: 12pt 0; }
th, td { border: 1pt solid #888; padding: 6pt 10pt; }
th { background: #ebe6d8; }
td.num { text-align: right; }
strong { background: #f7e9c8; padding: 0 2pt; }
"""


INVOICE_TEMPLATE = """# 請求書 INV-{{ period }}-{{ client_id }}

**{{ company }} 御中**
{{ name }} 様

下記のとおりご請求申し上げます。

| 項目 | 内容 |
|------|------|
| 請求番号 | INV-{{ period }}-{{ client_id }} |
| 請求日 | {{ today }} |
| 支払期限 | {{ due }} |
| 請求先 | {{ company }} / {{ name }} 様 |
| 件数 | {{ items|length }} 件 |

## 業務内訳

| 日付 | 業務 | 時間 | 単価 | 金額 |
|------|------|----|------|------|
{% for it in items -%}
| {{ it.date }} | {{ it.description }} | {{ "%.1f"|format(it.hours) }} h | {{ "%d"|format(it.rate)|comma }} 円 | {{ "%d"|format(it.amount)|comma }} 円 |
{% endfor %}

| 項目 | 金額 |
|------|------|
| 小計 | {{ subtotal_str }} 円 |
| 消費税(10%) | {{ tax_str }} 円 |
| **合計** | **{{ total_str }} 円** |

---

aiseed.dev ｜ 振込先: 〇〇銀行 普通 1234567 アイシード(カ
"""


def comma(n):
    return f"{int(n):,}"


def main():
    t0 = time.perf_counter()

    clients = {r["client_id"]: r for r in csv.DictReader((DATA / "clients.csv").open())}

    # 業務ログを顧客ごとに集計
    log_df = pd.read_csv(DATA / "work_log.csv", parse_dates=["date"])
    log_df["amount"] = log_df["hours"] * log_df["rate"]

    by_client = defaultdict(list)
    for _, row in log_df.iterrows():
        by_client[row["client_id"]].append(row.to_dict())

    # 請求書 PDF を顧客ごとに生成
    today = date(2026, 5, 1)
    due = date(2026, 5, 31)
    invoices_summary = []
    env = Environment()
    env.filters["comma"] = comma
    tpl = env.from_string(INVOICE_TEMPLATE)

    for cid, items in by_client.items():
        cli = clients[cid]
        subtotal = sum(it["amount"] for it in items)
        tax = int(subtotal * 0.10)
        total = int(subtotal) + tax
        for it in items:
            it["date"] = it["date"].strftime("%Y-%m-%d")

        md_text = tpl.render(
            period=PERIOD, client_id=cid,
            company=cli["company"], name=cli["name"],
            today=today.isoformat(), due=due.isoformat(),
            items=items,
            subtotal_str=comma(subtotal),
            tax_str=comma(tax),
            total_str=comma(total),
        )
        (INVOICES_DIR / f"INV-{PERIOD}-{cid}.md").write_text(md_text)

        html_body = md.render(md_text)
        full = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html_body}</body></html>"
        HTML(string=full).write_pdf(INVOICES_DIR / f"INV-{PERIOD}-{cid}.pdf")

        invoices_summary.append({
            "client_id": cid,
            "company": cli["company"],
            "items": len(items),
            "subtotal": int(subtotal),
            "total": total,
        })

    # 経費集計
    exp = pd.read_csv(DATA / "expenses.csv")
    by_cat = exp.groupby("category")["amount"].sum().sort_values(ascending=False)
    expense_total = int(exp["amount"].sum())

    # 確定申告風の経費仕訳 CSV(月次)
    tax_csv = OUT / "tax-expenses.csv"
    with tax_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["日付", "勘定科目", "金額", "摘要"])
        for _, r in exp.iterrows():
            w.writerow([r["date"], r["category"], int(r["amount"]), r["note"]])

    # 売上集計
    revenue_total = sum(s["total"] for s in invoices_summary)
    pretax_revenue = int(revenue_total / 1.10)
    profit = pretax_revenue - expense_total

    # 月次サマリ Markdown
    summary_md = OUT / "summary.md"
    summary_md.write_text(f"""# 月次サマリ {PERIOD}

## 売上(税抜)

| 顧客 | 件数 | 税込合計 |
|------|-----|---------|
""" + "".join(f"| {s['company']} | {s['items']} 件 | {comma(s['total'])} 円 |\n" for s in invoices_summary) + f"""

| 項目 | 金額 |
|------|------|
| 売上(税込) | **{comma(revenue_total)} 円** |
| 売上(税抜)| {comma(pretax_revenue)} 円 |

## 経費

| カテゴリ | 金額 |
|----------|------|
""" + "".join(f"| {c} | {comma(v)} 円 |\n" for c, v in by_cat.items()) + f"""
| **経費合計** | **{comma(expense_total)} 円** |

## 利益(税抜売上 - 経費)

**{comma(profit)} 円**(利益率 {profit/pretax_revenue*100:.1f}%)

## 翌月への申し送り

- 確定申告用の経費 CSV: `tax-expenses.csv`
- 各顧客への請求書: `invoices/INV-{PERIOD}-AXXX.pdf` を {today} に送付済
- 入金確認は支払期限 {due} 後にチェック

---

これは `build_month.py` が CSV から自動生成した。
来月は CSV を 3 つ更新して `make all` するだけ。
""")

    # 月次サマリ PDF
    html_body = md.render(summary_md.read_text())
    full = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html_body}</body></html>"
    HTML(string=full).write_pdf(OUT / "summary.pdf")

    # index.md
    index_md = OUT / "index.md"
    index_md.write_text(f"""# {PERIOD} 月次成果物一覧

| ファイル | 用途 |
|----------|------|
| `summary.md` / `summary.pdf` | 月次サマリ(自分用) |
| `invoices/*.md` | 請求書 Markdown(下書き) |
| `invoices/*.pdf` | 請求書 PDF(送付用) |
| `tax-expenses.csv` | 確定申告用の経費仕訳 |

## 数字

- 売上(税込): **{comma(revenue_total)} 円**
- 経費: **{comma(expense_total)} 円**
- 利益: **{comma(profit)} 円**
- 顧客: {len(invoices_summary)} 社
- 業務件数: {len(log_df)} 件
""")

    elapsed = time.perf_counter() - t0
    print(f"\n=== 月次クロージング完了 ({PERIOD}) ===")
    print(f"  実行時間: {elapsed:.2f} 秒")
    print()
    print(f"  顧客 : {len(invoices_summary)} 社")
    print(f"  業務 : {len(log_df)} 件")
    print(f"  経費 : {len(exp)} 件")
    print()
    print(f"  売上(税込): {comma(revenue_total)} 円")
    print(f"  経費       : {comma(expense_total)} 円")
    print(f"  利益       : {comma(profit)} 円  (利益率 {profit/pretax_revenue*100:.1f}%)")
    print()
    files = sorted((OUT.rglob("*")))
    out_files = [f for f in files if f.is_file()]
    print(f"  生成ファイル: {len(out_files)} 個 / {sum(f.stat().st_size for f in out_files)/1024:.1f} KB")
    for f in out_files:
        print(f"    - {f.relative_to(OUT.parent)}")


if __name__ == "__main__":
    main()
