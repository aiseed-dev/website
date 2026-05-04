# 実例 1 — 1 つの Markdown から 5 つの形式

序章の主張 ── **「Markdown / JSON / Python / テキストで、Office 以上のものが
作れる」** ── をその場で証明するためのフォルダ。

## やること

1 つの `source.md`(序章の本文そのもの)から、5 種類の出力を生成する。

| 出力 | 用途 |
|------|------|
| `out/prologue.html` | Web 公開、ブラウザ閲覧 |
| `out/prologue.epub` | 電子書籍リーダー |
| `out/slides.html` | reveal.js 講演スライド |
| `out/plain.txt` | grep / AI への入力 |
| `out/prologue.pdf` | A5 印刷物、入稿可能な体裁 |

`make all` 一発で全部できる。

## 構成

```
example-1/
├── README.md         ── このファイル
├── source.md         ── ../ja.md のコピー(入力)
├── book-style.css    ── PDF 用 CSS(A5、ページ番号、CJK フォント)
├── Makefile          ── ビルド定義
├── results.md        ── 実行結果(ビルド時間、サイズ、ページ数)
└── out/              ── 生成物(コミット済み)
    ├── prologue.html
    ├── prologue.epub
    ├── slides.html
    ├── plain.txt
    ├── body.html     ── PDF の中間生成物
    └── prologue.pdf
```

## 実行

```bash
# 必要なツール
sudo apt install pandoc fonts-noto-cjk
pip install weasyprint

# 全形式を生成
make clean && make all
```

合計 **約 11.7 秒**。詳細は [`results.md`](./results.md)。

## なぜこれが「実例」になるのか

Word なら 1 ファイル = 1 形式。フォーマットを変えるなら別途作業が要る。
Markdown は **ソース 1 本から、用途ごとに展開できる**。

- 同僚に Web で読ませる → HTML
- Kindle で読む → EPUB
- 講演する → reveal.js スライド
- AI に渡す / 検索する → プレーンテキスト
- 印刷所に出す → PDF(A5、CJK フォント埋め込み、7 ページ)

しかも全部、**コマンドラインで、無料のツールで、十数秒で**。

これが序章の言う「Pythonとテキストの世界」の最小実演。
