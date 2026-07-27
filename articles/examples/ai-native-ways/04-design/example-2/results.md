# 計測結果 — 第 03 章 example-2

実行環境: Linux 6.18 / Marp CLI 4.x / Chrome (puppeteer 同梱)

## ビルド時間

| 出力 | コマンド | 実測 |
|------|----------|------|
| HTML(7 枚) | `marp deck.md -o deck.html` | **0.76 秒** |
| PDF(7 ページ A4 横) | `marp deck.md -o deck.pdf --pdf` | **32 秒** |
| PNG(7 枚 / 1.5x) | `marp deck.md --images png --image-scale 1.5` | **2.8 秒** |

PDF が遅いのは Chromium 起動コスト。HTML と PNG は瞬時。

## サイズ

| ファイル | サイズ |
|----------|-------|
| `deck.md`(入力) | 約 1.1 KB / 60 行 |
| `deck.html` | 約 90 KB(reveal.js + コンテンツ) |
| `deck.pdf` | 約 180 KB / 7 ページ |
| `out/png/*.png` | 7 ファイル / 合計約 800 KB |

## PowerPoint との比較(章本文の数字)

| 項目 | PowerPoint | Marp |
|------|-----------|------|
| 30 分のプレゼンを作る時間 | 4 時間 | **30 分**(書く時間が大半) |
| ビルド時間 | (ない、保存だけ) | 0.8〜32 秒 |
| Git 差分 | "binary changed" | **1 行追加が 1 行追加** |
| 編集ツール | PowerPoint(縛り) | **任意のエディタ** |
| 配布形式 | .pptx, .pdf, 画像 | **HTML / PDF / PNG / PPTX** |
| 10 年後 | フォントずれ・互換性 | **ソースは生き続ける** |

## 同じ Markdown から複数フォーマット

```bash
marp deck.md -o deck.html              # ブラウザ用
marp deck.md -o deck.pdf --pdf         # 配布用
marp deck.md --images png              # スクリーンショット
marp deck.md -o deck.pptx --pptx       # PowerPoint 化(必要なら)
```

**1 つの Markdown** から **4 形式**。これが Office との根本的な違い。

## 「PowerPoint じゃないと困る」場合

組織が PowerPoint を要求するなら、出口で `--pptx` で変換:

```bash
marp deck.md -o deck.pptx --pptx
```

**書くのは Markdown、配布は要求された形式**。これが章 05「Office から
離れる現実的な道筋」と一致する。

## 再現手順

```bash
npm install -g @marp-team/marp-cli
# (PDF が必要なら) Chrome / Chromium を入れる
make clean && make all
```

PDF を作らないなら HTML だけでもプレゼンできる(キーボードでスライド送り)。
