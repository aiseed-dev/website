#!/usr/bin/env python3
"""data/*.csv から月次報告書 (Markdown + Mermaid) を生成する。

事務職の月次報告フロー:
  Office 旧来: Excel で集計 → Word に貼る → 数字を直す → グラフを作って貼る → PowerPoint に書き直す
  AI ネイティブ: CSV を pandas で読む → Markdown のテンプレに値を埋める → Marp でスライドも一発生成

このスクリプトが「全部」だ。約 100 行。Claude が書く。月次のたびに走らせる。
"""
from __future__ import annotations

import time
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


def main():
    t0 = time.perf_counter()

    sales = pd.read_csv(DATA / "sales.csv", parse_dates=["date"])
    expenses = pd.read_csv(DATA / "expenses.csv", parse_dates=["date"])

    period = sales["date"].dt.to_period("M").iloc[0]
    by_region = sales.groupby("region")["revenue"].sum().sort_values(ascending=False)
    by_product = sales.groupby("product")["revenue"].sum().sort_values(ascending=False)
    by_category = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)
    revenue_total = int(sales["revenue"].sum())
    expense_total = int(expenses["amount"].sum())
    profit = revenue_total - expense_total

    # Mermaid のパイ図を組み立てる
    mermaid_region = "pie title 地域別売上\n" + "\n".join(
        f'    "{r}" : {v}' for r, v in by_region.items()
    )
    mermaid_category = "pie title 経費カテゴリ\n" + "\n".join(
        f'    "{c}" : {v}' for c, v in by_category.items()
    )

    # Markdown 報告書本体
    report = f"""---
marp: true
theme: default
paginate: true
---

# 2026 年 {period.month} 月度 月次報告
**期間: {period}**  会社: 株式会社 aiseed.dev

---

## 1. 概要

| 項目 | 金額 |
|------|------|
| 売上 | **{revenue_total:,} 円** |
| 経費 | {expense_total:,} 円 |
| 利益 | **{profit:,} 円** |
| 利益率 | {profit / revenue_total * 100:.1f}% |

---

## 2. 売上 — 地域別

| 地域 | 売上 |
|------|------|
"""
    for r, v in by_region.items():
        report += f"| {r} | {v:,} 円 |\n"
    report += f"""
```mermaid
{mermaid_region}
```

---

## 3. 売上 — 商品別

| 商品 | 売上 |
|------|------|
"""
    for p, v in by_product.items():
        report += f"| {p} | {v:,} 円 |\n"

    report += f"""
---

## 4. 経費 — カテゴリ別

| カテゴリ | 金額 |
|----------|------|
"""
    for c, v in by_category.items():
        report += f"| {c} | {v:,} 円 |\n"
    report += f"""
```mermaid
{mermaid_category}
```

---

## 5. コメント

- 売上は前月比でデータが無いため未計算
- 広告費が経費の {by_category.get('広告費', 0) / expense_total * 100:.0f}% を占める
- {by_region.index[0]} 地域が売上全体の {by_region.iloc[0] / revenue_total * 100:.0f}% を担う
- 来月以降のアクションは経営会議で決定

---

## 付録: 出典データ

- `data/sales.csv` — {len(sales)} 件
- `data/expenses.csv` — {len(expenses)} 件
- このレポートは `build_report.py` が CSV から自動生成
"""

    md_path = OUT / "report.md"
    md_path.write_text(report)

    elapsed = time.perf_counter() - t0
    print(f"  → {md_path}")
    print(f"  生成時間: {elapsed*1000:.1f} ms")
    print(f"  行数: {len(report.splitlines())}")
    print(f"  バイト数: {len(report.encode())}")


if __name__ == "__main__":
    main()
