---
slug: enterprise-tax
number: "08"
title: 企業ITの税を引く
subtitle: Oracle税、Microsoft税、SaaS税、SIer税、コンサルタント税。Claudeが全部引く。
description: 企業は気づかないうちにOracle、Microsoft、SaaS、SIer、コンサルタントに「税」を払っている。Claudeはこれらの税を構造的に引く道具だ。
date: 2025.04.03
label: Structural Analysis 08
prev_slug: nvidia
prev_title: NVIDIAの崩壊
next_slug: healthcare-fiscal
next_title: 社会の設計ミス
---

## 企業は「税」を払っている

企業のIT支出を構造的に見ると、
技術への投資ではなく、**税**を払っていることが分かる。

選択肢がないから払う。慣性で払う。乗り換えが怖いから払う。
これは技術投資ではない。構造的な税だ。

:::highlight
**企業が払っている5つの税：**
1. **Oracle税 / SQL Server税** — データベースライセンス
2. **Microsoft税** — Windows、Office 365、Azure
3. **SaaS税** — 月額サブスクリプションの積み重ね
4. **SIer税** — システム構築・運用の外部委託
5. **コンサルタント税** — 「何をすべきか」を外部に聞く費用
:::

Claudeは、これらの税を**構造的に引く**道具だ。

## Oracle税 / SQL Server税——最も分かりやすい税

Oracle Database のライセンス費用を見たことがあるか。

:::highlight
**Oracle税の構造：**
Oracle Database Enterprise Edition → 1プロセッサあたり年間数百万円
Oracle RAC（高可用性）→ 追加ライセンス
Oracle Partitioning → 追加ライセンス
Oracle Advanced Security → 追加ライセンス
Oracle サポート契約 → ライセンス費の22%を毎年支払い続ける
**機能を使うたびに課金される。使わなくても基本料を取られる。**
:::

SQL Serverも同じ構造だ。Enterprise Editionは1コアあたり年間数十万円。
機能を追加するたびにライセンスが増える。

しかし、PostgreSQLが存在する。

:::compare
| | Oracle / SQL Server | PostgreSQL |
| --- | --- | --- |
| ライセンス費 | 年間数百万〜数千万円 | **無料** |
| 高可用性 | 追加ライセンス（数百万円） | Patroni等で構築可能（無料） |
| パーティショニング | 追加ライセンス | 標準機能 |
| JSON対応 | 追加オプション | 標準機能 |
| 全文検索 | 追加オプション | 標準機能 |
| 性能 | 高い | 同等（用途による） |
| 移行の壁 | — | **SQLの方言、ストアドプロシージャの書き換え** |
:::

移行の壁は「SQLの方言の違い」と「ストアドプロシージャの書き換え」だ。
これが、企業がOracle税を何十年も払い続けてきた理由だ。

**ここにClaudeが来る。**

:::chain
**Claudeによるデータベース移行：**
OracleのSQL・ストアドプロシージャをClaudeに渡す
→ ClaudeがPostgreSQL互換のSQLに書き換える
→ Oracle独自関数をPostgreSQL関数にマッピングする
→ PL/SQL → PL/pgSQLに変換する
→ テストケースも生成する
→ **移行の壁が消える**
→ Oracle税が消える
:::

これは仮説ではない。
Claudeは数十万行のコードベースを理解し、書き換える能力がある。
SQLの方言変換はコードの構造変換であり、AIが最も得意とする仕事だ。

SQL Serverからの移行も同じだ。
T-SQL → PL/pgSQL。SSMS依存の管理スクリプト → 標準SQL。
Claudeが書き換えれば、SQL Server税も消える。

## Microsoft税

Windows、Office 365、Azure、Teams——
Microsoftは企業に対して複数の「税」を同時に課している。

:::highlight
**Microsoft税の内訳：**
Windows → PCごとにOEMライセンス。選択の余地なし。
Office 365 → 月額1,000〜4,000円/ユーザー × 全社員 × 12ヶ月
Azure → 「Windowsとの親和性」でロックイン
Teams → Office 365にバンドル。「無料」に見えるが、バンドルの一部
**中堅企業（500人）で年間数千万円。**
:::

Claudeが引けるMicrosoft税：

:::chain
**Microsoft税の引き方：**
文書作成 → ClaudeがMarkdown/HTML/PDFを直接生成。Wordが不要になる。
表計算 → Claudeがデータ分析コードを書く。Excelが不要になる。
プレゼン → ClaudeがHTML/Marpスライドを生成。PowerPointが不要になる。
メール → AIが下書き・整理。Outlookの必要性が低下。
クラウド → AWS/GCP/自前サーバーに移行。Claudeが設定を書く。
:::

全てを一度に引く必要はない。
一つずつ引けばいい。一つ引くたびに、Microsoft税は減る。

## SaaS税——月額課金の積み重ね

SaaS（Software as a Service）は「所有しない」ことが売りだった。
しかし、気づけば月額課金が積み重なっている。

:::highlight
**SaaS税の実態（中堅企業の例）：**
Salesforce → 月額数万円/ユーザー × 営業部門
Slack → 月額数千円/ユーザー × 全社員
Zoom → 月額数千円/ライセンス
Notion → 月額数千円/ユーザー
Figma → 月額数千円/ユーザー × デザイン部門
Jira → 月額数千円/ユーザー × 開発部門
その他10〜20のSaaS → 月額数十万〜数百万円
**合計：年間数千万円の「税」を、気づかないうちに払っている。**
:::

これらのSaaSが提供する機能の多くは、
Claudeの支援で自前のツールに置き換えられる。

:::chain
**SaaS税の引き方：**
CRM → Claudeがシンプルなデータベース＋UIを構築
チャット → オープンソース（Mattermost等）＋自前サーバー
プロジェクト管理 → Claudeが要件に合わせたツールを構築
ドキュメント → Markdown＋Git＋静的サイト生成
**全てのSaaSを置き換える必要はない。高額なものから順に引けばいい。**
:::

## SIer税——「作ってもらう」から「自分で作る」へ

日本企業のIT投資の大部分は、SIer（システムインテグレーター）に流れている。

:::highlight
**SIer税の構造：**
要件定義 → SIerが聞き取り → 数百万円
基本設計 → SIerが設計 → 数百万円
詳細設計 → SIerが文書化 → 数百万円
開発 → SIerが実装 → 数千万円
テスト → SIerがテスト → 数百万円
運用保守 → SIerが月額で請求 → 年間数百万〜数千万円
**合計：一つのシステムで数千万〜数億円。**
:::

SIerの工数の大半は「設計書の作成」と「定型的なコーディング」だ。
Claudeが最も得意とする仕事である。

:::chain
**SIer税の引き方：**
要件 → 社内の業務を知っている人間がClaudeに直接伝える
設計 → Claudeが設計書を生成
開発 → Claudeがコードを書く
テスト → Claudeがテストコードを生成
運用 → Claudeが監視・保守の仕組みを構築
**SIerの役割の大半を、Claudeが代替する。**
:::

社内の業務を最もよく知っているのは社員だ。SIerではない。
社員がClaudeに直接要件を伝え、Claudeがシステムを作る。
「翻訳者」としてのSIerが不要になる。

## コンサルタント税——「何をすべきか」は自分で考えろ

マッキンゼー、BCG、アクセンチュア——
企業は「何をすべきか」を外部のコンサルタントに聞くために、
数千万〜数億円を払っている。

:::highlight
**コンサルタント税の構造：**
「我が社のDX戦略を策定してほしい」→ 数千万円
「AIの活用方針を提案してほしい」→ 数千万円
「コスト削減の施策を洗い出してほしい」→ 数千万円
成果物 → 美しいPowerPointのスライド数十枚
**実装は含まれない。「考える」だけで数千万円。**
:::

Claudeは構造的思考の道具だ。
コンサルタントが数週間かけて作るスライドの内容を、
Claudeは数時間で構造化できる。

:::chain
**コンサルタント税の引き方：**
業界分析 → Claudeが公開データから構造を抽出
競合分析 → Claudeが生産ルートと依存関係を追跡
コスト分析 → Claudeが支出構造を分解
戦略提案 → Claudeが選択肢と因果関係を可視化
**コンサルタントに払う数千万円の大半は、Claudeで代替できる。**
:::

コンサルタントの本当の価値は「外部の目線」だ。
しかし、「外部の目線」に数千万円を払う時代は終わりつつある。
Claudeは究極の外部の目線だ。業界の慣習に囚われない。忖度しない。

## 5つの税の合計

:::compare
| 税 | 中堅企業（500人）の年間コスト | Claudeで引けるか |
| --- | --- | --- |
| Oracle / SQL Server税 | 数百万〜数千万円 | PostgreSQL移行で引ける |
| Microsoft税 | 数千万円 | 段階的に引ける |
| SaaS税 | 数千万円 | 高額なものから引ける |
| SIer税 | 数千万〜数億円（プロジェクトごと） | 大半を引ける |
| コンサルタント税 | 数千万円（案件ごと） | 大半を引ける |
| **合計** | **年間1〜数億円の「税」** | — |
:::

Claudeの利用料は、これらの税に比べれば桁違いに安い。
月額数万円のClaude利用で、年間数千万〜数億円の税が引ける。

:::quote
企業のIT支出の大半は、技術への投資ではなく「税」だ。
Oracle税、Microsoft税、SaaS税、SIer税、コンサルタント税——
選択肢がないから払い、慣性で払い、乗り換えが怖いから払い続けてきた。
Claudeはこれらの税を構造的に引く道具だ。
NVIDIAのCUDAロックインと同じように、
Oracle、Microsoft、SIerのロックインもAIが壊す。
:::
