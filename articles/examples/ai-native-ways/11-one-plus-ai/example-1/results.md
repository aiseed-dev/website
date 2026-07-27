# 計測結果 — 第 11 章 example-1

実行環境: Linux 6.18 / Python 3.x / pandas 3.0 / WeasyPrint 68.1

## ビルド結果

```
=== 1 人 + AI で SaaS を組み立てる ===

1. ランディングページ 4 枚を生成...
   → site/index.html    (2,470 B)
   → site/pricing.html  (2,175 B)
   → site/privacy.html  (2,201 B)
   → site/about.html    (2,091 B)

2. 月次レポート (Markdown + PDF) を生成...
   → monthly-report.md   (1,325 B)
   → monthly-report.pdf  (269,400 B)
   ★ 売上合計: 23,740 円

3. 投資家ピッチを生成...
   → pitch-deck.md
   → pitch-deck.html

4. システム構成図を生成...
   → architecture.md

=== 全成果物を 7958 ms で生成 ===
  生成ファイル: 9 個 / 合計 278.1 KB
```

## 入力 vs 出力

| ソース | サイズ |
|--------|-------|
| `site/*.md`(4 ファイル) | 約 2 KB |
| `sales.csv` | 約 0.5 KB |
| `build_all.py` | 約 8.5 KB |
| **入力合計** | **約 11 KB** |

| 出力 | サイズ |
|------|--------|
| サイト HTML 4 枚 | 約 9 KB |
| 月次レポート Markdown | 1.3 KB |
| 月次レポート PDF | 269 KB |
| ピッチ Markdown | 1.4 KB |
| ピッチ HTML | 2.4 KB |
| 構成図 Markdown | 1.3 KB |
| **出力合計** | **約 285 KB** |

11 KB のソースから 285 KB の **顧客に出せる成果物**ができる。

## 1 人 SaaS のコスト構造

`out/monthly-report.md` の数字より:

| 項目 | 月額 |
|------|------|
| Cloudflare Pages(フロント) | 0 円(無料枠) |
| Cloudflare R2(センサデータ) | 200 円/顧客 |
| Claude Pro | 3,000 円 |
| Claude API | 50 円/顧客 |
| LINE Messaging API | 0 円(無料枠) |
| ドメイン | 100 円(月割) |
| **固定費合計** | **約 3,100 円** |
| **変動費(顧客あたり)** | **250 円** |

利益率(売上 23,740 円ベース): **約 78%**。
顧客が増えれば 90% 超に向かう。

これが「**1 人 + AI** が新しい仕事の単位」の数値的な意味。

## 章本文との対応

- 「**創業者 1 人 + Claude + 必要に応じて時間契約の専門家**」 ── このフォルダ
  全体がそれ。法務だけ月 1 万円で外注する想定。
- 「**人件費が下がり、意思決定が速くなる**」 ── ローンチ準備が `make all`
  1 コマンド、来月の月次レポートも `sales.csv` を差し替えて `make all`。
- 「**書類仕事が消える**」 ── ピッチ・月次・サイトが Markdown で更新できる。
  PowerPoint も Word も Excel も一度も開いていない。

## 来月の運用

```bash
# 1. 新しい売上を sales.csv に追記
$EDITOR sales.csv

# 2. 全成果物を再生成
make all

# 3. PDF を投資家にメール、HTML を Cloudflare Pages にデプロイ
```

合計 5 分。

## 再現手順

```bash
pip install pandas markdown-it-py weasyprint
sudo apt install fonts-noto-cjk
make clean && make all
```
