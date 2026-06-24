---
slug: software-three-transitions
title: "In the AI era,\"Become a specialized engineer\" misreads the structure"
subtitle: The Second Renaissance has begun — software engineer → builder, software engineering → liberal arts, employment → free person
date: 2026.05.22
description: "The widely circulated advice — \"in the AI era, become a specialized engineer; hold a deep specialty AI cannot take, like security or ML\" — misreads the structure. AI is absorbing the whole layer of software engineering, not a particular subdomain. The medieval analogue: telling a serf, \"become a more specialized serf and you will be free.\" Freedom comes from stepping out of the lord's structure of control, not from deeper specialization. Software engineer → builder, software engineering → liberal arts, employment → free person — these three transitions are unfolding inside the Second Renaissance (the historical turning point of the AI era, with the LLM playing the role of the printing press). Creation and upheaval are two faces of the same time, and Trump is the canonical figure on the upheaval side. The article compresses aiseed.dev's \"AI-Native Ways of Working — Software\" sub-series (thirteen argument chapters) into three pairs of words."
lang: en
label: Blog
category: Structural Analysis Notes
hero_image: IMG_3481.jpg
---

# In the AI era,"Become a specialized engineer" misreads the structure

There is a widely circulated piece of advice — "in the AI era, become a specialized engineer; hold a deep specialty AI cannot take, like security or ML."

This **misreads the structure**.

What AI is absorbing is **the whole layer** of software engineering, not a particular subdomain inside it. Going deeper into a specialty only shifts the date by which the specialty itself is overtaken. The medieval analogue would be telling a serf, "become a more specialized serf and you will be free." Freedom does not come from going deeper into the specialty; it comes from **stepping out of the lord's structure of control**.

The structural change argued in aiseed.dev's [AI-Native Ways of Working — Software](/en/ai-native-ways/software/) sub-series (thirteen argument chapters) compresses into three transitions:

| Before | After |
|---|---|
| Software engineer | **Builder** |
| Software engineering | **Liberal arts** |
| Employment | **Free person** |

We look at why each one happens.

## Transition 1: Software engineer → builder

**The software engineer's work was writing code.** Specs come down, someone fluent in languages, frameworks, and patterns implements them. Adding people to the team raises writing speed; output scales as "head count × writing speed" — this has been the structure for the past thirty years.

**The builder's work is deciding what to build.** Concretely, four moves in a loop:

- **Decide** — from the customer, the field, your own context, judge what to build and how to divide it
- **Delegate** — hand AI the intent, constraints, acceptance criteria. AI writes the code
- **Evaluate** — judge whether the returned output runs, fits the design, and holds up in the intended context
- **Integrate** — fold the part into the whole, keep the whole consistent, return to the next "decide"

The loop turns dozens of times in a day. Code-writing time is minimized inside it — because AI is the one writing.

> An engineer's output is set by **head count × writing speed**.
> A builder's output is set by **judgment quality × loop turnover**.

In numbers: aiseed.dev's code base (about 6,000 lines — the build tool, templates, image generation, sitemap, and so on that carry five independent series and ~150 bilingual articles) was stood up by **one person + AI in 24 hours**. The same scope handed to an SIer would burn that much time on the proposal and quote alone.

"Add people and it goes faster" held in the engineer's world (with a ceiling). In the builder's world, **adding people does not make it faster** — the chain of judgment cannot be parallelized across heads.

See [1-04: The Builder Role](/en/ai-native-ways/software/builder/).

## Transition 2: Software engineering → liberal arts

"What skills should a builder develop?" — the answer differs from what the industry expects.

What the builder cultivates is **structural decomposition, verbalization, evaluative eye, integration judgment, selection**. All of these have been called **the liberal arts** (the *artes liberales*, the "seven liberal arts") for two thousand years.

| What a builder needs | Its liberal-arts counterpart |
|---|---|
| Structural decomposition | Logic, analysis (the *trivium*'s dialectic) |
| Verbalization (turning implicit intent into explicit description) | Grammar, rhetoric (the *trivium*) |
| Evaluative eye (separating "merely runs" from "fits the design") | Aesthetics, ethics |
| Integration judgment (seeing whether parts preserve the whole) | Systems thinking (geometry and the constructive sense of music) |
| Selection (picking "this one" from three options) | Ethics, theory of judgment |
| Reading context (cutting it out of customer and field) | History, social science, political philosophy |

**What AI took over is the core of software engineering** — algorithms, language specifications, frameworks, design patterns, how to write tests. The work that remains looks liberal-arts–shaped because, structurally, **it has to**.

To be clear, **computer science (CS) is a different thing**. Computability, algorithms, formal logic, discrete mathematics sit inside the liberal arts as a modern extension of the *quadrivium*'s mathematics and logic. Historically CS emerged from mathematics; Turing, Church, and von Neumann were mathematicians and logicians. **CS does not need to be discarded, and it does not need a special category** — it is folded into the builder's scaffold for judgment.

The etymology lines up, too. The medieval *artes liberales* were defined as **the arts a free person — one who is not enslaved — should learn**, set explicitly against the *artes mechanicae*, the slave's arts. The builder is the person who **does not hand judgment over to AI** — the contemporary form of the free person's arts.

See [1-04: The Builder Role — "A builder's foundation is liberal arts"](/en/ai-native-ways/software/builder/).

## Transition 3: Employment → free person

One more transition is easily missed. **Modern employment, examined structurally, sits in the same position as medieval serfdom.**

| Dimension | Medieval serf | Modern employee |
|---|---|---|
| Ownership of the means of production | Lord's land and tools | Employer's office, equipment, IP, data, infrastructure |
| Self-determination of labor | Cultivating at the lord's direction | Working at the supervisor's direction |
| Freedom of movement | Tied to the land | Tied by employment contract, mortgage, in-company career |
| Income predictability | Stable under the lord's protection | Trading freedom for salary stability |
| Locus of judgment | The lord | The employer |
| What is received in exchange | Food and protection | Salary and benefits |

This is not a claim of moral equivalence (modern employment has legal protections and contractual freedom). It is an analytical observation that **on the three axes of ownership, judgment, and mobility, the structure matches**.

And the reasons employment **stops fitting in the AI era** are structurally clear:

1. **The means of production are now individually ownable** — a few-thousand-yen-a-month AI, local LLMs, open source, one's own server. The employer no longer needs to monopolize them.
2. **One person + AI = a ten-person team** — the payoff of concentration disappears.
3. **The boundary between judgment and execution closes within one person** — the overhead of aggregation, coordination, and management becomes pure waste.
4. **Judgment-centered professions are intrinsically inclined to independence** — lawyers, doctors, accountants prefer solo practice and partnerships, not by accident.

**The rise of self-employment is structural necessity, not a policy or lifestyle question.** The same structure under which medieval free citizens, free farmers, and craftsmen were all "self-employed" returns in the AI era.

> Employment is the contemporary form of medieval serfdom.
> **Self-employment is the contemporary form of being a free person.**

See [3-08: "Employment is the AI era's serfdom"](/en/ai-native-ways/software/five-years/).

## This is the Second Renaissance

Lay the three transitions out — engineer → builder, software engineering → liberal arts, employment → free person — and they line up, item by item, with the structural change of the First Renaissance (14th–17th centuries).

| Element | First Renaissance | Second Renaissance (AI era) |
|---|---|---|
| The polymath ideal | Leonardo da Vinci | The builder, one person + AI |
| The classics being recovered | Greek and Roman classical learning | The liberal arts |
| Vernacular liberation | Dante's Italian, Luther's German | Natural language becomes "the programming language" |
| Free cities and guilds | Florence, Venice, the craft guilds | The AI-era free person, professional guilds |
| **The accelerator** | **The printing press (1450s) — democratized reading** | **The LLM — democratizes making** |
| New rising class | The bourgeoisie | The AI-native builder, the self-employed judgment professional |

History textbooks credit the printing press with preparing the ground for the Reformation, the scientific revolution, and the modern nation-state **over two hundred years**. The LLM holds **incomparably greater intensity** — what the printing press democratized was "reading" (access to existing knowledge), while what the LLM democratizes is "**making**" (knowledge generation, judgment, implementation). There is no literacy wall to clear first; natural language works for anyone.

The speed of diffusion is on another order. What took the printing press decades, the AI era achieves **in years**. The five-year horizon this sub-series draws is, against this difference in intensity, **a conservative estimate**.

The Second Renaissance cannot be captured by "the AI revolution" alone. The deeper arguments — **the AI revolution is the completion of the IT revolution** (the 70-year-late fulfillment of the automation promise), **the LLM is a statistical-processing tool, not a superintelligence** (structural rejection of the AGI hype), **app-making comes to resemble film-making** (holding across the Hollywood-to-YouTube range), **not only the AI revolution** (concurrent transitions in fossil resources, geopolitics, agriculture, finance, demographics, healthcare, and pensions), and **creation AND upheaval as two sides of the era** (Trump and Nadella share the same structural error of judgment-concentration) — are developed in [**Software sub-series, 3-08: "The transition completes in a few years"**](/en/ai-native-ways/software/five-years/).

## The alternative path to "specialized engineer" advice

Back to the opening question. "How do you move in the AI era?" — the answer is not deeper specialization. It is **stepping sideways**.

There are two paths:

1. **Sideways onto the liberal-arts axis** — sharpen judgment, verbalization, ethics, systems thinking. Become a builder.
2. **Sideways into builders who hold physical reality** — makers, embedded engineers, robotics, precision agriculture, carpenters using AI design tools. The middle layer that bridges pure software's abstraction with pure physical work's directness.

Both are roads out of the lord's manor.

## More in the Software sub-series

This article compresses aiseed.dev's **[AI-Native Ways of Working — Software](/en/ai-native-ways/software/)** sub-series (thirteen argument chapters) into three pairs of words. The arguments across the chapters:

- [1-01: AI Solves the World's Hardest Coding Problems](/en/ai-native-ways/software/coder-top/) — Codeforces 2700 tier; the top layer for $200/month
- [1-02: The Real Shift Is in Maintenance](/en/ai-native-ways/software/maintenance-shift/) — the unit of maintenance moves from code to design
- [1-03: AI Now Does the Software Engineer's Work](/en/ai-native-ways/software/coder-end/) — same structure as abacus → calculator
- [1-04: The Builder Role](/en/ai-native-ways/software/builder/) — decide, delegate, evaluate, integrate
- [1-05: Customers Co-develop with AI](/en/ai-native-ways/software/customer-codev/) — 90% is the customer; 10% goes to a specialist
- [3-01: Companies Don't Write Their Own Code — Office and Core, Two Parallel Worlds](/en/ai-native-ways/software/two-worlds/) — the two parallel worlds, the double tax, and their dissolution
- [3-02: Digital Sovereignty — The Microsoft Problem and the Trump Problem](/en/ai-native-ways/software/sovereignty/) — OSS and sovereign AI now win on both economics and security
- [3-03: The SIer Commission Model Is Structurally Uneconomic](/en/ai-native-ways/software/sier-uneconomic/)
- [3-04: An Order-of-Magnitude Price Gap](/en/ai-native-ways/software/price-gap/) — 10×–100× is market displacement, not competition
- [3-05: The Lock-In Problem](/en/ai-native-ways/software/lockin/) — Palantir FDE as the canonical case
- [3-06: The Master Builder Is a Profession That Sells Judgment](/en/ai-native-ways/software/hiring-builders/) — same position as lawyers and doctors
- [3-07: Japan's SIer Industry Transition](/en/ai-native-ways/software/japan-transition/) — multi-tier subcontracting paradoxically eases the transition
- [3-08: The Transition Completes in a Few Years](/en/ai-native-ways/software/five-years/) — irreversibility; the Second Renaissance

"**From software engineering to the liberal arts — the foundational shift of the technical profession**" is the subtitle of the sub-series and one axis for reading the structure of the AI era.

---

## Related

- [AI-Native Ways of Working — Prologue](/en/ai-native-ways/prologue/) — the contour of the AI-era free person
- [Structural Analysis 08: Removing the Enterprise IT Tax](/en/insights/enterprise-tax/) — the structural change on the company side
- [Structural Analysis 09: AI and the Individual Business](/en/insights/ai-and-individual/) — the structural change on the individual side
- [Microsoft's Nadella and Hegel's Philosophy](/en/blog/nadella-hegel-cunning-of-reason/) — the worldview on the opposite side
