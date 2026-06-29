# Software — AI-Native Ways of Working

**Subtitle: From software engineering to the liberal arts — the
foundational shift of the technical profession.**

A sub-series of the parent series *AI-Native Ways of Working*
(`../README.md`). Twenty-three chapters across three parts (Introduction,
Independence, Shift — each renumbered from 1) that argue the SIer commission
model is structurally uneconomic, and outline the industry shift that
arrives in the near future and — because the premise has inverted —
does not reverse. Once AI absorbs the core of
software engineering (algorithms, languages, frameworks, design
patterns), the role that remains on the human side — the
judgment-centered builder — rests on a different foundation:
**the liberal arts** (logic, verbalization, ethics, systems thinking,
history). This is the bass line of the sub-series.

The canonical source for structure and authoring is the skill
`building-ai-native-software-series` (`.agents/skills/`) — the once-aspirational
`docs/Ai-native-software-outline.md` was never created.
The full conceptual frame (15 interlocking concepts) lives in the
`framing-second-renaissance` skill. Japanese version of this README:
[`README.md`](README.md).

## Status

**All 23 chapters published** (JA + EN, 46 files in total). Three parts —
Introduction (1-01–1-05), Independence (2-01–2-11), Shift (3-01–3-07).

A short synthesizing entry point (promotional) lives in the blog post
[`articles/blog/021-software-three-transitions/`](../../blog/021-software-three-transitions/),
which compresses the sub-series argument into three pairs of words:
"software engineer → builder", "software engineering → liberal arts",
"employment → free person". The deeper arguments are concentrated in
the final chapter ("The Structural Transition That Won't Reverse", 3-07), in the Second
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

The breadcrumb is rendered as `series · chapter_label`. The sub-series
name lives on the `series` side. Because chapters renumber within each
part, `chapter_label` is **`part-name part-chapter`** (the short part
name + `partDigit-chapterNumber`, e.g. `Independence 2-10`). The
combined display:

- JA: `AIネイティブな仕事の作法 — ソフトウェア開発編 · 自立編 2-10`
- EN: `AI-Native Ways of Working — Software · Independence 2-10`

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

Display numbers are `part-chapter` (each part renumbered from 1); folders use a
global `NN-slug` prefix.

**Introduction — why build, and how to start**

| Ch | folder | slug | English title |
|---|---|---|---|
| 1-01 | `01-coder-top` | `coder-top` | AI Solves the World's Hardest Coding Problems |
| 1-02 | `02-maintenance-shift` | `maintenance-shift` | Maintenance-Phase Shift Is the Real Story |
| 1-03 | `03-coder-end` | `coder-end` | AI Now Does the Software Engineer's Work |
| 1-04 | `04-builder` | `builder` | The Builder Role |
| 1-05 | `05-customer-codev` | `customer-codev` | Customers Co-Develop with AI |

**Independence — break free of M365, Copilot, WordPress, core systems, GitHub**

| Ch | folder | slug | English title |
|---|---|---|---|
| 2-01 | `06-independence` | `independence` | Becoming Independent from Microsoft and Google — The Whole Map |
| 2-02 | `07-foundation` | `foundation` | Lay the Foundation — SQLite, PostgreSQL, pgvector, DuckDB, Polars |
| 2-03 | `08-auth` | `auth` | Stand Up the Gate — One Login with PocketBase |
| 2-04 | `09-code` | `code` | Bring Code In-House — Forgejo and Zed |
| 2-05 | `10-documents` | `documents` | Take Documents Back — OnlyOffice Docs on PocketBase |
| 2-06 | `11-mail` | `mail` | Mail on Your Own Side — Stalwart and Thunderbird |
| 2-07 | `12-meetings` | `meetings` | Meetings and Booking on Your Own Side — Jitsi and Cal.com |
| 2-08 | `13-web` | `web` | Publish the Web — Cloudflare Pages (a WordPress Replacement) |
| 2-09 | `14-fastapi` | `fastapi` | Build an API — Expose Core Logic with FastAPI |
| 2-10 | `15-structure-knowledge` | `structure-knowledge` | Make Your Knowledge Legible — Preparation Is the Main Body, AI the Last Move |
| 2-11 | `16-ai` | `ai` | Stand Up Your Own AI — LLM and RAG |

**Shift — the structural consequence**

| Ch | folder | slug | English title |
|---|---|---|---|
| 3-01 | `17-two-worlds` | `two-worlds` | Companies Don't Write Their Own Code — Office and Core, Two Parallel Worlds |
| 3-02 | `18-sovereignty` | `sovereignty` | Digital Sovereignty — The Microsoft Problem and the Trump Problem |
| 3-03 | `19-sier-uneconomic` | `sier-uneconomic` | The Structural Uneconomy of the SIer Model |
| 3-04 | `20-lockin` | `lockin` | The Lock-In Problem |
| 3-05 | `21-hiring-builders` | `hiring-builders` | Companies Hire Builders |
| 3-06 | `22-japan-transition` | `japan-transition` | Japan's SIer Industry Transition and Labor Mobility |
| 3-07 | `23-five-years` | `five-years` | The Structural Transition That Won't Reverse |

Slugs are finalized — they will not change, for URL stability.
