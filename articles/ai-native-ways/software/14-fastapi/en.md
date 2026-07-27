---
slug: fastapi
number: "09"
part: "2"
lang: en
title: "Build an API — Expose Core Logic with FastAPI"
subtitle: "Rewrite the core system via parallel operation and gather your own logic into one API"
description: "'Don't break it, don't touch it' is old advice. AI has cut the cost of rewriting a core system by 10x. Build the new AI-native system in FastAPI, run it in parallel with the old, compare outputs against reality, and when the diffs vanish, kill the old. Push business knowledge out into Markdown all at once, let the floor write the tests, and stop outsourcing. The new logic reads and writes the 2-02 PostgreSQL and verifies identity with the 2-03 gate's token. The reference implementation is kura."
date: 2026.07.15
label: Independence 9
title_html: Rewrite the core in <span class="accent">parallel</span>,<br>gather your logic into one <span class="accent">API</span>.
prev_slug: web
prev_title: "Publish the Web — Cloudflare Pages (a WordPress Replacement)"
next_slug: structure-knowledge
next_title: "Make Your Knowledge Legible — Preparation Is the Main Body, AI the Last Move"
---

# Build an API — Expose Core Logic with FastAPI

The Independence part's OSS covers the generic — auth, documents, mail,
meetings, the public web. What remains is **your own business logic,** the
substance of the core systems.

That core is usually old. Written in Java or C#, riding on Oracle or SQL Server,
understood in full by no one. This chapter **rewrites it via parallel operation**
and exposes your own logic as one API with **FastAPI** — the method is the
sequence for killing a core system, the tool is FastAPI. In order.

## "Don't break it, don't touch it" was advice for a different era

For the past 20 years, the standard advice given to people responsible for core
systems has been:

"Don't break it." "Don't touch it." "Don't change something that works." "Use the
legacy assets."

This was **advice from an era when the cost of rewriting was prohibitive**. When
rewriting took years and millions of dollars, "don't touch it" was indeed the
right answer.

The era has changed.

AI translates business logic to Python. AI extracts the intent of SQL into
Markdown. AI generates test data. AI mines undocumented rules out of legacy code.
**The cost of rewriting has fallen by a factor of ten.**

Saying "don't touch it" at one-tenth the cost is denying the new reality. **There
is no longer a reason to keep the legacy.**

## The logic of parallel operation

Even with rewriting cost down, the risk is not zero. No method can guarantee that
a new system behaves exactly like the old.

That is what **parallel operation** is for.

Build the new system in AI. Keep the old running. Feed the same input to both.
Compare the outputs.

```mermaid
flowchart LR
  Input["Production input"]
  Old["Old system<br/>Java/C#<br/>Oracle/SQL Server"]
  New["New system<br/>FastAPI + AI<br/>PostgreSQL"]
  Diff{"Compare<br/>every day"}
  Fix["Fix the new system<br/>(don't touch the old)"]
  Kill["Diff stays zero<br/>→ kill the old"]

  Input --> Old --> Diff
  Input --> New --> Diff
  Diff -->|diff present| Fix
  Fix --> New
  Diff -->|zero diff| Kill

  classDef old fill:#fef3e7,stroke:#c89559,color:#5a3f1a
  classDef new fill:#e8f5e9,stroke:#7a9a6d,color:#3a4d34
  classDef decision fill:#f0f0f0,stroke:#666
  class Old old
  class New,Kill new
  class Diff,Fix decision
```

If A and B match, the new system is correct. If they don't, one of them is wrong.
**Usually, a 20-year-old bug in the old system surfaces first** — a bug that was
never in any document.

Continue this for one month, three months. When diffs reach zero and edge cases
are covered, stop the old.

Parallel operation eliminates rewrite risk through **measurement**. Not
desk-checking. Not spec reviews. **Production environment, real data, run and
verify.**

## How long to keep the old running

The parallel-operation period should be at most six months, usually three is
enough.

If you need longer, the new system is not actually correct. Fix the new system.
**Don't run parallel "indefinitely."**

Inside organizations, there is a psychology of "keep the old around just in case."
This is a trap. Keeping it means:

- Operations cost doubles
- Engineers split their attention
- When something breaks, arguments erupt over who is responsible
- New features must be built in both, doubling the work
- The decision to kill the old gets postponed forever

> Parallel operation is a means, not an end. When the new is verified, kill the old.

If you can't kill it, you shouldn't have started rewriting. **When you do it, do it.**

"Use the legacy assets, augment with AI" — this approach ultimately permits the
old system to remain. New features pile up on the outside; the substance stays
old. Three years pass, five years pass, and the organization is still not
AI-native. **Half-hearted coexistence freezes the organization.** "Augment" was
acceptable when rewriting was truly too expensive. That era is over.

## How to kill vendor products

Oracle, SAP, Salesforce, Microsoft business products — these aren't selling
"products." They are selling "**the situation in which you have to keep using the
product**."

Pattern for killing via parallel operation:

1. Export data from the product daily (the product keeps running)
2. The new AI-built system processes the export and runs the same business
3. Compute the same business metrics (sales, inventory, customer state) in both
4. When the numbers match, **don't renew the product contract**
5. Take a final "full data export" from the product and switch entirely to the new

**Time it for the contract renewal cycle.** This is a strategic schedule. Renewal
in October? Start parallel in June. Run for three months. Decide in September.

The vendor will pull every card to keep you: "migration risk," "data integrity,"
"your veterans will leave." Parallel operation with matching outputs answers all
of them. **You have the evidence.** License fees are tens of thousands of dollars
per year. Stopping that recovers the new-system development cost in months.

## Push business knowledge out — all at once

As preparation for parallel operation, push business knowledge into Markdown.
**All at once.**

Old common sense said documenting business knowledge was a months-to-years
project. Someone scribbles in spare hours. Before half is written, that person
transfers. The project collapses partway. **Ultimately, it never gets written.**

The era has changed.

Hand Claude **everything** — old code, comments, SQL, runbooks, past incident
reports. Tell it: "extract the business logic and organize it as Markdown." A
codebase of a few thousand lines: hours for the first draft. Tens of thousands of
lines: days at most.

It does not have to be perfect. **80% is enough.** The remaining 20% will surface
as output diffs during parallel operation. Resolve them one by one, and the
documentation completes itself.

> Compress months of work into days. This is what AI is actually for.

This is also the hidden benefit of parallel operation. **Business rules that were
never written down all surface during parallel run.** Rules that no spec captured,
only operations knew — these get pulled out, both from Claude's first-pass
Markdown and from the diffs the parallel run produces. (Taking documents back onto
your own side was 2-05; the core's business knowledge, too, falls into the
same readable material.)

## Business rules live with the people who do the work — the floor writes the tests

Who does the rewriting?

Old common sense: the IT department, SI vendors, or consultants gather
requirements from the floor, then write code. When done, the floor performs
acceptance testing. This was the shape of an era when the knowledge needed for a
rewrite was distributed. **Coding ability lived in IT; business-rule knowledge
lived on the floor.**

That has changed.

**Coding ability is held by Claude.** What remains is business-rule knowledge. And
the people who know business rules most deeply are the people running that business
every day. The people on the floor have Claude write the code. **That is the whole
loop.** No middle layer of "translation" needed.

What matters in parallel operation is finding output diffs. "Does the new system
produce the same output as the old?" — verifying this requires test data. The
people best suited to creating this test data are the people on the floor.

"July billing closes on the 10th, but we extend by Obon to the 5th of the
following month" — the floor knows this rule. They tell Claude: "make 50 billing
test cases that account for the Obon extension in July." Claude makes them. They
are run through the old system to capture expected outputs. This becomes the test
data.

Rules that were never in any spec materialize as tests. **Business knowledge flows
from the floor → tests → code.** This is a kind of test the IT department, by
itself, cannot write. They do not know the rules. **Rewrites have failed because
people who didn't know the rules wrote the tests.**

## Stop outsourcing

Once you reach this point, the conclusion is clear.

**You do not need to outsource core-system rewrites to IT vendors or consultants.**

The traditional rationale for outsourcing was twofold: (1) coding ability lived
only on the outside; (2) business knowledge had to be transferred to the outside.
(1) was solved by Claude. (2) is no longer needed in the first place. **The floor +
Claude completes the loop.**

Outsourcing fees are the single largest cost item in core-system rewrites. Tens of
millions to hundreds of millions of yen per year. That cost disappears. People on
the floor — who know the rules — have Claude write the code, Claude write the
tests, and verify by parallel operation. **Rewriting changes from "something to
outsource" to "something done in-house."**

This is not a contraction of the IT department's role. IT focuses on supporting the
(floor + Claude) teams: infrastructure, databases, deploy environments, security.
**They escape the duplicative role of "business-logic intermediary."**

> The people who know the business use Claude to rewrite their own systems. That is the new floor practice.

## Migrate the DB and the logic layer in parallel

The same parallel-run approach used to rewrite the logic layer into FastAPI
applies to the DB.

Keep the database. **But drop the vendor dialect.** `SELECT`, `JOIN`, `GROUP BY`,
window functions — standard SQL has run for 50 years and will run for 50 more.
Claude writes it perfectly. **Keep standard SQL, drop the vendor dialect** — that
line is the crux.

But Oracle's **PL/SQL** and Microsoft SQL Server's **T-SQL** — drop them. They are
**vendor-specific dialects**. Embedding business logic inside the database has been
the last bastion of vendor lock-in. Business logic embedded in PL/SQL stored
procedures gets rewritten in Python. Hand Claude the PL/SQL; it extracts the
business rules and outputs Python. **Business logic returns from invisible stored
procedures into code.** Readable. Version-controlled. Testable.

The DB itself moves to PostgreSQL. This too is parallel operation — sync data
daily from the old DB into PostgreSQL; the new system (FastAPI) reads/writes
PostgreSQL while the old reads/writes Oracle / SQL Server. Verify consistency via
output comparison, and when stable, stop the old DB.

> Drop Oracle / SQL Server. That is your graduation certificate from vendor lock-in.

The DDL dialect translation and the concrete migration steps using Azure SQL and
pgloader were covered in detail in **2-02**. Here you only need to hold the
judgment: "keep standard SQL, pull out the dialect and the logic." Rewriting just
the logic layer is only half-escaping the lock-in. **Migrating to PostgreSQL is the
final step out.** And the annual license cost recovers the new-system development
cost in a few months. Financially, there is no reason left not to rewrite.

## The way out of every lock-in is the same

Everything described above has the same structure.

- Replace the Java / C# logic layer with FastAPI (Python)
- Replace Oracle / SQL Server with PostgreSQL
- Replace PL/SQL stored procedures with Python functions
- Replace SAP / Salesforce with your own systems
- Replace IT vendor and consultant outsourcing with the floor + Claude

These are not separate problems. **The same move escapes them all — rewrite via
parallel operation.**

Don't stop the old. Build the new beside it. Feed the same inputs to both; compare
the outputs. When diffs vanish, kill the old. Time it to the contract renewal
cycle. Lock-in is a psychological device that makes you feel "I can't touch it, I
can't leave." Parallel operation dismantles that psychology physically. **Without
touching the old, build the new mainstream beside it.** When the new works, that
the old is unnecessary becomes visible to everyone.

> The way out of every vendor lock-in is the same: rewrite via parallel operation.

## On top of the foundation and the gate

The new logic layer — the rewritten core logic — is exposed as one API with
**FastAPI**. Why make it an API? To gather core logic (inventory, ordering,
pricing…) **into one place** instead of scattering it across screens. The
public-web form (2-08) and the in-house apps call the same API — duplication
disappears. In Python (FastAPI), AI writes it fast, with types and automatic docs
(OpenAPI).

The API reads and writes the 2-02 **PostgreSQL** and verifies identity with
the 2-03 **gate (PocketBase)** token. No new foundation — it rides on what
already exists.

```python
# FastAPI — verify the gate's token, query the foundation (DB)
from fastapi import FastAPI, Depends
app = FastAPI()

@app.get("/orders")
def orders(user=Depends(verify_token)):       # the 2-03 gate verifies who
    return db.query("SELECT * FROM orders WHERE user_id=%s", [user.id])  # the 2-02 DB
```

Don't expose all the core at once. **The most-used operations, one at a time.**
Write it with AI in dialogue and check against the running version (the same way as
parent series Chapter 2, VBA → Python). This is nothing but running the very logic
of parallel operation at the granularity of a single API. Heavy work runs in Python
behind it, returning only the result.

The public repo **kura** (`aiseed-dev/workspace`) is this setup — PocketBase auth +
**FastAPI** + a Flet front end. The code lives in the 2-04 Forgejo, called
from the 2-08 public web and the in-house apps. The core logic rewritten via
parallel operation lands, finally, as this one API.

## Example: monthly closing batch

Take a closing batch that runs at month-end.

**Old**: A COBOL or Java batch from five years ago. No one fully understands the
internals. Runs at month-end. Failure stops accounting.

**Week 1**: Export 12 months of inputs (last month's transaction data) and outputs
(closing summaries) from the old batch. Treat as ground truth.

**Week 2**: Hand Claude the old code and runbooks; have it write equivalent
processing in Python on FastAPI. Run 12 months of data through it; verify output
matches ground truth. Resolve mismatches.

**Weeks 3–6**: At the production timing when the old runs, also feed the same input
to the new. Compare every month. When diffs appear, identify and fix.

**Month 3**: When zero diffs occur for consecutive months, the responsible person
decides: "from next month, run the new." **Stop the old batch.**

Three months to complete the rewrite. Engineer load is doubled only during parallel
run; afterward it is halved. **And the business logic now lives in both code and
Markdown.**

## Example: getting out from under SAP shipping

A mid-sized manufacturer runs shipping management on SAP. License cost: **tens of
millions of yen per year.**

1. **Data layer**: Nightly batch exports shipping data from SAP to **Parquet**
   (parent series, Chapter 5) — SAP is not touched, read-only.
2. **New logic layer**: Stock matching, shipment decisions, carrier routing written
   in Python with Polars + DuckDB (Claude generates the first version from floor
   interviews and screenshots of the existing SAP configuration screens).
3. **API and screen layer**: The floor-facing shipping instruction is exposed as an
   API with **FastAPI** (this chapter) and rendered in HTML. Runnable inside the LAN
   on the 2-04 miniPC.
4. **Reconciliation**: Compare SAP's shipping output with the new system's daily;
   investigate any differences with Claude. **Nearly every week, an "undocumented
   rule" inside SAP surfaces.**
5. **Three months in**: When the diff has been zero for two weeks, promote the new
   system to production. **Cancel SAP before the next contract renewal.**

**Result**: the **tens-of-millions-of-yen license fee disappears**. Business logic
emerges into **Markdown and Python** (no more SAP "business consultant" middlemen).
Customizations happen on the floor the same day (previously: ask the SAP vendor,
wait months).

This is 2-05's "take documents back onto your own side" in **core-system
form**. Same structure as "don't drop Excel all at once, get out of CSV" — "don't
drop SAP all at once, kill it through parallel run."

## In numbers

Translating 5,000 lines of PL/SQL business logic to Python, SI vendor quote: about
**30M yen**. On-floor staff rewrite using Claude: 1-month development, about 1M yen
in personnel cost. **One-thirtieth.**

Oracle Enterprise Edition license: about **40M yen/year** for 20 CPUs + 22%
maintenance. Migrating to PostgreSQL: zero per year. **New-system development cost
recovered in one month.**

Undocumented business rules surfaced during 3 months of parallel operation:
typically **20–50 per system**. Rules invisible on paper specs all emerge as output
diffs.

Migrating business knowledge into Markdown: 6 months to 1 year if done in spare
time. Hand the whole codebase to Claude, do it in one sweep: **80% in one week.**

To see a small business system whole, there are worked examples in public
repos — **seminar-kit**
([`aiseed-dev/seminar-kit`](https://github.com/aiseed-dev/seminar-kit):
training-course management, where an xlsx form is the single form definition
and the pending queue is a mailbox) and **mfg-kit**
([`aiseed-dev/mfg-kit`](https://github.com/aiseed-dev/mfg-kit): quotes and
orders for a small manufacturer). Both stand on FastAPI + plain SQL + Flet —
the manner of this chapter.

## The territory you don't build, and the rules around it

The boundary line is part of the spec. **Accounting, payroll, tax — buy, don't
build.** Domains wired to national institutions are the opposite of
"company-specific" — they are society-wide generic, and for the same reason as
the OSS-first move of 1-05, they belong with proven off-the-shelf products.
This is the outer edge of this chapter's principle that you rewrite only your
own logic.

Reports and forms are a kind of exit. An invoice or a delivery slip is FastAPI
emitting the data and merging it into a template as a PDF — the "exit" of
2-05's entrance/contents/exit, and boilerplate an AI writes. No dedicated
forms product is needed.

Approval flows are not a product either. Request → approve → finalize is **a
few lines of business rules** (who, from what amount, with whose approval), a
few dozen lines of a state-holding API, and notification mail (2-06). Buying a
workflow platform was the answer of an era that could not write code.

One last check before the old system is folded — **statutory retention.**
Ledgers and invoices carry retention periods; the period is one line in the
business-rules Markdown. Before the parallel run ends and the old system is
killed, confirm the retained data sits complete in your own DB and files.
Audit records, too — on your own box, the logs are all there. No product
needed; only the rules.

## Before you build a screen — four design basics, no more

The rewritten core landed as an API. What remains is the **screens.** The tool
can simply be **Flet** (declarative UI in the same Python as the API; kura's
front end is Flet too). The tool is not the problem — the problem is that
**no one outside front-end engineering was ever taught design.** So they
cannot judge the screens the AI produces, and all they can say is "make it
look nicer."

You don't need the skill of drawing. You need **a vocabulary for seeing and
naming.** There are only four basics.

- **Proximity** — related things sit close; unrelated things sit apart. A
  screen whose items look scattered has broken this distance
- **Alignment** — line up the edges. If it's left-aligned, everything is
  left-aligned. An unaligned screen looks careless all by itself
- **Repetition** — the same role gets the same shape, every time. Buttons and
  headings that change color and form from screen to screen lack repetition
- **Contrast** — what matters is bigger and darker; everything else smaller
  and lighter. A screen where everything is the same size says nothing

Two more, and that is all: **at most three colors** (background + text + one
accent) and **one or two typefaces.** When in doubt, remove rather than add.

With this vocabulary, your instructions change. Not "make it look nicer," but
"the proximity between labels and inputs is weak," "the button color isn't
repeating," "strengthen the contrast on the total" — instructions that can be
acted on directly. Design knowledge works not as a drawing skill but as **a
vocabulary of judgment.**

And beyond the four principles, most of design is **rules, not taste.**
Spacing moves in fixed steps (multiples of 8, say). Font sizes come from a
small fixed scale. Text-to-background contrast has standard thresholds
(accessibility norms). Buttons look like buttons. Irreversible actions get a
confirmation step — all conventions, none of it flair.

And rules can be written. Exactly as business rules were pushed out into
Markdown, **design rules can be fixed on a single page** — the spacing steps,
the type scale, the three colors, the component shapes. Hand that one page
over with every screen request, and the AI applies the same rules to every
screen. Repetition enforces itself.

The strongest single rule is the **grid.** Cut the screen into equal columns
(twelve, usually), and every component sits on a column boundary — that is
the whole rule, and it enforces most of alignment and repetition **by
itself.** Web and app designers tend to dislike the grid — "rigid," "boring";
to a trade that sells originality, a lattice looks like a cage. But a
business screen doesn't need originality. It needs **predictability** — the
same thing in the same place on every screen you open — and nothing supplies
predictability more cheaply than a grid. Better still, columns and gutters
are numbers, which makes the grid the design instruction an AI follows most
precisely. Nor is the gain only visual — a grid **fixes the layout.**
Positions are decided before the content arrives, so the renderer never
recomputes the arrangement to fit incoming data: **screens draw faster,** and
nothing jumps around while loading. The discipline doubles as performance.
And the worry — "what if the content stops fitting?" — is **a memory of
paper.** On paper the area is finite, so content that doesn't fit is a real
problem. A screen is different: it is smaller than paper to begin with, so
showing everything at once was never an option — the machinery for expanding
(scrolling, collapse and expand) comes as standard. Only the placement is
fixed; content that grows simply **expands when needed.** The case where
fixing hurts never reaches the screen.

Besides, the office floor knows the grid well already. Shrink Excel's cells
into tiny squares and compose a form on the graph paper — Japan's notorious
**"kami-Excel"** (grid-paper Excel). The IT industry has long sneered at it
as the worst case of machine-unreadable data. But "unreadable" was a lie.
Kami-Excel is something **plain Python reads just fine** — the content sits
in a structured file all along, and a few dozen lines of script lift it out
of the boxes into tables (writing that script is now AI's job; the
preparation work of 2-10 is exactly this). So why the relentless mockery?
Look at what the graph paper actually does. **As long as everything snaps to
the squares, an amateur can build it — and an amateur can fix it.** Move a
box, add a column, and the form changes. A tool the floor can build and fix
for itself makes development orders unnecessary. The "worst case" sneer was
**a pretext for sealing off the floor's self-sufficiency and holding up the
price of rebuild projects.** Nobody taught the floor to do it; laying out a
form, they reached for a grid anyway — the instinct of snapping every box to
a lattice was right all along. Grid design inherits that instinct as it is —
**the frame goes to the screen's grid, the content goes to the database.**
And the graph paper's real virtue — amateurs can fix it — carries straight
over to the screen. You move the content not because it is unreadable, but
because putting it in a database once is cheaper than digging it out of the
boxes with a script every time. That is the whole reason. To designers it
looked like a cage; to the floor it looked like graph paper — the same
lattice. **That is why the amateur uses a grid layout.** For the reader of
this chapter, there is no fitter default.

The one-page rule sheet starts with this line: "12-column grid,
spacing in multiples of 8, input forms 6 columns wide."

Because the territory is made of rules, **AI can do design.** The common
screen patterns, the component shapes, the ways of spacing — the conventions
are in its training, and asked for a screen, it produces a standard, sound
one. Even the one-page rule sheet can start as an AI draft.

What AI cannot do is **original design.** Its output converges on the average
it learned. A look no one has seen, a new style that defines a brand — that
does not come out of an AI. But a business screen doesn't need originality —
what the floor uses without hesitation is precisely the familiar standard
form. Where originality is required (a brand, a storefront, design that *is*
the product), the human brings the defining image. Business screens hold up
without a designer exactly because no originality is required there.

And needing no originality is not a design-only fact.

> Everyone but the professional designer uses generic design patterns.
> Everyone but the professional programmer combines OSS libraries.
> Everyone but the professional writer writes plain prose.
> **Originality is a profession, not a default.**

Originality belongs to the trades that sell it. Where it is not the product,
the shared convention is fastest, cheapest, and least breakable — and because
conventions sit at the center of what AI learned, they are what AI reproduces
most reliably. Assembling OSS parts (1-05), writing business rules in plain
Markdown (this chapter), snapping screens to a grid — all one and the same
discipline.

Two practical challenges remain, and both yield to the same move — rules.

**First, screen diversity.** PC, tablet, phone — widths vary, and building a
screen per device never ends. Take it with rules instead: fix two or three
width steps (narrow = one column; wide = two columns plus a side rail), and
add the arrangement per step to the same one-page sheet. With a grid in
place, that addition is one line about **dropping the column count** — "wide
widths get 12 columns, narrow widths get 4." Flet ships the same
code to desktop, web, and mobile, so handling diversity stops being
"build a screen per device" and becomes **adding a few lines of rules.**

**Second, Japanese fonts.** CJK fonts carry thousands of glyphs, so they are
heavy, the choices few, and the good ones paid — a decades-old problem. Not
anymore: some of Morisawa's UD typefaces (universal-design faces built for
misread-resistance) are free to use — **BIZ UD Gothic / Mincho** ship with
Windows and are served by Google Fonts. On the rule sheet, one line suffices:
"body text BIZ UD Gothic, else the system font." This site's own body text is
set the same way (UD faces where the device has them, system faces
otherwise).

Design practice in full — diagrams and slides included — is the parent
series' Chapter 4.

> Most of design is rules, not taste.
> **Rules can be written down and handed over** — just like business rules.

## In summary

"Getting along with" a core system is old.

Rewrite, with parallel operation. Build the new system in FastAPI; run it parallel
with the old. Compare outputs against reality. When diffs vanish, kill the old.
Push business knowledge out into Markdown all at once, let the floor write the
tests, stop outsourcing. The rewritten core logic lands as one **API** riding on
**the 2-02 DB and the 2-03 gate** — no new foundation needed.

**When you do it, do it.** Half-hearted coexistence freezes the organization. In an
era when AI cuts rewriting cost by 10x, there is no reason left to keep the legacy.

Next, we lay **AI (a self-hosted LLM and RAG)** on top of all of this and cut the
dependency on Copilot.

---

## Related articles

- [2-02: Lay the Foundation — PostgreSQL, SQLite, and more](/en/ai-native-ways/software/foundation/)
- [2-03: Stand Up the Gate — One Login with PocketBase](/en/ai-native-ways/software/auth/)
- [2-05: Take Documents Back — OnlyOffice Docs on PocketBase](/en/ai-native-ways/software/documents/)
- [Reference implementation kura — a self-hosted Microsoft 365 / Google Workspace alternative](https://github.com/aiseed-dev/workspace)
</content>
