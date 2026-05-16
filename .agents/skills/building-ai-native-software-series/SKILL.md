---
name: building-ai-native-software-series
description: Drives the "ソフトウェア開発編" sub-series of "AIネイティブな仕事の作法" — eleven chapters that argue the SIer-commissioned development model is structurally obsolete and will be replaced within several years by builder-led, AI-native development. Use when adding any chapter in this sub-series, when reconciling the chapter outline against `docs/Ai-native-software-outline.md`, or when verifying that the sub-series stays internally consistent. Pair with authoring-aiways-chapter (mechanical scaffold) and writing-aiways-voice (prose conventions).
---

# Building the "ソフトウェア開発編" sub-series

This sub-series sits inside `articles/ai-native-ways/` and follows the existing chapters 00–12. It is not a separate series — it shares the template, frontmatter schema, and `/ai-native-ways/` URL space. What makes it a coherent sub-series is its **thesis arc**, not its directory.

The canonical outline is `docs/Ai-native-software-outline.md`. If this skill drifts from that file, the file wins.

## Thesis arc

The eleven chapters trace one argument, in order:

1. AI has reached top-human level at writing code — accessible for a few thousand yen per month.
2. The bigger shift is in **maintenance**: legacy decoding cost collapses, the unit of maintenance moves from code to design/specification.
3. The "coder" role — whose work centers on writing code itself — disappears.
4. A new role emerges: the **builder**, who decides what to make, has AI make it, evaluates outputs, and integrates structure. Demonstrated by aiseed.dev (one person, 30,000 lines + 40 pages in 24 hours).
5. Customers themselves co-develop with AI; they hand off only the parts they cannot solve.
6. The SIer-commissioned model becomes structurally uneconomic — the overhead of outsourcing itself exceeds the AI-native build cost.
7. The price gap is one to two orders of magnitude. This is market displacement, not competition.
8. Lock-in is the SIer model's true product — proprietary frameworks, abstraction layers, human dependency. Palantir's FDE model is examined as the archetype.
9. Companies will hire builders directly, as a professional class (compare lawyers, physicians).
10. Japan's multi-tier subcontracting structure paradoxically enables the transition — primes can detach subcontractor agreements without firing anyone.
11. The transition completes within roughly five years and is irreversible.

Two themes are **explicitly out of scope** (per the outline's footer):

- Hardware-domain outsourcing patterns (EMS vs SIer)
- Generalization to knowledge work beyond software

Do not let these slip back in. If they come up, note them and stop.

## Chapter-to-folder mapping

The existing series ends at `12-one-plus-ai`. This sub-series uses chapter numbers **13 through 23**, continuing the same zero-padded sequence so the build sort order is correct.

| # | folder | working title (JA) | working slug | hinge claim |
|---|---|---|---|---|
| 13 | `13-coder-top` | AIがコードを書く能力で人間トップクラスに到達した | `coder-top` | Codeforces 2700; price floor |
| 14 | `14-maintenance-shift` | 保守フェーズの構造変化こそ本質 | `maintenance-shift` | maintenance unit moves to design/spec |
| 15 | `15-coder-end` | コーダーの仕事はなくなる | `coder-end` | execution vs judgment split |
| 16 | `16-builder` | ビルダーという役割 | `builder` | aiseed.dev 24h demonstration |
| 17 | `17-customer-codev` | 顧客がAIと協働して開発する時代 | `customer-codev` | 9-tenths self-build |
| 18 | `18-sier-uneconomic` | SIer委託モデルの構造的不経済 | `sier-uneconomic` | outsourcing overhead exceeds build cost |
| 19 | `19-price-gap` | 価格競争力の桁違いの差 | `price-gap` | 10–100× displacement |
| 20 | `20-lockin` | ロックイン問題 | `lockin` | Palantir FDE as archetype |
| 21 | `21-hiring-builders` | 各社がビルダーを雇用する時代 | `hiring-builders` | builders as a professional class |
| 22 | `22-japan-transition` | 日本のSIer業界の転換と雇用流動性 | `japan-transition` | multi-tier subcontracting enables shift |
| 23 | `23-five-years` | 数年で完了する構造転換 | `five-years` | irreversible, ~5 year horizon |

Slugs are **suggestions** — finalize them on the first chapter, then keep the rest consistent. Once a slug ships, do not rename it (it becomes a stable URL).

## Setup before drafting chapter 13

1. Update chapter 12's frontmatter (`articles/ai-native-ways/12-one-plus-ai/{ja,en}.md`) so `next_slug` / `next_title` point at chapter 13. Currently chapter 12 is the series' tail and has empty `next_*`.
2. Decide the publication-date cadence. Existing chapters use `2026.05.0X`. Continue from where chapter 12 ends; a one-week stride keeps the series-index ordering readable.
3. Reserve URLs. Each chapter exposes `/ai-native-ways/{slug}/` and `/en/ai-native-ways/{slug}/`. Run the full build (`python3 tools/build_article.py --all`) after chapter 13 to verify the series TOC picks it up.

## Drafting workflow per chapter

For each chapter:

1. Re-read the outline entry for that chapter in `docs/Ai-native-software-outline.md`. Use its bullets as the section spine, not as the prose. The chapter expands each bullet into a declarative h2 + body, in the voice defined by `writing-aiways-voice`.
2. Decide the **hinge claim** for the chapter (the one sentence that goes in bold near the top). The table above has a starting point.
3. Identify the **legacy/AI-native axis** for the chapter (the two-language framing the voice skill expects). Examples:
   - 13: 競技プロのレーティング vs ライセンス保有者の単価
   - 15: 実行能力 vs 判断能力
   - 18: 外注プロセスの工数 vs AIネイティブ開発の工数
   - 20: 独自抽象層 vs 標準コード
4. Draft `ja.md`, then `en.md`. Keep section count and order parallel across languages; adapt accent concepts per `writing-aiways-voice`.
5. Add at least one `> blockquote` per chapter that compresses the hinge claim.
6. Add a Mermaid `flowchart` only where it earns its place — the structural-change argument lends itself to diagrams in 14, 16, 20, 22. Other chapters may go without.
7. Update prev/next links on the neighboring chapters (both languages).
8. Build the single chapter, view the output, then run `--all` to refresh indices.

## Cross-chapter consistency rules

These keep the sub-series internally coherent.

- **One vocabulary for the roles**: コーダー / ビルダー / SIer / 顧客 / 元請け / 下請け. Do not introduce synonyms ("エンジニア" stays absent when "コーダー" is meant; "発注者" stays absent when "顧客" is meant).
- **Palantir FDE** is introduced in chapter 20 only. Earlier chapters may name Palantir but should not unpack the FDE mechanic until 20.
- **The "24 hours, 30,000 lines, 40 pages" demonstration** belongs to chapter 16. Earlier chapters may allude to "one person at speed"; later chapters may reference it briefly. Do not redescribe it in every chapter.
- **Numbers**: when chapter 19 cites the 10–100× price gap, that is the only place a numeric range is asserted as the thesis. Other chapters can cite component prices (monthly subscriptions, project quotes) but must defer the ratio claim to 19.
- **The five-year horizon** belongs to chapter 23. Chapters 14–22 can speak of "数年で" only loosely; the explicit five-year claim is reserved for 23.

## Evidence (`example-N/`) ideas

The sub-series is argument-heavy. Treat evidence folders as load-bearing where possible:

- **13**: a Codeforces rating snapshot, a single Claude-generated solution to a 2400+ rated problem with timings.
- **14**: a before/after of a legacy code-reading task — minutes to comprehend with vs without an AI assistant.
- **16**: pointers to actual aiseed.dev commits in this repository that show the 24-hour build (with a `Makefile` that rebuilds the same artifacts from sources).
- **19**: a side-by-side quote table — three real SIer quotes vs an AI-native cost stack (subscription + builder day-rate × N days). Anonymize as needed.
- **20**: a checklist that classifies a real codebase as "AI-native portable" vs "FDE-locked" with concrete file-level evidence.

Numbers belong in `results.md` inside each example folder, not in the chapter body. The chapter body cites the number and links to the folder.

## Audience and scope reminders

- Readers know what Codeforces, JIRA, SAP, Salesforce, and an SIer are. Define a term only when the **definition itself** is the move (e.g. the precise definition of "コーダー" in chapter 15).
- The sub-series is **not** a programming tutorial. No code listings except where a few lines make a structural point.
- The sub-series is **not** a career-advice column. Avoid second-person address ("あなたは…"); state the structural fact and let the implication land.

## What to do if the outline must change

Edit `docs/Ai-native-software-outline.md` first, then update this skill's chapter table to match. The outline is the source of truth; this skill summarizes and operationalizes it.

## Pointers

- Outline: `docs/Ai-native-software-outline.md`
- Series spec: `articles/ai-native-ways/README.md`
- Mechanical scaffold for a chapter: skill `authoring-aiways-chapter`
- Prose conventions: skill `writing-aiways-voice`
- Build entry point: `tools/build_article.py::build_aiways_chapter` (line 462)
- Chapter 12 frontmatter (must be updated when 13 lands): `articles/ai-native-ways/12-one-plus-ai/{ja,en}.md`
