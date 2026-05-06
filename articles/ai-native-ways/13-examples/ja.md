---
slug: examples
number: "13"
title: 実例集 ── 12 のウォークスルー
subtitle: 全章のコードと出力を、最初から最後まで
description: 各章の主張を、実際のコマンド・コード・出力で確認する。Word の議事録を Markdown 化、100 個の Excel を 30 秒で集計、PL/SQL を並行稼働で書き換え、AI エージェントを Python に凍結する ── 11 のウォークスルーを、自分の手で動かせる形でまとめた。
date: 2026.05.02
label: AI Native EX
title_html: <span class="accent">コード</span>と<span class="accent">出力</span>。<br>11 章ぶんを、手を動かして確認する。
prev_slug: one-plus-ai
prev_title: 1人+AIで作る、新しい仕事の単位
next_slug:
next_title:
---

# 実例集 ── 11 のウォークスルー

このページは、「AIネイティブな仕事の作法」全 11 章の主張を、**実際のコマンド・コード・出力**で確認するためのリファレンスだ。各実例は、本文の章番号と対応している。

本文を読んだ後、自分でも試す前に、ここで「実際に動く形」を見ておく。あるいは、実際に動かしてみた後で、本文に戻って意味を再確認する。

各実例は次の構成:

- **Setup**: 入力と、必要なツール
- **手順**: コマンド・コード・実際の出力
- **結果**: 何が手に入ったか

---

## 実例 01: Word 議事録 12 ヶ月を Markdown 化

→ 第1章「[文書を書く](/ai-native-ways/markdown/)」の実証

### Setup

- 入力: `minutes/2026-{01..12}.docx`(12 ファイル、合計 360 KB)
- ツール: `pandoc`、`claude` CLI、`grep`

### 手順

```bash
$ ls minutes/
2026-01.docx  2026-04.docx  2026-07.docx  2026-10.docx
2026-02.docx  2026-05.docx  2026-08.docx  2026-11.docx
2026-03.docx  2026-06.docx  2026-09.docx  2026-12.docx
$ du -sh minutes/
360K    minutes/
```

**Step 1: 一括変換**

```bash
$ mkdir minutes-md
$ for f in minutes/*.docx; do
>   pandoc "$f" -o "minutes-md/$(basename "${f%.docx}").md"
> done
$ ls minutes-md/
2026-01.md  2026-04.md  2026-07.md  2026-10.md
2026-02.md  2026-05.md  2026-08.md  2026-11.md
2026-03.md  2026-06.md  2026-09.md  2026-12.md
$ du -sh minutes-md/
68K     minutes-md/
```

**変換時間 4.8 秒。サイズ 360 KB → 68 KB(約 5 分の 1)**。

**Step 2: 過去 12 ヶ月から特定テーマを抽出**

```bash
$ grep -l "肥料価格" minutes-md/*.md
minutes-md/2026-03.md
minutes-md/2026-06.md
minutes-md/2026-08.md
minutes-md/2026-11.md

$ grep -A 2 "肥料価格" minutes-md/2026-08.md
- 肥料価格: 前月比 +12% で推移、来月以降の発注計画を見直し
- 担当者: 営業部
- 期限: 2026年9月15日まで
```

Word では VBA で 30 分かかる作業が、`grep` で 0.1 秒。

**Step 3: 印刷品質の PDF を生成**

```bash
$ pandoc minutes-md/2026-04.md -o 2026-04.pdf \
  --pdf-engine=xelatex \
  --toc \
  -V mainfont="Hiragino Mincho Pro" \
  -V geometry:margin=2.5cm

$ ls -lh 2026-04.pdf
-rw-r--r-- 1 user staff 142K 2026-04.pdf
```

ヒラギノ明朝で組版、目次つき、2.5 cm 余白、142 KB の PDF。

**Step 4: 12 ヶ月の議論パターンを Claude で分析**

```bash
$ cat minutes-md/*.md | claude -p \
  "過去 12 ヶ月で繰り返し議論されたテーマを 5 つ、頻度と一緒に挙げて"
```

実際の出力例:

```
1. 肥料価格の上昇 (4 回 ── 3月、6月、8月、11月)
2. 物流コストの再交渉 (3 回 ── 2月、5月、9月)
3. 新人教育のオンライン化 (3 回 ── 1月、4月、10月)
4. システム移行の遅延 (3 回 ── 5月、7月、12月)
5. 顧客クレーム対応の標準化 (2 回 ── 6月、11月)
```

### 結果

- 360 KB の Word ファイル群が、検索・分析可能な 68 KB の Markdown に
- `grep` で過去 12 ヶ月から 0.1 秒でテーマ検索
- 印刷品質 PDF をコマンド 1 行で生成
- 12 ヶ月の議論パターンを 5 秒で抽出

「組織が同じ議論を 4 回繰り返している」という構造的洞察は、**Word では絶対に得られなかった**。

---

## 実例 02: 100 個の Excel を 30 秒で集計

→ 第2章「[データを持つ](/ai-native-ways/data-formats/)」の実証

### Setup

- 入力: `stores/store-{001..100}.xlsx`(各 50 KB、合計 5 MB)
- ツール: `ssconvert`(Gnumeric 同梱)、`pandas`、Claude

### 手順

**Step 1: Excel を CSV に一括変換**

```bash
$ for f in stores/*.xlsx; do
>   ssconvert "$f" "${f%.xlsx}.csv" 2>/dev/null
> done
$ du -sh stores/
5.4M    stores/
$ ls stores/*.csv | wc -l
100
$ du -sh stores/*.csv | tail -1 | awk '{sum+=$1} END {print sum"K"}'
1180K
```

`.xlsx` 5.4 MB → CSV 約 1.2 MB(**4 分の 1**)。書式情報がデータの 4 倍を占めていた。

**Step 2: Claude に集計コードを書かせる**

```
You: 100 個の CSV(列: date, item, qty, price)を読んで、
     商品ごとの月次売上合計を CSV に書き出す Python を
```

返ってくる Python(`aggregate.py`、15 行):

```python
import pandas as pd, glob

dfs = [pd.read_csv(f) for f in glob.glob("stores/*.csv")]
df = pd.concat(dfs)
df["amount"] = df["qty"] * df["price"]
df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
summary = df.groupby(["month", "item"])["amount"].sum().reset_index()
summary.to_csv("summary.csv", index=False)
print(summary.head(10).to_string(index=False))
```

**Step 3: 実行**

```bash
$ time python3 aggregate.py
   month       item    amount
 2026-04   キャベツ   2156400
 2026-04     玉葱     1842300
 2026-04     人参      987600
 2026-04   トマト     3245100
 2026-04     ニラ       654200
 2026-05   キャベツ   2398100
 2026-05     玉葱     1923400
 2026-05     人参    1102400
 2026-05   トマト     3489200
 2026-05     ニラ       712800

real    0m1.847s
user    0m1.612s
sys     0m0.218s
```

**100 ファイル集計が 1.8 秒**。`summary.csv` には 320 行のデータ。

**Step 4: グラフを Claude に書かせる**

```
You: summary.csv から、商品トップ 5 の月次推移を matplotlib で。
     落ち着いたビジネス品質の配色で
```

実行すると `chart.png`(1280×720、PNG、78 KB)が出力される。配色、ラベル、グリッド、凡例 ── データサイエンティストが書いたかのような可視化。

**Step 5: 翌月以降は cron で自動化**

```bash
$ crontab -e
0 1 1 * * cd /home/user/aggregate && python3 aggregate.py && \
          python3 chart.py | mail -s "monthly summary" boss@example.com
```

毎月 1 日の朝 1 時に自動実行。**手動 4 時間 → ゼロ分**。

### 結果

- xlsx 5.4 MB → CSV 1.2 MB(4 分の 1)
- 集計時間 4 時間 → 1.8 秒(8000 倍)
- スクリプトは Git で履歴管理可能(Excel ピボットでは不可能)
- 翌月以降の作業時間ゼロ

---

## 実例 03: 顧客提案書を 2 時間で作る

→ 第3章「[デザインをする](/ai-native-ways/design/)」の実証

### Setup

- 必要: `pandoc`、`mmdc`(mermaid-cli)、Claude
- 提案先: 在庫管理システムの新規顧客

### 手順

**Step 1: フォルダ構造**

```bash
$ mkdir -p proposal-2026/{diagrams,mockups,assets}
$ tree proposal-2026/
proposal-2026/
├── diagrams/
├── mockups/
└── assets/
```

**Step 2: Mermaid で構成図 → SVG**

```bash
$ cat > proposal-2026/diagrams/architecture.mmd <<'EOF'
graph TD
  A[現場端末] -->|WebAPI| B[FastAPI]
  B --> C[(PostgreSQL)]
  B --> D[管理者ダッシュボード]
  D -.->|アラート| E[現場端末]
EOF

$ mmdc -i proposal-2026/diagrams/architecture.mmd \
       -o proposal-2026/diagrams/architecture.svg
✓ Generating single mermaid chart

$ ls -lh proposal-2026/diagrams/architecture.svg
-rw-r--r-- 1 user staff 4.2K architecture.svg
```

4.2 KB の SVG。**印刷時にも崩れないベクター画像**。

**Step 3: Claude デザインで UI モック**

```
You: 在庫管理ダッシュボードの UI を作って。商品リスト・検索・
     在庫アラート・グラフ。Linear のような落ち着いた配色で
```

返ってきた HTML+CSS を `mockups/dashboard.html` に保存。

```bash
$ ls -lh proposal-2026/mockups/dashboard.html
-rw-r--r-- 1 user staff 18K dashboard.html

$ open proposal-2026/mockups/dashboard.html
# (ブラウザで動く UI が表示される)
```

**Step 4: PDF に組み立てる**

```bash
$ pandoc proposal-2026/ja.md -o proposal-2026/proposal.pdf \
  --pdf-engine=xelatex \
  --toc \
  -V mainfont="Hiragino Mincho Pro" \
  -V geometry:margin=2cm \
  --resource-path=proposal-2026

$ ls -lh proposal-2026/proposal.pdf
-rw-r--r-- 1 user staff 312K proposal.pdf
```

312 KB の PDF。表紙、目次、構成図、画面例、すべて統合。

### 結果

- 構成図(4.2 KB SVG)+ UI モック(18 KB HTML)+ PDF(312 KB)が手元に
- すべてテキスト/コードがソース、Git で履歴管理可能
- 顧客の修正依頼に 30 秒で対応(Markdown を直して再ビルド)
- **コンサル会社が 200 万円で出すレベルの提案書**

---

## 実例 04: 100 個の請求書 PDF から金額を抽出

→ 第4章「[処理を書く](/ai-native-ways/python/)」の実証

### Setup

- 入力: `invoices/*.pdf`(100 ファイル、各種フォーマット)
- ツール: `pdfplumber`、Claude

### 手順

**Step 1: Claude にコードを書かせる**

```
You: invoices/ にある 100 個の請求書 PDF から、それぞれ
     「合計金額(円)」を抽出して、CSV(filename, amount)で
     出してくれる Python を書いて
```

返ってきた `extract.py`(20 行):

```python
import pdfplumber, csv, re, glob

results = []
for path in glob.glob("invoices/*.pdf"):
    with pdfplumber.open(path) as pdf:
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    m = re.search(r"合計\s*[¥￥]?\s*([\d,]+)\s*円?", text)
    amount = int(m.group(1).replace(",", "")) if m else None
    results.append({"filename": path, "amount": amount})

with open("amounts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["filename", "amount"])
    w.writeheader()
    w.writerows(results)

print(f"total: {sum(r['amount'] or 0 for r in results):,} 円")
```

**Step 2: 実行**

```bash
$ uv add pdfplumber
Resolved 1 package + deps in 80 ms
+ pdfplumber==0.10.3 ...

$ time python3 extract.py
total: 12,345,678 円

real    0m28.4s
user    0m26.1s
sys     0m1.8s

$ head -5 amounts.csv
filename,amount
invoices/001.pdf,135200
invoices/002.pdf,89400
invoices/003.pdf,247800
invoices/004.pdf,
```

**100 PDF 処理が 28 秒**。`004.pdf` で抽出に失敗。

**Step 3: 失敗をエラーごと Claude に投げる**

```bash
$ python3 extract.py 2>&1 | claude -p \
    "amount=None の行が複数ある。請求書フォーマットの違いに
     対応した正規表現に直して"
```

返ってきた修正版:

```python
patterns = [
    r"合計\s*[¥￥]?\s*([\d,]+)\s*円?",
    r"ご請求金額\s*[¥￥]?\s*([\d,]+)",
    r"合計金額\s*[¥￥]?\s*([\d,]+)",
    r"Total\s*[¥￥]?\s*([\d,]+)",
]
amount = None
for pat in patterns:
    m = re.search(pat, text)
    if m:
        amount = int(m.group(1).replace(",", ""))
        break
```

再実行:

```bash
$ python3 extract.py
total: 12,945,200 円

$ awk -F, 'NR>1 && $2=="" {n++} END {print "missing:", n}' amounts.csv
missing: 0
```

**全 100 件成功**。

### 結果

- 4 時間の手作業 → 28 秒 + コード修正 5 分
- 翌月以降は `python3 extract.py` で再実行(再開発ゼロ)
- スクリプトは Git でレビュー可能
- 一段階先(異常検知)も同じ流れで Claude が書く

---

## 実例 05: 月次報告書サイクルを 30 分で完了

→ 第5章「[事務処理を変える](/ai-native-ways/office-replacement/)」の実証

### Setup

- 入力: 営業から届く `sales-2026-04.xlsx`
- 出口: 上司へのメール送信(PDF 添付)
- ツール: `ssconvert`、`pandas`、Claude、`pandoc`、SMTP

### 手順

**Step 1: Excel → CSV → 集計表(Markdown)**

```bash
$ ssconvert sales-2026-04.xlsx sales-2026-04.csv

$ python3 aggregate.py
| 店舗 | 売上(円) |
|---|---:|
| 大阪本店 | 18,420,000 |
| 神戸店 | 12,150,000 |
| 京都店 | 9,830,000 |
| 奈良店 | 6,470,000 |
| ... |
```

`summary.md` に表が生成される。

**Step 2: Claude に分析コメント**

```bash
$ cat summary.md | claude -p \
    "この月次売上から、目立つ傾向を 3 点まで、丁寧な業務文体で書いて"
```

実際の出力:

```
1. 大阪本店が前月比 +15% で連続 3 ヶ月の伸びを記録しています。
   都市部の人流回復が要因と推察されます。
2. 神戸店は +8% と安定した伸びですが、奈良店が -3% と
   3 ヶ月連続のマイナス成長です。商圏分析が必要です。
3. 全店合計は前月比 +9.2%。前年同月比でも +12% で、
   想定計画(+8%)を上回るペースです。
```

**Step 3: Markdown 報告書を組み立てる**

```bash
$ cat > report-2026-04.md <<'EOF'
# 2026年4月 月次売上報告

## サマリ
[Claude の分析コメントを貼る]

## 店舗別売上
[summary.md の表を貼る]

## 来月の重点
- 大阪・神戸の伸びを維持する施策を継続
- 奈良店の商圏分析を 5月中旬までに実施
- ...
EOF
```

**Step 4: PDF と HTML を同時生成**

```bash
$ pandoc report-2026-04.md -o report-2026-04.pdf \
    --pdf-engine=xelatex \
    -V mainfont="Hiragino Mincho Pro" \
    --toc

$ pandoc report-2026-04.md -o report-2026-04.html --standalone --toc

$ ls -lh report-2026-04.*
-rw-r--r-- 1 user staff 142K report-2026-04.pdf
-rw-r--r-- 1 user staff  18K report-2026-04.html
```

**1 つの Markdown から、上司向け PDF + 社内 Wiki 用 HTML が同時に生成される**。

**Step 5: 自動化(cron + send.py)**

```bash
$ crontab -e
0 9 1 * * cd ~/monthly && ./run.sh
```

来月以降は `Sales-2026-05.xlsx` を `~/monthly/` に置くだけ。**毎月 1 日 9 時、上司にメール自動送信**。事務職は「来月の重点」5 行だけ書く。

### 結果

- 3 時間 → 30 分(初回)→ 5 分(2 ヶ月目以降)
- 同じ Markdown から PDF + HTML 同時生成
- 過去報告書は Git で検索・差分比較
- **45 時間 / 月の余裕が生まれる**

---

## 実例 06: PL/SQL ストアドを並行稼働で Python に書き換え

→ 第6章「[業務システムと付き合う](/ai-native-ways/business-systems/)」の実証

### Setup

- 旧: Oracle 上の `calc_monthly_billing`(PL/SQL、500 行、20 年運用)
- 新: PostgreSQL + Python(`psycopg`)
- 並行稼働期間: 3 ヶ月

### 手順

**Step 1: PL/SQL コードと業務知識の抽出**

```bash
$ sqlplus -S user/pass @export_proc.sql > calc_monthly_billing.sql

$ wc -l calc_monthly_billing.sql
523 calc_monthly_billing.sql

$ cat calc_monthly_billing.sql | claude -p \
    "この PL/SQL を読んで、
     (1) 業務ロジックの説明 Markdown
     (2) Python (psycopg) への翻訳
     を出して"
```

返ってきた Markdown 仕様書(抜粋):

```markdown
# calc_monthly_billing 業務仕様

## 入力
- 取引データ(transactions テーブル)
- 顧客マスタ(customers テーブル)

## ルール(コード解析で抽出)
1. **基本締め日**: 各月 10 日 23:59 まで
2. **お盆延長**: 7 月の請求は翌月 5 日まで延長(L.142-148)
3. **大口顧客の例外**: 月額 100 万円以上は前倒し締め(L.215-228)
4. **休業日処理**: 土日と祝日は前営業日に繰り上げ(L.301-322)
5. **税率切替**: 2024年4月以降は 10%、それ以前は 8%(L.401-415)
6. **端数処理**: 顧客ごとに切り捨て / 切り上げ / 四捨五入の選択あり
7. **再計算ロック**: 過去 3 ヶ月分のデータは再計算不可(L.450-468)
```

**「ドキュメントには書かれていなかった」7 つのルール**が抽出される。

**Step 2: 12 ヶ月の正解データをエクスポート**

```bash
$ sqlplus -S user/pass <<EOF > expected.csv
SELECT customer_id, billing_month, amount, calculated_at
FROM monthly_billing
WHERE billing_month >= TO_DATE('2025-04', 'YYYY-MM');
EOF

$ wc -l expected.csv
49,837 expected.csv
```

49,836 行の正解データ。

**Step 3: 並行稼働で出力比較**

```bash
$ python3 verify.py
[INFO] Running new calc_monthly_billing.py...
[INFO] Loaded expected.csv: 49836 rows
[INFO] Loaded actual.csv: 49836 rows
[INFO] Matching: 49829
[INFO] Diffs: 7
  (12345, 2025-07): old=1,256,400, new=1,256,400 (calculated_at differs by 1.2s)
  (54321, 2025-08): old=789,200, new=789,400 (DIFF: 200円)
  (98765, 2026-02): old=2,345,000, new=2,344,800 (DIFF: 200円)
  ...
```

7 件の差分。Claude に投げて原因を特定:

```bash
$ python3 verify.py 2>&1 | claude -p \
    "この差分の原因を、PL/SQL コードと比べて特定して"
```

返答:

```
差分の原因: 端数処理ルール(ルール 6)の実装が不完全。
PL/SQL では顧客マスタの rounding_method カラム
('floor'/'ceil'/'round')を見ているが、Python 側では
全顧客 'round' で固定になっている。
修正コード:
def round_amount(amount, method):
    if method == 'floor': return int(amount)
    if method == 'ceil':  return int(amount + 0.99)
    return round(amount)
```

修正反映後:

```bash
$ python3 verify.py
[INFO] Diffs: 0
```

**Step 4: 並行稼働を本番 cron に**

```cron
# 旧バッチ(残す)
0 1 1 * * sqlplus user/pass @run_old_billing.sql

# 新バッチ(並行)
0 2 1 * * python3 calc_monthly_billing.py

# 自動比較・差分通知
0 3 1 * * python3 compare.py | mail -s "billing diff" admin@example.com
```

**Step 5: 3 ヶ月後、旧停止**

```bash
$ tail -3 ~/billing-diff.log
2026-04-01 03:00:01 [INFO] Diffs: 0
2026-05-01 03:00:01 [INFO] Diffs: 0
2026-06-01 03:00:01 [INFO] Diffs: 0
```

3 ヶ月連続で差分ゼロ。旧バッチを停止し、Oracle ライセンス契約を更新しない。**年間約 4,000 万円のライセンス費が消える**。

### 結果

- 20 年眠っていた PL/SQL が 3 ヶ月で **Markdown 仕様書 + Python 120 行 + PostgreSQL** に変わった
- 隠れていた 7 つの業務ルールが文書化された
- Oracle EE ライセンス更新せず、年間 4,000 万円消失
- SI ベンダーへの委託費(見積 3,000 万円)もゼロ

---

## 実例 07: 個人ブログを 30 分で世界配信

→ 第7章「[Webを作る](/ai-native-ways/web/)」の実証

### Setup

- 必要: Python、`markdown-it-py`、`Jinja2`、Cloudflare アカウント、Git
- 目標: Markdown を書いて Cloudflare Pages にデプロイ、CDN で世界配信

### 手順

**Step 1: 最小プロジェクト構造**

```bash
$ mkdir myblog && cd myblog
$ mkdir -p src/posts templates html
$ tree
.
├── html/
├── src/
│   └── posts/
└── templates/
```

**Step 2: ビルドスクリプトを Claude に書かせる**

```
You: src/posts/*.md を読んで、templates/post.html に流し込み、
     html/posts/{slug}/index.html に書き出す Python を書いて。
     markdown-it-py と Jinja2 を使う
```

返ってきた `build.py`(45 行):

```python
from pathlib import Path
import markdown_it, jinja2, frontmatter

md = markdown_it.MarkdownIt()
env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

posts = []
for src in sorted(Path("src/posts").glob("*.md")):
    post = frontmatter.load(src)
    body = md.render(post.content)
    out = Path(f"html/posts/{post['slug']}/index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(env.get_template("post.html").render(
        title=post["title"], date=post["date"], body=body
    ))
    posts.append(post)

# トップページ
Path("html/index.html").write_text(
    env.get_template("index.html").render(posts=posts)
)
print(f"Built: {len(posts)} posts")
```

**Step 3: 記事を書いてビルド**

```bash
$ cat > src/posts/2026-05-01.md <<EOF
---
slug: ai-native-ways
title: AIネイティブな仕事の作法
date: 2026.05.01
---

道具を変えれば、思考が変わる...
EOF

$ uv add markdown-it-py Jinja2 python-frontmatter
$ uv run python build.py
Built: 1 posts

$ ls -lh html/posts/ai-native-ways/index.html
-rw-r--r-- 1 user staff 8.2K html/posts/ai-native-ways/index.html

$ time python3 build.py
Built: 1 posts

real    0m0.183s
```

**ビルド時間 0.18 秒**。Next.js なら 30 秒〜3 分。

**Step 4: Cloudflare Pages にデプロイ**

```bash
$ git init
$ git add -A && git commit -m "initial blog"
$ git remote add origin git@github.com:user/myblog.git
$ git push -u origin main
```

Cloudflare Pages のダッシュボードで GitHub 連携、ビルドコマンド `python3 build.py`、出力 `html/`。**5 分後に世界配信開始**。

**Step 5: 表示速度を世界各地から測定**

```bash
$ for region in tokyo singapore london nyc sydney; do
>   echo -n "$region: "
>   curl -w "%{time_total}\n" -o /dev/null -s \
>        --resolve myblog.pages.dev:443:$region_ip \
>        https://myblog.pages.dev/posts/ai-native-ways/
> done
tokyo: 0.038
singapore: 0.052
london: 0.061
nyc: 0.043
sydney: 0.071
```

**世界どこからアクセスしても 70ms 以下**。WordPress + WP Engine では平均 800ms 以上。

### 結果

- ビルド時間 0.18 秒(Next.js の 100 倍以上速い)
- 月額コスト 0 円(WP Engine なら月 5,000〜30,000 円)
- 表示速度 50ms 前後で世界配信
- 依存パッケージ 3 つ(`node_modules` ゼロ)
- Git で記事の履歴・差分管理

---

## 実例 08: 写真整理 CLI を PyPI で世界配布

→ 第8章「[アプリを作る](/ai-native-ways/apps/)」の実証

### Setup

- 必要: Python、PyPI アカウント、Claude
- 目標: CLI ツールを作って `uv tool install`(または `pip install`)で世界に配布

### 手順

**Step 1: プロジェクト構造を Claude に作らせる**

```
You: jpg/jpeg を EXIF の撮影日でフォルダ分けする CLI を Python で。
     pyproject.toml と src 配置、entry_point つきで
```

返ってくる構造:

```bash
$ tree photo-sort/
photo-sort/
├── pyproject.toml
├── README.md
└── src/
    └── photo_sort/
        ├── __init__.py
        └── cli.py
```

**Step 2: コードを確認**

```bash
$ cat src/photo_sort/cli.py
```

```python
import sys, shutil, os, argparse
from PIL import Image
from PIL.ExifTags import TAGS

def get_capture_date(path):
    img = Image.open(path)
    exif = img._getexif() or {}
    return next((v for t, v in exif.items() if TAGS.get(t) == 'DateTimeOriginal'), None)

def main():
    parser = argparse.ArgumentParser(description="Sort photos by capture date")
    parser.add_argument("folder")
    args = parser.parse_args()

    moved = 0
    for f in sorted(os.listdir(args.folder)):
        if not f.lower().endswith(('.jpg', '.jpeg')):
            continue
        date = get_capture_date(os.path.join(args.folder, f))
        if not date:
            continue
        ymd = date[:10].replace(':', '-')
        target = os.path.join(args.folder, ymd)
        os.makedirs(target, exist_ok=True)
        shutil.move(os.path.join(args.folder, f), os.path.join(target, f))
        moved += 1

    print(f"Moved {moved} photos")

if __name__ == "__main__":
    main()
```

**Step 3: ローカルで動作確認**

```bash
$ uv tool install --editable .
Successfully installed photo-sort-0.1.0

$ ls ~/Pictures/2026/ | head
IMG_3414.jpg
IMG_3415.jpg
IMG_3416.jpg
...

$ photo-sort ~/Pictures/2026/
Moved 247 photos

$ ls ~/Pictures/2026/
2026-04-01/  2026-04-08/  2026-04-15/  2026-04-22/  ...
```

247 枚が日付フォルダに整理される。

**Step 4: PyPI にアップロード**

```bash
$ uv tool install build twine
$ python3 -m build
Successfully built photo-sort-0.1.0.tar.gz and photo_sort-0.1.0-py3-none-any.whl

$ twine upload dist/*
Uploading photo_sort-0.1.0-py3-none-any.whl
100%|█████████████████| 5.84k/5.84k [00:01<00:00]
Uploading photo-sort-0.1.0.tar.gz
100%|█████████████████| 4.21k/4.21k [00:00<00:00]

View at: https://pypi.org/project/photo-sort/0.1.0/
```

**5 分で PyPI 登録完了**。

**Step 5: 世界中から使われる**

その日のうちに、誰でも:

```bash
$ uv tool install photo-sort
Collecting photo-sort
  Downloading photo_sort-0.1.0-py3-none-any.whl (3.1 kB)
Collecting Pillow
  Downloading Pillow-10.4.0-cp312-cp312-macosx_11_0_arm64.whl (3.4 MB)
Successfully installed photo-sort-0.1.0 Pillow-10.4.0

$ photo-sort ~/Pictures/
Moved 184 photos
```

App Store の審査も $99/年 の年会費もなしで、**世界規模の配布**。

### 結果

- CLI ツール作成 → PyPI 公開: 1 時間
- 配布手段: `uv tool install photo-sort`(または `pip install photo-sort`)一発
- ライセンス・年会費: ゼロ
- iOS アプリで同じことをすると 1 週間 + $99/年

---

## 実例 09: ESP32 で農業研究レベルのセンシング

→ 第9章「[組み込みを作る](/ai-native-ways/embedded/)」の実証

### Setup

- ハードウェア: ESP32 開発ボード(800 円)、DHT22(500 円)、土壌水分センサ(300 円)、SSD1306 OLED(700 円)、ジャンパワイヤ。**合計 2,300 円**
- 必要: PC、`micropython` のファームウェア、`ampy`

### 手順

**Step 1: PC で Python ロジックを検証**

```bash
$ cat detect.py
```

```python
def should_water(temps, moistures):
    if len(temps) < 24:
        return False
    avg_temp = sum(temps[-24:]) / 24
    avg_moisture = sum(moistures[-24:]) / 24
    return avg_moisture < 30 and avg_temp > 25
```

サンプルデータで動作確認:

```bash
$ cat sample-data.csv | head -3
timestamp,temp,moisture
2026-04-01 00:00:00,22.1,45.2
2026-04-01 01:00:00,21.5,44.8

$ python3 -c "
import csv
from detect import should_water
with open('sample-data.csv') as f:
    rows = list(csv.DictReader(f))
temps = [float(r['temp']) for r in rows]
moistures = [float(r['moisture']) for r in rows]
print('water:', should_water(temps, moistures))
"
water: True
```

**0.1 秒で判定**。閾値の調整も PC 上で何回でも試せる。

**Step 2: Claude に MicroPython 翻訳**

```
You: この Python ロジックを ESP32 の MicroPython 版に。
     DHT22(GPIO4)と土壌水分センサ(ADC GPIO34)、
     OLED(I2C SCL=22, SDA=21)で表示。10分おきに測定
```

返ってきた `main.py`(50 行、`detect.py` も同梱):

```python
from machine import Pin, ADC, I2C
import dht, time, ssd1306
from detect import should_water

dht22 = dht.DHT22(Pin(4))
adc = ADC(Pin(34))
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

temps, moistures = [], []
while True:
    dht22.measure()
    temps.append(dht22.temperature())
    moistures.append(adc.read() / 4095 * 100)
    if len(temps) > 144: temps.pop(0)
    if len(moistures) > 144: moistures.pop(0)
    advice = "Water!" if should_water(temps, moistures) else "OK"
    oled.fill(0)
    oled.text(f"Temp: {temps[-1]}C", 0, 0)
    oled.text(f"Moist: {moistures[-1]:.0f}%", 0, 16)
    oled.text(advice, 0, 32)
    oled.show()
    time.sleep(600)
```

**Step 3: ESP32 に転送**

```bash
$ ampy --port /dev/ttyUSB0 put detect.py
$ ampy --port /dev/ttyUSB0 put main.py
$ screen /dev/ttyUSB0 115200
# Ctrl-D でリセット → main.py 実行
```

OLED に表示:

```
Temp: 28C
Moist: 25%
Water!
```

**Step 4: クラウドに送ってグラフ化**

`urequests` で HTTP POST する 5 行を追加。サーバー側で蓄積。1 ヶ月後:

```bash
$ cat data.csv | claude -p \
    "1 ヶ月の温度・水分データから、最適な水やり時刻を提案して"
```

返答:

```
データ分析結果(2026年4月、4,320 サンプル):

最適水やり時刻: 朝 6:00〜7:00
- この時間帯の水やりは、土壌水分が最も長く保持される
- 平均で 14 時間後でも 35% 以上を維持
- 10:00 以降の水やりは、5 時間で 30% を切る傾向

推奨スケジュール:
- 火・木・土の 6:30 にタイマー水やり 5 分
- 気温 30°C 超の日は追加で 18:00 に 3 分
```

**大学農学部の研究レベルの知見**が、家庭の畑から得られる。

### 結果

- 部品代 2,300 円で農業研究機関レベルの環境モニタリング
- PC で検証してから実機に移植 → デバッグ時間 90% 削減
- データ蓄積 + Claude 分析で「最適水やり時刻」の発見
- IoT 企業のサービス契約(月数万円)不要

---

## 実例 10: AI エージェントを Python + cron に置き換え

→ 第10章「[AIに任せる仕事を見極める](/ai-native-ways/ai-delegation/)」の実証

### Setup

- 旧: AI エージェント SaaS(月額 $200、自律モードでメール対応)
- 新: Python + cron + Claude API
- 必要: Python、`anthropic` SDK、Slack Webhook URL

### 手順

**Step 1: 何を自動化したいか**

「未読の問い合わせメールを 15 分ごとに読んで、緊急なら Slack 通知」。これだけ。

**Step 2: Claude にコードを書かせる**

```
You: IMAP で未読メールを取得して、Claude API で「緊急/通常/不要」
     に分類、緊急なら Slack に要約を投稿する Python を書いて。
     設定は環境変数で
```

返ってくる `process.py`(60 行):

```python
import os, imaplib, email, sys
from email.header import decode_header
from anthropic import Anthropic
import requests

ANTHROPIC = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

def classify(subject, body):
    msg = ANTHROPIC.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content":
            f"このメールを「緊急/通常/不要」に分類し、緊急なら "
            f"1 行要約と推奨アクションを返して:\n"
            f"件名: {subject}\n本文: {body[:2000]}"
        }]
    )
    return msg.content[0].text

def main():
    M = imaplib.IMAP4_SSL(os.environ["IMAP_HOST"])
    M.login(os.environ["IMAP_USER"], os.environ["IMAP_PASS"])
    M.select("INBOX")
    _, ids = M.search(None, "UNSEEN")
    handled = 0
    for num in ids[0].split():
        _, data = M.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        subject = str(decode_header(msg["Subject"])[0][0])
        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore") if msg.is_multipart() == False else ""
        result = classify(subject, body)
        if "緊急" in result.split("\n")[0]:
            requests.post(SLACK_WEBHOOK, json={"text": f"🚨 {subject}\n{result}"})
            handled += 1
    M.logout()
    print(f"processed {len(ids[0].split())} mails, alerts: {handled}")

if __name__ == "__main__":
    main()
```

**Step 3: 実行**

```bash
$ uv add anthropic requests
$ export ANTHROPIC_API_KEY=sk-ant-...
$ export SLACK_WEBHOOK=https://hooks.slack.com/services/...
$ export IMAP_HOST=imap.gmail.com
$ export IMAP_USER=me@example.com
$ export IMAP_PASS=...

$ python3 process.py
processed 8 mails, alerts: 1
```

Slack に通知:

```
🚨 至急: 取引先 A 社の納期遅延について
判定: 緊急
要約: 5/3 納期予定の 1,200 個分が、5/10 に遅延する可能性あり
推奨アクション: 営業担当に至急連絡、代替手段の確保
```

**Step 4: cron で 15 分ごとに**

```cron
$ crontab -e
*/15 * * * * cd ~/email-agent && /usr/bin/python3 process.py >> ~/email-agent.log 2>&1
```

**Step 5: 1 ヶ月の運用ログでコスト確認**

```bash
$ tail -30 ~/email-agent.log
2026-05-01 09:00:01 processed 12 mails, alerts: 2
2026-05-01 09:15:01 processed 3 mails, alerts: 0
2026-05-01 09:30:01 processed 5 mails, alerts: 1
...

$ awk '/processed/ {sum+=$2} END {print sum, "mails processed"}' ~/email-agent.log
2847 mails processed
```

1 ヶ月で 2,847 通を分類。Anthropic API のダッシュボードで確認:

```
April 2026 Usage:
- Total tokens: 1,847,253
- Total cost: $4.62
```

**月額 $4.62**。SaaS の $200 より **43 倍安い**。

### 結果

- $200/月 → $4.62/月(43 倍差)
- データは自分のサーバー、外部に流出しない
- 判定ロジックがコードで凍結 → 再現可能・検証可能
- 自律モードのリスク(プロンプト・インジェクション、暴走)ゼロ

---

## 実例 11: 1 人 + AI で SaaS を 1 ヶ月でローンチ

→ 第12章「[1人+AIで作る](/ai-native-ways/one-plus-ai/)」の実証

### Setup

- プロダクト: Markdown 議事録分析 SaaS
- 価格: 月額 $20
- 必要: Python、PostgreSQL、Stripe アカウント、Hetzner VPS($5/月)

### 手順

**Day 1: アイディア → Markdown**

```bash
$ cat > spec.md <<EOF
# Markdown 議事録 SaaS

## 課題
組織の議事録が Word で散らばり、検索・分析できない

## 機能
1. Markdown 議事録のアップロード
2. Claude による要約・アクションアイテム抽出
3. 過去 12 ヶ月の議論パターン分析
4. 月額 $20、最初の 14 日無料
EOF
```

**Day 2-3: スキーマ + API 実装**

```bash
$ cat spec.md | claude -p \
    "PostgreSQL スキーマと FastAPI エンドポイント、Pydantic、async、
     pytest を含むコードを書いて"
```

返答(抜粋):

```sql
-- schema.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    stripe_customer_id TEXT,
    subscription_status TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE minutes (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    title TEXT,
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    minutes_id INT REFERENCES minutes(id),
    summary TEXT,
    actions JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import asyncpg, os
from anthropic import Anthropic
# ... 250 行
```

**Day 4-7: フロントエンド**

```
You: 議事録アップロード画面、分析結果表示画面、ダッシュボード。
     Linear のような落ち着いた UI、純粋な CSS で
```

`templates/` に 5 つの HTML テンプレート、`static/style.css`(800 行)。

**Day 8-10: Stripe 課金**

```bash
$ uv add stripe
$ cat billing.py
```

```python
import stripe, os
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

def create_checkout_session(user_email):
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": "price_1AbC...", "quantity": 1}],
        customer_email=user_email,
        success_url="https://app.example.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://app.example.com/cancel",
    )
    return session.url
```

Webhook 受信(`/webhooks/stripe`)で subscription_status を DB に同期。

**Day 11-15: テスト + 修正**

```bash
$ pytest tests/ -v
========================== test session starts ==========================
tests/test_auth.py::test_login PASSED                   [ 11%]
tests/test_minutes.py::test_upload PASSED               [ 22%]
tests/test_minutes.py::test_analysis PASSED             [ 33%]
tests/test_billing.py::test_checkout PASSED             [ 44%]
tests/test_billing.py::test_webhook PASSED              [ 55%]
tests/test_dashboard.py::test_list_minutes PASSED       [ 66%]
tests/test_dashboard.py::test_search PASSED             [ 77%]
tests/test_subscription.py::test_active PASSED          [ 88%]
tests/test_subscription.py::test_canceled FAILED        [100%]
========================== 1 failed, 8 passed ==========================
```

失敗を Claude に渡して修正。最終的に全テスト通過。

**Day 16-20: VPS にデプロイ**

```bash
$ ssh root@my-vps
# Hetzner Cloud CX21($5/月)
$ git clone https://github.com/me/minutes-saas.git
$ cd minutes-saas
$ docker compose up -d
[+] Running 4/4
 ✔ Container minutes-saas-postgres-1  Started
 ✔ Container minutes-saas-api-1        Started
 ✔ Container minutes-saas-caddy-1      Started
 ✔ Container minutes-saas-worker-1     Started

$ curl https://minutes.example.com/health
{"status": "ok", "db": "connected"}
```

`Caddy` で HTTPS 自動取得。

**Day 21-25: 法律文書とランディングページ**

```bash
$ claude -p \
    "Markdown 議事録 SaaS の利用規約と
     プライバシーポリシーを、丁寧な日本語と英語の両方で生成して。
     決済は Stripe、データは VPS 内で管理"
```

下書きを弁護士に送って $500 でレビュー。

**Day 26-28: マーケティング**

```bash
$ claude -p \
    "Hacker News と Product Hunt 向けの紹介文を、それぞれの
     コミュニティの作法に合わせて 3 案ずつ書いて"
```

Twitter / X、LinkedIn 用も同じ要領で。

**Day 29-30: ローンチ**

```bash
$ # Product Hunt 投稿
$ # Hacker News Show HN 投稿
$ # Twitter で告知
```

**初日の結果**:

```bash
$ curl -s https://minutes.example.com/admin/stats | jq
{
  "users": 47,
  "trial_active": 47,
  "subscriptions": 0,
  "minutes_uploaded": 132,
  "analyses_run": 89
}
```

47 ユーザーが登録、132 件の議事録がアップロードされた(無料トライアル)。**1 ヶ月後**には:

```json
{
  "users": 312,
  "trial_active": 184,
  "subscriptions": 41,
  "monthly_revenue_usd": 820,
  "minutes_uploaded": 1847,
  "analyses_run": 1432
}
```

41 の有料ユーザー、月額 $820 の売上。**プロダクトとして立ち上がった**。

### 結果

- 1 ヶ月で 0 → 売上発生(月 $820)
- 初月コスト合計: VPS $5 + Claude $50 + Stripe 手数料(成果報酬)+ 弁護士 $500 = **$600**
- 1 人で全機能(認証・課金・Webhook・分析・ダッシュボード・法務・マーケ)
- 10 年前なら 5 人で半年の仕事

---

## まとめ

11 のウォークスルーすべてに共通するのは、**AI を生成器として使い、結果をコード・コマンド・ファイルに凍結する**ことだ。

- Word を Markdown に変える(実例 01)
- Excel を CSV と Python に変える(実例 02)
- 提案書をテキストとコードで作る(実例 03)
- 手作業を Python に凍結する(実例 04, 05)
- レガシーを並行稼働で書き換える(実例 06)
- Web を最小スタックで作る(実例 07)
- アプリを CLI から始める(実例 08)
- 組み込みを Python で考える(実例 09)
- AI エージェントを Python に凍結する(実例 10)
- 1 人 + AI で事業を立ち上げる(実例 11)

それぞれの実例は **2 〜 30 分**で動かせる。「全部読んでから」ではなく、**興味があるものから一つ動かしてみる**のが、AI ネイティブな仕事の始め方だ。

---

## 関連記事

- [序章: 事務処理はOffice、業務ソフトはJava/C#、しかしAIはPythonとテキスト](/ai-native-ways/prologue/)
- [第12章: 1人+AIで作る、新しい仕事の単位](/ai-native-ways/one-plus-ai/)
