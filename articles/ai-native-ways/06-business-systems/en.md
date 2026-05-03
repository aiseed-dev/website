---
slug: business-systems
number: "06"
lang: en
title: "Working with Business Systems — Rewrite via Parallel Operation"
subtitle: "'Don't break it, don't touch it' is old advice"
description: The cost of rewriting a business system has fallen by 10x with AI. There is no reason left to keep the legacy. Build a new AI-native system, run it in parallel with the old, compare outputs against reality every day, and when the diffs vanish, kill the old. This is the new attitude toward business systems.
date: 2026.05.02
label: AI Native 06
title_html: Run the legacy in <span class="accent">parallel</span>.<br>When the new one works, <span class="accent">kill</span> it.
prev_slug: office-replacement
prev_title: "Changing Paperwork — A Realistic Path Away from Office"
next_slug: web
next_title: "Building for the Web — Back to HTML+CSS+JavaScript"
---

# Working with Business Systems — Rewrite via Parallel Operation

The path of "getting along with" a business system is no longer needed.

**Rewrite, with parallel operation as the safety mechanism.** Build the new system in AI. Run the old in parallel. Compare outputs every day. When the diffs vanish, kill the old.

This is the AI-native attitude toward business systems. No half-measures. No comfortable coexistence.

## "Don't break it, don't touch it" was advice for a different era

For the past 20 years, the standard advice given to people responsible for business systems has been:

"Don't break it." "Don't touch it." "Don't change something that works." "Use the legacy assets."

This was **advice from an era when the cost of rewriting was prohibitive**. When rewriting took years and millions of dollars, "don't touch it" was indeed the right answer.

The era has changed.

AI translates business logic to Python. AI extracts the intent of SQL into Markdown. AI generates test data. AI mines undocumented rules out of legacy code. **The cost of rewriting has fallen by a factor of ten.**

Saying "don't touch it" at one-tenth the cost is denying the new reality. **There is no longer a reason to keep the legacy.**

## The logic of parallel operation

Even with rewriting cost down, the risk is not zero. No method can guarantee that a new system behaves exactly like the old.

That is what **parallel operation** is for.

Build the new system in AI. Keep the old running. Feed the same input to both. Compare the outputs.

```
Production input
   │
   ├──→ Old system (Java/C#) ──→ Output A
   │
   └──→ New system (Python+AI) ──→ Output B

Compare A and B every day
```

If A and B match, the new system is correct. If they don't, one of them is wrong. **Usually, a 20-year-old bug in the old system surfaces first** — a bug that was never in any document.

Continue this for one month, three months. When diffs reach zero and edge cases are covered, stop the old.

Parallel operation eliminates rewrite risk through **measurement**. Not desk-checking. Not spec reviews. **Production environment, real data, run and verify.**

## How long to keep the old running

The parallel-operation period should be at most six months, usually three is enough.

If you need longer, the new system is not actually correct. Fix the new system. **Don't run parallel "indefinitely."**

Inside organizations, there is a psychology of "keep the old around just in case." This is a trap. Keeping it means:

- Operations cost doubles
- Engineers split their attention
- When something breaks, arguments erupt over who is responsible
- New features must be built in both, doubling the work
- The decision to kill the old gets postponed forever

> Parallel operation is a means, not an end. When the new is verified, kill the old.

If you can't kill it, you shouldn't have started rewriting. **When you do it, do it.**

## Why "augment" is not enough

"Use the legacy assets, augment with AI" — this approach ultimately permits the old system to remain.

New features pile up on the outside. The substance stays old. Engineers move between two worlds. Three years pass, five years pass, and the organization is still not AI-native.

Parallel operation has a deadline. Replace within the deadline. **Half-hearted coexistence freezes the organization.**

"Augment" was acceptable when rewriting was truly too expensive. That era is over.

## How to kill vendor products

Oracle, SAP, Salesforce, Microsoft business products — these aren't selling "products." They are selling "**the situation in which you have to keep using the product**."

Pattern for killing via parallel operation:

1. Export data from the product daily (the product keeps running)
2. The new AI-built system processes the export and runs the same business
3. Compute the same business metrics (sales, inventory, customer state) in both
4. When the numbers match, **don't renew the product contract**
5. Take a final "full data export" from the product and switch entirely to the new

**Time it for the contract renewal cycle.** This is a strategic schedule. Renewal in October? Start parallel in June. Run for three months. Decide in September.

The vendor will pull every card to keep you: "migration risk," "data integrity," "your veterans will leave." Parallel operation with matching outputs answers all of them. **You have the evidence.**

License fees are tens of thousands of dollars per year. Stopping that recovers the new-system development cost in months.

## Push business knowledge out — all at once

As preparation for parallel operation, push business knowledge into Markdown. **All at once.**

Old common sense said documenting business knowledge was a months-to-years project. Someone scribbles in spare hours. Before half is written, that person transfers. The project collapses partway. **Ultimately, it never gets written.**

The era has changed.

Hand Claude **everything** — old code, comments, SQL, runbooks, past incident reports. Tell it: "extract the business logic and organize it as Markdown." A codebase of a few thousand lines: hours for the first draft. Tens of thousands of lines: days at most.

"What this code does." "What rules are embedded." Human-readable Markdown lands in your hands **all at once**.

It does not have to be perfect. **80% is enough.** The remaining 20% will surface as output diffs during parallel operation. Resolve them one by one, and the documentation completes itself.

> Compress months of work into days. This is what AI is actually for.

This is also the hidden benefit of parallel operation. **Business rules that were never written down all surface during parallel run.** Rules that no spec captured, only operations knew — these get pulled out, both from Claude's first-pass Markdown and from the diffs the parallel run produces.

A rewrite is also a documentation exercise. **Finish it this week.** There is no time left to keep "we'll document it someday" projects on the books.

## Business rules live with the people who do the work

Who does the rewriting?

Old common sense: the IT department, SI vendors, or consultants gather requirements from the floor, then write code. When done, the floor performs acceptance testing.

This was the shape of an era when the knowledge needed for a rewrite was distributed. **Coding ability lived in IT; business-rule knowledge lived on the floor.** They had to be coordinated.

That has changed.

**Coding ability is held by Claude.** What remains is business-rule knowledge. And the people who know business rules most deeply are the people running that business every day.

The people on the floor have Claude write the code. **That is the whole loop.** No middle layer of "translation" needed.

## The floor writes the tests

What matters in parallel operation is finding output diffs. "Does the new system produce the same output as the old?" — verifying this requires test data.

The people best suited to creating this test data are the people on the floor.

"July billing closes on the 10th, but we extend by Obon to the 5th of the following month" — the floor knows this rule. They tell Claude: "make 50 billing test cases that account for the Obon extension in July." Claude makes them. They are run through the old system to capture expected outputs. This becomes the test data.

Rules that were never in any spec materialize as tests. **Business knowledge flows from the floor → tests → code.**

This is a kind of test the IT department, by itself, cannot write. They do not know the rules. **Rewrites have failed because people who didn't know the rules wrote the tests.**

## Stop outsourcing

Once you reach this point, the conclusion is clear.

**You do not need to outsource business-system rewrites to IT vendors or consultants.**

The traditional rationale for outsourcing was twofold:

1. Coding ability lived only on the outside.
2. Business knowledge had to be transferred to the outside.

(1) was solved by Claude. (2) is no longer needed in the first place. **The floor + Claude completes the loop.**

Outsourcing fees are the single largest cost item in business-system rewrites. Tens of millions to hundreds of millions of yen per year. That cost disappears.

People on the floor — who know the rules — have Claude write the code, Claude write the tests, and verify by parallel operation. **Rewriting changes from "something to outsource" to "something done in-house."**

This is not a contraction of the IT department's role. IT focuses on supporting the (floor + Claude) teams: infrastructure, databases, deploy environments, security. **They escape the duplicative role of "business-logic intermediary."** The work that for years consisted of writing specs without understanding the business and then revising them, simply disappears.

> The people who know the business use Claude to rewrite their own systems. That is the new floor practice.

To stop outsourcing is also to take responsibility back.

## Keep SQL. Drop PL/SQL and T-SQL

Keep the database. **But drop the vendor dialect.**

Keep SQL as a standard language. `SELECT`, `JOIN`, `GROUP BY`, window functions — these have run for 50 years and will run for 50 more. Claude writes them perfectly.

But Oracle's **PL/SQL** and Microsoft SQL Server's **T-SQL** — drop them. They are **vendor-specific dialects**. Embedding business logic inside the database has been the last bastion of vendor lock-in.

Migrate to PostgreSQL. **The cost benefit is enormous.**

PostgreSQL is open source, free, and commercially usable. Functionally on par with or better than Oracle and SQL Server.

- **Zero license fees.** Oracle Enterprise Edition costs millions of yen per CPU. For a mid-sized organization, tens of millions to over one hundred million yen per year. That disappears.
- **Functionality**: JSON types, array types, window functions, CTEs, full-text search, logical replication — everything business needs.
- **Performance**: With proper design, comparable to Oracle. For most workloads, no measurable gap.
- **AI-writability**: Claude is best at PostgreSQL dialect (it has the most open-source training data).
- **Ecosystem**: AWS RDS, Google Cloud SQL, Azure Database — every cloud has a managed offering.

Business logic embedded in PL/SQL stored procedures gets rewritten in Python. Hand Claude the PL/SQL; it extracts the business rules and outputs Python. **Business logic returns from invisible stored procedures into code.** Readable. Version-controlled. Testable.

## Migrate the DB and the logic layer in parallel

The same parallel-run approach used for the logic layer applies to the DB.

1. Create the same schema in PostgreSQL (Claude writes the DDL dialect translation)
2. Sync data daily from the old DB into PostgreSQL
3. The new system (Python) reads/writes PostgreSQL
4. The old system (Java/C#, PL/SQL) continues with Oracle / SQL Server
5. Verify consistency between both via output comparison
6. Pick a cut-over day. PostgreSQL becomes primary; the old DB goes read-only
7. After weeks of stable operation, stop the old DB

Rewriting just the logic layer to Python is only half-escaping the lock-in. As long as the DB is Oracle, you keep paying Oracle license fees. **Migrating to PostgreSQL is the final step out of lock-in.**

And **the annual license cost recovers the new-system development cost in a few months.** Financially, there is no reason left not to rewrite.

> Drop Oracle / SQL Server. That is your graduation certificate from vendor lock-in.

## The way out of every lock-in is the same

Everything described above has the same structure.

- Replace the Java / C# logic layer with Python
- Replace Oracle / SQL Server with PostgreSQL
- Replace PL/SQL stored procedures with Python functions
- Replace SAP / Salesforce with your own systems
- Replace IT vendor and consultant outsourcing with the floor + Claude

These are not separate problems. **The same move escapes them all.**

**Rewrite via parallel operation.**

Don't stop the old. Build the new beside it. Feed the same inputs to both; compare the outputs. When diffs vanish, kill the old. Time it to the contract renewal cycle.

Lock-in is a psychological device that makes you feel "I can't touch it, I can't leave." Parallel operation dismantles that psychology physically. **Without touching the old, build the new mainstream beside it.** When the new works, that the old is unnecessary becomes visible to everyone.

> The way out of every vendor lock-in is the same: rewrite via parallel operation.

This is not just about business systems. Office, Microsoft 365, Google Workspace, CRM — wherever a vendor claims "your business stops without us," the same approach works.

## Example: monthly closing batch

Take a closing batch that runs at month-end.

**Old**: A COBOL or Java batch from five years ago. No one fully understands the internals. Runs at month-end. Failure stops accounting.

Steps for parallel operation:

**Week 1**: Export 12 months of inputs (last month's transaction data) and outputs (closing summaries) from the old batch. Treat as ground truth.

**Week 2**: Hand Claude the old code and runbooks; have it write equivalent processing in Python. Run 12 months of data through it; verify output matches ground truth. Resolve mismatches.

**Weeks 3–6**: At the production timing when the old runs, also feed the same input to the new. Compare every month. When diffs appear, identify and fix.

**Month 3**: When zero diffs occur for consecutive months, the responsible person decides: "from next month, run the new." **Stop the old batch.**

Three months to complete the rewrite. Engineer load is doubled only during parallel run; afterward it is halved. **And the business logic now lives in both code and Markdown.** That is significant.

## To those who say "don't touch what works"

Inside organizations, people oppose rewriting. Their argument almost always reduces to one: "if you touch it, it might stop."

Parallel operation answers exactly this. **You are not touching it.** The old keeps running during parallel. You verify daily that the new produces the same output as the old.

If a diff appears on a given day, you identify the cause that same day. Fix the new. Don't touch the old. **Keep the old running as the reference for what "correct" means.**

When parallel operation ends, three months of production data has proven the new behaves identically. **The risk of stopping the old at this point is far smaller than the risk those who originally opposed rewriting imagined.**

People who keep saying "don't touch what works" cannot show data. People proposing parallel operation show data daily. **The argument lands on facts.**

## In summary

"Getting along with" a business system is old.

Rewrite, with parallel operation. Build the new system in AI; run it parallel with the old. Compare outputs against reality. When diffs vanish, kill the old.

**When you do it, do it.** Half-hearted coexistence freezes the organization. In an era when AI cuts rewriting cost by 10x, there is no reason left to keep the legacy.

The next chapter moves to the web. "You don't need React. HTML, CSS, and JavaScript are enough" — a return to the origin.

---

## Related

- [Chapter 05: Changing Paperwork — A Realistic Path Away from Office](/en/ai-native-ways/office-replacement/)
- [Chapter 04: Writing Logic — Have AI Write Python For You](/en/ai-native-ways/python/)
- [Structural Analysis 08: Removing the Enterprise IT Tax](/en/insights/enterprise-tax/)
- [Structural Analysis 11: Regulation Redesign](/en/insights/regulation-redesign/)
