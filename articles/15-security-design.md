---
slug: security-design
number: "15"
title: Mythos時代のセキュリティ設計
subtitle: AIで開発し、プロダクトにはAIを入れない。攻撃面ゼロの実践。
description: aiseed.devはClaude Codeで開発され、本番環境は静的HTML＋Nginx。AI無し、CMS無し、データベース無し。Mythos級AIが来ても侵入・横展開するエントリーポイントがない。これが構造分析シリーズの結論の実証だ。
date: 2025.04.13
label: Structural Analysis 15
prev_slug: subtraction-design
prev_title: 引き算の設計
next_slug: 
next_title: 
---

## 人間はコードを1行も書いていない

[aiseed.dev](https://aiseed.dev/)は、**Claude Code**（Anthropic社のAI開発ツール）だけで開発された。

HTML、CSS、JavaScript、Python、Markdown——全てClaudeが生成した。
人間がやったのは、何を作るかを決めて、Claudeに指示を出すことだけだ。

## 数字で見る

:::compare
| 項目 | 数値 |
| --- | --- |
| 総行数（コード＋コンテンツ） | 30,000+ |
| HTMLページ | 42 |
| 記事数 | 26（日本語13 + 英語13） |
| 開発期間 | 約24時間 |
| gitコミット | 104 |
| 人間が書いたコード | **0行** |
:::

## 何が作られたか

:::chain
**サイトの構成：**
全13章の構造分析シリーズ（日本語＋英語）
Markdown → HTML ビルドツール（Python / Jinja2 / markdown-it-py）
カスタムブロック構文（:::chain, :::highlight, :::quote, :::compare）
OGP / Twitter Card / hreflang / canonical / CSP 対応
sitemap.xml / robots.txt 自動生成
Cloudflare Pages でホスティング
**全てClaude Codeが生成**
:::

## 人間は何をしたか

:::highlight
**人間の役割：**
構造分析のテーマを決めた（化石資源、農業、AI、NVIDIA、企業IT税……）
記事の方向性をClaudeに伝えた（「クラウド税も入れて」「エプスタインを最後に」）
出来上がったものを読んで、修正を指示した（「自宅→自社」「fade-inは不要」）
デプロイした（git push → Cloudflare Pages）
**コードは一切書いていない。**
:::

## これが第8章の実証だ

第8章「[企業ITの税を引く](/insights/enterprise-tax/)」で書いた構造は、このサイト自体が実証している。

:::chain
**このサイトで消えた「税」：**
SIer税 → 外部委託ゼロ。Claudeがコードを全部書いた
Microsoft税 → Windows不使用。Linux＋Claude
クラウド税 → Cloudflare Pages（無料）。AWSもAzureも不要
SaaS税 → WordPress不使用。CMS不使用。Markdownとビルドツール
コンサルタント税 → 「何を作るべきか」もClaudeと対話して決めた
:::

かかったコストはClaudeの月額利用料だけだ。

## SIerに発注したら

:::highlight
**同じサイトをSIerに発注した場合の見積もり：**
要件定義 → 数十万〜百万円
デザイン → 数十万円
コーディング（42ページ＋ビルドツール） → 数百万円
多言語対応（日英26記事） → 数百万円
SEO対策（OGP、sitemap、CSP等） → 数十万円
テスト・デプロイ → 数十万円
**合計：500万〜1,000万円。納期：2〜3ヶ月。**
Claudeでやったら：**24時間。コストはほぼゼロ。**
:::

## ビルドシステム——Claude自身が作ったツールチェーン

このサイトのビルドシステム自体が、AIによるソフトウェア開発の実例だ。

:::chain
**ビルドパイプライン：**
記事をMarkdownで書く（カスタム拡張構文を含む）
→ build_article.py がMarkdownを解析
→ カスタムブロック（:::chain, :::highlight等）をHTMLに変換
→ markdown-it-py（CommonMark準拠）で残りを変換
→ Jinja2テンプレートに流し込む
→ OGP、canonical、hreflang等のSEOタグを自動付与
→ sitemap.xml、robots.txt を自動生成
→ 全42ページを一括ビルド
**このパイプライン全体をClaudeが設計・実装した**
:::

:::highlight
**最初はPython-Markdownとf-string テンプレートだった。**
開発途中でJinja2 + markdown-it-pyに移行した。
移行もClaude自身が行った。
テンプレートの構文変更、CSSブレース二重化の解消、ビルドスクリプトの書き換え——
人間は「この例を活かせるはずです」とリポジトリのURLを渡しただけだ。
:::

## ソースコードは公開されている

全てのコードは[GitHub](https://github.com/aiseed-dev/website)で公開されている。
ライセンスは[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。
誰でも使える。構造を見れば、AIで何ができるかが分かる。

:::quote
AIを「使う側」に必要なのはGPUではなく、知性だ。
何を作るかを決められる人間と、それを実装できるAI。
この組み合わせが、数百万円の「税」を24時間でゼロにする。
:::
