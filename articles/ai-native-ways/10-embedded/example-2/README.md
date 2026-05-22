# 実例 2 — センサーデータ 1 週間 → SQLite → グラフ + Markdown レポート

第 09 章「組み込みを作る ── Pythonで考え、Claudeに翻訳させる」の **2 番目の角度**:
**実機の前段(データ可視化と異常検知)を Python で完成させる**。

## 章のどの主張に対応するか

> センサデータの可視化: 自前で Web ダッシュボードを作ると 1 週間。
> Python の `matplotlib` で `plot()` 1 行 + Claude に「これを HTML レポートにして」と
> 頼むと **30 分**で実用レベル。

(章本文「実例: 数字で見る」より)

example-1 が「温度制御ロジックの C 翻訳」、これは **データ収集 → 可視化 →
判定 → レポート** までの周辺パイプラインを実演する。

## やること

1. **`collect.py`**: 1 週間ぶん(7×24×12 = 2,016 件 × 3 センサ = **6,048 件**)を
   SQLite に投入(実機がまだ無くても、データの形を決めて先にコードを書く)
2. **`analyze.py`**: SQL で集計 + matplotlib で 3 段グラフ + 自動観察コメント
3. **出力**:
   - `out/sensor.db` ── 生データ
   - `out/sensor.png` ── 温度・湿度・土壌水分の推移グラフ(日本語タイトル)
   - `out/report.md` ── 統計表 + 観察コメントの Markdown

## 構成

```
example-2/
├── README.md
├── collect.py    ── 模擬センサーから SQLite へ 6,048 件
├── analyze.py    ── SQL 集計 + matplotlib グラフ + Markdown
├── Makefile
├── results.md
└── out/
    ├── sensor.db        ── SQLite(約 220 KB)
    ├── sensor.png       ── 3 段グラフ(温度/湿度/土壌)
    └── report.md        ── 自動観察コメント付き
```

## 実行

```bash
pip install matplotlib
sudo apt install fonts-noto-cjk
make clean && make all
```

数秒で 6,048 件投入 + グラフ + レポートが完成。

## なぜこれが「実例」になるのか

組み込み開発で詰まりやすい順:

1. ハードを買う(数日〜数週間、調達待ち)
2. 配線・はんだ付け(物理作業)
3. ファーム書き込み(実機ループの遅さ ── 章 example-1 の主題)
4. **データを集める**(動き始めたが、見方がわからない)
5. **可視化**(ここで詰まる)

このフォルダが **(4) と (5) を実機抜きで完成させる**:

- スキーマ(`measurements (sensor, value, unit, ts)`)を Python で先に固定
- 集計クエリ(min / avg / max / 1 時間平均)を先に書ける
- グラフのレイアウトも先に決まる
- 実機を繋いだ瞬間、`INSERT` を 1 行送るだけ

これは章 09 の主軸 ── **「Python で全部完成 → 実機側は最後の一行だけ」** の
**周辺パイプライン版**。

## 自動観察コメント

`analyze.py` の最後にあるルール:

```python
if t["max"] - t["min"] > 8:
    md.append(f"- 温度の日内変動が **{t['max']-t['min']:.1f}℃** ── 大きい。")
if sm["max"] - sm["min"] > 5:
    md.append(f"- 土壌水分が低下 ── 灌水が必要。")
```

数値しきい値で「気づき」を Markdown に出す。これは **エージェントを呼ばずに**
判断ができる例 ── 章 10「コードに凍結する」と一致する。
基準が変わったら if 文を書き換えるだけ。
