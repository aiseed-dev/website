# 実例 1 — 100 個の請求書 PDF から金額を抽出する

第 04 章「処理を書く ── AIにPythonで書いてもらう」の主張を裏付ける。

## 章のどの主張に対応するか

> 100 個の請求書 PDF から金額を抽出する月次作業: 手作業で **4 時間**。
> Claude が書いた Python で **3 秒**。翌月も同じスクリプトで 3 秒。**4,800 倍**の差。

(章本文「実例: 数字で見る」より)

実測 **1.0 秒**。100 件すべて抽出成功。詳細は [`results.md`](./results.md)。

## やること

1. **入力を作る**: WeasyPrint で 100 件の請求書 PDF(各 A4 1 枚)を生成
   - 宛名、明細表、小計・消費税・合計、振込先、フッターまで
2. **抽出する**: pypdf で各 PDF からテキストを取り出し、正規表現で
   請求番号・宛名・合計金額を取る
3. **集計する**: 全 100 件の合計、顧客別ランキング上位 10 社
4. **検算する**: 生成時の正解と、抽出結果の合計が一致するか確認

全部 `make all` で動く。

## 構成

```
example-1/
├── README.md
├── generate_invoices.py   ── 100 件の PDF を WeasyPrint で生成
├── extract_amounts.py     ── pypdf で金額を抽出 → CSV / JSON
├── Makefile
├── results.md
├── pdf/                   ── 入力 (100 ファイル, 約 24 MB)
└── out/
    ├── extracted.csv      ── 抽出結果(全 100 件、列: file, invoice_no, customer, total)
    ├── summary.json       ── 集計結果(合計、顧客別ランキング)
    └── run.log            ── 実行ログ
```

## 実行

```bash
pip install weasyprint pypdf
make clean && make all
```

## なぜこれが「実例」になるのか

請求書 PDF の金額抽出は、**典型的に手作業で残っている事務処理**だ。

- PDF を 1 枚ずつ開く
- 合計金額を目で読む
- Excel に書き写す
- 100 件繰り返す

`extract_amounts.py` の核心は **30 行**:

```python
INVOICE_NO_RE = re.compile(r"INV-2026-(\d{4})")
CUSTOMER_RE   = re.compile(r"請求先[:：]\s*(.+?)\s*御中")
TOTAL_RE      = re.compile(r"合計金額[:：]?\s*([\d,]+)\s*円")

def parse_pdf(path):
    text = "\n".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)
    return {
        "invoice_no": INVOICE_NO_RE.search(text).group(0),
        "customer":   CUSTOMER_RE.search(text).group(1),
        "total":      int(TOTAL_RE.search(text).group(1).replace(",", "")),
    }
```

これを Claude に「100 個の請求書 PDF から合計金額を抽出して、顧客別に集計して」
と頼めば書いてくれる。**人間は意図を伝えるだけ**。実装は AI に渡る。

そして翌月、新しい 100 件が届く。同じスクリプトを `python extract_amounts.py`
で実行 ── **また 1 秒で終わる**。手作業なら毎月 4 時間ずつ消える。

これが章で言う「**繰り返しの仕事が、一回限りの仕事になる**」の具体形。
