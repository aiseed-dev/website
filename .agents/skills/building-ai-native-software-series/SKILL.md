---
name: building-ai-native-software-series
description: Drives the "ソフトウェア開発編" sub-series of "AIネイティブな仕事の作法" — 22 chapters in three 編 (parts, each numbered from 1: 導入編/自立編/転換編) that argue the SIer-commissioned development model is structurally obsolete and will be replaced within several years by builder-led, AI-native development. The sub-series lives in `articles/ai-native-ways/software/` and renumbers from chapter 1. Use when adding any chapter in this sub-series, or when verifying that the sub-series stays internally consistent. Pair with authoring-aiways-chapter (mechanical scaffold) and writing-aiways-voice (prose conventions).
---

# Building the "ソフトウェア開発編" sub-series

This sub-series sits **inside** `articles/ai-native-ways/` but lives in its own subdirectory `software/` (global folders 01–22) and its own series-index page. It is organized into **three 編, each numbered from 1** (導入編 1–5 / 自立編 1–10 / 転換編 1–7). It shares the chapter template, frontmatter schema, voice, and accent palette with the parent series — what makes it a sub-series is the dedicated folder, the dedicated index page, and the **thesis arc**.

This SKILL.md is the source of truth for the sub-series structure (the once-aspirational `docs/Ai-native-software-outline.md` was never created). Keep this file current when the structure changes.

## Three 編 (parts)

The sub-series is presented in **three 編 (parts), each numbered from 1**. The index (`build_aiways_subseries_index`) groups chapters under part headings, driven by the keyed `parts` list in `AIWAYS_SUBSERIES["software"]` (`tools/build_article.py`); each chapter declares its `part` ("1"/"2"/"3") in front matter, and `_render_aiways_chapter_list` inserts a heading when `part` changes.

| 編 (part) | 第n章 / folders | what it does |
|---|---|---|
| **導入編 ── なぜ作り、どう始めるか** (part 1) | 第1–5章 / 01–05 | Concept only (1–5: why the builder/AI-native shift). The worked examples (VBA→Python, website, embedded) live in the **parent series' individual track**, not here. |
| **自立編 ── M365・Copilot・WordPress・基幹・GitHub から自立する** (part 2) | 第1–10章 / 06–15 | Overview/map (1: Microsoft と Google からの自立 — the bundle, the one-to-one mapping, no build steps) + hands-on build guide (2–10): replace the vendor products with OSS, one stack on the previous. "書くのではなく、立てる"; "the effect of OSS > the effect of AI." |
| **転換編 ── 産業構造の帰結** (part 3) | 第1–7章 / 16–22 | The structural consequence: why the SIer-commissioned model is now obsolete. |

The thesis arc is carried by 導入編 1–5 (concept) and the 転換編 (consequence). The worked examples now live in the parent series' individual track; the 自立編 is the install-guide register (compose files, DNS, migration) — structural-assertive but concrete, each stack on the previous.

## Relationship to the parent series

- The parent `/ai-native-ways/` index page links to this sub-series **prominently at the top** (a hero card), and does **not** include this sub-series' chapters in its flat chapter list.
- This sub-series has its own index at `/ai-native-ways/software/` (and `/en/ai-native-ways/software/`).
- Chapter URLs use the form `/ai-native-ways/software/{slug}/`.
- The breadcrumb combines `series` + `chapter_label` → `ソフトウェア開発編 · 導入編 1-01` (compound `部-章` = part digit + `-` + zero-padded chapter). `chapter_label` is built by `_aiways_chapter_label(number, lang, subseries, part_short, part)`, where `part_short` (`導入編`/`自立編`/`転換編`) comes from the chapter's `part` via the `parts` config.
- `prev_slug` / `next_slug` chain **inside** the sub-series only, across all **22** chapters in global folder order: folder 01's `prev_*` is empty, folder 22's `next_*` is empty. The chain runs continuously across the three 編 (…導入編5 `customer-codev` → 自立編1 `independence` → 自立編2 `foundation` → … → 自立編10 `ai` → 転換編1 `two-worlds` → 転換編2 `sier-uneconomic` …). It does not cross into the parent series. Re-run the chain over all folders after adding/moving a chapter.

## Thesis arc

The thesis arc is carried by the 概念編 (steps 1–5, chapters 01–05) and the 転換編 (steps 6–11, chapters 14–19). The 導入編 (06–13) sits between them as the hands-on proof that step 5's "build it yourself" is materially true.

1. (Ch 01) AI has reached top-human level at writing code — accessible for a few thousand yen per month.
2. (Ch 02) The bigger shift is in **maintenance**: legacy decoding cost collapses, the unit of maintenance moves from code to design/specification.
3. (Ch 03) The "coder" AND "software engineer" roles — designing and writing code yourself — disappear; AI does the SE's work (Opus codes, Fable/Mythos design), and the human moves to dialogue with AI (the builder).
4. (Ch 04) A new role emerges: the **builder**, who decides what to make, has AI make it, evaluates outputs, and integrates structure. The SE solves narrowly-closed problems (AI's domain even at high difficulty); the builder handles open problems (no precedent → AI weak). AI has only trained weights / no lived history, so value-judgment and responsibility stay human — judgment is not delegated to AI; choose a trustworthy developer's model.
5. (Ch 05) Customers themselves become builders — but the first move is OSS, not code. Generic → use proven OSS (most economical, also more secure); personal → customize OSS in dialogue with AI (worked examples = parent series individual track); organization → stand up a generic foundation with OSS replacing M365/Copilot/WordPress (the 自立編). Only the company-specific logic is written with AI. What AI cannot do, the SIer cannot do either.
   — *自立編 (folders 06–15): the customer actually stands up the OSS stack (data → auth → documents → code → mail → meetings → web → AI).*
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

The sub-series has **22 chapters in three 編**, each 編 **numbered from 1**. Folders use a global `NN-slug` prefix (01–22) for ordering; the *displayed* number is the per-編 number, set in front matter (`number` = per-編, `part` = "1"/"2"/"3"). Slugs are stable URLs at `/ai-native-ways/software/{slug}/` and must not be renamed. Each chapter's front matter carries `part`; the build groups the index and builds the breadcrumb (`ソフトウェア開発編 ◯○編 1-01`, compound `部-章`) from it.

**導入編 ── なぜ作り、どう始めるか (part "1", 第1–5章 / folders 01–05)** — concept only (1–5). The worked examples (VBA→Python, website, embedded) live in the parent series' individual track (親シリーズ 第2章/第6章/第8章).

| 第n章 | folder | title (JA) | slug | hinge / what it does |
|---|---|---|---|---|
| 1 | `01-coder-top` | AIがコードを書く能力で人間トップクラスに到達した | `coder-top` | Codeforces 2700 → design (cyberattack = design ability) → AI = strongest SIer; price floor |
| 2 | `02-maintenance-shift` | 保守フェーズの構造変化こそ本質 | `maintenance-shift` | AI understands context → code-level maintenance unnecessary; unit → design/spec/context |
| 3 | `03-coder-end` | ソフトウェアエンジニアの仕事を AI がするようになる | `coder-end` | AI does code+design (Opus=coder, Fable/Mythos=SE); humans do the broader system build/operate in dialogue |
| 4 | `04-builder` | ビルダーという役割 | `builder` | SE solves narrowly-closed problems (AI's domain) vs builder handles open problems; AI=weights/no history, human judges value; don't delegate judgment |
| 5 | `05-customer-codev` | 顧客がAIと協働して開発する時代 | `customer-codev` | OSS-first: generic→use OSS (economical + secure); personal→OSS+AI customize (worked examples = parent series individual track); org→OSS foundation replacing M365/Copilot/WordPress (自立編); only the specific written with AI; what AI can't do, the SIer can't either |

**自立編 ── M365・Copilot・WordPress・基幹システム・GitHub から自立する (part "2", 第1–10章 / folders 06–15)** — 第1章 is the overview/map (no build steps); 第2–10章 are the install-guide register, each standing up one OSS stack, replacing a vendor product. The 自立編 replaces **both Microsoft 365 AND Google Workspace** (the stack is an alternative to both suites).

| 第n章 | folder | title (JA) | slug | stands up (replaces) |
|---|---|---|---|---|
| 1 | `06-independence` | Microsoft と Google から自立する ── 全体像と対応表 | `independence` | **overview/map only — NO build steps.** Both suites are bundled; the one-to-one mapping (M365 + Google Workspace → OSS) per layer, link to each build chapter; cost/operations/基幹-seam framing |
| 2 | `07-foundation` | 土台を据える ── SQLite・PostgreSQL・pgvector・DuckDB・Polars | `foundation` | data layer (Azure SQL / Excel / Power BI). **SQLite-first** ("普通は SQLite で十分"); PostgreSQL only when sharing/concurrent |
| 3 | `08-auth` | 門番を立てる ── PocketBase | `auth` | authentication (Entra ID / Google ID) |
| 4 | `09-code` | コードを手元に ── Forgejo と Zed | `code` | **GitHub** / Azure DevOps |
| 5 | `10-documents` | 文書を取り戻す ── OnlyOffice Docs を PocketBase に組み込む | `documents` | **M365** Word/Excel/PPT, OneDrive (Google Docs/Sheets/Slides) — OnlyOffice Docs editor on PocketBase + files/xattr. NOT Nextcloud, NOT DocSpace (re-adds AD). Also carries the "leave Office on your own terms" philosophy (入口・中身・出口/Office を通過させる/処理する人→判断する人) as a why→how preface — folded from the **former parent ch6 「事務処理を変える」**, now removed. Two example-N/ (月次報告書, 差し込み印刷) moved here. |
| 6 | `11-mail` | メールを自分の側に ── Stalwart | `mail` | **M365** Exchange/Outlook (Gmail) |
| 7 | `12-meetings` | 会議と予約を自分の側に ── Jitsi と Cal.com | `meetings` | **M365** Teams/Bookings (Google Meet/Calendar), BigBlueButton for classes |
| 8 | `13-web` | Webを公開する ── Cloudflare Pages（WordPress 代替） | `web` | **WordPress** — publish the parent series Ch6 site; static, no server; build→verify→deploy separated |
| 9 | `14-fastapi` | API を作る ── FastAPI で基幹のロジックを出す | `fastapi` | **基幹システム** logic as one API on the foundation+gate (matches kura). Now the substantive chapter on **replacing a legacy 基幹 system via parallel-run** (並行稼働/業務知識を Markdown に/現場がテスト/委託は止める) — folded from the **former parent ch7 「業務システムと付き合う」**, now removed (SQL/T-SQL migration mechanics defer to 第2章). Two example-N/ (PL/SQL→Python parallel rewrite, Java/C#→Markdown rule extraction) moved here. |
| 10 | `15-ai` | 自前の AI を据える ── LLM と RAG | `ai` | **Copilot** (Gemini); Ollama/vLLM + RAG on pgvector |

**転換編 ── 産業構造の帰結 (part "3", 第1–7章 / folders 16–22)**

| 第n章 | folder | title (JA) | slug | hinge claim |
|---|---|---|---|---|
| 1 | `16-two-worlds` | 企業は自分でコードを書かない ── 事務と基幹、二つの世界の並立 | `two-worlds` | **premise of the 転換編**: in-house dev was inefficient → office bought (Microsoft) + core outsourced (SIer) = two parallel separately-locked worlds + double tax; AI inverts the efficiency → both collapse together |
| 2 | `17-sier-uneconomic` | SIer委託モデルの構造的不経済 | `sier-uneconomic` | outsourcing overhead exceeds build cost |
| 3 | `18-price-gap` | 価格競争力の桁違いの差 | `price-gap` | 10–100× displacement |
| 4 | `19-lockin` | ロックイン問題 | `lockin` | Palantir FDE archetype |
| 5 | `20-hiring-builders` | 各社がビルダーを雇用する時代 | `hiring-builders` | builders as a professional class |
| 6 | `21-japan-transition` | 日本のSIer業界の転換と雇用流動性 | `japan-transition` | multi-tier subcontracting enables shift |
| 7 | `22-five-years` | 数年で完了する構造転換 | `five-years` | irreversible, ~5 year horizon |

When cross-referencing chapters in body text, use the **compound `部-章` form `P-NN`** (P = part digit 1/2/3, NN = zero-padded per-編 chapter): e.g. `1-06`, `2-05`, `3-01`. It is self-locating, so **same-編 and cross-編 refs use the same form, with no 編 name** (this is what removed the old 導入編/自立編 naming drift from references). From OUTSIDE the sub-series (parent series, insights, blog), prefix with the series name: `ソフトウェア開発編 2-05` / `Software 2-05`. Parent-series references stay `親シリーズ第N章` / `parent series Chapter N` (the parent series uses flat `第N章` numbering, NOT `P-NN`); `構造分析`/insights links are untouched. The breadcrumb still shows the 編 name + compound (`導入編 1-06`).

## Build & verify (already in place)

The build supports the sub-series end to end: `collect_aiways_chapters(lang, "software")` scopes chapters, `build_aiways_chapter` emits `/ai-native-ways/software/{slug}/`, `build_aiways_subseries_index` emits the 3-編 index (grouped via the `parts` config in `AIWAYS_SUBSERIES["software"]`, by `_render_aiways_chapter_list`), and the parent `/ai-native-ways/` index shows a hero card and excludes sub-series chapters from its flat list. Dates run `2026.05.0X` (parent) → `2026.06.01`+ (this sub-series).

Per chapter: keep `date` monotonic within the sub-series (the index sorts by folder number, but monotonic dates keep the displayed dates clean), then run `python3 tools/build_article.py --all` and confirm the chapter, the 3-編 grouping, and the prev/next chain.

## Drafting workflow per chapter

For each chapter:

1. Re-read the chapter's row in the mapping table above (hinge claim / what it stands up). Expand it into declarative h2 + body, in the voice defined by `writing-aiways-voice`. For 導入編 chapters the register is concrete (compose files, DNS, migration commands) but still structural-assertive.
2. Decide the **hinge claim** for the chapter (the one sentence that goes in bold near the top). The table above has a starting point.
3. Identify the **legacy/AI-native axis** for the chapter (the two-language framing the voice skill expects). Examples:
   - 01: 競技プロのレーティング vs ライセンス保有者の単価(さらに 設計能力=自律サイバー攻撃 → 最強の SIer)
   - 03: コードを書く役割 vs AIと対話してシステムを作り動かす役割
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
- **自立編 tool choices are fixed** (shipped): data PostgreSQL/SQLite/pgvector/DuckDB/Polars · auth PocketBase · code Forgejo+Zed (replaces GitHub) · documents OnlyOffice Docs embedded in PocketBase (no Nextcloud — heavy legacy monolith) · mail Stalwart · meetings Jitsi/Cal.com/BigBlueButton · web **public site = static → Cloudflare Pages (no server); build→verify→deploy separated, no auto-rebuild. Caddy is only the internal-apps reverse proxy (introduced in 2-03 auth)** · API FastAPI · AI Ollama/vLLM+RAG. Recurring framing: "書くのではなく立てる," "人は Excel(OnlyOffice)・機械は Polars/DuckDB," and "control yours, capability borrowed / 窓は借り金庫は自分に" (mail relay / Cloudflare Pages / frontier-model API).

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

This SKILL.md is the source of truth (no separate outline file). To change the structure: update the mapping table and 編 list here, mirror any number-range changes into the `parts` config in `AIWAYS_SUBSERIES["software"]` (`tools/build_article.py`), and — critically — if you renumber, shift every sibling `P-NN` (`部-章`) cross-reference in the affected chapter bodies and related-links (protecting `親シリーズ` / `parent series` flat refs and `構造分析` concept refs). Never rename a shipped slug.

## Pointers

- **Reference implementation of the 自立編 stack**: `aiseed-dev/workspace` (kura) — a self-hosted Microsoft 365 / Google Workspace alternative (Python: FastAPI + Flet). PocketBase for auth (pluggable token validation + short cache), **file-native storage with xattr permissions** (`user.ws.perm` / `user.ws.creator`, no permissions DB), OnlyOffice Docs via JWT + callbacks, calendar via `.ics`. Cross-cutting principles: "the AI interface is files," "APIs only at boundaries," "operational AI = local OSS, no external subscription." 2-05 (documents) and 2-03 (auth) are aligned to and cross-reference kura; the FastAPI chapter (2-09) names kura directly. When writing 自立編 chapters, prefer the file-native / xattr model over storing blobs in a DB.
- Parent series spec: `articles/ai-native-ways/README.md`
- Mechanical scaffold for a chapter: skill `authoring-aiways-chapter`
- Prose conventions: skill `writing-aiways-voice`
- Build entry points (all implemented): `tools/build_article.py` — `AIWAYS_SUBSERIES` (config + `parts`), `collect_aiways_chapters(lang, subseries)`, `build_aiways_chapter`, `build_aiways_subseries_index`, `_render_aiways_chapter_list` (3-編 grouping), `build_aiways_index` (parent hero card).
