---
slug: large-proves-small
title: "If Large-Scale Works, Small-Scale Is Immediate — Converting the Million-Line, Two-Week Proof to Fifty Thousand Lines"
subtitle: "What the Bun port demonstrated was a method, not a scale barrier — apply the same procedure to a small company's business system and the timeline fits in a weekend, with the cost down by two orders of magnitude"
date: 2026.07.28
description: The previous piece cited the Bun port reported on Anthropic's engineering blog — one million lines of Zig to Rust in under two weeks, 100% of the existing tests passing, roughly $165,000 in API costs — as proof that distillation runs at industrial scale. This piece does the conversion. The same article carries a second example — an individual moved a 165,000-line Python project to TypeScript over a single weekend. The custom portion of a small company's business system is usually a few thousand to a few tens of thousands of lines — an order of magnitude below that proof. Divide by line count and the cost lands in the low thousands of dollars and the timeline in a weekend. The procedure is the same, and the difference is exactly one: Bun had a test suite, and business systems usually do not. So the first job is extracting the tests — the distillation of the previous piece. Use the running system as the teacher, copy its behavior, put scripts up as the referee, and work through a mechanical queue. A lighter target still is the website, whose behavior is fully exposed from the start — extracting the tests takes a single crawl, and going static removes the maintenance fee and the attack surface along with it. The wall the large-scale proof knocked down was not technical. It was the assumption that "this is beyond us."
lang: en
label: Blog
category: Structural Analysis Notes
---

# If Large-Scale Works, Small-Scale Is Immediate

## Conclusion

[The previous piece](https://aiseed.dev/en/blog/distilling-business-systems/) cited Anthropic's report of the Bun port — **one million lines** of Zig to Rust in **under two weeks**, with **100% of the existing tests passing**. This piece does the conversion.

**If the method holds at large scale, it becomes easy at small scale.** The custom portion of a small company's business system is usually one-tenth to one-hundredth the size of that proof. Divide by line count and the timeline fits in a weekend, with the cost down by two orders of magnitude. And before the business system there is a lighter target still — **the website, whose behavior is already fully exposed, so extracting the tests takes a single crawl.** What remains standing is not a technical wall but the assumption: "this is beyond us."

## Fact — The Demonstrated Numbers

The numbers reported on Anthropic's engineering blog (16 July), in order.

**The Bun port.** The core of the JavaScript runtime Bun: one million lines of Zig, moved to Rust. Finished in under two weeks, with 100% of the existing test suite passing. Nineteen regressions surfaced after merge; all were fixed. API cost was roughly $165,000 — 5.9 billion input tokens, 690 million output tokens.

**The individual port.** The same article carries a second example. A single developer moved a 165,000-line Python project to TypeScript **over one weekend**, with eight phase gates and three rounds of adversarial review.

The method is the same in both. **You don't fix the code; you fix the process (loop) that produces the code.** Run the wheel of translate → compile → test → verify, and "let scripts — a compiler, a diff, a test suite — be the referee." Keep the work queue mechanical, rebuilt from disk every time — which makes the migration resumable by construction.

## Conversion — What Happens at Fifty Thousand Lines

The custom portion of a small company's business system — sales, inventory, invoicing, production — usually runs from a few thousand to a few tens of thousands of lines. Set it at fifty thousand and divide by the demonstrated numbers.

**Scale.** One-twentieth of Bun. Compared even with the individual port that fit in a weekend (165,000 lines), it is one-third the size.

**Cost.** Bun came to about $165,000 for a million lines — roughly $0.17 per line. Straight proportion gives about $8,000 for fifty thousand lines. But that is close to an upper bound. A runtime's core is among the densest code there is; the decisions, forms, and approval flows of a business system are thinner. And as the preceding pieces noted, this is the era in which near-frontier weights open for free. **Landing in the low thousands of dollars is the natural outcome.**

**Timeline.** If 165,000 lines fit in a weekend, fifty thousand lines fit in a weekend. Most of the elapsed time is AI execution, not human work.

The premise of the estimate should be stated: line count is a crude ruler, and what actually governs the effort is not lines but the next section's question — whether tests exist.

## Procedure — The Difference Is Exactly One

The procedure for the Bun port and for rebuilding a business system is almost identical. The difference is the starting point. **Bun had an existing test suite. Business systems usually do not.**

So the first job is extracting the tests. This is precisely the distillation of the previous piece — put questions to the running system and record the answers. Enter an order, this document; close the period, this balance. **The current system is the teacher model, and the recorded behavior is the training material.**

From there, follow the demonstrated procedure.

1. **Turn behavior into tests.** Without stopping the current system, record inputs and outputs and write them up as automated tests. Most of the test data the model can generate. Humans add only the quirks of real data and the combinations that are impossible in the business.
2. **Put scripts up as the referee.** Feed the same inputs to old and new, and confirm that forms, journal entries, and balances match by diff. The judge must be able to score both on equal terms.
3. **Work through a mechanical queue.** One screen, one report at a time; strike each off as it passes. If the queue is rebuilt from disk every time, you can stop at any point and resume without explanation.
4. **Keep the gates and the adversarial review.** Even the weekend port kept its eight phase gates and three review rounds. The speed comes from automating verification, not from skipping it.
5. **Run in parallel, check the answers, switch over.** Retire the current system section by section, wherever the match holds.

[The practice of proceeding one thread at a time without stopping the current system](https://aiseed.dev/en/blog/in-house-business-systems/) was covered earlier; what is new is that the scale and cost now carry demonstrated values.

## For a Website, It Is Even Easier

Before the business system, there is a lighter target still. **The website.**

From the standpoint of distillation, a website occupies a special position: **its behavior is already fully exposed.** Give it a URL and a page comes back — those input-output pairs are the entire behavior. The test extraction that was the first job for a business system reduces, for a website, to a single crawl. The training material is public; you do not even need to put questions to the teacher.

The procedure fits in three lines. Crawl the current site and record every page. Have AI rebuild it as a static site with the same appearance and structure. Diff old pages against new, and when they match, switch the DNS.

A sense of scale: the "custom portion" of a CMS-driven company site is a few hundred to a few thousand lines of theme and plugin modifications, if that — the rest is vendor code, which there is no need to copy. What gets copied is the appearance and the content: the behavior. The cost drops another order of magnitude below the previous section's conversion, and the timeline is not a weekend but an afternoon.

And the migration is not the only gain. As [the containment piece](https://aiseed.dev/en/blog/nadella-yang-what-to-do-now/) put it, a static site has no database, no server-side execution environment, no admin panel, no plugin-update treadmill. **If it is breached, files get rewritten — nothing more.** The CMS maintenance fee and the vulnerability chasing disappear on the day of the switch.

This site carries a product of the same procedure: an old site that ran on ASP.NET Core (about 450 pages), copied into a static file bundle that runs no .NET at all, served under the same domain. It sat on a dynamic framework, but its substance was effectively static — a live example of "what needs copying is only the behavior."

## What to Watch

**Cases.** Whether rebuilds of business systems in the tens-of-thousands-of-lines class — test extraction → AI reimplementation → parallel run — get reported at costs in the low thousands of dollars and timelines in weeks.

**The failure condition.** If rebuilds of that class, with tests in place, still keep landing at months and seven figures, this piece's conversion is wrong. If it fails, that will be written here.

---

## Related

- Blog [Distillation Is Not Only About AI — AI Builds the Business System](https://aiseed.dev/en/blog/distilling-business-systems/) — the previous piece; tests copy the behavior
- Blog [With Fable's Release, In-House Development Wins for Business Systems](https://aiseed.dev/en/blog/in-house-business-systems/) — rebuilding without stopping, with the current system as oracle
- Blog [The Person the AI Era Needs — When Software Gets Cheap, So Does Attack](https://aiseed.dev/en/blog/three-conditions-ai-era/) — the structure by which software cost heads to zero
- Blog [Hailed as Prescient for Leading AI-First](https://aiseed.dev/en/blog/nadella-yang-what-to-do-now/) — the practice of containment, including "make the website static"

## References

1. Anthropic: AI code migration — https://claude.com/blog/ai-code-migration
