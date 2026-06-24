# Software — AI-Native Ways of Working

**Subtitle: From software engineering to the liberal arts — the
foundational shift of the technical profession.**

A sub-series of the parent series *AI-Native Ways of Working*
(`../README.md`). Eleven chapters that argue the SIer commission model
is structurally uneconomic, and outline the industry shift that
arrives in the near future and — because the premise has inverted —
does not reverse. Once AI absorbs the core of
software engineering (algorithms, languages, frameworks, design
patterns), the role that remains on the human side — the
judgment-centered builder — rests on a different foundation:
**the liberal arts** (logic, verbalization, ethics, systems thinking,
history). This is the bass line of the sub-series.

The canonical outline is `docs/Ai-native-software-outline.md`. The
authoring playbook lives in the skill
`building-ai-native-software-series` (`.agents/skills/`).
The full conceptual frame (15 interlocking concepts) lives in the
`framing-second-renaissance` skill. Japanese version of this README:
[`README.md`](README.md).

## Status

**All 11 chapters published** (JA + EN, 22 files in total).

A short synthesizing entry point (promotional) lives in the blog post
[`articles/blog/021-software-three-transitions/`](../../blog/021-software-three-transitions/),
which compresses the sub-series argument into three pairs of words:
"software engineer → builder", "software engineering → liberal arts",
"employment → free person". The deeper arguments are concentrated in
Chapter 11 ("The Structural Transition That Won't Reverse"), in the Second
Renaissance section (9-item table + AI revolution as IT revolution's
completion + LLM as statistical-processing tool + app-making resembles
film-making + not only the AI revolution + creation AND upheaval).

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
| 03 | `coder-end` | ソフトウェアエンジニアの仕事を AI がするようになる | AI Now Does the Software Engineer's Work |
| 04 | `builder` | ビルダーという役割 | The Builder Role |
| 05 | `customer-codev` | 顧客がAIと協働して開発する時代 | Customers Co-Develop with AI |
| 06 | `sier-uneconomic` | SIer委託モデルの構造的不経済 | The Structural Uneconomy of the SIer Model |
| 07 | `price-gap` | 価格競争力の桁違いの差 | The Order-of-Magnitude Price Gap |
| 08 | `lockin` | ロックイン問題 | The Lock-In Problem |
| 09 | `hiring-builders` | 各社がビルダーを雇用する時代 | Companies Hire Builders |
| 10 | `japan-transition` | 日本のSIer業界の転換と雇用流動性 | Japan's SIer Industry Transition and Labor Mobility |
| 11 | `five-years` | もう戻らない構造転換 | The Structural Transition That Won't Reverse |

Slugs are finalized — they will not change, for URL stability.
