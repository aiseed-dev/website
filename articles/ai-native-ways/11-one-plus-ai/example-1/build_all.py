#!/usr/bin/env python3
"""1 人 SaaS の全アセットを 1 コマンドで生成する。

含むもの:
  1. ランディングページ + 料金 + プライバシー + 会社情報(HTML, 4 ページ)
  2. 月次売上レポート (Markdown + PDF)
  3. 投資家向けピッチ (Marp スライド HTML)
  4. システム構成図 (Mermaid SVG)

これは第 1〜10 章の道具をすべて使う実演。1 人 + Claude で SaaS をローンチ
するときの「現実的な成果物の集合」。
"""
from __future__ import annotations

import csv
import re
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from markdown_it import MarkdownIt
from weasyprint import HTML

HERE = Path(__file__).parent
SITE = HERE / "site"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

md = MarkdownIt("commonmark", {"html": True}).enable("table")

CSS = """
:root { --ink: #1a1a1a; --paper: #f8f5ee; --accent: #c8442a; --rule: #d4cdb8; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Hiragino Mincho ProN", "游明朝", "Noto Serif CJK JP", serif;
  background: var(--paper); color: var(--ink); line-height: 1.85;
  max-width: 720px; margin: 0 auto; padding: 32px 24px;
}
h1 { font-size: 38px; border-bottom: 3px double var(--ink); padding-bottom: 14px; margin-bottom: 24px; }
h2 { font-size: 22px; border-left: 4px solid var(--accent); padding-left: 12px; margin: 32px 0 16px; }
p, ul, ol, table, blockquote { margin-bottom: 18px; }
ul, ol { padding-left: 1.5em; }
table { width: 100%; border-collapse: collapse; }
th, td { border: 1px solid var(--rule); padding: 10px 14px; text-align: left; }
th { background: #ebe6d8; font-weight: 700; }
blockquote { background: #ebe6d8; border-left: 4px solid var(--accent); padding: 16px 20px; }
code { font-family: ui-monospace, monospace; background: #ebe6d8; padding: 1px 5px; border-radius: 2px; font-size: 0.9em; }
a { color: var(--accent); }
nav { margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--rule); font-size: 13px; }
strong { background: linear-gradient(to top, #f7e9c8 35%, transparent 35%); padding: 0 2px; }
"""

PAGE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Mochi.ai</title>
<style>{css}</style>
</head>
<body>
{body}
<nav>© 2026 Mochi.ai · 1 人 + Claude で運営</nav>
</body>
</html>
"""


def build_site() -> dict:
    """ランディング 4 ページを HTML に焼く。"""
    out_dir = OUT / "site"
    out_dir.mkdir(exist_ok=True)
    pages = sorted(SITE.glob("*.md"))
    sizes = {}
    for src in pages:
        text = src.read_text()
        m = re.match(r"# (.+?)\n", text)
        title = m.group(1) if m else src.stem
        html = md.render(text)
        out = out_dir / f"{src.stem}.html"
        out.write_text(PAGE.format(title=title, css=CSS, body=html))
        sizes[src.stem] = out.stat().st_size
    return sizes


def build_monthly_report() -> int:
    """sales.csv → 月次レポート Markdown + PDF。"""
    df = pd.read_csv(HERE / "sales.csv", parse_dates=["date"])
    period = df["date"].dt.to_period("M").iloc[0]
    by_plan = df.groupby("plan")["amount"].agg(["count", "sum"])
    total = int(df["amount"].sum())

    report = f"""# Mochi.ai 月次レポート — {period}

期間: {period}

## サマリ

| 項目 | 値 |
|------|-----|
| 新規契約数 | {len(df)} 件 |
| MRR(月次経常収益) | **{total:,} 円** |
| 平均単価 | {total // len(df):,} 円 |

## プラン別

| プラン | 契約数 | 売上 |
|--------|-------|------|
"""
    for plan, row in by_plan.iterrows():
        report += f"| {plan} | {int(row['count'])} | {int(row['sum']):,} 円 |\n"

    report += f"""
## コスト

| 項目 | 月額 |
|------|------|
| Cloudflare Pages | 0 円(無料枠内) |
| Cloudflare R2(センサデータ) | 約 200 円 |
| Claude Pro($20) | 約 3,000 円 |
| Claude API(異常判定 + 月次集計) | 約 2,000 円 |
| LINE Messaging API | 0 円(無料枠内) |
| ドメイン | 月割 100 円 |
| **合計** | **約 5,300 円** |

## 利益

```
売上    {total:>10,} 円
コスト  -    5,300 円
─────────────────────
利益    {total - 5300:>10,} 円(利益率 {(total - 5300) / total * 100:.1f}%)
```

## アクション

- 商工会経由のプロプランが順調 → 5 月は商工会向けセミナーを 2 件
- ライトプランの解約はゼロ → 製品適合性 OK
- センサ追加の問い合わせが 4 件 → スタンダードへの誘導フローを改善

---

このレポートは `build_all.py` が `sales.csv` から自動生成した。
人間は数値を打ち込んでいない。
"""
    md_path = OUT / "monthly-report.md"
    md_path.write_text(report)

    html_str = PAGE.format(title=f"月次レポート {period}", css=CSS, body=md.render(report))
    pdf_path = OUT / "monthly-report.pdf"
    HTML(string=html_str, base_url=str(HERE)).write_pdf(pdf_path)
    return total


def build_pitch_deck() -> Path:
    """投資家向けピッチを Marp 互換 Markdown + 簡易 HTML 化。"""
    deck = """---
marp: true
theme: default
paginate: true
---

# Mochi.ai
**古民家のための AI 管理人**

1 人 + Claude で運営する、月額 980 円の SaaS

---

## 課題

- 築 100 年の家が日本に 250 万軒
- 持ち主の多くが遠方在住・高齢
- センサ・通報の市場価格は 月額 1 万円〜
- **手の届かない**

---

## 解決

センサキット同梱 + LINE 通知 + AI 月次レポート

**月額 980 円**

- ハードは 1 個 1,500 円(中国製モジュール)
- 通信は Wi-Fi(顧客負担)
- ソフトは 1 人 + Claude が運用
- AI 利用料は 1 顧客あたり月 50 円

---

## 規模

- 2026/04 ローンチ
- **2026/06 末の MRR: ¥850,000**
- 解約率: 0%(まだ 3 ヶ月)
- 顧客獲得コスト: 商工会経由で実質ゼロ

---

## チーム

**1 人 + Claude**

- 代表: 山田 太郎
- 法務: 月 1 万円のスポット契約
- 経理: freee + Claude
- カスタマーサポート: LINE 公式 + Claude が下書き

---

## 数字で見るコスト

| 項目 | 月額 |
|------|------|
| サーバ・ストレージ | 200 円 / 顧客 |
| AI 利用料 | 50 円 / 顧客 |
| 顧客獲得 | 商工会経由で 0 円 |
| 人件費 | 1 人体制 |
| **限界利益率** | **97%** |

---

## 募集

シードラウンド 3,000 万円(評価 3 億円)

- センサキットの量産
- 沖縄・北海道のローカルパートナー獲得
- 英語版 (台湾の古民家向け)
"""
    deck_path = OUT / "pitch-deck.md"
    deck_path.write_text(deck)

    # Marp の代わりに簡易 HTML スライド(セクション ごとに改ページ)
    body_md = re.sub(r"^---$", "<hr>", deck, flags=re.MULTILINE)
    html = md.render(body_md)
    slide_html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Mochi.ai Pitch</title>
<style>
  body {{ font-family: serif; max-width: 900px; margin: 0 auto; padding: 24px; }}
  h1 {{ font-size: 48px; margin-top: 24px; }}
  h2 {{ font-size: 28px; }}
  hr {{ border: none; border-top: 2px dashed #c8442a; margin: 48px 0; }}
  table {{ border-collapse: collapse; }}
  th, td {{ border: 1px solid #ccc; padding: 8px 12px; }}
</style>
</head><body>{html}</body></html>"""
    (OUT / "pitch-deck.html").write_text(slide_html)
    return deck_path


def build_architecture_diagram() -> Path:
    """システム構成図(Mermaid テキスト + 説明)。"""
    diagram = """# Mochi.ai システム構成

```mermaid
flowchart TB
    subgraph 顧客宅
        S[センサキット] --> R[Wi-Fi ルータ]
    end
    R -->|HTTPS| API[FastAPI on Cloudflare]
    API --> Q[(R2 ストレージ)]
    API --> J[ジョブキュー]
    J -->|異常判定 / 要約| C[Claude API]
    C --> J
    J --> LINE[LINE Messaging API]
    LINE --> 顧客スマホ
    API --> Cron[週次/月次 Cron]
    Cron --> R2[(月次 PDF)]
```

## 各コンポーネントの役割

| コンポーネント | 役割 | コスト |
|----------------|------|-------|
| センサキット | 温湿度・人感を 5 分間隔で送信 | 仕入 1,500 円/個(顧客買い切り) |
| Cloudflare Pages + Workers | フロント + API | 無料枠 |
| R2 ストレージ | センサデータ + PDF 保存 | 200 円/月/顧客 |
| Claude API | 異常判定 + 週次/月次サマリ | 50 円/月/顧客 |
| LINE Messaging API | 通知 | 無料枠 |

## 1 人 + AI で回せる理由

- フロントは静的 HTML(このフォルダの `site/` で生成)
- API は FastAPI 1 ファイル(コードは Claude が書く)
- 月次レポートは `build_all.py` の関数 1 つ
- カスタマー対応の下書きは Claude
- 経理は freee + 週 1 回の Claude チェック

**手作業の合計時間: 週 5〜10 時間**。
"""
    arch_path = OUT / "architecture.md"
    arch_path.write_text(diagram)
    return arch_path


def main():
    t0 = time.perf_counter()
    print("=== 1 人 + AI で SaaS を組み立てる ===\n")

    print("1. ランディングページ 4 枚を生成...")
    sizes = build_site()
    for name, sz in sizes.items():
        print(f"   → site/{name}.html  ({sz:,} B)")

    print("\n2. 月次レポート (Markdown + PDF) を生成...")
    revenue = build_monthly_report()
    md_size = (OUT / "monthly-report.md").stat().st_size
    pdf_size = (OUT / "monthly-report.pdf").stat().st_size
    print(f"   → monthly-report.md   ({md_size:,} B)")
    print(f"   → monthly-report.pdf  ({pdf_size:,} B)")
    print(f"   ★ 売上合計: {revenue:,} 円")

    print("\n3. 投資家ピッチを生成...")
    deck = build_pitch_deck()
    print(f"   → {deck.name}")
    print(f"   → pitch-deck.html")

    print("\n4. システム構成図を生成...")
    arch = build_architecture_diagram()
    print(f"   → {arch.name}")

    elapsed = time.perf_counter() - t0
    print(f"\n=== 全成果物を {elapsed*1000:.0f} ms で生成 ===")
    total_size = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    files = sum(1 for _ in OUT.rglob("*") if _.is_file())
    print(f"  生成ファイル: {files} 個 / 合計 {total_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
