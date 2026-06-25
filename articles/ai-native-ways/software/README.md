# ソフトウェア開発編 — AIネイティブな仕事の作法

**副題: ソフトウェア工学から、リベラルアーツへ ── 技術職の基盤転換**

親シリーズ「AIネイティブな仕事の作法」(`../README.md`)のサブシリーズ。
SIer 委託モデルの構造的不経済を 11 章で論証し、近い将来に起き、前提の逆転
ゆえに不可逆な産業構造転換の輪郭を描く。AI がソフトウェア工学の核心(アルゴリズム、言語、
フレームワーク、設計パターン)を引き受けた結果、人間側に残る判断中心の役割
── ビルダー ── の基盤学問が、ソフトウェア工学からリベラルアーツ(論理・
言語化・倫理・体系的思考・歴史)へ移ること。これが本サブシリーズの底流だ。

主旨と章構成は `docs/Ai-native-software-outline.md` を正本とする。執筆運用は
スキル `building-ai-native-software-series`(`.agents/skills/`)に従う。
概念フレーム全体は `framing-second-renaissance` スキル(15 概念体系)。
EN 版 README は [`README.en.md`](README.en.md)。

## 状態

**全 11 章公開済み** (JA + EN、各 22 ファイル)。

合成的な入口(短縮版・宣伝用)として、ブログ
[`articles/blog/021-software-three-transitions/`](../../blog/021-software-three-transitions/)
が「ソフトウェアエンジニア → ビルダー」「ソフトウェア工学 → リベラルアーツ」
「雇用 → 自由人」の三対の語にサブシリーズの論証を圧縮している。深い論証は
第11章「もう戻らない構造転換」に集約(第二次ルネサンス節として、9項目
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
名は `series` 側に入るので、`chapter_label` 単体は短い形 (`第N章` /
`Chapter N`) を使う。連結後の表示は次のとおり。

- JA: `AIネイティブな仕事の作法 — ソフトウェア開発編 · 第N章`
- EN: `AI-Native Ways of Working — Software · Chapter N`

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

| # | slug | 日本語タイトル |
|---|---|---|
| 01 | `coder-top` | AI は、世界で最も難しいコーディング問題を解く |
| 02 | `maintenance-shift` | 保守フェーズの構造変化こそ本質 |
| 03 | `coder-end` | ソフトウェアエンジニアの仕事を AI がするようになる |
| 04 | `builder` | ビルダーという役割 |
| 05 | `customer-codev` | 顧客がAIと協働して開発する時代 |
| 06 | `sier-uneconomic` | SIer委託モデルの構造的不経済 |
| 07 | `lockin` | ロックイン問題 |
| 08 | `hiring-builders` | 各社がビルダーを雇用する時代 |
| 09 | `japan-transition` | 日本のSIer業界の転換と雇用流動性 |
| 10 | `five-years` | もう戻らない構造転換 |

slug は確定済み。URL の安定性のため、以後変更しない。
