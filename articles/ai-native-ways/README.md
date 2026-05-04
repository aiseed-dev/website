# AIネイティブな仕事の作法

aiseed.dev の連載エッセイシリーズ。Office・Java・C# から離れ、Markdown・JSON・
Python・テキストで AI を同僚として使うための実用的な作法。

## ファイル構成

```
articles/ai-native-ways/
├── README.md                ── このファイル
├── template.html            ── 日本語版テンプレート(Jinja2)
├── template.en.html         ── 英語版テンプレート(Jinja2)
└── NN-slug/                 ── 1章 = 1フォルダ
    ├── ja.md                ── 日本語版本文 + frontmatter
    ├── en.md                ── 英語版本文 + frontmatter
    └── example-N/           ── 章ごとの実例(任意・複数可)
        ├── README.md
        ├── source.md / *.py / その他入力
        ├── Makefile         ── 再現用ビルド定義
        ├── results.md       ── 実測値(時間・サイズ・ページ数)
        └── out/             ── 生成物(コミットする)
```

実体例:

```
articles/ai-native-ways/
├── README.md
├── template.html / template.en.html
└── 00-prologue/
    ├── ja.md
    ├── en.md
    └── example-1/           ── 1 つの Markdown から 5 形式
        ├── README.md
        ├── source.md
        ├── book-style.css
        ├── Makefile
        ├── results.md
        └── out/{prologue.html,prologue.epub,slides.html,plain.txt,prologue.pdf}
```

ビルドパイプラインは `NN-slug/` 配下のうち**先頭が数字でないフォルダ**(つまり
`example-N/`)を無視する(`tools/build_article.py::_iter_article_files` の
`if not sub.name[:1].isdigit(): continue` フィルタ)。実例フォルダはサイトの
ページとしては出力されない。リポジトリ内の証拠資料として残る。

## 設計方針

**独立テンプレート**

このシリーズは aiseed.dev の他のシリーズ(Insights、Claude × Debian、Blog)
とは別の独自タイポグラフィを使う:

- 本文: システム明朝(ヒラギノ・游明朝・Noto Serif CJK)/ Crimson Pro
- 見出し: Shippori Mincho 700/800 / Crimson Pro 700/800
- 等幅: JetBrains Mono(両言語共通)
- アクセント色: `#c8442a`(朱色)
- 紙の質感を出すグレインテクスチャ

このため共有テンプレート `tools/templates/article.html` ではなく、ここにある
`template.html` / `template.en.html` を `build_aiways_chapter()` が直接読み込む。

**フロントマターは他シリーズと共通スキーマ**

`articles/insights/`, `articles/claude-debian/`, `articles/blog/` と同じ
スキーマを使う(slug, number, title, subtitle, description, date, label,
prev_slug, prev_title, next_slug, next_title)。シリーズ固有の表示ラベル
(序章/第N章、年など)はビルド側で導出する。

## フロントマター仕様

```yaml
---
slug: prologue                  # URL: /ai-native-ways/{slug}/
number: "00"                    # 章番号(ゼロ埋め文字列)
lang: en                        # EN 版のみ必須
title: 記事タイトル
subtitle: 副題(hero-subtitle に表示)
description: SEO/OG 用の短い説明
date: 2026.05.01                # ドット区切り(他シリーズと統一)
label: AI Native 00             # 識別ラベル
title_html: ...<br>...          # 任意: hero-title を HTML 断片で上書き
prev_slug:
prev_title:
next_slug:
next_title:
---
```

`title_html` は単一行で、`<br>` `<span class="accent">` などを含めて書く。
未指定なら `title` がプレーンテキストで表示される。

例(00-prologue):

```yaml
title_html: 事務処理は<span class="accent">Office</span>。<br>業務ソフトは<span class="accent">Java/C#</span>。<br>しかしAIは、<span class="accent">Pythonとテキスト</span>。
```

関連リンクは frontmatter ではなく、Markdown 本文末に `## 関連記事` として
書く(他シリーズと同じ流儀)。

## テンプレートのプレースホルダ一覧

ビルドスクリプト(`tools/build_article.py::build_aiways_chapter`)が以下の変数を
注入する:

| 変数                  | 由来                                          |
|-----------------------|-----------------------------------------------|
| `{{ title }}`         | frontmatter の `title`                        |
| `{{ title_html }}`    | frontmatter の `title_html`(任意)             |
| `{{ subtitle }}`      | frontmatter の `subtitle`                     |
| `{{ description }}`   | frontmatter の `description`                  |
| `{{ date }}`          | frontmatter の `date`(例: `2026.05.01`)      |
| `{{ year }}`          | `date` から先頭4桁を抽出(例: `2026`)         |
| `{{ number }}`        | frontmatter の `number`(例: `"00"`)          |
| `{{ label }}`         | frontmatter の `label`                        |
| `{{ series }}`        | "AIネイティブな仕事の作法" / "AI-Native Ways of Working" |
| `{{ series_index_url }}` | `/ai-native-ways/` または `/en/ai-native-ways/` |
| `{{ chapter_label }}` | `00` → "序章"/"Prologue", それ以外は "第N章"/"Chapter N" |
| `{{ content_html }}`  | Markdown 本文を CommonMark で変換した HTML    |
| `{{ canonical_url }}` | このページの正規 URL                          |
| `{{ hreflang_ja }}`   | JA 版 URL(対訳がある場合)                    |
| `{{ hreflang_en }}`   | EN 版 URL(対訳がある場合)                    |
| `{{ og_image }}`      | OG 画像 URL(`hero_image` から自動生成 or デフォルト) |
| `{{ other_lang_url }}`| 対訳ページの URL(言語スイッチャー用)          |
| `{{ other_lang_label }}` | "EN" / "日本語"                             |

## ビルド

リポジトリ全体のビルドツールに統合済み。

```bash
# 全シリーズ含めて一括ビルド
python3 tools/build_article.py --all

# このシリーズの単一章だけビルド
python3 tools/build_article.py articles/ai-native-ways/00-prologue/ja.md
python3 tools/build_article.py articles/ai-native-ways/00-prologue/en.md
```

出力先:

| ソース                                          | 出力                                    | URL                       |
|-------------------------------------------------|-----------------------------------------|---------------------------|
| `00-prologue/ja.md`                             | `html/ai-native-ways/prologue/index.html` | `/ai-native-ways/prologue/` |
| `00-prologue/en.md`                             | `html/en/ai-native-ways/prologue/index.html` | `/en/ai-native-ways/prologue/` |
| (シリーズ目次・自動生成) | `html/ai-native-ways/index.html` | `/ai-native-ways/` |
| (シリーズ目次・自動生成) | `html/en/ai-native-ways/index.html` | `/en/ai-native-ways/` |

シリーズ目次は共有 `tools/templates/index.html` を再利用してサイト全体と
統一感を保つ(章ページだけが独立タイポグラフィ)。目次の文言は
`tools/build/template_vars.py::aiways_index_vars()` で定義。

## 新しい章を追加する手順

1. `articles/ai-native-ways/NN-slug/` を作成

```bash
mkdir articles/ai-native-ways/01-markdown
$EDITOR articles/ai-native-ways/01-markdown/ja.md
$EDITOR articles/ai-native-ways/01-markdown/en.md
```

2. frontmatter を上記スキーマで書く。`prev_slug` / `next_slug` で前後ナビ。

3. 必要なら `title_html` でアクセント装飾。

4. ビルド

```bash
python3 tools/build_article.py --all
```

サイトマップ・トップページの最新記事枠・シリーズ目次が一括更新される。

## Markdown → HTML 変換

CommonMark + tables 拡張(`tools/build/markdown.py`)。

| Markdown        | HTML                              |
|-----------------|-----------------------------------|
| `## 見出し2`    | `<h2>`                            |
| `### 見出し3`   | `<h3>`                            |
| `> 引用`        | `<blockquote><p>`                 |
| `1. 項目`       | `<ol><li>`                        |
| ```` ```code``` ```` | `<pre><code>`                |
| `` `inline` ``  | `<code>`                          |
| `**bold**`      | `<strong>`(マーカー風ハイライト)    |
| `*italic*`      | `<em>`(アクセント色)               |
| `[text](url)`   | `<a href="url">text</a>`          |
| `---`           | `<hr>`(`◆ ◆ ◆` 装飾)              |

`# 見出し1` は frontmatter の `title` と重複するため自動で剥がされる。

## CSS 変数

テンプレート内で定義(他シリーズの CSS とは独立):

```css
:root {
  --ink:        #1a1a1a;  /* 本文色 */
  --paper:      #f4f1ea;  /* 背景色 */
  --paper-deep: #ebe6d8;  /* 背景の濃い版(blockquote等) */
  --accent:     #c8442a;  /* アクセント色(朱色) */
  --rule:       #d4cdb8;  /* 罫線色 */
  --whisper:    #6b665a;  /* 控えめな文字色 */
  --highlight:  #f7e9c8;  /* マーカー色 */
}
```

色を変えたい場合は `template.html` / `template.en.html` の冒頭 `:root`
ブロックを編集する。

## 実例フォルダ(`example-N/`)の作法

各章の主張は、**実行可能な証拠**で裏付ける。章フォルダの直下に
`example-1/`, `example-2/` … を作り、次の 5 点を揃える:

1. **`README.md`** ── 何を実演するか・章のどの主張に対応するか
2. **入力**(`source.md`、サンプル `*.docx`、CSV、コードなど)
3. **`Makefile`**(または `run.sh`)── 再現コマンドを 1 つに集約
4. **`results.md`** ── 実測値(ビルド時間、出力サイズ、ページ数、トークン比)
5. **`out/`** ── 生成物そのもの(コミットする。ブラウザで `git` 経由で開ける)

設計原則:

- **再現可能であること**: `make all` または `bash run.sh` で誰でも再走できる
- **計測値を出すこと**: 「速い」「小さい」ではなく「11.7 秒」「9 KB」と書く
- **生成物をコミットすること**: 読者が手元で動かせない場合でも、結果を見られる
- **依存関係を明記すること**: `pandoc` のバージョン、`pip install` するもの

ビルドパイプライン側では `example-N/` は無視される(数字始まりではないため)。
シリーズページや章ページとしては出力されない。リポジトリ内の証拠資料・
読者のコピー元として存在する。

雛形は `00-prologue/example-1/` を参照。

## このシリーズの章立て(計画)

```
00. 序章 ── 事務処理はOffice、業務ソフトはJava/C#、しかしAIはPythonとテキスト ✅

I. 共通の作法
01. 文書を書く ── Markdownという最小の選択
02. データを持つ ── JSON/CSV/YAMLで考える
03. デザインをする ── Mermaid と Claude デザインで作る
04. 処理を書く ── AIにPythonで書いてもらう

II. 仕事の種類別
05. 事務処理を変える ── Officeから離れる現実的な道筋
06. 業務システムと付き合う ── 並行稼働で書き換える
07. Webを作る ── HTML+CSS+JavaScriptという原点回帰
08. アプリを作る ── CLIツール、Fletアプリ、Flutterアプリ
09. 組み込みを作る ── Pythonで考え、Claudeに翻訳させる

III. 共通の発展
10. AIに任せる仕事を見極める
11. 1人+AIで作る、新しい仕事の単位

付録
12. 実例集 ── 11 のウォークスルー(コード + 出力)
```

すべての章で同じテンプレートを使い回す。章ごとの差はフロントマターと
任意の `title_html` のみ。
