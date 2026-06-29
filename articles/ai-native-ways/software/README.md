# ソフトウェア開発編 — AIネイティブな仕事の作法

**副題: ソフトウェア工学から、リベラルアーツへ ── 技術職の基盤転換**

親シリーズ「AIネイティブな仕事の作法」(`../README.md`)のサブシリーズ。
SIer 委託モデルの構造的不経済を、三編・全 23 章(導入編・自立編・転換編、各編
1 から再採番)で論証し、近い将来に起き、前提の逆転ゆえに不可逆な産業構造転換の
輪郭を描く。AI がソフトウェア工学の核心(アルゴリズム、言語、
フレームワーク、設計パターン)を引き受けた結果、人間側に残る判断中心の役割
── ビルダー ── の基盤学問が、ソフトウェア工学からリベラルアーツ(論理・
言語化・倫理・体系的思考・歴史)へ移ること。これが本サブシリーズの底流だ。

主旨・章構成・執筆運用は、スキル `building-ai-native-software-series`
(`.agents/skills/`)を正本とする(かつての `docs/Ai-native-software-outline.md`
は作成されなかった)。概念フレーム全体は `framing-second-renaissance`
スキル(15 概念体系)。EN 版 README は [`README.en.md`](README.en.md)。

## 状態

**全 23 章公開済み** (JA + EN、計 46 ファイル)。三編構成 ── 導入編(1-01〜1-05)・
自立編(2-01〜2-11)・転換編(3-01〜3-07)。

合成的な入口(短縮版・宣伝用)として、ブログ
[`articles/blog/021-software-three-transitions/`](../../blog/021-software-three-transitions/)
が「ソフトウェアエンジニア → ビルダー」「ソフトウェア工学 → リベラルアーツ」
「雇用 → 自由人」の三対の語にサブシリーズの論証を圧縮している。深い論証は
最終章「もう戻らない構造転換」(3-07)に集約(第二次ルネサンス節として、9項目
対応表 + AI 革命=IT 革命の完成 + LLM 統計処理ツール本質 + アプリ=映画作り
+ AI 革命だけの話ではない + 創造と混乱の両側)。

## ファイル構成

```
articles/ai-native-ways/software/
├── README.md           ── このファイル (JA)
├── README.en.md        ── EN 版
└── NN-slug/            ── サブシリーズ内で 01 から再採番
    ├── ja.md
    ├── en.md
    └── example-N/      ── 章ごとの実例(任意)
```

親シリーズの `template.html` / `template.en.html` をそのまま使う。フロント
マターの schema も親シリーズと共通。EN 版は `lang: en` を明示する。

## URL

| ソース | 出力 | URL |
|---|---|---|
| `01-coder-top/ja.md` | `html/ai-native-ways/software/coder-top/index.html` | `/ai-native-ways/software/coder-top/` |
| `01-coder-top/en.md` | `html/en/ai-native-ways/software/coder-top/index.html` | `/en/ai-native-ways/software/coder-top/` |
| (サブシリーズ目次・自動生成) | `html/ai-native-ways/software/index.html` | `/ai-native-ways/software/` |
| (サブシリーズ目次・自動生成) | `html/en/ai-native-ways/software/index.html` | `/en/ai-native-ways/software/` |

## 章ラベル

ブレッドクラムでは `series · chapter_label` の形で連結される。サブシリーズ
名は `series` 側に入る。`chapter_label` は編内採番なので **`編名 部-章`**
(編の短名 + `部digit-章番号`、例 `自立編 2-10`)になる。連結後の表示は
次のとおり。

- JA: `AIネイティブな仕事の作法 — ソフトウェア開発編 · 自立編 2-10`
- EN: `AI-Native Ways of Working — Software · Independence 2-10`

## prev / next チェーン

サブシリーズ**内**で閉じる。01 章は `prev_slug: ""` / `prev_title: ""`、
最終章は `next_slug: ""` / `next_title: ""` のままにする。親シリーズに
ブリッジしない。

## 親シリーズ目次との関係

- 親シリーズ目次 (`/ai-native-ways/`) は先頭にヒーローカードでこの
  サブシリーズへ誘導する。
- 親シリーズの章リスト本体にこのサブシリーズの章は **含まれない**。
- サブシリーズ目次 (`/ai-native-ways/software/`) は親シリーズ目次への
  「← 目次へ戻る」リンクを冒頭に持つ。

## 章一覧

表示番号は `部-章`(編内で 1 から)。フォルダは全体順の `NN-slug`。

**導入編 ── なぜ作り、どう始めるか**

| 部-章 | folder | slug | 日本語タイトル |
|---|---|---|---|
| 1-01 | `01-coder-top` | `coder-top` | AI は、世界で最も難しいコーディング問題を解く |
| 1-02 | `02-maintenance-shift` | `maintenance-shift` | 保守フェーズの構造変化こそ本質 |
| 1-03 | `03-coder-end` | `coder-end` | ソフトウェアエンジニアの仕事を AI がするようになる |
| 1-04 | `04-builder` | `builder` | ビルダーという役割 |
| 1-05 | `05-customer-codev` | `customer-codev` | 顧客がAIと協働して開発する時代 |

**自立編 ── M365・Copilot・WordPress・基幹システム・GitHub から自立する**

| 部-章 | folder | slug | 日本語タイトル |
|---|---|---|---|
| 2-01 | `06-independence` | `independence` | Microsoft と Google から自立する ── 全体像と対応表 |
| 2-02 | `07-foundation` | `foundation` | 土台を据える ── SQLite・PostgreSQL・pgvector・DuckDB・Polars |
| 2-03 | `08-auth` | `auth` | 門番を立てる ── PocketBase で認証を一つに |
| 2-04 | `09-code` | `code` | コードを手元に ── Forgejo と Zed |
| 2-05 | `10-documents` | `documents` | 文書を取り戻す ── OnlyOffice Docs を PocketBase に組み込む |
| 2-06 | `11-mail` | `mail` | メールを自分の側に ── Stalwart と Thunderbird |
| 2-07 | `12-meetings` | `meetings` | 会議と予約を自分の側に ── Jitsi と Cal.com |
| 2-08 | `13-web` | `web` | Webを公開する ── Cloudflare Pages（WordPress 代替） |
| 2-09 | `14-fastapi` | `fastapi` | API を作る ── FastAPI で基幹のロジックを出す |
| 2-10 | `15-structure-knowledge` | `structure-knowledge` | 社内情報を整える ── 整備こそ本体、AI は最後の一手 |
| 2-11 | `16-ai` | `ai` | 自前の AI を据える ── LLM と RAG |

**転換編 ── 産業構造の帰結**

| 部-章 | folder | slug | 日本語タイトル |
|---|---|---|---|
| 3-01 | `17-two-worlds` | `two-worlds` | 企業は自分でコードを書かない ── 事務と基幹、二つの世界の並立 |
| 3-02 | `18-sovereignty` | `sovereignty` | デジタル主権 ── Microsoft 問題と Trump 問題 |
| 3-03 | `19-sier-uneconomic` | `sier-uneconomic` | SIer委託モデルの構造的不経済 |
| 3-04 | `20-lockin` | `lockin` | ロックイン問題 |
| 3-05 | `21-hiring-builders` | `hiring-builders` | 各社がビルダーを雇用する時代 |
| 3-06 | `22-japan-transition` | `japan-transition` | 日本のSIer業界の転換と雇用流動性 |
| 3-07 | `23-five-years` | `five-years` | もう戻らない構造転換 |

slug は確定済み。URL の安定性のため、以後変更しない。
