# AIネイティブな仕事の作法 — 序章

aiseed.dev に組み込むための、序章の素材一式(日本語版・英語版)。

## ファイル構成

```
chapter-00-content.md         ── 日本語版 本文(Markdown + frontmatter)
chapter-00-content.en.md      ── 英語版 本文
chapter-00-template.html      ── 日本語版 HTMLテンプレート
chapter-00-template.en.html   ── 英語版 HTMLテンプレート
chapter-00-README.md          ── このファイル
```

## 設計方針

**コンテンツとテンプレートの分離**

- `chapter-00-content.md` / `.en.md` は内容のみ。フロントマターでメタデータを保持。
- `chapter-00-template.html` / `.en.html` は構造とスタイルのみ。プレースホルダで内容を受け取る。
- aiseed.dev 既存サイトに組み込む際、テンプレート側を既存スタイルに差し替えれば内容はそのまま使える。

**日本語版と英語版の差異**

| 項目             | 日本語版                       | 英語版                          |
|------------------|------------------------------|--------------------------------|
| 本文フォント     | システム明朝(ヒラギノ・游明朝) | Crimson Pro(セリフ)           |
| 見出しフォント   | Shippori Mincho 700/800      | Crimson Pro 700/800            |
| 関連リンクのpath | `/insights/...`              | `/en/insights/...`             |
| マストヘッド     | "AIネイティブな仕事の作法"    | "AI-Native Ways of Working"    |
| 章ラベル         | "序章"                       | "Prologue"                     |

両言語とも、JetBrains Mono を等幅・装飾用フォントとして共通使用。

**プレースホルダの記法**

テンプレート内では Jinja2 風の `{{ variable }}` および `{% for %}` 記法を使用。
Claude Code で組み込む際は、aiseed.dev のテンプレートエンジン(11ty / Astro / Hugo / Eleventy 等の実際の構成)に合わせて変換する。

## フロントマターの構造

```yaml
title: 記事のタイトル
series: シリーズ名(例: "AIネイティブな仕事の作法")
chapter: 章番号(数値、序章は 0)
chapter_label: 章ラベル(例: "序章" / "第1章")
date: YYYY-MM-DD
description: メタディスクリプション(OGP用)
read_time: 推定読了時間
related:
  - series: 関連シリーズ名
    chapter: 関連章番号
    title: 関連記事タイトル
    url: 関連記事URL
  - type: blog
    title: 関連ブログタイトル
    url: 関連ブログURL
```

## テンプレートのプレースホルダ一覧

| プレースホルダ        | 意味                                |
|-----------------------|-------------------------------------|
| `{{ title }}`         | 記事タイトル                        |
| `{{ series }}`        | シリーズ名                          |
| `{{ chapter }}`       | 章番号(数値)                        |
| `{{ chapter_label }}` | 章ラベル                            |
| `{{ date }}`          | 公開日                              |
| `{{ description }}`   | 概要                                |
| `{{ read_time }}`     | 読了時間                            |
| `{{ content_html }}`  | Markdown を HTML 変換した本文       |
| `{{ related }}`       | 関連記事配列(for ループで展開)      |

## hero-title のカスタマイズ

序章の hero-title は、3行構成で `<span class="accent">` を使った強調を含む。
他の章で使い回す場合は、テンプレートのこの部分を直接編集するか、
フロントマターから HTML 断片として受け取る形に変える。

```html
<!-- 現在の固定HTML(序章用) -->
<h1 class="hero-title">
  事務処理は<span class="accent">Office</span>。<br>
  業務ソフトは<span class="accent">Java/C#</span>。<br>
  しかしAIは、<span class="accent">Pythonとテキスト</span>。
</h1>
```

将来的には、フロントマターに `title_html` として持たせる:

```yaml
title_html: |
  事務処理は<span class="accent">Office</span>。<br>
  業務ソフトは<span class="accent">Java/C#</span>。<br>
  しかしAIは、<span class="accent">Pythonとテキスト</span>。
```

## Markdown → HTML 変換の対応

Markdown 本文を HTML に変換する際の対応表:

| Markdown        | HTML                              |
|-----------------|-----------------------------------|
| `# 見出し1`     | (タイトルとして hero 側で扱う、本文では使わない) |
| `## 見出し2`    | `<h2>`                            |
| `### 見出し3`   | `<h3>`                            |
| `> 引用`        | `<blockquote><p>`                 |
| `1. 項目`       | `<ol><li>`                        |
| ```` ```code``` ```` | `<pre><code>`                |
| `` `inline` ``  | `<code>`                          |
| `**bold**`      | `<strong>`                        |
| `*italic*`      | `<em>`                            |
| `[text](url)`   | `<a href="url">text</a>`          |
| `---`           | `<hr>`(本文中の区切り装飾)       |

CSS は上記すべての要素に対応済み。一般的な Markdown パーサ
(markdown-it, remark, marked, python-markdown 等)で変換すれば
そのまま機能する。

## CSS 変数(既存サイトに合わせる場合)

aiseed.dev 既存のスタイルに統合する際は、以下の CSS 変数を
既存サイトの値に差し替える:

```css
:root {
  --ink:        /* 本文色 */
  --paper:      /* 背景色 */
  --paper-deep: /* 背景の濃い版(blockquote等) */
  --accent:     /* アクセント色(リンク・強調) */
  --rule:       /* 罫線色 */
  --whisper:    /* 控えめな文字色 */
  --highlight:  /* マーカー色 */
}
```

## フォント戦略(重要)

**読み込み速度を優先**。本文はシステム明朝(ヒラギノ・游明朝・Noto Serif CJK)を使い、
Webフォントは見出しとタイトルにのみ使用。

- Shippori Mincho: 700/800 のみ(タイトル・h2 用)
- JetBrains Mono: 400/700 のみ(等幅・コード用)
- 本文・h3・h4・blockquote: システム明朝(Webフォント不要)

aiseed.dev 既存サイトが別のフォント戦略を採っている場合は、
`@import` 部分と `font-family` 指定を既存サイトに揃える。

## このシリーズの章立て(計画)

```
00. 序章 ── 事務処理はOffice、業務ソフトはJava/C#、しかしAIはPythonとテキスト

I. 共通の作法(全員向け)
01. 文書を書く ── Markdownという最小の選択
02. データを持つ ── JSON/CSV/YAMLで考える
03. 図を描く ── Mermaidで構造を残す

II. 仕事の種類別(該当者向け)
04. 事務処理を変える ── Officeから離れる現実的な道筋
05. 業務システムと付き合う ── 既存資産を活かしつつAIで補う
06. Webを作る ── HTML+CSS+JavaScriptという原点回帰
07. アプリを作る ── Flutterの中でAIをどう使うか
08. 組み込みを作る ── Pythonで考え、Claudeに翻訳させる

III. 共通の発展(全員向け)
09. AIに任せる仕事を見極める
10. 1人+AIで作る、新しい仕事の単位
```

すべての章で同じテンプレートを使い回せる構造にしてある。
章ごとの差は、フロントマターと hero-title の HTML 断片のみ。
