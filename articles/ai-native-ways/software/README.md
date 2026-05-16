# ソフトウェア開発編 — AIネイティブな仕事の作法

親シリーズ「AIネイティブな仕事の作法」(`../README.md`)のサブシリーズ。
SIer 委託モデルの構造的不経済を 11 章で論証し、数年単位で完了する不可逆な
産業構造転換の輪郭を描く。

主旨と章構成は `docs/Ai-native-software-outline.md` を正本とする。執筆運用は
スキル `building-ai-native-software-series`(`.agents/skills/`)に従う。

## ファイル構成

```
articles/ai-native-ways/software/
├── README.md           ── このファイル
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
- 親シリーズの章リスト本体にこのサブシリーズの章は**含まれない**。
- サブシリーズ目次 (`/ai-native-ways/software/`) は親シリーズ目次への
  「← 目次へ戻る」リンクを冒頭に持つ。

## 章一覧(計画)

| # | slug | 日本語タイトル(working) |
|---|---|---|
| 01 | `coder-top` | AIがコードを書く能力で人間トップクラスに到達した |
| 02 | `maintenance-shift` | 保守フェーズの構造変化こそ本質 |
| 03 | `coder-end` | コーダーの仕事はなくなる |
| 04 | `builder` | ビルダーという役割 |
| 05 | `customer-codev` | 顧客がAIと協働して開発する時代 |
| 06 | `sier-uneconomic` | SIer委託モデルの構造的不経済 |
| 07 | `price-gap` | 価格競争力の桁違いの差 |
| 08 | `lockin` | ロックイン問題 |
| 09 | `hiring-builders` | 各社がビルダーを雇用する時代 |
| 10 | `japan-transition` | 日本のSIer業界の転換と雇用流動性 |
| 11 | `five-years` | 数年で完了する構造転換 |

slug は仮。第 1 章で確定したら以降は変更しない(URL の安定性のため)。
