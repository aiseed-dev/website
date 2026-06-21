---
name: building-ai-native-software-series
description: Drives the "ソフトウェア開発編" sub-series of "AIネイティブな仕事の作法" — nineteen chapters in three 編 (parts) that argue the SIer-commissioned development model is structurally obsolete and will be replaced within several years by builder-led, AI-native development. The sub-series lives in `articles/ai-native-ways/software/` and renumbers from chapter 1. Use when adding any chapter in this sub-series, or when verifying that the sub-series stays internally consistent. Pair with authoring-aiways-chapter (mechanical scaffold) and writing-aiways-voice (prose conventions).
---

# Building the "ソフトウェア開発編" sub-series

This sub-series sits **inside** `articles/ai-native-ways/` but lives in its own subdirectory `software/` with its own chapter numbering (01–19) and its own series-index page. It shares the chapter template, frontmatter schema, voice, and accent palette with the parent series — what makes it a sub-series is the dedicated folder, the dedicated index page, and the **thesis arc** carried across its nineteen chapters.

This SKILL.md is the source of truth for the sub-series structure (the once-aspirational `docs/Ai-native-software-outline.md` was never created). Keep this file current when the structure changes.

## Three 編 (parts)

The sub-series is presented in **three 編 (parts)** on its index page. The index page (`build_aiways_subseries_index`) groups chapters under part headings, driven by the `parts` list in `AIWAYS_SUBSERIES["software"]` in `tools/build_article.py` (each entry groups chapters whose number is `<= upto`):

| 編 | chapters | what it does |
|---|---|---|
| **概念編 ── なぜ作るのか** | 01–05 | Why the builder/AI-native shift happens at all (the conceptual case). |
| **導入編 ── 汎用は OSS で立てる** | 06–13 | A hands-on build guide: replace Microsoft 365 + vendor products with OSS, one tool at a time. "書くのではなく、立てる." Demonstrates the thesis "the effect of OSS is greater than the effect of AI." |
| **転換編 ── 産業構造の帰結** | 14–19 | The structural consequence: why the SIer-commissioned model is now obsolete. |

The 概念編 (01–05) and 転換編 (14–19) carry the **thesis arc** below. The 導入編 (06–13) is a practical, install-guide register (compose files, DNS, migration commands) — still in the structural-assertive voice, but concrete; each chapter stands up one OSS stack on top of the previous (data → auth → documents → … → AI). It exists to make the abstract claim ("you can build it yourself") materially true.

## Relationship to the parent series

- The parent `/ai-native-ways/` index page links to this sub-series **prominently at the top** (a hero card), and does **not** include this sub-series' chapters in its flat chapter list.
- This sub-series has its own index at `/ai-native-ways/software/` (and `/en/ai-native-ways/software/`).
- Chapter URLs use the form `/ai-native-ways/software/{slug}/`.
- Chapter labels combine as `ソフトウェア開発編 第N章` / `AI-Native Ways of Working — Software · Chapter N` in the breadcrumb (`series` + `chapter_label`). The `chapter_label` itself stays short (`第N章` / `Chapter N`); the sub-series name lives in the `series` field, so the breadcrumb does not repeat the sub-series name twice.
- `prev_slug` / `next_slug` chain **inside** the sub-series only, across all 19 chapters in number order: chapter 01's `prev_*` is empty, chapter 19's `next_*` is empty. The 導入編 sits in the chain between 概念編 and 転換編 (…05 → 06 → … → 13 → 14 → …). The chain does not cross into the parent series.

## Thesis arc

The thesis arc is carried by the 概念編 (steps 1–5, chapters 01–05) and the 転換編 (steps 6–11, chapters 14–19). The 導入編 (06–13) sits between them as the hands-on proof that step 5's "build it yourself" is materially true.

1. (Ch 01) AI has reached top-human level at writing code — accessible for a few thousand yen per month.
2. (Ch 02) The bigger shift is in **maintenance**: legacy decoding cost collapses, the unit of maintenance moves from code to design/specification.
3. (Ch 03) The "coder" role — whose work centers on writing code itself — disappears.
4. (Ch 04) A new role emerges: the **builder**, who decides what to make, has AI make it, evaluates outputs, and integrates structure. Demonstrated by aiseed.dev (one person, 30,000 lines + 40 pages in 24 hours).
5. (Ch 05) Customers themselves co-develop with AI; they hand off only the parts they cannot solve.
   — *導入編 06–13: the customer actually stands up the OSS stack (data → auth → documents → code → mail → meetings → web → AI).*
6. (Ch 14) The SIer-commissioned model becomes structurally uneconomic — the overhead of outsourcing itself exceeds the AI-native build cost.
7. (Ch 15) The price gap is one to two orders of magnitude. This is market displacement, not competition.
8. (Ch 16) Lock-in is the SIer model's true product — proprietary frameworks, abstraction layers, human dependency. Palantir's FDE model is examined as the archetype.
9. (Ch 17) Companies will hire builders directly, as a professional class (compare lawyers, physicians).
10. (Ch 18) Japan's multi-tier subcontracting structure paradoxically enables the transition — primes can detach subcontractor agreements without firing anyone.
11. (Ch 19) The transition completes within roughly five years and is irreversible.

Two themes are **explicitly out of scope** (per the outline's footer):

- Hardware-domain outsourcing patterns (EMS vs SIer)
- Generalization to knowledge work beyond software

Do not let these slip back in. If they come up, note them and stop.

## Chapter-to-folder mapping

The sub-series numbers its own chapters from **01 through 19**, independently of the parent series, in three 編. Folders live under `articles/ai-native-ways/software/`. All slugs below have **shipped** — they are stable URLs at `/ai-native-ways/software/{slug}/` and must not be renamed.

**概念編 ── なぜ作るのか (01–05)**

| # | folder | title (JA) | slug | hinge claim |
|---|---|---|---|---|
| 01 | `software/01-coder-top` | AIがコードを書く能力で人間トップクラスに到達した | `coder-top` | Codeforces 2700; price floor |
| 02 | `software/02-maintenance-shift` | 保守フェーズの構造変化こそ本質 | `maintenance-shift` | maintenance unit moves to design/spec |
| 03 | `software/03-coder-end` | コーダーの仕事はなくなる | `coder-end` | execution vs judgment split |
| 04 | `software/04-builder` | ビルダーという役割 | `builder` | aiseed.dev 24h demonstration |
| 05 | `software/05-customer-codev` | 顧客がAIと協働して開発する時代 | `customer-codev` | 9-tenths self-build |

**導入編 ── 汎用は OSS で立てる (06–13)** — install-guide register; each chapter stands up one OSS stack on the previous.

| # | folder | title (JA) | slug | stands up (replaces) |
|---|---|---|---|---|
| 06 | `software/06-foundation` | 土台を据える ── PostgreSQL・SQLite・pgvector・DuckDB・Polars | `foundation` | data layer (Azure SQL / Excel / Power BI) |
| 07 | `software/07-auth` | 門番を立てる ── PocketBase で認証を一つに | `auth` | authentication (Entra ID) |
| 08 | `software/08-documents` | 文書を取り戻す ── OnlyOffice Docs を PocketBase に組み込む | `documents` | Word/Excel/PPT, OneDrive/SharePoint — **OnlyOffice Docs (editor engine) embedded in the Ch.7 PocketBase. NOT Nextcloud (heavy legacy), NOT DocSpace (re-introduces AD/LDAP/SAML + 20-conn cap). Docs 9.4 CE lifted the 20-connection limit.** |
| 09 | `software/09-code` | コードを手元に ── Forgejo と Zed | `code` | GitHub / Azure DevOps |
| 10 | `software/10-mail` | メールを自分の側に ── Stalwart と Thunderbird | `mail` | Exchange / Outlook |
| 11 | `software/11-meetings` | 会議と予約を自分の側に ── Jitsi と Cal.com | `meetings` | Teams/Zoom, Calendly/Bookings, BigBlueButton for classes |
| 12 | `software/12-web` | 社外に見せる窓 ── 静的サイトと Cloudflare Pages | `web` | public web on Cloudflare Pages (no server); build→verify→deploy kept as separate steps. The Caddy reverse proxy is a Ch.7 *internal-apps* concern, not the public site |
| 13 | `software/13-ai` | 自前の AI を据える ── LLM と RAG | `ai` | Copilot; Ollama/vLLM + RAG on pgvector; closes 導入編 |

**転換編 ── 産業構造の帰結 (14–19)**

| # | folder | title (JA) | slug | hinge claim |
|---|---|---|---|---|
| 14 | `software/14-sier-uneconomic` | SIer委託モデルの構造的不経済 | `sier-uneconomic` | outsourcing overhead exceeds build cost |
| 15 | `software/15-price-gap` | 価格競争力の桁違いの差 | `price-gap` | 10–100× displacement |
| 16 | `software/16-lockin` | ロックイン問題 | `lockin` | Palantir FDE as archetype |
| 17 | `software/17-hiring-builders` | 各社がビルダーを雇用する時代 | `hiring-builders` | builders as a professional class |
| 18 | `software/18-japan-transition` | 日本のSIer業界の転換と雇用流動性 | `japan-transition` | multi-tier subcontracting enables shift |
| 19 | `software/19-five-years` | 数年で完了する構造転換 | `five-years` | irreversible, ~5 year horizon |

When cross-referencing chapters in body text, use the **current numbers above** (転換編 is 14–19, not 6–11). Bare `第N章` / `Chapter N` refer to sibling sub-series chapters; parent-series references must be prefixed `親シリーズ第N章` / `parent series Chapter N`.

## Build & verify (already in place)

The build supports the sub-series end to end: `collect_aiways_chapters(lang, "software")` scopes chapters, `build_aiways_chapter` emits `/ai-native-ways/software/{slug}/`, `build_aiways_subseries_index` emits the 3-編 index (grouped via the `parts` config in `AIWAYS_SUBSERIES["software"]`, by `_render_aiways_chapter_list`), and the parent `/ai-native-ways/` index shows a hero card and excludes sub-series chapters from its flat list. Dates run `2026.05.0X` (parent) → `2026.06.01`+ (this sub-series).

Per chapter: keep `date` monotonic within the sub-series (the index sorts by folder number, but monotonic dates keep the displayed dates clean), then run `python3 tools/build_article.py --all` and confirm the chapter, the 3-編 grouping, and the prev/next chain.

## Drafting workflow per chapter

For each chapter:

1. Re-read the chapter's row in the mapping table above (hinge claim / what it stands up). Expand it into declarative h2 + body, in the voice defined by `writing-aiways-voice`. For 導入編 chapters the register is concrete (compose files, DNS, migration commands) but still structural-assertive.
2. Decide the **hinge claim** for the chapter (the one sentence that goes in bold near the top). The table above has a starting point.
3. Identify the **legacy/AI-native axis** for the chapter (the two-language framing the voice skill expects). Examples:
   - 01: 競技プロのレーティング vs ライセンス保有者の単価
   - 03: 実行能力 vs 判断能力
   - 06: 外注プロセスの工数 vs AIネイティブ開発の工数
   - 08: 独自抽象層 vs 標準コード
4. Draft `ja.md`, then `en.md`. Keep section count and order parallel across languages; adapt accent concepts per `writing-aiways-voice`.
5. Add at least one `> blockquote` per chapter that compresses the hinge claim.
6. Add a Mermaid `flowchart` only where it earns its place — the structural-change argument lends itself to diagrams in 02, 04, and the 転換編 (e.g. 14, 16, 18). 導入編 chapters can use one to show how a stack sits on the previous. Other chapters may go without.
7. Update prev/next links on the neighboring chapters **within the sub-series only** (both languages). Chapter 01 keeps empty `prev_*`; chapter 19 keeps empty `next_*`.
8. Build the single chapter, view the output, then run `--all` to refresh the sub-series index and the parent hero card.

## Cross-chapter consistency rules

These keep the sub-series internally coherent.

- **The IT-revolution-completing frame** (introduced in Chapter 1, section "ここで、IT 革命は成就する" / "This is where the IT revolution actually completes"): what was called the "IT revolution" was incomplete because **software itself was still produced by hand-labor** — the revolution's core (mechanization) had not reached the revolution's own tool. AI taking execution closes that loop. Later chapters can refer back to this frame ("IT 革命の成就" / "the IT revolution finally completing") in one or two lines as the over-arching historical lens for the structural transition the sub-series describes. Do not re-explain the frame in every chapter; cite Ch 1 and move on.
- **One vocabulary for the roles**: コーダー / ビルダー / SIer / 顧客 / 元請け / 下請け. Do not introduce synonyms ("エンジニア" stays absent when "コーダー" is meant; "発注者" stays absent when "顧客" is meant).
- **Why multi-tier subcontracting existed** (introduced briefly in Ch 17, deep-dived in Ch 18): the SIer industry's multi-tier subcontracting structure existed primarily because **writing code required a large workforce that no single company could keep in-house at the scale needed**. Frame it as a head-count / person-month sourcing structure, not just "outsourcing because IT was a technical specialty." When AI takes execution, the demand for large coder head-count disappears — and the multi-tier structure loses its reason for being.
- **The scarcity inversion — software → physical things** (introduced in Ch 18): the SIer-industry shrinkage sits inside a macro context where labor demand rises elsewhere — driven by three parallel forces on the same time scale: (i) **physical-infrastructure demand from the AI boom itself** (data centers, GPUs, power, cooling — the visible bottleneck of "AI cheap to run, hard to build infrastructure for"), (ii) **manufacturing reshoring** triggered by geopolitical / energy-cost disruption, (iii) **forced shift to natural farming** as chemical-fertilizer supply chains break down (raises agricultural labor demand). Cite this frame as "the era's scarce resource flips from software to physical things" when relevant. The sub-series should never read as a unilateral employment-crisis narrative — the displaced labor is absorbed by demand on the other side.
- **Palantir FDE** is a recurring theme — name it freely from early chapters when it is the natural concrete example (the upper bound of the legacy access path in Ch 1, the boutique-high-end of SIer commission in Ch 14, the extreme of the price gap in Ch 15). Chapter 16 remains the canonical deep dive: independent Ontology, customer-embedded engineers, long-term contracts, and why the lock-in resists AI-native displacement. Earlier mentions should cite FDE in one or two sentences and defer mechanics to Ch 16 ("第 16 章で詳述" / "covered in detail in Chapter 16").
- **The "24 hours, 30,000 lines, 40 pages" demonstration** belongs to chapter 04. Earlier chapters may allude to "one person at speed"; later chapters may reference it briefly. Do not redescribe it in every chapter.
- **Numbers**: when chapter 15 cites the 10–100× price gap, that is the only place a numeric range is asserted as the thesis. Other chapters can cite component prices (monthly subscriptions, project quotes) but must defer the ratio claim to 15.
- **The five-year horizon** belongs to chapter 19. Earlier chapters can speak of "数年で" only loosely; the explicit five-year claim is reserved for 19.
- **導入編 tool choices are fixed** (shipped): data PostgreSQL/SQLite/pgvector/DuckDB/Polars · auth PocketBase · documents OnlyOffice Docs embedded in PocketBase (no Nextcloud — it is a heavy legacy monolith) · code Forgejo+Zed · mail Stalwart · meetings Jitsi/Cal.com/BigBlueButton · web **public site = static → Cloudflare Pages (no server); build→verify→deploy separated, no auto-rebuild. Caddy is only the Ch.7 internal-apps reverse proxy** · AI Ollama/vLLM+RAG. Recurring framing: "書くのではなく立てる," "人は Excel(OnlyOffice)・機械は Polars/DuckDB," and "control yours, capability borrowed / 窓は借り金庫は自分に" (mail relay / Cloudflare Pages / frontier-model API).

## Evidence (`example-N/`) ideas

The sub-series is argument-heavy. Treat evidence folders as load-bearing where possible:

- **01**: a Codeforces rating snapshot, a single Claude-generated solution to a 2400+ rated problem with timings.
- **02**: a before/after of a legacy code-reading task — minutes to comprehend with vs without an AI assistant.
- **04**: pointers to actual aiseed.dev commits in this repository that show the 24-hour build (with a `Makefile` that rebuilds the same artifacts from sources).
- **15**: a side-by-side quote table — three real SIer quotes vs an AI-native cost stack (subscription + builder day-rate × N days). Anonymize as needed.
- **16**: a checklist that classifies a real codebase as "AI-native portable" vs "FDE-locked" with concrete file-level evidence.

Numbers belong in `results.md` inside each example folder, not in the chapter body. The chapter body cites the number and links to the folder.

## Audience and scope reminders

- Readers know what Codeforces, JIRA, SAP, Salesforce, and an SIer are. Define a term only when the **definition itself** is the move (e.g. the precise definition of "コーダー" in chapter 03).
- The sub-series is **not** a programming tutorial. No code listings except where a few lines make a structural point.
- The sub-series is **not** a career-advice column. Avoid second-person address ("あなたは…"); state the structural fact and let the implication land.

## What to do if the structure must change

This SKILL.md is the source of truth (no separate outline file). To change the structure: update the mapping table and 編 list here, mirror any number-range changes into the `parts` config in `AIWAYS_SUBSERIES["software"]` (`tools/build_article.py`), and — critically — if you renumber, shift every sibling `第N章` / `Chapter N` cross-reference in the affected chapter bodies and related-links (protecting `親シリーズ` / `parent series` and concept refs). Never rename a shipped slug.

## Pointers

- **Reference implementation of the 導入編 stack**: `aiseed-dev/workspace` (kura) — a self-hosted Microsoft 365 / Google Workspace alternative (Python: FastAPI + Flet). PocketBase for auth (pluggable token validation + short cache), **file-native storage with xattr permissions** (`user.ws.perm` / `user.ws.creator`, no permissions DB), OnlyOffice Docs via JWT + callbacks, calendar via `.ics`. Cross-cutting principles: "the AI interface is files," "APIs only at boundaries," "operational AI = local OSS, no external subscription." Ch.8 (documents) and Ch.7 (auth) are aligned to and cross-reference kura. When writing 導入編 chapters, prefer the file-native / xattr model over storing blobs in a DB.
- Parent series spec: `articles/ai-native-ways/README.md`
- Mechanical scaffold for a chapter: skill `authoring-aiways-chapter`
- Prose conventions: skill `writing-aiways-voice`
- Build entry points (all implemented): `tools/build_article.py` — `AIWAYS_SUBSERIES` (config + `parts`), `collect_aiways_chapters(lang, subseries)`, `build_aiways_chapter`, `build_aiways_subseries_index`, `_render_aiways_chapter_list` (3-編 grouping), `build_aiways_index` (parent hero card).
