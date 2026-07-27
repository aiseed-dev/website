# 計測結果 — 第 05 章 example-2

実行環境: Linux 6.18 / Python 3.x / Jinja2 / WeasyPrint 68.1 / markdown-it-py

## 一括生成(主目的)

```
=== 差し込み印刷結果 ===
  対象 : 10 件
  実行時間: 76.96 秒  (1 件あたり 7,696 ms)

  Markdown 合計: 7.9 KB
  PDF 合計     : 2,510.9 KB
  TEXT 合計    : 7.6 KB
```

PDF 生成が支配的(WeasyPrint で 1 件 7.7 秒)。Markdown と TEXT の生成は
ほぼ瞬時。

## Word 差し込みとの比較

| 項目 | Word 差し込み | この Python |
|------|-------------|------------|
| テンプレ作成 | Word + フィールド埋め込み | Markdown + `{{ var }}` |
| データ | Excel または CSV | CSV |
| 出力形式 | Word / PDF | **Markdown / PDF / TEXT 同時** |
| 10 件生成 | 約 5 分(Word 起動 + 確認) | **約 77 秒**(全自動) |
| バージョン管理 | "Binary changed" | **テンプレと CSV の Git diff** |
| AI 連携 | × | **テンプレを Claude に書かせる** |

## サンプル出力(`out/letters/C001.md`)

```markdown
# 契約更新のご案内

**山田農園 御中**
山田 太郎 様

いつも Mochi.ai をご利用いただきありがとうございます。
お客様のご契約は **スタンダードプラン**(月額 **1,980 円**)で、
**2026-08-01** に更新予定です。

## ご契約情報

| 項目 | 内容 |
|------|------|
| 顧客番号 | C001 |
| プラン | スタンダード |
| 月額 | 1,980 円 |
| 更新日 | 2026-08-01 |
| 当期末までの残額 | **5,940 円** |
...
```

PDF 版は同じ内容を A4 + Noto Serif CJK JP で印刷可能な形に。
TEXT 版はメール本文に貼り付けるだけで済む。

## 1 顧客 = 3 ファイル × 10 顧客 = 30 ファイル

```
$ ls out/letters/ | head -9
C001.md
C001.pdf
C001.txt
C002.md
C002.pdf
C002.txt
C003.md
C003.pdf
C003.txt
```

ファイル名 = 顧客 ID。Web フロントから「顧客 ID で更新案内 PDF を取得」
する API を作るのも簡単。

## 来月の運用

```bash
# 1. 新しい更新対象の CSV を data/ に置く
cp ~/Downloads/2026-09-renewals.csv data/recipients.csv

# 2. 走らせる
make all

# 3. PDF を一括メール送信(別途 SMTP スクリプト)
for f in out/letters/*.pdf; do
  python3 send_email.py --to "$(...)" --attach "$f"
done
```

Word でやれば月 50 時間。Python なら月 1 時間。**49 時間の節約**は、
本当の仕事(顧客との対話、戦略判断)に回せる。

## 再現手順

```bash
pip install jinja2 markdown-it-py weasyprint
sudo apt install fonts-noto-cjk
make clean && make all
```
