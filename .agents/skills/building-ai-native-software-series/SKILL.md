---
name: building-ai-native-software-series
description: Drives the series "AI ネイティブなソフトウェア開発" (articles/ai-native-software.adoc, URL /ai-native-software/) — an independent series of three parts (導入編 / 自立編 / 転換編, each numbered from 1) arguing that AI has drawn level with the top human tier at writing code, that the coder's and software engineer's work moves to AI while the deciding builder remains, that a company can stand up its whole toolset off Microsoft and Google with one person plus AI, and that the SIer commission model has become structurally uneconomic. Use when adding or revising any chapter of this series, when checking that a chapter agrees with the others (the map in 2-01, the hand-offs between parts, the three-section block in 自立編), or when deciding what a chapter must contain. Pair with authoring-series-chapter (mechanics) and writing-series-voice (prose).
---

# Building "AI ネイティブなソフトウェア開発"

An **independent series** in one file, `articles/ai-native-software.adoc`, registered in `site.json` with `url_base: /ai-native-software`. It replaced two retired series on 2026-09-21 — 「AIネイティブな仕事の作法」 (12 chapters) and its 「ソフトウェア開発編」 (23 chapters). The useful material from both was migrated in; old URLs 301 to the new ones via `html/_redirects`. Do not refer to either retired series in the text.

The series subtitle: 「SIer に頼まない ── 自分で立てて、自分で動かす」.

## Three parts

| part | name | role |
|---|---|---|
| 1 | 導入編 | Why: what changed and who now builds. Argument chapters. |
| 2 | 自立編 | How: stand up the toolset, one layer at a time. **Each chapter is read as the first spec a reader hands to an AI.** |
| 3 | 転換編 | So what: the structural consequence for the SIer model, employment, and Japan. |

## Chapters (as of 2026-10-02)

| # | slug | title |
|---|---|---|
| 1-01 | `coder-top` | AI は、世界で最も難しいコーディング問題を解く |
| 1-02 | `maintenance-shift` | 保守フェーズの構造変化こそ本質 |
| 1-03 | `coder-end` | ソフトウェアエンジニアの仕事を AI がするようになる |
| 1-04 | `builder` | ビルダーという役割 |
| 1-05 | `customer-codev` | 顧客が AI と協働して開発する時代 |
| 2-01 | `independence` | Microsoft と Google から自立する ── 全体像と対応表 |
| 2-02 | `ai-pc` | AI に PC を一台渡す ── 自立編を動かす機械 |
| 2-03 | `foundation` | 土台を据える ── SQLite・PostgreSQL・pgvector・DuckDB・Polars |
| 2-04 | `python` | 処理を書く ── Python と Flet で、自分の道具を持つ |
| 2-05 | `auth` | 門番を立てる ── PocketBase で認証を一つに |
| 2-06 | `code` | コードを手元に ── Forgejo と Zed |
| 2-07 | `documents` | 文書を取り戻す ── 読む物は adoc、触る表は格子、刷る紙はテンプレート |
| 2-08 | `mail` | メールを自分の側に ── Stalwart と Thunderbird |
| 2-09 | `meetings` | 会議とカレンダーを自分の側に ── Jitsi と CalDAV |
| 2-10 | `web-build` | Web を作る ── HTML と CSS と JavaScript に戻る |
| 2-11 | `web` | Web を公開する ── 自分の一台か、Cloudflare Pages か |
| 2-12 | `fastapi` | API を作る ── FastAPI で基幹のロジックを出す |
| 2-13 | `design` | 図と資料を作る ── Mermaid・Marp・そのほかの道具 |
| 2-14 | `embedded` | 電子工作から IoT まで ── Python で考え、AI に翻訳させる |
| 2-15 | `structure-knowledge` | 社内情報を整える ── 整備こそ本体、AI は最後の一手 |
| 2-16 | `ai` | 自前の AI を据える ── LLM と RAG |
| 2-17 | `ai-delegation` | AI に任せる範囲を決める ── 自律で動かさず、コードに凍結する |
| 3-01 | `two-worlds` | 企業は自分でコードを書かない ── 事務と基幹、二つの世界の並立 |
| 3-02 | `verify-narratives` | 物語を確かめる ── ベンダーの語りを一次情報で検算する |
| 3-03 | `sovereignty` | デジタル主権 ── Microsoft 問題と Trump 問題 |
| 3-04 | `sier-uneconomic` | SIer委託モデルの構造的不経済 |
| 3-05 | `lockin` | ロックイン問題 |
| 3-06 | `hiring-builders` | 各社がビルダーを雇用する時代 |
| 3-07 | `japan-transition` | 日本の SIer 業界の転換と雇用流動性 |
| 3-08 | `revolution-from-below` | AI 革命は下から起きる |
| 3-09 | `five-years` | もう戻らない構造転換 |

Refer to chapters as `{part}-{number}` in prose. The article IDs inside the file (`15-web-build` etc.) are internal and lag the numbers.

## The spine, chapter by chapter

**導入編**

1. **1-01** AI has entered the top competitive-programming tier and can design (attack, design, verification are faces of one power), so it became the strongest SIer — callable for **$20 a month**. The base plan is enough for light use and running; the building period runs on Max (from $100 — breakdown in 2-02). The API is about ten times dearer for the same volume, computed in the text from list prices; do not use it.
2. **1-02** The real shift is in maintenance (40–80 %, average 60 %, of software cost — Glass 2001; ~58 % of developer time goes to comprehension — Xia et al. 2018). The unit of maintenance moves from code to design, spec, and context — held as text in git — and *that* is the first spec you hand to an AI.
3. **1-03** The coder's and the SE's work both move to AI, because writing code and deciding structure are one power, not two tiers. The role of designing-and-coding-yourself moves to the builder. Tools arrive fast once cheap (one million Casio Minis in ten months); the swap itself runs long.
4. **1-04** The builder: decide → build with AI → check → integrate. The SE solves narrowly closed problems; the builder handles open ones. Humans hold judgment because they have a **stake** and can **carry responsibility**. Its foundation is the liberal arts — three abilities sit in the medieval seven arts, four outside them in the modern liberal arts. Anthropic reported that 80 %+ of the code it merged in May 2026 was Claude-written (VentureBeat) — only that figure was verified; do not add the "90 %" or "single digits" claims.
5. **1-05** Customers build: the generic on OSS, the personal on OSS + AI, the organization from the foundation; only the specific gets written with AI. What AI cannot do, the SIer cannot do either. Hands off to 2-01.

**自立編** — 2-01 is the map (correspondence table with Microsoft 365 / Google Workspace, the order of untying, list prices). 2-02 … 2-17 each stand one layer up. 2-01's table and order **must list every 自立編 chapter**; chapters with no suite counterpart (2-14, 2-15, 2-17) are named as outside the table.

**転換編** — two worlds (office and core) and their double tax; verifying vendor narratives against primary sources; digital sovereignty; why the SIer commission is uneconomic; lock-in; companies hiring builders; Japan's SIer transition; the revolution starting from below; why it does not reverse (the Second Renaissance frame — see framing-second-renaissance).

## What every 自立編 chapter must contain

1. **Decisions first.** What to use, what not to use, where it lives, how much you hold yourself, where borrowing begins. This list is what the reader hands to the AI.
2. **Minimal code.** A few lines that show shape. The AI knows the syntax.
3. **The three-section block** just before `== まとめ`: `確かめ方` / `人が持つ物` / `確かめた版と日付` (EN: How to check you are done / What the human holds / Versions checked, and when).
4. **Borrowed vs held, said plainly.** If a chapter uses a hosted service, say it is borrowed and name the self-held route.
5. **Links to its neighbours** where the layers actually connect (auth at 2-05, storage in 2-03, notification through 2-08, the API in 2-12).
6. **FastAPI is the default for anything that moves** (contact forms, intake from IoT devices, core logic). Flet is the default screen (2-04).

## Fixed facts the chapters agree on

- One Debian machine (2-02) is where the AI works and where everything else is stood up; it can also publish the public web (2-11, Caddy). **The one exception is the self-hosted LLM (2-16), which goes on a separate server.** Windows is not discussed at all.
- **No Docker.** Services are installed with apt and run under systemd; anything apt lacks goes in as the project's single published file, registered with systemd. Docker is a tool for distributing, not for building. 2-02 gives the reasons (one update stream; the AI sees config, logs, and data directly; Docker routes published ports ahead of ufw). The single exception: software whose project ships it only as a container runs from the official image — never build an image of your own. No docker compose remains in 自立編 (as of 2026-10-05).
- In the body the AI is called "AI", not "Claude" — the reader may be running another vendor's AI (2-02). Product names appear only as sourced facts (prices, published figures).
- Two AIs from **different vendors** check each other (2-02). Cost: $120/month while building (Claude Max $100 + another vendor's base plan $20), $40 in operation (Pro $20 + $20) — ex-tax, monthly, checked 2026-10-05. Only the builder talks to the AI; a personal plan is not shared (Anthropic Consumer Terms). The group uses the tools the AI built.
- Documents (2-07, rewritten 2026-10-05) split three ways by use: **things you read** are AsciiDoc in the Forgejo repo (2-06), edited in Zed, printed by a build with the design in a template; **tables you work in** stay in a grid (Excel, Euro-Office, LibreOffice, or aiseed office — the series does not depend on aiseed office), with the data outside the grid (2-03); **pages you print** (published statistical tables, forms, slips) pour text values into a template — their `.docx`/`.xlsx` for other people's forms — and page-layout reproduction is not pursued. No document store, no kura, no ONLYOFFICE back-story.
- **Claude Docs** (beta from 2026-09-16) is a place to pass through for drafting and co-editing, not where the finished manuscript lives — structurally it is the same as Microsoft 365 (documents live in claude.ai).
- Meetings are Jitsi (official apt, behind Caddy) and calendars Radicale (CalDAV, apt) in 2-09. **Booking is not an OSS to stand up** — Cal.com's self-hosted edition became Cal.diy, "personal, non-production" — so booking is written in 2-12 as a small FastAPI app (slots and bookings in PostgreSQL, events in Radicale, confirmations via 2-08 mail, Jitsi link). BigBlueButton needs a dedicated Ubuntu machine and appears only as a one-line step-up.
- Web: build in 2-10 (AsciiDoc — Markdown works the same — + HTML/CSS baked by Python with `pyasciidoc` + Jinja2; a single-digit dependency count), publish in 2-11 (own machine with Caddy, or Cloudflare Pages).
- Prices quoted: Claude Pro $20/month for light use, Max from $100/month during the building period (2-02); Microsoft 365 Business ¥1,049–3,298 per seat per month (July 2026 revision, ex-tax, annual); Google Workspace Business Standard ¥1,600 (annual), Gemini included since March 2025.
- The rewrite-cost figure "10 分の 1" was removed from 2-01 and 2-12 (no source); they now say the cost fell by an order of magnitude. **3-06 still carries a different claim** ("初期構築で 10 分の 1 以下" for a corporate site) — not yet reviewed.
- 1-03's soroban figures: Banshu production peaked at 3.6 million in 1960 and is now about 150,000 a year, about 70 % of Japan's output (Ono City). Not 450,000.

## Consistency checks before committing

- The JA/EN parity script and the internal-link check from authoring-series-chapter.
- Search with line breaks removed (prose is hard-wrapped; a phrase can straddle two lines). Then check the file for: `サブシリーズ`, `ソフトウェア開発編`, `親シリーズ`, `sub-series`, `parent series`, `本書`, `序章`, `/ai-native-ways/` — all should be zero.
- `grep` for model names used as tiers (`Opus は`, `Fable / Mythos`).
- If you change a chapter number, grep the other series files (`blog.adoc`, `insights.adoc`, `claude-debian.adoc`, `fable.adoc`, `phosphorus-and-farming.adoc`) for the old `{part}-{number}`.
- If you change what 自立編 contains, update 2-01's table, order list, and summary, and 1-05's list.

## Review status

自立編 (2-01 … 2-17) was reviewed chapter by chapter on 2026-10-02 … 2026-10-06; 転換編 (3-01 … 3-09) is next.


The chapter-by-chapter review with the site owner is tracked in `docs/plan/rensai-minaoshi-hikitsugi.md` — which chapters are done, what was changed, and the rules that came out of it. Read it before touching a chapter.
