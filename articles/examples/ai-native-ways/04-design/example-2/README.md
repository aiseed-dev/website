# 実例 2 — Markdown から Marp で 7 枚のスライド

第 03 章「デザインをする ── Mermaid と Claude デザインで作る」の **2 番目の角度**:
**スライドも Markdown で**。

## 章のどの主張に対応するか

> PowerPoint で 30 ページのスライド作成: 文章とレイアウトが混在で **4 時間**。
> 同じ内容を Marp で書くと、Markdown 30 行、ビルド 1 秒、修正は Markdown を
> 直すだけで合計 **30 分**。**8 倍の差**。

(章本文「実例: 数字で見る」より)

example-1 が「Mermaid 5 種を SVG/PNG に焼く」だったのに対し、
このフォルダは **Marp** によるスライド作成を実演する。

## やること

1. **入力**: `deck.md`(Markdown 1 ファイル、約 60 行)
2. **HTML スライド**: `marp deck.md -o deck.html`(0.8 秒、ブラウザで開ける)
3. **PDF スライド**: `marp deck.md -o deck.pdf --pdf`(印刷・配布用、7 ページ)
4. **PNG スライド**: `marp deck.md --images png`(各スライドを画像化)

すべて `make all` 一発。

## 構成

```
example-2/
├── README.md
├── deck.md            ── スライド本体(60 行)
├── .marprc.yml        ── Marp 設定(Chromium 指定)
├── Makefile
├── results.md
└── out/
    ├── deck.html      ── ブラウザで開けるスライド(キーで送る)
    ├── deck.pdf       ── 7 ページの A4 横 PDF
    └── png/deck.NNN.png  ── 各スライドの画像(7 枚)
```

## 実行

```bash
npm install -g @marp-team/marp-cli
make clean && make all
```

## なぜこれが「実例」になるのか

PowerPoint で 30 分のプレゼンを作ると:

1. テンプレートを選ぶ
2. テキストボックスを配置
3. フォントとサイズを揃える
4. アニメーションを設定
5. 矢印・図形を描く
6. ノート編集モードで台本を書く

合計 **3〜4 時間**。

Marp なら:

1. Markdown を **書く** (60 行)
2. `marp deck.md -o deck.pdf` で焼く (32 秒)

合計 **約 30 分**(書く時間が大半)。Markdown はそのまま:

- GitHub に push して履歴管理
- 同僚に渡せばそのまま読める(レンダリング不要)
- Claude に「これをもっと簡潔に」と頼める
- 別のテーマや色味で再ビルド可能

これが章で言う「**Markdown が本体、装飾は Marp / Claude デザインで**」の具体形。

PowerPoint の代替が要るのではない。**スライドが Markdown でできるなら、
他の文書も同じ流れで作れる**。提案書、報告書、月次資料 ── 全部 Markdown。
