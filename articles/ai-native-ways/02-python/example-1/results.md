# 計測結果 — 第 04 章 example-1

実行環境: Linux 6.18 / pypdf 6.10 / WeasyPrint 68.1 / Python 3.x

## 抽出時間(主目的)

```
=== 100 個の請求書 PDF から金額抽出 ===
  処理時間: 1.025 秒  (100 ファイル)
  抽出成功: 100 / 100 件
  合計金額: 112,714,129 円
```

| 項目 | 数値 |
|------|------|
| 処理対象 | 100 PDF, 各 A4 1 枚 |
| PDF 合計サイズ | 約 24 MB |
| 処理時間(pypdf による全文抽出 + 正規表現) | **1.025 秒** |
| 抽出成功率 | **100/100 (100%)** |
| 抽出した合計金額 | 112,714,129 円 |
| 生成時の正解金額 | 112,714,129 円(完全一致) |

章本文の主張「Python で 3 秒」よりも速かった(**1 秒**)。
手作業 4 時間 = 14,400 秒との比は **約 14,000 倍**。

## 顧客別ランキング(`out/summary.json`)

```
清水運送              10,112,216 円
吉田出版               7,710,720 円
木村電機               7,410,206 円
森精密                7,213,563 円
加藤建設               7,078,098 円
高橋食品               7,072,101 円
斎藤運輸               6,917,039 円
小林技研               6,838,507 円
田中株式会社           6,583,454 円
山田農園               5,829,126 円
```

抽出結果が CSV と JSON で残るので、**翌月そのまま再利用できる**。
来月も `python extract_amounts.py` で 1 秒。来年も同じ。

## 抽出後のデータ(`out/extracted.csv` 抜粋)

```csv
file,invoice_no,customer,total
INV-2026-0001.pdf,INV-2026-0001,鈴木商店,1054720
INV-2026-0002.pdf,INV-2026-0002,森精密,627000
INV-2026-0003.pdf,INV-2026-0003,清水運送,4297540
INV-2026-0004.pdf,INV-2026-0004,池田化学,1031206
...
```

CSV になれば、後段の処理は何でもできる。

```bash
# 顧客別合計を 1 行で
awk -F, 'NR>1 {a[$3]+=$4} END {for (c in a) print c, a[c]}' out/extracted.csv | sort -k2 -n -r

# 100 万円以上の請求だけ
awk -F, 'NR>1 && $4 > 1000000' out/extracted.csv | wc -l
```

## エラーが出たら

extract_amounts.py を Claude が初回で完璧に書く保証はない。たとえば:

```
TypeError: extract_text() returned None for page 3
```

このエラーをそのまま Claude に貼ると、`p.extract_text() or ""` で
None を空文字に置換するコードが返る。**それで進む**。

章本文の言う「**エラー文をそのまま Claude に貼る。Claude が直す。これで進む**」
の具体形。

## 再現手順

```bash
pip install weasyprint pypdf
sudo apt install fonts-noto-cjk

make clean && make all
```

PDF 100 件の生成に 数秒、抽出に 1 秒。
