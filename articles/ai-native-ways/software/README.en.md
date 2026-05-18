# Software — AI-Native Ways of Working

A sub-series of the parent series *AI-Native Ways of Working*
(`../README.md`). Eleven chapters that argue the SIer commission model
is structurally uneconomic, and outline the irreversible industry
shift that completes within a few years.

The canonical outline is `docs/Ai-native-software-outline.md`. The
authoring playbook lives in the skill
`building-ai-native-software-series` (`.agents/skills/`).
Japanese version of this README: [`README.md`](README.md).

## Status

**All 11 chapters published** (JA + EN, 22 files in total).

## File layout

```
articles/ai-native-ways/software/
├── README.md           ── This file in Japanese
├── README.en.md        ── This file
└── NN-slug/            ── Chapter folders, renumbered from 01 inside the sub-series
    ├── ja.md
    ├── en.md
    └── example-N/      ── Optional per-chapter evidence folders
```

Uses the parent series' `template.html` / `template.en.html` as-is.
The frontmatter schema is also shared with the parent. EN files
declare `lang: en` explicitly.

## URLs

| Source | Output | URL |
|---|---|---|
| `01-coder-top/ja.md` | `html/ai-native-ways/software/coder-top/index.html` | `/ai-native-ways/software/coder-top/` |
| `01-coder-top/en.md` | `html/en/ai-native-ways/software/coder-top/index.html` | `/en/ai-native-ways/software/coder-top/` |
| (sub-series index, auto-generated) | `html/ai-native-ways/software/index.html` | `/ai-native-ways/software/` |
| (sub-series index, auto-generated) | `html/en/ai-native-ways/software/index.html` | `/en/ai-native-ways/software/` |

## Chapter labels

The breadcrumb is rendered as `series · chapter_label`. The
sub-series name lives on the `series` side, so `chapter_label` stays
short (`第N章` / `Chapter N`). The combined display:

- JA: `AIネイティブな仕事の作法 — ソフトウェア開発編 · 第N章`
- EN: `AI-Native Ways of Working — Software · Chapter N`

## prev / next chain

The chain closes **inside the sub-series**. Chapter 01 keeps empty
`prev_slug` / `prev_title`; the last chapter keeps empty `next_slug` /
`next_title`. The chain does not bridge into the parent series.

## Relationship with the parent series index

- The parent series index (`/ai-native-ways/`) presents this sub-series
  at the top as a prominent hero card.
- The parent series' flat chapter list does **not** include the
  sub-series chapters.
- The sub-series index (`/ai-native-ways/software/`) opens with a
  "← back to parent index" link.

## Chapter list

| # | slug | Japanese title | English title |
|---|---|---|---|
| 01 | `coder-top` | AI は、世界で最も難しいコーディング問題を解く | AI Solves the World's Hardest Coding Problems |
| 02 | `maintenance-shift` | 保守フェーズの構造変化こそ本質 | Maintenance-Phase Shift Is the Real Story |
| 03 | `coder-end` | コーダーの仕事はなくなる | The Coder's Job Goes Away |
| 04 | `builder` | ビルダーという役割 | The Builder Role |
| 05 | `customer-codev` | 顧客がAIと協働して開発する時代 | Customers Co-Develop with AI |
| 06 | `sier-uneconomic` | SIer委託モデルの構造的不経済 | The Structural Uneconomy of the SIer Model |
| 07 | `price-gap` | 価格競争力の桁違いの差 | The Order-of-Magnitude Price Gap |
| 08 | `lockin` | ロックイン問題 | The Lock-In Problem |
| 09 | `hiring-builders` | 各社がビルダーを雇用する時代 | Companies Hire Builders |
| 10 | `japan-transition` | 日本のSIer業界の転換と雇用流動性 | Japan's SIer Industry Transition and Labor Mobility |
| 11 | `five-years` | 数年で完了する構造転換 | The Structural Transition Completes in a Few Years |

Slugs are finalized — they will not change, for URL stability.
