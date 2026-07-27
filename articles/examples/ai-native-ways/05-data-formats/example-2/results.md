# 計測結果 — 第 02 章 example-2

実行環境: Linux 6.18 / Python 3.x / jq 1.7

## 形式変換の速度とサイズ

```
=== 形式変換 ===
  CSV → list[dict] :    0.2 ms
  → JSON           :    0.1 ms  ( 1942 B)
  → YAML           :    1.5 ms  ( 1320 B)
  JSON → CSV 往復   :    0.1 ms

  CSV ⇄ JSON ⇄ CSV 完全往復: ✓ 一致
```

| 形式 | サイズ(15 顧客) | 1 顧客あたり |
|------|----------------|------------|
| CSV  | 約 700 B  | 47 B |
| JSON | 約 1,940 B | 130 B |
| YAML | 約 1,320 B | 88 B |

CSV が最も小さい(キー名を 1 回しか書かないため)。JSON はキーが
毎行繰り返されるので冗長。YAML はその中間。

**業務でのデータの大半は表(行と列)** なので、保存は CSV が経済的。
階層が必要なら JSON。設定なら YAML。

## jq クエリ

### 1. プロプランだけ抽出

```bash
jq '.[] | select(.plan == "プロ") | {name, region, monthly_yen}' out/customers.json
```

```json
{ "name": "鈴木商店", "region": "大阪", "monthly_yen": 4980 }
{ "name": "田中株式会社", "region": "東京", "monthly_yen": 4980 }
{ "name": "小林技研", "region": "大阪", "monthly_yen": 4980 }
{ "name": "山本印刷", "region": "徳島", "monthly_yen": 4980 }
{ "name": "木村電機", "region": "北海道", "monthly_yen": 4980 }
```

### 2. 地域別の MRR 合計

```bash
jq 'group_by(.region) | map({region:.[0].region, customers:length, mrr:(map(.monthly_yen)|add)})
    | sort_by(-.mrr)' out/customers.json
```

```
大阪    : 3 顧客 / MRR 11,940 円
東京    : 4 顧客 / MRR  8,920 円
北海道  : 3 顧客 / MRR  7,940 円
徳島    : 3 顧客 / MRR  7,940 円
沖縄    : 2 顧客 / MRR  2,960 円
```

### 3. 全顧客の MRR 合計

```bash
jq '[.[] | .monthly_yen] | add' out/customers.json
# → 39700
```

## awk で CSV に対して同じこと

```bash
awk -F, 'NR>1 {a[$3]+=$5; n[$3]++} END {for (r in a) printf "%s : %d / %d\n", r, n[r], a[r]}' \
    data/customers.csv | sort
```

```
北海道 : 3 顧客 / MRR 7940 円
大阪   : 3 顧客 / MRR 11940 円
徳島   : 3 顧客 / MRR 7940 円
東京   : 4 顧客 / MRR 8920 円
沖縄   : 2 顧客 / MRR 2960 円
```

jq と awk で結果は **完全一致**。形式は違うが、データは同じ。

## YAML 抜粋

```yaml
- customer_id: C001
  name: 山田農園
  region: 徳島
  plan: スタンダード
  monthly_yen: 1980
  started: '2025-08-01'
- customer_id: C002
  name: 鈴木商店
  ...
```

設定ファイルや短い人手編集データには YAML が読みやすい。

## 「Excel と何が違うのか」

Excel ファイルでも同じ集計はできる(ピボットテーブル)。違いは:

- Excel: マウス操作、操作の記録は残らない、来月の自分は手順を忘れる
- jq / awk: **コマンドが記録**、`Makefile` に書けば来月も同じ結果

これが章で言う「**処理の再現性**」と「**形式と道具の対応**」の具体形。

## 再現手順

```bash
pip install pyyaml
sudo apt install jq
make clean && make all
```
