# build_article.py

Markdown ファイルから HTML を生成するビルドツール。

## 使い方

```bash
# 単一記事をビルド
python3 tools/build_article.py articles/insights/13-cases/ja.md

# 全記事＋インデックスページをビルド
python3 tools/build_article.py --all

# 記事一覧を表示
python3 tools/build_article.py --list
```

### 別ディレクトリのサイトをビルド

ツールのある場所に縛られないので、`--site` で任意のサイトルートを指定できる
（省略時はスクリプトの親ディレクトリ、または `$AISEED_SITE`）。

サイト側に必要なレイアウト:

```
<site>/articles/   <site>/html/
<site>/tools/templates/   # 任意（バンドルテンプレートを上書きしたい時のみ）
```

```bash
python3 /path/to/website/tools/build_article.py --site /path/to/other-site --all
AISEED_SITE=/path/to/other-site python3 /path/to/website/tools/build_article.py --all
```

テンプレートは `<site>/tools/templates/` があればそちらを優先、無ければ
このリポジトリ同梱の `tools/templates/` を使う。

## 依存ライブラリ

```bash
pip install -r requirements.txt
```

- [Jinja2](https://jinja.palletsprojects.com/) — テンプレートエンジン（`{{ variable }}` 構文）
- [markdown-it-py](https://markdown-it-py.readthedocs.io/) — CommonMark 準拠の Markdown パーサー
- [Pillow](https://pillow.readthedocs.io/) — OGP画像 (1200×630) の自動生成

markdown-it-py は `table` 拡張を有効化済み。

## ファイル構成

**1記事 = 1フォルダ**。同じフォルダ内に `ja.md` / `en.md` と関連アセット
（画像・PDF）を同居させる。

```
articles/
  insights/
    01-climate-mistake/
      ja.md                  # 日本語版
      en.md                  # 英語版
    02-fossil-materials/
      ja.md
      en.md
    ...
  claude-debian/             # 「Claudeと一緒に学ぶDebian」
    00-prologue/
      ja.md
      en.md
    ...
  blog/
    015-japan-windows-disaster-risk/
      ja.md
      en.md
      015-IMG_3433.jpg       # 共有/JAアセット（両言語に配信）
      en-015-foo.pdf         # EN専用アセット（en- プレフィックス）
    ...
tools/
  build_article.py           # CLI エントリーポイント + ビルド orchestration
  build/
    config.py                # サイト設定・Jinja2 env
    markdown.py              # frontmatter + :::カスタムブロック + CommonMark
    images.py                # 画像コピー + OGP画像生成
    template_vars.py         # 各テンプレートの変数ビルダー
  templates/
    article.html             # 記事・ブログページテンプレート（Jinja2）
    index.html               # インデックスページテンプレート（Jinja2）
html/
  insights/                  # 日本語 Insights HTML 出力先
  en/insights/               # 英語 Insights HTML 出力先
  blog/                      # 日本語 Blog HTML 出力先
  en/blog/                   # 英語 Blog HTML 出力先
  claude-debian/             # 「Claudeと一緒に学ぶDebian」出力先
  en/claude-debian/          # 英語版出力先
```

## 出力先

| 記事 | 出力先 |
|------|--------|
| `articles/insights/09-healthcare-fiscal/ja.md` | `html/insights/healthcare-fiscal/index.html` |
| `articles/insights/09-healthcare-fiscal/en.md` | `html/en/insights/healthcare-fiscal/index.html` |
| `articles/blog/015-japan-windows-disaster-risk/ja.md` | `html/blog/japan-windows-disaster-risk/index.html` |
| `articles/claude-debian/00-prologue/ja.md` | `html/claude-debian/prologue/index.html` |

URL パスのスラッグはフロントマターの `slug:` で決まる（フォルダ名の `NN-` 接頭辞は剥がされる）。

---

# Markdown 記法マニュアル

## フロントマター

ファイル先頭に `---` で囲んで記述する。**全てのフィールドは1行で書く**（YAML のネスト・配列は非対応）。パーサは `tools/build/markdown.py::parse_frontmatter()` の自前実装で、`key: value` を行単位で読むだけ。値両端のダブルクォートは剥がされる。

記事タイプは配置ディレクトリで決まる:

| タイプ | 置き場所 | 出力先 | URL例 |
|---|---|---|---|
| Insights記事 (連載) | `articles/insights/NN-slug/ja.md` | `html/insights/slug/index.html` | `/insights/slug/` |
| Insights記事 (英語) | `articles/insights/NN-slug/en.md` | `html/en/insights/slug/index.html` | `/en/insights/slug/` |
| Blog記事 (時事ノート) | `articles/blog/NNN-slug/ja.md` | `html/blog/slug/index.html` | `/blog/slug/` |
| Blog記事 (英語) | `articles/blog/NNN-slug/en.md` | `html/en/blog/slug/index.html` | `/en/blog/slug/` |

### フィールド一覧

| フィールド | Insights | Blog | 必須 | 用途 |
|---|:---:|:---:|:---:|---|
| `slug` | ○ | ○ | **必須** | URLパスと出力ディレクトリ名 |
| `title` | ○ | ○ | **必須** | `<title>`, `<h1>`, OGP title |
| `subtitle` | ○ | ○ | 推奨 | 記事冒頭のサブタイトル |
| `description` | ○ | ○ | 推奨 | `<meta description>`, OGP description |
| `date` | ○ | ○ | 推奨 | 表示日付 (`2026.04.19` 形式)。sitemap の lastmod にも使用 |
| `lang` | ○ | ○ | 英語版のみ | `en` を指定すると `/en/` 配下に出力 |
| `label` | ○ | ○ | 任意 | ページヒーローのラベル (例: `Structural Analysis 09`, `Blog`) |
| `hero_image` | ○ | ○ | 任意 | ページ内アイキャッチ（ファイル名のみ）。**OGP画像の自動生成元**にもなる |
| `og_image` | ○ | ○ | 任意 | SNSサムネイル手動上書き用の絶対URL。通常は不要（`hero_image` から自動生成） |
| `number` | ○ | — | Insights必須 | 連載番号 (`"09"` のようにクォート推奨) |
| `prev_slug` / `prev_title` | ○ | — | 任意 | 前記事ナビゲーション |
| `next_slug` / `next_title` | ○ | — | 任意 | 次記事ナビゲーション |
| `category` | — | ○ | 任意 | Blogサイドラベル (既定: `ブログ` / `Blog`) |
| `cta_*` | ○ | — | 任意 | CTAブロックのカスタマイズ（下記） |

### Insights記事の例

```yaml
---
slug: healthcare-fiscal
number: "09"
title: 社会の設計ミス
subtitle: 軍需産業、IT企業、デスクワーカー、医療、年金
description: 透析医療の化石資源依存、社会保険料30%超...
date: 2025.04.04
label: Structural Analysis 09
prev_slug: enterprise-tax
prev_title: 企業ITの税を引く
next_slug: subtraction-design
next_title: 引き算の設計
---
```

### Blog記事の例

```yaml
---
slug: copilot-correct-looking-but-wrong
title: MicrosoftのCopilotの課題 ― コードの「正しそうで間違っている」問題
subtitle: AIが書いたコードをAIがレビューする閉じた系
description: GitHub Copilotが生成するコードの約40%に致命的な脆弱性……
date: 2026.04.19
label: Blog
category: 構造分析ノート
hero_image: 012-IMG_3424.jpg
---
```

`og_image` は書かなくてよい。`hero_image` から 1200×630 の `og-image.jpg` が自動生成され、SNSメタタグもそれを指す。

### 英語版の追加フィールド

```yaml
lang: en
```

これがあると `/en/insights/` または `/en/blog/` 配下に出力される。

## 画像とOGPサムネイル

### 画像のコピー規則

`build_article.py` は記事フォルダ内のすべてのアセット（画像・PDF）を出力ディレクトリにコピーする (`tools/build/images.py::copy_images()`)。

| ファイル名 | JAビルド | ENビルド | 用途 |
|---|:---:|:---:|---|
| `<name>.<ext>` | ✓ | ✓ | 共有/JA-only |
| `en-<name>.<ext>` | — | ✓ | EN専用 |

つまり EN ビルドは記事フォルダ内のすべてをコピー、JA ビルドは `en-` プレフィックスがあるものだけスキップする。**フォルダ自体が記事に紐づくため、ファイル名側に番号プレフィックスを付ける必要はない**（ただし既存記事との互換のため番号プレフィックス付きでも動く）。

### `hero_image` — ページ内の表示画像

記事ページ内に `<img>` として表示される（`article.html` の `{{ img_path }}`）。

- **書式**: ファイル名のみ (`012-IMG_3424.jpg`)
- **解決**: ビルド時に `../../images/FILE` のような相対パスに展開される
- **省略時**: `IMG_3285.jpg`（サイト既定画像）にフォールバック

### `og_image` — SNSサムネイル（OGP / Twitter Card）

X・Facebook・LINE・Slack・Discord等でURLを共有したとき、プレビューカードに表示される画像。

ビルド結果の HTML に以下が出力される（`tools/templates/article.html:22-34`）:

```html
<meta property="og:image"  content="{{ og_image }}">
<meta name="twitter:image" content="{{ og_image }}">
```

**解決ロジック** (`tools/build/images.py::resolve_og_image`)：

| 条件 | 結果 |
|---|---|
| `og_image` がフロントマターに `http://` / `https://` で書かれている | その URL をそのまま使用（手動上書き） |
| `hero_image` が指定されている | ビルド時に **1200×630 JPEGへ自動生成** し `og-image.jpg` として出力。URL は `{canonical_url}/og-image.jpg` |
| どちらもなし | `DEFAULT_OG_IMAGE` (`/images/IMG_3285.jpg`) にフォールバック |

### OGP画像の自動生成

`hero_image` を書けば OGP用画像が自動で作られる。別途 `og_image` を書く必要はない。

- **入力**: `hero_image` に指定した画像（例: `012-IMG_3424.jpg`）
- **処理**: EXIF回転を適用 → アスペクト比1200:630 に**中央クロップ** → 1200×630 にリサイズ → JPEG (quality=85, progressive)
- **出力**: 記事の出力ディレクトリ直下に `og-image.jpg`
  - 例: `html/blog/copilot-correct-looking-but-wrong/og-image.jpg`
- **URL**: `https://aiseed.dev/blog/{slug}/og-image.jpg`

iPhone縦写真(4:3) や横写真(16:9) を素材に使うとSNS側で見切れる問題が起きるが、このクロップで **X/Facebook/LINE等が等しく綺麗にレンダーできる 1.91:1** に揃う。

**手動で上書きしたい場合** は `og_image:` に絶対URLを書く（別画像を配信したい・イラストを使いたい等）。

### OGPだけ再生成

デザインだけ差し替えたい時は `--ogp` で OGP画像だけ作り直せる（HTML再生成なし）:

```bash
python3 tools/build_article.py --ogp articles/blog/012-copilot_correct_looking_but_wrong/ja.md
```

### 確認方法（デプロイ後）

- Facebook: <https://developers.facebook.com/tools/debug/>
- LINE: <https://poke.line.me/>
- 生成されたHTML: `grep 'og:image\|twitter:image' html/blog/{slug}/index.html`
- 生成画像: `python3 -c "from PIL import Image; print(Image.open('html/blog/{slug}/og-image.jpg').size)"` → `(1200, 630)`

## CTAカスタマイズ（Insights記事のみ、省略可）

省略すると日英それぞれのデフォルト値が使われる。

```yaml
cta_label: Back to Soil
cta_title: 自然とともにあれば、生きられる
cta_text: 全ての構造分析は、一つの結論に向かう。
cta_btn1_text: 自然農法とは
cta_btn1_link: /about/
cta_btn2_text: Light Farming
cta_btn2_link: /light-farming/
```

## 標準 Markdown

Python-Markdown の仕様に従う。GitHub Flavored Markdown (GFM) とは一部異なる。

### 見出し

```markdown
## 大見出し
### 中見出し
```

### 太字・強調

```markdown
**太字** → <strong>太字</strong>
*斜体* → <em>斜体</em>
```

### リンク

```markdown
[テキスト](https://example.com)
```

### リスト

```markdown
- 項目1
- 項目2
- 項目3
```

番号付き:

```markdown
1. 最初
2. 次
3. 最後
```

### 段落

空行で段落を分ける。空行がないと同じ段落になる。

```markdown
最初の段落。

次の段落。
```

### テーブル（tables 拡張）

カスタムブロック外でもテーブルが使える。

```markdown
| 見出し1 | 見出し2 |
| ------- | ------- |
| セル1   | セル2   |
```

### 属性リスト（attr_list 拡張）

要素にクラスやIDを追加できる。

```markdown
段落テキスト
{: .my-class #my-id }
```

## 注意: Python-Markdown と GFM の違い

| 記法 | GFM | Python-Markdown |
|------|-----|-----------------|
| `~~取り消し線~~` | 対応 | **非対応** |
| 自動リンク `https://...` | 対応 | **非対応**（`[text](url)` で書く） |
| タスクリスト `- [ ]` | 対応 | **非対応** |
| コードブロック ` ``` ` | 対応 | 対応（ただしシンタックスハイライトなし） |

## カスタムブロック（独自拡張）

`:::type` で開始し `:::` で終了する。**Python-Markdown の機能ではなく、build_article.py 独自の前処理**。

### :::chain — 構造チェーン

因果関係や構造的な連鎖を表示する。`→` が矢印アイコンに変換される。

```markdown
:::chain
**タイトル：**
原因 → 結果1
→ 結果2
→ **最終結論**
:::
```

出力: 左ボーダー付きボックス。`→` は緑色の矢印になる。
内部では `**太字**` と改行のみ対応。標準 Markdown は処理されない。

### :::highlight — ハイライトボックス

重要な数字や事実を強調する。内部は標準 Markdown として処理される。

```markdown
:::highlight
**タイトル：**
項目1：数値
項目2：数値
**結論文**
:::
```

出力: 薄緑の背景ボックス。内部は `markdown.markdown()` で処理されるので、太字・リスト・リンク等が使える。

### :::quote — 引用ブロック

印象的な一文やまとめに使う。

```markdown
:::quote
自然は、壊されても回復する力を持っている。
人間も同じだ。
:::
```

出力: 左ボーダー付き、明朝体で表示。改行は `<br>` に変換される。
**太字等の Markdown は処理されない**（プレーンテキストのみ）。

### :::compare — 比較テーブル

パイプ記法のテーブルを比較用スタイルで表示する。

```markdown
:::compare
| 項目 | 従来 | 転換後 |
| --- | --- | --- |
| 土壌 | 化学肥料 | 微生物 |
| 水 | 地下水採掘 | 雨水循環 |
:::
```

出力: スタイル付きテーブル。1行目がヘッダー、`---` 行はスキップされる。

## カスタムブロック内の記法まとめ

| ブロック | `**太字**` | `→` 矢印 | Markdown 処理 | 改行 |
|----------|-----------|----------|--------------|------|
| :::chain | 対応 | 対応（緑矢印） | なし | `<br>` |
| :::highlight | 対応 | なし | **あり**（完全） | Markdown 準拠 |
| :::quote | なし | なし | なし | `<br>` |
| :::compare | なし | なし | なし | テーブル行 |

## 新しい記事を追加する手順

### Insights記事 (articles/insights/)

1. `articles/insights/NN-slug/` フォルダを作成し、`ja.md` と `en.md` を置く

```bash
mkdir articles/insights/16-new-topic
$EDITOR articles/insights/16-new-topic/ja.md
$EDITOR articles/insights/16-new-topic/en.md
```

2. フロントマターを書く（slug, number, title, subtitle, description, date, label, prev_slug, prev_title, next_slug, next_title）

3. 前の章の `next_slug` / `next_title` を更新する

4. ビルド

```bash
python3 tools/build_article.py --all
```

### Blog記事 (articles/blog/)

1. `articles/blog/NNN-slug/` フォルダを作成（番号はゼロ埋め3桁、例: `017-...`）

```bash
mkdir articles/blog/017-new-post
$EDITOR articles/blog/017-new-post/ja.md
$EDITOR articles/blog/017-new-post/en.md
```

2. フロントマターを書く（slug, title, subtitle, description, date, label, category, hero_image）。前後ナビは不要。`hero_image` を書けばOGP画像も自動生成されるので、通常 `og_image` は不要。

3. 関連アセットを同じフォルダに置く

```bash
articles/blog/017-new-post/thumb.jpg       # hero_image に指定 → OGP画像の元素材
articles/blog/017-new-post/en-thumb.jpg    # 英語版でのみ差し替えたい場合
articles/blog/017-new-post/factcheck.pdf   # 共有 PDF
```

4. ビルド（`--all` でインデックス・sitemap・トップページの最新記事枠も一括更新）

```bash
python3 tools/build_article.py --all
```

5. 生成確認

```bash
grep -E 'og:image|twitter:image' html/blog/{slug}/index.html
ls html/blog/{slug}/                    # アセット一式 + og-image.jpg が揃っているか
python3 -c "from PIL import Image; print(Image.open('html/blog/{slug}/og-image.jpg').size)"
# → (1200, 630) になっていればOK
```

6. OGP画像だけ作り直したい場合（HTMLは再生成しない）

```bash
python3 tools/build_article.py --ogp articles/blog/017-new-post/ja.md
```
