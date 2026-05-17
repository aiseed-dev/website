---
name: building-ai-native-software-series
description: Drives the "ソフトウェア開発編" sub-series of "AIネイティブな仕事の作法" — eleven chapters that argue the SIer-commissioned development model is structurally obsolete and will be replaced within several years by builder-led, AI-native development. The sub-series lives in `articles/ai-native-ways/software/` and renumbers from chapter 1. Use when adding any chapter in this sub-series, when reconciling the chapter outline against `docs/Ai-native-software-outline.md`, or when verifying that the sub-series stays internally consistent. Pair with authoring-aiways-chapter (mechanical scaffold) and writing-aiways-voice (prose conventions).
---

# Building the "ソフトウェア開発編" sub-series

This sub-series sits **inside** `articles/ai-native-ways/` but lives in its own subdirectory `software/` with its own chapter numbering (01–11) and its own series-index page. It shares the chapter template, frontmatter schema, voice, and accent palette with the parent series — what makes it a sub-series is the dedicated folder, the dedicated index page, and the **thesis arc** carried across its eleven chapters.

The canonical outline is `docs/Ai-native-software-outline.md`. If this skill drifts from that file, the file wins.

## Relationship to the parent series

- The parent `/ai-native-ways/` index page links to this sub-series **prominently at the top** (a hero card), and does **not** include this sub-series' chapters in its flat chapter list.
- This sub-series has its own index at `/ai-native-ways/software/` (and `/en/ai-native-ways/software/`).
- Chapter URLs use the form `/ai-native-ways/software/{slug}/`.
- Chapter labels combine as `ソフトウェア開発編 第N章` / `AI-Native Ways of Working — Software · Chapter N` in the breadcrumb (`series` + `chapter_label`). The `chapter_label` itself stays short (`第N章` / `Chapter N`); the sub-series name lives in the `series` field, so the breadcrumb does not repeat the sub-series name twice.
- `prev_slug` / `next_slug` chain **inside** the sub-series only: chapter 01's `prev_*` is empty, chapter 11's `next_*` is empty. The chain does not cross into the parent series.

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

The sub-series numbers its own chapters from **01 through 11**, independently of the parent series. Folders live under `articles/ai-native-ways/software/`.

| # | folder | working title (JA) | working slug | hinge claim |
|---|---|---|---|---|
| 01 | `software/01-coder-top` | AIがコードを書く能力で人間トップクラスに到達した | `coder-top` | Codeforces 2700; price floor |
| 02 | `software/02-maintenance-shift` | 保守フェーズの構造変化こそ本質 | `maintenance-shift` | maintenance unit moves to design/spec |
| 03 | `software/03-coder-end` | コーダーの仕事はなくなる | `coder-end` | execution vs judgment split |
| 04 | `software/04-builder` | ビルダーという役割 | `builder` | aiseed.dev 24h demonstration |
| 05 | `software/05-customer-codev` | 顧客がAIと協働して開発する時代 | `customer-codev` | 9-tenths self-build |
| 06 | `software/06-sier-uneconomic` | SIer委託モデルの構造的不経済 | `sier-uneconomic` | outsourcing overhead exceeds build cost |
| 07 | `software/07-price-gap` | 価格競争力の桁違いの差 | `price-gap` | 10–100× displacement |
| 08 | `software/08-lockin` | ロックイン問題 | `lockin` | Palantir FDE as archetype |
| 09 | `software/09-hiring-builders` | 各社がビルダーを雇用する時代 | `hiring-builders` | builders as a professional class |
| 10 | `software/10-japan-transition` | 日本のSIer業界の転換と雇用流動性 | `japan-transition` | multi-tier subcontracting enables shift |
| 11 | `software/11-five-years` | 数年で完了する構造転換 | `five-years` | irreversible, ~5 year horizon |

Slugs are **suggestions** — finalize them on the first chapter, then keep the rest consistent. Once a slug ships, do not rename it (it becomes a stable URL at `/ai-native-ways/software/{slug}/`).

## Setup before drafting chapter 01

1. Confirm the build tool has been extended to discover `articles/ai-native-ways/software/NN-slug/{ja,en}.md`, to emit `/ai-native-ways/software/{slug}/` URLs, and to build the sub-series index at `/ai-native-ways/software/`. If not yet done, this is Phase 2 work and must precede chapter 01 going live.
2. Confirm the parent index page (`/ai-native-ways/`) renders a prominent hero card linking to `/ai-native-ways/software/` and does **not** include the sub-series chapters in its flat list.
3. Decide the publication-date cadence. The parent series uses `2026.05.0X`; this sub-series can start at `2026.06.01` and increment per chapter. Keep `date` monotonic within the sub-series so the index sort is stable.
4. Reserve URLs. Each chapter exposes `/ai-native-ways/software/{slug}/` and `/en/ai-native-ways/software/{slug}/`. Run the full build (`python3 tools/build_article.py --all`) after each chapter to verify both the sub-series index and the parent hero card pick it up.

## Drafting workflow per chapter

For each chapter:

1. Re-read the outline entry for that chapter in `docs/Ai-native-software-outline.md`. Use its bullets as the section spine, not as the prose. The chapter expands each bullet into a declarative h2 + body, in the voice defined by `writing-aiways-voice`.
2. Decide the **hinge claim** for the chapter (the one sentence that goes in bold near the top). The table above has a starting point.
3. Identify the **legacy/AI-native axis** for the chapter (the two-language framing the voice skill expects). Examples:
   - 01: 競技プロのレーティング vs ライセンス保有者の単価
   - 03: 実行能力 vs 判断能力
   - 06: 外注プロセスの工数 vs AIネイティブ開発の工数
   - 08: 独自抽象層 vs 標準コード
4. Draft `ja.md`, then `en.md`. Keep section count and order parallel across languages; adapt accent concepts per `writing-aiways-voice`.
5. Add at least one `> blockquote` per chapter that compresses the hinge claim.
6. Add a Mermaid `flowchart` only where it earns its place — the structural-change argument lends itself to diagrams in 02, 04, 08, 10. Other chapters may go without.
7. Update prev/next links on the neighboring chapters **within the sub-series only** (both languages). Chapter 01 keeps empty `prev_*`; chapter 11 keeps empty `next_*`.
8. Build the single chapter, view the output, then run `--all` to refresh the sub-series index and the parent hero card.

## Cross-chapter consistency rules

These keep the sub-series internally coherent.

- **The IT-revolution-completing frame** (introduced in Chapter 1, section "ここで、IT 革命は成就する" / "This is where the IT revolution actually completes"): what was called the "IT revolution" was incomplete because **software itself was still produced by hand-labor** — the revolution's core (mechanization) had not reached the revolution's own tool. AI taking execution closes that loop. Later chapters can refer back to this frame ("IT 革命の成就" / "the IT revolution finally completing") in one or two lines as the over-arching historical lens for the structural transition the sub-series describes. Do not re-explain the frame in every chapter; cite Ch 1 and move on.
- **One vocabulary for the roles**: コーダー / ビルダー / SIer / 顧客 / 元請け / 下請け. Do not introduce synonyms ("エンジニア" stays absent when "コーダー" is meant; "発注者" stays absent when "顧客" is meant).
- **Palantir FDE** is a recurring theme — name it freely from early chapters when it is the natural concrete example (the upper bound of the legacy access path in Ch 1, the boutique-high-end of SIer commission in Ch 6, the extreme of the price gap in Ch 7). Chapter 08 remains the canonical deep dive: independent Ontology, customer-embedded engineers, long-term contracts, and why the lock-in resists AI-native displacement. Earlier mentions should cite FDE in one or two sentences and defer mechanics to Ch 8 ("第 8 章で詳述" / "covered in detail in Chapter 8").
- **The "24 hours, 30,000 lines, 40 pages" demonstration** belongs to chapter 04. Earlier chapters may allude to "one person at speed"; later chapters may reference it briefly. Do not redescribe it in every chapter.
- **Numbers**: when chapter 07 cites the 10–100× price gap, that is the only place a numeric range is asserted as the thesis. Other chapters can cite component prices (monthly subscriptions, project quotes) but must defer the ratio claim to 07.
- **The five-year horizon** belongs to chapter 11. Chapters 02–10 can speak of "数年で" only loosely; the explicit five-year claim is reserved for 11.

## Evidence (`example-N/`) ideas

The sub-series is argument-heavy. Treat evidence folders as load-bearing where possible:

- **01**: a Codeforces rating snapshot, a single Claude-generated solution to a 2400+ rated problem with timings.
- **02**: a before/after of a legacy code-reading task — minutes to comprehend with vs without an AI assistant.
- **04**: pointers to actual aiseed.dev commits in this repository that show the 24-hour build (with a `Makefile` that rebuilds the same artifacts from sources).
- **07**: a side-by-side quote table — three real SIer quotes vs an AI-native cost stack (subscription + builder day-rate × N days). Anonymize as needed.
- **08**: a checklist that classifies a real codebase as "AI-native portable" vs "FDE-locked" with concrete file-level evidence.

Numbers belong in `results.md` inside each example folder, not in the chapter body. The chapter body cites the number and links to the folder.

## Audience and scope reminders

- Readers know what Codeforces, JIRA, SAP, Salesforce, and an SIer are. Define a term only when the **definition itself** is the move (e.g. the precise definition of "コーダー" in chapter 15).
- The sub-series is **not** a programming tutorial. No code listings except where a few lines make a structural point.
- The sub-series is **not** a career-advice column. Avoid second-person address ("あなたは…"); state the structural fact and let the implication land.

## What to do if the outline must change

Edit `docs/Ai-native-software-outline.md` first, then update this skill's chapter table to match. The outline is the source of truth; this skill summarizes and operationalizes it.

## Pointers

- Outline: `docs/Ai-native-software-outline.md`
- Parent series spec: `articles/ai-native-ways/README.md`
- Sub-series README (to be created in Phase 2): `articles/ai-native-ways/software/README.md`
- Mechanical scaffold for a chapter: skill `authoring-aiways-chapter`
- Prose conventions: skill `writing-aiways-voice`
- Build entry points (Phase 2 work): `tools/build_article.py::build_aiways_chapter`, `collect_aiways_chapters`, `build_aiways_index` — all need sub-series awareness. A new `build_aiways_subseries_index` should emit `/ai-native-ways/software/{,en/}index.html`.

## Pending Phase 2 work (must precede chapter 01 going live)

1. Extend `collect_aiways_chapters` to scope by sub-series and to skip the `software/` subfolder when listing parent chapters (and vice versa).
2. Update `build_aiways_chapter` output path resolution: detect sub-series from `md_path.parent.parent.name` (or read a frontmatter field) and emit to `html/ai-native-ways/software/{slug}/`.
3. Update `build_aiways_chapter` URL generators (`canonical_url`, `hreflang_*`, prev/next link rendering) to include the `/software/` segment.
4. Extend `_aiways_chapter_label` to take a sub-series argument and return `ソフトウェア開発編 第N章` / `Software · Chapter N` when applicable.
5. Add `build_aiways_subseries_index` (mirrors `build_aiways_index` but limits to the sub-series and writes to the sub-series base path).
6. Update `build_aiways_index` to prepend a hero card linking to the sub-series index, and to exclude sub-series chapters from its flat chapter list.
7. Update `_aiways_chapter_examples_html` (around `tools/build_article.py:488`) to emit `/ai-native-ways/software/{slug}/example-N/` URLs when the chapter is in a sub-series.
8. Update `articles/ai-native-ways/README.md` to document the sub-series convention.
