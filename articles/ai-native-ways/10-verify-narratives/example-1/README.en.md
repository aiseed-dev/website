# Example 1 — Should You Adopt Node.js at Work? Verifying Narratives with AI

A walkthrough that applies the practices from Chapter 11, "Verifying Narratives with AI," to a familiar real-world scenario: **deciding whether to adopt Node.js**.

## What this page demonstrates

When someone proposes "let's adopt Node.js across the company," this page shows the concrete five-step procedure for verifying the narrative together with AI.

Where the WordPress / Mullenweg case (the chapter's main example) showed a governance failure of **excessive concentration in one person**, Node.js shows the **opposite** failure pattern — **no one is managing the whole**.

> Both share the trait of "being unmanaged."
> With AI, you can see which failure mode you'll face *before* adopting.

---

## The surface narrative (what proponents typically tell you)

Suppose someone proposes adopting Node.js internally. Drawing from the proponent's pitch, vendor materials, tech blogs, Stack Overflow surveys, and Hacker News comments, a narrative roughly like this gets assembled:

1. **"Node.js is the standard for modern web development"** — used in nearly every modern stack
2. **"Backed by major companies"** — Microsoft, IBM, Red Hat, Google, etc. Under the OpenJS Foundation
3. **"A mature ecosystem"** — npm has **millions of packages**; everything is there
4. **"Proven at world scale at Netflix, Uber, LinkedIn, etc."** — if big enterprises use it, it must be safe
5. **"Open source, vendor-neutral"** — not tied to any one company
6. **"Excellent performance and scalability"** — handles heavy load

It all sounds great. "With this much track record, there's no reason not to adopt it." This is where you bring AI in to verify.

---

## Step 1: Extract and classify the claims

First, have Claude lay out the terrain of claims.

> From the Node.js adoption pitch above, extract the claims and classify them into (a) objective facts, (b) opinions / evaluations, (c) metaphor / rhetoric.

Claude's response (summarized):

| Claim | Category | Verifiability |
|---|---|---|
| "Standard for modern web development" | Evaluation (adoption fact + value judgment) | Partially verifiable |
| "Backed by major companies" | Factual claim | Verifiable |
| "Mature ecosystem" | Evaluation | Depends on definition of "mature" |
| "Used by Netflix and others" | Factual claim | Verifiable |
| "Vendor-neutral" | Factual claim | Verifiable |
| "Excellent performance" | Evaluation | Depends on the comparison |

Just by separating (a) from (c), the terrain of the argument becomes visible. "Standard," "mature," "excellent" — these are evaluative words, not facts.

---

## Step 2: Cross-check factual claims against primary sources

Verify "backed by major companies" against primary sources.

> Lay out the timeline of the Node.js Foundation / OpenJS Foundation board and sponsors from 2009 to the present. Include sponsorship amounts, where influence sits, and how the governance structure has shifted.

What Claude organizes (key points):

- **2009**: Ryan Dahl creates Node.js as an individual. Joyent employs and sponsors him.
- **2014**: Joyent clashes with several core developers → **io.js fork**.
- **2015**: io.js reunifies as the Node.js Foundation (under the Linux Foundation).
- **2019**: Merges with the JS Foundation to form the **OpenJS Foundation**.
- **2020**: **npm Inc. is acquired by GitHub (Microsoft)** — the npm registry is effectively Microsoft property.
- Today: the Node.js runtime sits under the OpenJS Foundation, the npm registry under Microsoft, and the **two governance lines are separate**.

A critical finding emerges here.

> **"Node.js" is not monolithic. The runtime and its distribution infrastructure (npm) are run by different organizations.**

"Backed by major companies" is factually true, but **the backing is split**. Node.js itself sits under a foundation, yet **the npm registry that developers touch every day is held by a single company (Microsoft)**. That collides head-on with the claim of being "vendor-neutral."

---

## Step 3: Check the timeline for consistency

This is the most dramatic part of the Node.js narrative.

> Lay out a timeline of statements by Node.js's creator Ryan Dahl from 2009 to the present. Show how his evaluation of Node.js has changed.

Claude organizes (key points):

- **2009–2012**: Promotes Node.js enthusiastically. Calls it "a revolution in server-side JavaScript."
- **2018 (JSConf EU)**: Gives a talk titled **"10 Things I Regret About Node.js"**, publicly enumerating fundamental design mistakes in his own work `[unverified]`
  - npm's design, the build system, module resolution, the security model, package.json bloat, etc.
- **2018**: Ryan Dahl announces **Deno** — an alternative runtime built from scratch to fix Node.js's design problems.
- **2021**: Founds Deno Land, continuing development in a different direction from Node.js.
- In parallel: **Jarred Sumner announces Bun in 2022** — yet another alternative runtime, addressing performance and developer-experience problems.

> Node.js's founder is publicly disavowing the design of what he created and building a from-scratch replacement. **This collides head-on with the narrative of "a mature, trustworthy standard."**

Because if it really were a "mature standard," the founder would address issues through incremental improvement. Forks and replacements appear because **the judgment is that the foundational design cannot be fixed.**

---

## Step 4: Cross-check against verifiable third-party records

Verify the practical implications of adopting Node.js against third-party records.

> Lay out the major Node.js / npm supply-chain incidents over the past decade, with scope of damage, root cause, and response.

Claude organizes (just the major ones):

- **2018: event-stream incident** — malicious code targeting cryptocurrency wallets slipped into an official package after a maintainer handover. Millions of downloads. `[unverified]`
- **2021: ua-parser-js incident** — account takeover of a popular package with over 600 million downloads. Miners and a RAT injected. `[unverified]`
- **2022: colors / faker incident** — intentional sabotage by a well-known maintainer himself. Millions of projects affected.
- **2024: xz-utils backdoor** — not npm, but a lesson in long-term, planned internal infiltration.
- **2026: SAP npm package contamination incident** — over 1,100 repositories leaked. `[unverified]` (covered in detail in Chapter 7).

On top of that, **testimony from the maintainer side** is also on record.

- 2024: maintainers of major packages like lodash and moment.js publicly speak about "burnout."
- The pattern of "**a multi-billion-dollar business depends on one or two unpaid volunteers**" gets pointed out repeatedly.

> Behind the narrative of "backed by major companies" and "a mature ecosystem," **the code that supports millions of businesses leans on the goodwill of unpaid volunteers**. That isn't backing — it's closer to parasitism.

---

## Step 5: Sort what's been determined from what's still unknown

After this verification, lay out **what has been factually established**.

| Item | Conclusion |
|---|---|
| Adoption | Genuinely widely used (fact) |
| Vendor neutrality | **Inaccurate**. The npm registry is owned by Microsoft. |
| Major-company support | True, but it papers over structural fragility |
| Founder's evaluation | **Negative**. Ryan Dahl built Deno and walked away. |
| Design maturity | **Doubtful**. The founder himself enumerated foundational problems; multiple replacements have appeared. |
| Adoption by large companies | True. But the larger the company, **the more they maintain it with a dedicated team**. |
| Supply-chain safety | **Structurally fragile**. Major incidents nearly every year. |
| Maintainer base | **Fragile**. Depends on unpaid volunteers. |

And **what has not yet been verified**:

- Whether Deno or Bun has fully matured as a replacement (still in transition).
- How widely npm's alternative registries (JSR, jsdelivr, etc.) have spread.
- Real numbers on large companies migrating away from Node.js.

---

## The "unmanaged" structure that surfaces

In the WordPress case (the chapter body), what surfaced was **excessive concentration in one individual, Matt Mullenweg**. The boundaries between WordPress.org, the foundation, and Automattic flex with one person's circumstances — a structural fragility.

What surfaces in the Node.js case is **the opposite problem** — the fragility of **no one managing the whole**.

- The runtime is under a foundation, the registry under a single company, quality at the mercy of individual maintainers' goodwill.
- The founder has left and is building a replacement.
- Maintainers are exposed to burnout and account takeovers.
- Security incidents recur structurally.
- It's described as "backed by major companies," but **when something goes wrong, no one is on the hook**.

WordPress — "**one person bearing too much responsibility**." Node.js — "**no one bearing responsibility**." Both are governance failures, just in opposite directions.

> The open-source narrative often says "**the whole community supports it**." Verify with AI, and that "community" often turns out to be **a distribution of irresponsibility**.

---

## Implications for the adoption decision

After this verification, the following questions emerge about the Node.js adoption decision.

- **Who takes responsibility?** — Registry: Microsoft. Runtime: a foundation. Individual packages: volunteers. When an incident happens, there is no organization you can hold accountable.
- **Is there an alternative path?** — Should the migration-cost estimate include "the possibility of moving to Deno or Bun"?
- **Can you see the dependency tree?** — If you adopt, are you prepared to audit the whole dependency graph yourselves?
- **What's the long-term maintenance setup?** — Can you afford a dedicated team like the existing big enterprises do? If not, you should be considering other options.

These are not arguments for "don't adopt Node.js." They are about **what you should be prepared for, and how far**, *if* you adopt — visible through structure rather than narrative.

---

## The power of narrative verification

What this example was meant to demonstrate is the experience of **a narrative splitting down the middle**.

The proponent's narrative isn't a lie. Node.js really is widely adopted and really is used by major enterprises. **But the structural fragility the narrative omitted surfaces under AI verification.**

"**Widely used**" and "**safely usable for the long term**" are different claims. "**Backed by major companies**" and "**someone takes responsibility when an incident happens**" are also different claims. Make adoption decisions while these are conflated, and later you'll be saying "this isn't what we were told."

> Excessive concentration in one individual (WordPress / Mullenweg) and
> total absence at the whole (Node.js) —
> both are states of **being unmanaged**.
> Knowing which problem you'll face at adoption time
> makes the work afterward orders of magnitude easier.

This is the practical value of verifying narratives with AI. **The structure becomes visible before adoption,** and that changes the quality of your work after adoption.

---

## Related

- Chapter 11 main text: [Verifying Narratives with AI](/en/ai-native-ways/verify-narratives/)
- Chapter 7: [Building the Web — Drop React, Write in Markdown and HTML/CSS](/en/ai-native-ways/web/) (concrete countermeasures for npm's structural fragility)
- Structural Analysis series: [Security Design for the Mythos Era](/en/insights/security-design/)
