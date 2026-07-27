# 計測結果 — 序章 example-1

実行環境: Linux 6.18 / pandoc 3.x / WeasyPrint 68.1 / Python 3.x / Noto Serif CJK JP

`make clean && make all` の出力を整理。

## ビルド時間

| 形式 | コマンド | real time |
|------|----------|-----------|
| HTML | `pandoc source.md -o prologue.html --standalone --css=book-style.css` | **0.056s** |
| EPUB | `pandoc source.md -o prologue.epub` | **0.057s** |
| reveal.js スライド | `pandoc source.md -o slides.html -t revealjs --slide-level=2` | **0.068s** |
| プレーンテキスト | `pandoc source.md -o plain.txt -t plain` | **0.047s** |
| PDF (A5/CJK) | `weasyprint(body.html) → prologue.pdf` | **11.502s** |
| **5 形式合計** | | **約 11.7 秒** |

PDF が支配的で、それ以外の 4 形式は合計 0.23 秒。

## 出力サイズ

| ファイル | バイト | 備考 |
|----------|-------|------|
| `source.md` | 7,404 | 入力(frontmatter 含む) |
| `out/prologue.html` | 10,568 | TOC 付き、`book-style.css` リンク |
| `out/prologue.epub` | 9,207 | EPUB3、9 ファイル構造 |
| `out/slides.html` | 15,150 | reveal.js、13 枚スライド |
| `out/plain.txt` | 6,505 | テキストのみ、grep 可能 |
| `out/prologue.pdf` | 494,258 | A5 / 7 ページ / フォント埋め込み |

## PDF の中身

```
Title:    序章
Producer: WeasyPrint 68.1
Pages:    7
```

`book-style.css` で次を指定:

- A5 ページ、フッターにページ番号
- Noto Serif CJK JP、本文 10pt、行間 1.85
- `h1` 二重下線、`h2` 朱色サイドルール (`#c8442a`)
- `**強調**` は黄色マーカー風グラデーション
- `>` 引用は朱色サイドルール + 斜体
- コードブロックは黒地に白文字

7 ページに収まる小冊子サイズ。フォント埋め込み済みで、印刷所に入稿できる体裁。

## reveal.js スライドの構造

`--slide-level=2` で `## 見出し` ごとにスライド分割。

```
$ grep -c '<section' out/slides.html
13
```

序章本文の `##` セクション数と一致。1 つの Markdown が、講演用スライドに変身している。

## トークン経済(参考)

文字数で粗い概算:

| 形式 | 文字数 | 比 |
|------|-------|-----|
| `source.md` | 約 7,400 | 1.00 |
| `out/plain.txt` | 約 6,500 | 0.88 |
| `out/prologue.html` | 約 10,600 | 1.43 |

HTML は Markdown より約 43% 多い。AI に長文を渡すなら Markdown が経済的。

## 再現手順

```bash
# 必要なツール(Debian/Ubuntu)
sudo apt install pandoc fonts-noto-cjk
pip install weasyprint

# このフォルダで
make clean
make all
```

すべて 12 秒前後で完了する。Office 起動が要らない。GUI が要らない。
