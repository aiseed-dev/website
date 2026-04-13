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
cta_label: Structure
cta_title: 構造が全てだ。
cta_text: AIは開発に使う。プロダクトの中には入れない。それだけで攻撃面がゼロになる。
cta_btn1_text: Mythosが来た
cta_btn1_link: /insights/mythos/
cta_btn2_text: 全ての構造分析
cta_btn2_link: /insights/
---

## Mythos時代のセキュリティとは何か

第5章「[Mythosが来た](/insights/mythos/)」で、Mythos級AIの出現によりサイバー攻撃の経済学が根底から崩壊したことを示した。第6章「[Microsoftの崩壊](/insights/microsoft/)」で、密結合した巨大エコシステムが最も脆弱な標的になることを示した。

では、Mythos時代にどうやって守るのか。

答えは単純だ。**攻撃面をゼロにする。**

:::highlight
**Mythos時代のセキュリティ原則：**
1. AIで開発する。プロダクトにはAIを入れない
2. CMS、データベース、APIを本番環境に置かない
3. 静的HTMLだけを公開する
4. サーバーは1台、1アプリ、疎結合
5. ブラックボックスを排除する
**攻撃者がどれほど賢くても、入口がなければ侵入できない。**
:::

## このサイトが実証だ

[aiseed.dev](https://aiseed.dev/)は、この原則を実装したサイトだ。

:::chain
**このサイトのアーキテクチャ：**
開発 → Claude Code（AIが全コードを生成）
ビルド → Python + Jinja2 + markdown-it-py（ローカルで実行）
公開 → 静的HTML + CSS + 画像ファイルのみ
サーバー → Nginx（静的ファイル配信のみ）
AI → **本番環境にはゼロ**
CMS → **なし**
データベース → **なし**
API → **なし**
:::

:::compare
| 要素 | WordPress（43%のウェブ） | aiseed.dev |
| --- | --- | --- |
| CMS | あり（攻撃面） | なし |
| データベース | MySQL（SQLインジェクション） | なし |
| PHP | あり（リモートコード実行） | なし |
| プラグイン | 多数（未知の脆弱性） | なし |
| 管理画面 | あり（認証突破の標的） | なし |
| AI/Copilot | プラグインで追加可能（バックドア） | なし |
| 攻撃面 | **巨大** | **ゼロ** |
:::

Mythosクラスの推論能力を持つAIが来ても、静的HTMLには入口がない。SQLインジェクションの対象となるデータベースがない。リモートコード実行の対象となるサーバーサイドスクリプトがない。横展開するための内部ネットワークがない。

**攻撃面がゼロなら、攻撃能力は無関係だ。**

## 「AIで開発する」と「AIを入れる」は違う

ここが最も重要な区別だ。

:::chain
**AIで開発する（安全）：**
Claude Codeがコードを生成 → 人間がレビュー → ビルド → 静的HTMLを公開
AIは開発プロセスにだけ存在する
本番環境にAIのコードは一切動いていない
**AIは道具として使い、成果物にはAIを入れない**
:::

:::chain
**AIを入れる（危険）：**
Copilot → エディタに常駐 → コードベースを外部に送信（第5章）
AIプラグイン → CMSに統合 → 外部API経由でデータが流出
Security Copilot → テレメトリーに依存 → テレメトリーが偽装される（第6章）
**AIをプロダクトに入れた瞬間、攻撃面が爆発的に増大する**
:::

この区別を理解していない組織が、Mythos時代に最初に崩壊する。

## 人間はコードを1行も書いていない

このサイトは**Claude Code**だけで開発された。

HTML、CSS、JavaScript、Python、Markdown——全てClaudeが生成した。
人間がやったのは、何を作るかを決めて、Claudeに指示を出すことだけだ。

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

:::highlight
**人間の役割：**
構造分析のテーマを決めた（化石資源、農業、AI、NVIDIA、企業IT税……）
記事の方向性をClaudeに伝えた（「クラウド税も入れて」「エプスタインを最後に」）
出来上がったものを読んで、修正を指示した（「自宅→自社」「fade-inは不要」）
デプロイした
**コードは一切書いていない。**
:::

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

## 消えた「税」

第8章「[企業ITの税を引く](/insights/enterprise-tax/)」で書いた構造は、このサイト自体が実証している。

:::chain
**このサイトで消えた「税」：**
SIer税 → 外部委託ゼロ。Claudeがコードを全部書いた
Microsoft税 → Windows不使用。Linux＋Claude
クラウド税 → AWSもAzureも不要
SaaS税 → WordPress不使用。CMS不使用。Markdownとビルドツール
コンサルタント税 → 「何を作るべきか」もClaudeと対話して決めた
:::

かかったコストはClaudeの月額利用料だけだ。

## ビルドシステム——Claude自身が作ったツールチェーン

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

## 構造の結論

全15章の構造分析は、一つの結論に収束する。

:::chain
**構造分析の結論：**
化石資源は枯渇する（第1〜4章）
→ Mythos級AIが来た。密結合した巨大システムは崩壊する（第5〜6章）
→ 巨大組織は逃げられない（第7〜8章）
→ 個人＋AIが構造を変える（第9〜12章）
→ 引き算で設計し直す（第13〜14章）
→ **実証：AIで開発し、攻撃面ゼロのプロダクトを作る（第15章）**
:::

ソースコードは[GitHub](https://github.com/aiseed-dev/website)で公開されている。
ライセンスは[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。
誰でも使える。構造を見れば、Mythos時代の設計が分かる。

:::quote
AIを「使う側」に必要なのはGPUではなく、知性だ。
何を作るかを決められる人間と、それを実装できるAI。
この組み合わせが、数百万円の「税」を24時間でゼロにする。
そして攻撃面をゼロにする。
:::
