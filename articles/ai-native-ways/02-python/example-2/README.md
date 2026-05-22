# 実例 2 — 100 枚の写真にリサイズ・サムネイル・透かしを一括

第 04 章「処理を書く ── AIにPythonで書いてもらう」の **2 番目の角度**:
**繰り返しの画像処理を Python に渡す**。

## 章のどの主張に対応するか

> 100 個の `.xlsx` から特定列を抽出する月次作業: Excel VBA で半日。
> `pandas` で `glob` を使って一気に処理すれば 30 秒。

(章本文「実例: 数字で見る」より)

example-1 が「PDF から金額抽出」、これは **画像の一括加工** を実演する。
Photoshop でアクション組んでも 1 枚 5 秒以上。**Python なら並列で 24 ms / 枚**。

## やること

100 枚の JPEG (1920×1280, 計 11.3 MB) に対して:

1. **リサイズ**: 長辺 1200px に縮小(Web 公開用)
2. **サムネイル**: 200×200 中央クロップ(一覧画面用)
3. **透かし**: 右下に半透明の `© aiseed.dev 2026`(配布用)

これを **ProcessPoolExecutor で並列実行**(全 CPU コアを使う)。

## 構成

```
example-2/
├── README.md
├── generate_samples.py    ── 100 枚のサンプル JPEG を生成
├── process.py             ── リサイズ + サムネイル + 透かし
├── Makefile
├── results.md
├── src/                   ── 入力 (100 枚, 11.3 MB) ── git 除外
└── out/
    ├── resized/           ── リサイズ後(100 枚, 2.9 MB)── git 除外
    ├── thumbs/            ── サムネイル(100 枚, 0.3 MB)── git 除外
    ├── watermarked/       ── 透かし入り(100 枚, 3.3 MB)── git 除外
    └── sample/            ── 各種類 2 枚ずつコミット(計 6 枚)
```

## 実行

```bash
pip install Pillow
make clean && make all
```

100 枚の処理が **約 2.4 秒** で完了する。

## なぜこれが「実例」になるのか

商品写真を 100 枚撮影 → Web 公開用に整える、というのは小売・農業・
不動産・士業の Web サイト運営でよくある作業。

**手作業**(Photoshop / プレビュー):

- 1 枚ずつ開く: 3 秒
- リサイズ: 5 秒
- 別名保存: 3 秒
- × 3 種類(リサイズ/サムネイル/透かし)
- × 100 枚 = **9,000 秒 = 2.5 時間**

**Python**:

```python
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageOps

def process_one(path):
    img = Image.open(path)
    img.thumbnail((1200, 1200))
    img.save("resized/" + path.name)
    # ... thumbnail / watermark
```

- **2.4 秒**で完了
- 来月新しい 100 枚が来ても、`python3 process.py` だけで同じ結果
- 仕様が変わったら、コードの 1 行を書き換えれば 100 枚に反映

これが章で言う「**繰り返しの仕事を、一回限りの仕事にする**」の具体形。

## 透かしのカスタマイズ

文字、フォント、位置、不透明度はすべてコード内の定数:

```python
WATERMARK = "© aiseed.dev 2026"
font = ImageFont.truetype("DejaVuSans.ttf", 24)
fill = (255, 255, 255, 220)  # 半透明白
```

「Claude にこの透かしを赤色で右上に変えて」と頼めば、
コードがすぐ書き換わる。**画像処理の中身が、自分が読める言葉になる**。
