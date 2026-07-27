# 実例 2 — CSV ⇄ JSON ⇄ YAML 相互変換 + jq / awk クエリ

第 02 章「データを持つ ── JSON/CSV/YAMLで考える」の主張の **2 番目の角度** を裏付ける。

## 章のどの主張に対応するか

> 表(行と列) → CSV / 階層(ネスト) → JSON / 設定(コメント付き) → YAML
> 一つのプロジェクトで全部使ってもいい。

> JSON / CSV を Claude に渡したときの認識率: ほぼ 100%。

(章本文より)

example-1 が「Excel → CSV → pandas 集計」だったのに対し、
このフォルダは:

- **3 形式の相互変換 + 完全往復**(データが壊れない)
- **jq での JSON クエリ**(階層データ向き)
- **awk での CSV クエリ**(表データ向き)

を実演する。

## やること

1. 顧客マスタ `data/customers.csv`(15 行)を入力に
2. `convert.py` で **CSV → JSON → CSV 往復**(完全一致を確認)
3. **CSV → YAML** にも変換(可読性の比較)
4. `jq` で JSON に対する3種類のクエリ
5. `awk` で同じ処理を CSV に対して(jq と awk の対応表)

## 構成

```
example-2/
├── README.md
├── convert.py        ── CSV ⇄ JSON / CSV → YAML
├── Makefile          ── 変換 + クエリ
├── results.md
├── data/customers.csv
└── out/
    ├── customers.json
    ├── customers.yaml
    ├── customers-roundtrip.csv  (元と完全一致)
    ├── q-pro.json               (jq: プロプランだけ)
    └── q-region-mrr.json        (jq: 地域別 MRR)
```

## 実行

```bash
pip install pyyaml
sudo apt install jq
make clean && make all
```

## なぜこれが「実例」になるのか

業務で出会うデータは、形が違うだけで本質は同じ:

- 取引先がくれた **Excel** → CSV にする
- API から落とした **JSON** → そのまま使うか CSV に
- 設定ファイル → **YAML**

これらは 3 形式とも **完全に往復できる**。データが壊れない。だから、
組織の入口で受け取った形式から、**自分の作業形式**(扱いやすい
1 つ)に変換して使い、出口で必要な形式に戻せばいい。

しかも、それぞれの形式に **そのまま使えるクエリツール** がある:

| 形式 | クエリ | 例 |
|------|-------|-----|
| JSON | `jq` | `jq '.[] \| select(.plan=="プロ")'` |
| CSV | `awk` `cut` `sort` | `awk -F, '$4=="プロ"'` |
| YAML | `yq` または `jq`(YAML→JSON 変換後) | |

これが章で言う「**用途で使い分ける、変換は変換層に押し込む**」の具体形。
