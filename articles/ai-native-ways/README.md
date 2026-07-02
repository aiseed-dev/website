# AIネイティブな仕事の作法

**副題: AI 時代の自由人のための道具たち**。
aiseed.dev の連載エッセイシリーズ。Office・Java・C# から離れ、Markdown・JSON・
Python・テキストで AI を同僚として使うための実用的な作法。
第 1 章「活用マニュアル」が普通の人向けの 6 つのコツを置き、
第 2 章以降がそれを領域別の道具立てに落としていく。

**底流**: AI が技術職の核心(ソフトウェア工学)を引き受ける結果、人間側に残る
判断中心の役割の基盤が、**ソフトウェア工学からリベラルアーツへ** 移る ──
これは「特化エンジニアになれ」助言の構造的誤りを衝き、「**AI 時代の自由人**」
の輪郭を描く論考である。詳しくは概念フレーム `framing-second-renaissance`
スキル (`.agents/skills/`) と、合成的入口となるブログ
[`articles/blog/021-software-three-transitions/`](../blog/021-software-three-transitions/)
を参照。

## 状態

**親シリーズ全 14 章公開済み**(00 序章 + 01〜13 章、JA + EN)。
**サブシリーズ「ソフトウェア開発編」全 11 章公開済み**(`software/`)。

## ファイル構成

```
articles/ai-native-ways/
├── README.md                ── このファイル
├── NN-slug/                 ── 1章 = 1フォルダ(親シリーズ)
│   ├── ja.md                ── 日本語版本文 + frontmatter
│   ├── en.md                ── 英語版本文 + frontmatter
│   └── example-N/           ── 章ごとの実例(任意・複数可)
│       ├── README.md
│       ├── source.md / *.py / その他入力
│       ├── Makefile         ── 再現用ビルド定義
│       ├── results.md       ── 実測値(時間・サイズ・ページ数)
│       └── out/             ── 生成物(コミットする)
└── <subseries>/             ── サブシリーズ(例: software/)
    ├── README.md            ── サブシリーズ仕様
    └── NN-slug/             ── 1章 = 1フォルダ(サブシリーズ内で 01 から再採番)
        ├── ja.md
        ├── en.md
        └── example-N/
```

サブシリーズは `tools/build_article.py::AIWAYS_SUBSERIES` に登録されたサブ
ディレクトリのみ有効。サブシリーズ章の URL は `/ai-native-ways/<subseries>/{slug}/`、
専用の目次ページが `/ai-native-ways/<subseries>/` に生成される。親シリーズの
目次ページ (`/ai-native-ways/`) はサブシリーズの章を含めず、代わりに先頭に
ヒーローカードでサブシリーズを案内する。

詳細はサブシリーズ自身の README(例: `software/README.md`)を参照。

実体例:

```
articles/ai-native-ways/
├── README.md
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

このエッセイ型デザインはサイト全記事の共通テンプレートに昇格しており、
`tools/templates/chapter.html` / `chapter.en.html` を `build_aiways_chapter()`
が他シリーズと同様に使う。

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

色を変えたい場合は `tools/templates/chapter.html` / `chapter.en.html` の
冒頭 `:root` ブロックを編集する(全シリーズ共通に効く)。

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

## 親シリーズの章一覧(公開済み)

| # | slug | 日本語タイトル |
|---|---|---|
| 00 | `prologue` | AIの母国語は、PythonとMarkdown形式のテキスト |
| 01 | `manual` | AI（ChatGPT・Claudeなど）活用マニュアル ── 普通の人のための6つのコツ |
| 02 | `python` | 処理を書く ── AIにPythonで書いてもらう |
| 03 | `markdown` | 文書を書く ── Markdownという最小の選択 |
| 04 | `design` | デザインをする ── Mermaid と Claude デザインで作る |
| 05 | `data-formats` | データを持つ ── JSONとYAMLで考える |
| 08 | `web` | Webを作る ── HTML+CSS+JavaScriptという原点回帰 |
| 09 | `apps` | アプリを作る ── CLIツール、Fletアプリ、Flutterアプリ |
| 10 | `embedded` | 組み込みを作る ── Pythonで考え、Claudeに翻訳させる |
| 11 | `ai-delegation` | AIに任せる仕事を見極める |
| 12 | `verify-narratives` | AIで物語を検証する |
| 13 | `one-plus-ai` | 1人+AIで作る、新しい仕事の単位 |

旧 06「事務処理を変える」と 07「業務システムと付き合う」は、組織の基盤づくり
としてサブシリーズ「ソフトウェア開発編」自立編に統合・移設した（06 → 自立編
第5章 `documents`、07 → 自立編第9章 `fastapi`）。本編の番号 06・07 は欠番。

序章「AI 時代の自由人」節で中世の自由人の4条件パラレル(経済的自立・政治的
自治・実体に触れる力・教養)、その下の「中間層」「第二次ルネサンス」を
位置付けている。各章はそれぞれの領域で具体的作法を扱う。

## サブシリーズ「ソフトウェア開発編」

`software/` 配下。**副題: ソフトウェア工学から、リベラルアーツへ ── 技術職の
基盤転換**。全 11 章で、SIer 委託モデルが構造的に成立しなくなり、判断中心の
「ビルダー」「上級ビルダー」が AI 時代の専門職として立ち上がる構造を論証。
詳細は [`software/README.md`](software/README.md)。

合成的な入口として、ブログ
[`articles/blog/021-software-three-transitions/`](../blog/021-software-three-transitions/)
が「ソフトウェアエンジニア → ビルダー」「ソフトウェア工学 → リベラルアーツ」
「雇用 → 自由人」の三対の語に圧縮した版を提供している。

すべての章で同じテンプレートを使い回す。章ごとの差はフロントマターと
任意の `title_html` のみ。
