---
slug: five-years
number: "11"
lang: en
title: The Structural Transition Completes in a Few Years
subtitle: The chain of change, a roughly five-year horizon, irreversibility — but bounded to software development
description: From AI reaching top-tier capability through coder displacement, builder demand, and SIer shrinkage, the changes chain together and the main part completes in roughly five years. Once a structure moves, it does not move back. But this "complete replacement" applies only to verifiable-correctness domains like software; in desk work, self-driving, and robotics, AI is blocked at the last 1% and complete replacement does not happen — those are productivity-gain stories. The writing of this very sub-series is itself evidence of that bound.
date: 2026.08.10
label: Software 11
title_html: In <span class="accent">five years</span>, the main changes<br>complete — irreversibly.
prev_slug: japan-transition
prev_title: Japan's SIer Industry Transition and Labor Mobility
next_slug:
next_title:
---

# The Structural Transition Completes in a Few Years

**The final chapter of the Software sub-series. The structural changes
shown across the previous ten chapters are not independent — they
chain together. The chain completes its main part in about five
years, and once a structure has moved, it does not move back**.

But this "complete replacement" only applies in the specific domain of
software development. The boundary is made explicit in the second
half of the chapter.

## The chain of change

Put the claims from Chapters 1 through 10 back in the order in which
they cascade.

- **AI reaches human-top execution capability** (Chapter 1) —
  Codeforces 2700 tier, $200/month
- **The main battleground of maintenance moves to design** (Chapter 2)
- **The role called "coder" goes away** (Chapter 3)
- **A new role — the builder — emerges** (Chapter 4)
- **Customers themselves become builders** (Chapter 5) — nine-tenths
  in-house, only one-tenth outsourced
- **The SIer commission model becomes structurally uneconomic**
  (Chapter 6) — the same effort builds it in-house
- **The price gap runs at orders of magnitude** (Chapter 7) — 10× to
  100×, market displacement, not competition
- **Lock-in dissolves** (Chapter 8) — AI-native standard code, the
  opposite end from Palantir's FDE
- **Companies hire builders** (Chapter 9) — same professional
  position as lawyers and doctors. The supply is not only former
  coders; AI + Python + Flet bring in **the VB / VBA generation,
  makers, shop-floor engineers, and students** as new entrants
- **Multi-tier subcontracting absorbs the transition** (Chapter 10)
  — shrinkage without internal lay-offs

These are not independent observations. **They cascade from one fact
— AI taking execution — in chain**.

```mermaid
flowchart LR
  AI["AI reaches human-top<br/>execution capability<br/>(Ch 1)"]
  Coder["Coder role<br/>goes away (Ch 3)"]
  Builder["Builder demand<br/>(Ch 4, 9)"]
  Customer["Customer<br/>self-build (Ch 5)"]
  SIer["SIer<br/>shrinkage (Ch 6, 7)"]
  Lock["Lock-in<br/>dissolves (Ch 8)"]
  Industry["Industry<br/>transition (Ch 10)"]
  Done["Main changes<br/>complete in ~5 years"]

  AI --> Coder
  AI --> Builder
  Builder --> Customer
  Coder --> SIer
  Customer --> SIer
  Lock --> SIer
  SIer --> Industry
  Industry --> Done

  classDef good fill:#e8f5e9,stroke:#7a9a6d,color:#3a4d34
  class AI,Coder,Builder,Customer,SIer,Lock,Industry,Done good
```

Within the chain, what moves fastest is **new projects and
extensions**. What moves slowest is **full replacement of core
business systems**. But both point in the same direction, and the
direction does not reverse.

## Why only coding moves to complete replacement

This is where the **scoping** of the sub-series needs to be made
explicit.

Software development is a broad field — requirements gathering,
design, **coding**, testing, deployment, operations, incident
response, stakeholder coordination. **What AI fully replaces is only
the "coding" inside this list**. The reason: two conditions hold at
once for coding:

1. **The rules are explicit** — language specs, standard-library APIs,
   type systems, syntax — all defined formally and unambiguously.
   There is little interpretive room for "the correct way to write
   it."
2. **Correctness is verifiable** — whether code compiles, whether
   tests pass, whether a competitive-programming problem is solved
   — all checkable mechanically.

When both conditions hold, AI receives, during training, an enormous
volume of feedback both on "did it follow the rules" and "is it
correct." That is why AI reaches superhuman levels **in the coding
domain**.

> AI reaches superhuman levels in **domains where the rules are
> explicit and correctness is verifiable**.
> **"Coding" inside software development** is the textbook case.

The other parts of software development — requirements, design,
operations, incident response, stakeholder work — carry the same
structural 1% problem we will see in self-driving and Shinkansen
later. This is what Chapter 3's "coders go away, builders remain"
means: **coding gets complete replacement; builder work gets
productivity gain** — both happen inside the same field at once.

A warning here: now that coding is fully replaced, **the importance
of the requirements side actually rises**. **Skimp on requirements,
and AI only mass-produces "commonplace code"** that does not address
the specific business problem. AI is excellent at probabilistically
reproducing what it has seen in prior samples from the same domain,
but **pinning down "the non-negotiable conditions of this
organization's particular business"** can only be done by the human
writing the requirements.

The faster AI gets, the faster and larger the cost of sloppy
requirements piles up — a vast amount of "runs but ordinary" code
gets produced and maintenance collapses (the same vibe-coding failure
mode from Chapter 2, now faster and at greater volume). In a world
where coding is cheap, **requirements are what determine a software
system's differentiation and lifespan**.

## Other AI applications stall at the last 1%

In the reverse — **domains where the rules are not explicit, or
correctness is hard to verify** — AI does not advance at the same
speed. Missing either condition is enough to leave a stubborn last 1%.
Three representative domains:

- **Desk work** — 99% of the work (routine documents, email replies,
  meeting-minute summaries, draft research, data organization,
  translation drafts) can be handed to AI. But the last 1% — unwritten
  rules inside the organization, decisions that carry responsibility,
  subtle adjustments with stakeholders, the final judgment of whether
  to submit — determines the quality and the trust of the work.
- **Self-driving** — 99% of situations are no problem. But the
  remaining 1% — an unexpected pedestrian, edge weather judgments, a
  child's ball — is what decides between safety and death. The
  difficulty of moving from 99% to 100% is the substance.
- **Robotics** — 99% of motion (routine assembly, picking, food
  delivery, cleaning, repeated actions) can be mechanized. But the
  last 1% — unexpected object placement, handling soft items, safely
  sharing space with humans, adapting to unknown environments —
  determines real-world usability.

Look at rail — especially Japan's **Shinkansen**, where route and
obstacles are tightly controlled — a **closed system**. Almost all
normal operation can be automated. The rules are explicit; correctness
in normal operation is easy to verify. But the judgment for
**accidents and equipment failures** — derailment, defective
equipment, natural disasters — is the kind of problem that cannot be
enumerated at design time. It still falls to humans. **The last 1%
sits not in the system's openness, but in the unpredictability of
abnormal events** — no matter how closed the system, that part does
not disappear.

This "judgment in abnormal events" is structurally hard for two
reasons:

- **(1) The expansion of what must be anticipated** — enumerate one
  accident or failure, and its variants, combinations, and new
  patterns keep appearing. **The "list of cases we've thought of" is
  always incomplete**; what actually occurs in the field sits outside
  the design-time list. List more and the list grows; stop and the
  gaps remain.
- **(2) The absence of a body** — humans detect anomalies by taking
  in vision, touch, sound, smell, and vibration through the body all
  at once. AI has no body, so **cameras and sensors** have to be
  installed in its place. Each physical quantity to be sensed requires
  its own equipment; placement, power, networking, and maintenance
  costs pile up. And **what to sense in the first place is itself
  another problem of predicting abnormal events** — the anomaly you
  did not anticipate has no sensor on it.

Because (1) and (2) compound, complete replacement in the physical
world — even in a closed system — stays structurally hard.

In these domains, AI delivers enormous value **as a productivity
tool** — document drafts, driver assistance, routine work by
collaborative robots. But **complete replacement does not happen**.
There is a deep valley between "can do 99%" and "can do 100%."

The IT industry's AI narrative often overlooks — or pretends not to
see — this 99/100 valley. Every time AI comes up, lines like "solves
labor shortages across every industry" and "all white-collar work gets
automated" surface. **That is overestimation**.

This sub-series stands apart from that overestimation. **We argue
complete replacement only for one specific area — "coding" inside
software development — where the rules are explicit and correctness
is mechanically verifiable**. We do not claim the same complete
replacement at the same speed in the rest of software development or
in other domains.

> There is a deep valley between "can do 99%" and "can do 100%."
> **"Coding" inside software development** is the area that has
> crossed that valley. Most other areas (including the rest of
> software development) have not.

## The writing of this article is itself the example

Living evidence of this claim sits in **the writing process of this
sub-series itself**.

As Chapter 4 noted, this sub-series was written by one person plus AI
in about a week. But that week included a long list of human
corrections:

- "A few tens of thousands of yen a month" as the price anchor was
  corrected to **Claude Max ($200/mo ≈ ¥30,000/mo)**
- "30,000 lines" of code base was corrected to the measured **6,000
  lines**
- The **abacus (soroban)** was added as the primary example alongside
  the human computer
- The calculator transition was corrected from "decades" to
  **"roughly a decade"**
- Chapter 1 added the **"IT revolution completing"** framing
- The origin of multi-tier subcontracting was correctly attributed to
  **"large coder head-count demand"**
- Chapter 10 added the **"physical goods become scarcer than
  software"** section
- This chapter's scoping — **"complete replacement is only in
  coding"** — was added

All of these are **corrections produced by a human reading the AI's
draft and judging**. AI alone lets factual errors, slanted arguments,
and tonal slips — exactly the kind of problems that cost a reader's
trust — pass through. The level of this sub-series **required human
judgment, in every loop**.

In other words, the writing process of this sub-series carried **the
same structure as desk work, self-driving, and robotics** — AI writes
most of the draft; the human holds judgment and correction.
**Productivity multiplies several times, but complete replacement
does not happen**.

> "Coding is complete replacement; writing is productivity gain" —
> the claim of this sub-series and the writing process of this
> sub-series line up in the same structure.

## The five-year horizon

The "few years" of this sub-series — fix the concrete time scale here.
**The main changes complete in about five years** — that is the
outlook of this book.

Why five? Several independent time scales converge in that band:

- **The AI capability curve** — crossed the threshold in 2024-2025
  (Chapter 1). Capability-wise, transition is already feasible.
- **The customer learning curve** — it takes a few years for
  customers to learn to pair with AI (Chapter 5). It is moving now.
- **The contract-renewal cycle** — SIer long-term maintenance
  contracts typically run 3-5 years. The next renewal becomes the
  evaluation window for replacement (Chapter 8).
- **The pace of multi-tier shrinkage** — without internal employment
  adjustment, shrinkage on the order of a few years is achievable
  (Chapter 10).
- **The historical calculator/abacus transition** — completed in
  about ten years from the 1972 Casio Mini (Chapter 3). The AI shift
  is faster than that.

The band where these overlap is **roughly five years**. Not so slow
that it deserves "ten years," not so fast that it deserves "one to
two." **The main changes complete in about five years** — that is
the concrete time-scale outlook.

But "five years" refers only to the main changes, not everything.
Core-system replacement in regulated industries takes longer. Some
areas will still hold old models after ten years. Even so, **the
mainstream of the industry moves to AI-native within about five years**.

## The transition is irreversible

Finally, confirm the **irreversibility** of the change.

- Once a customer has experienced AI-native in-house development,
  they do not go back to SIer commissioning (Chapter 5) — the
  learning cost has been paid already
- Once an SIer has shrunk its multi-tier subcontracting, it does not
  hire subcontractors back at scale (Chapter 10) — the contracts that
  were closed do not re-form
- Once the builder is recognized as a profession, that role
  definition persists (Chapter 9) — what moved into the position of
  lawyer and doctor does not move back
- The fact that AI generates standard code at low cost does not
  change — the structure of "top-tier coding for $200/month" remains
  in place (Chapter 1)

Each piece moves only in one direction. So the chain as a whole moves
in one direction. **Once the chain starts, no structural force exists
that stops it**.

One historical comparison to keep in view. The invention of the
printing press in the 1450s reshaped the structures of the church,
the university, and the state **over two hundred years** — preparing
the ground for the Reformation, the scientific revolution, and the
modern nation-state itself. The LLM holds **incomparably greater
intensity**. What the printing press democratized was **reading**
(access to existing knowledge); what the LLM democratizes is
**making** (knowledge generation, judgment, implementation). There
is no wall of literacy to clear first; natural language works for
anyone. The speed of diffusion is on a different order — what took
the printing press decades, the AI era achieves **in years**. Read
against this difference in intensity, the five-year horizon this
sub-series draws is, if anything, **a conservative estimate**.

> The change completing in five years is irreversible.
> It is driven by one-way forces only, so a rewind cannot happen
> structurally.

## The free person of the Middle Ages, and the free person of the AI era

When the medieval European "free person" emerged out from under
feudal lords, four conditions came together at once.
**Economic autonomy** (the free farmer who tilled his own land,
the urban citizen, merchant, and craftsman who traded
independently), **political self-governance** (the free cities that
won their charters from lords), **the means of touching reality**
(the right to bear arms, the capacity to grow one's own crops),
and **education** — the seven liberal arts.

The conditions that converge as the AI-era "free person" — the
builder of this sub-series — stands up correspond one-to-one.

| Dimension | Medieval freedom | AI-era freedom |
|---|---|---|
| Economic autonomy | One's own land, independent trade | Building one's own back office and software with a few-thousand-yen-a-month AI; exiting SaaS and SIer dependence |
| Political self-governance | Free cities that wrested charters from lords | Holding one's own data, judgment, and systems on one's own machine; exit from cloud-vendor dependence |
| Means of touching reality | Bearing arms, growing one's own food | Local LLMs, open source, one's own server; infrastructure that keeps running through blackouts and network outages |
| Education | The seven liberal arts | The contemporary liberal arts — judgment, verbalization, logic, systems thinking, ethics (Chapter 4) |

Just as the medieval liberal arts could not stand on education
alone, the contemporary liberal arts cannot stand by themselves
either. **A free person comes into being only when all four
converge**. And just as the free citizens of medieval cities formed
**guilds** to strengthen their economic and political weight, the
AI-era builders will move, as **a profession that sells judgment**,
toward bar-association– and medical-society–like **guilds of their
own** (Chapter 9).

### Employment is the AI era's serfdom — the rise of self-employment is structural

Placed next to the "medieval free person," one more thing becomes
visible — **modern employment (the salaried worker) sits, structurally,
in the same position as the medieval serf**.

| Dimension | Medieval serf | Modern employee |
|---|---|---|
| Ownership of the means of production | Lord's land and tools | Employer's office, equipment, IP, data, infrastructure |
| Self-determination of labor | Cultivating at the lord's direction | Working at the supervisor's direction |
| Freedom of movement | Tied to the land | Tied by employment contract, mortgage, in-company career |
| Income predictability | Stable under the lord's protection | Trading freedom for salary stability |
| Locus of judgment | The lord | The employer |
| What is received in exchange | Food and protection | Salary and benefits |

The "stability of employment" and the "stability of serfdom" are
**the same trade-off, structurally** — handing over the right of
self-determination in exchange for predictability of survival. This
is not a claim of moral equivalence (modern employment has legal
protections and contractual freedom). It is an analytical
observation that **on the three axes of ownership, judgment, and
mobility, the structure matches**.

And the reasons employment **stops fitting in the AI era** are
structurally clear:

1. **The means of production are now individually ownable** —
   a few-thousand-yen-a-month AI, local LLMs, open source, one's
   own server. The employer no longer needs to monopolize them.
2. **One person + AI = a ten-person team** (Chapter 4) — the
   payoff of concentration disappears.
3. **The boundary between judgment and execution closes within
   one person** (Chapter 4) — the overhead of aggregation,
   coordination, and management becomes pure waste.
4. **Judgment-centered professions are intrinsically inclined to
   independence** — lawyers, doctors, accountants prefer solo
   practice and partnerships not by accident (Chapter 9).

**The rise of self-employment is not a policy or lifestyle
question. It is structural necessity**. The same structure under
which medieval free citizens, free farmers, and craftsmen were all
"self-employed" returns in the AI era.

> Employment is the contemporary form of medieval serfdom.
> **Self-employment is the contemporary form of being a free person.**

The structural changes this sub-series has been arguing — the
SIer commission model's structural uneconomy (Chapter 6), customers
building for themselves (Chapter 5), the judgment-centered builder
(Chapters 4 and 9), the error of the "specialized engineer" advice
(this chapter) — all converge on one point: **the industry
structure organized around employment is reshaped in the AI era**.

### The middle layer — builders who hold physical reality

Between the pure-software free person (the builder of this
sub-series) and the pure-physical free person (of the natural-
farming series), a **middle layer** that bridges the two rises up.

The medieval world had the same layer — the stonemasons, carpenters,
smiths, weavers. They held guilds, had work in both city and
countryside, and **kept a foot in both the city's self-governance
and the soil's reality**. It was precisely this craft layer that
accumulated the technical capital the Renaissance was built on.

The middle layer of the AI era sits in the same structural place —
**inputs from physical reality** (sensors, observation, material),
**outputs in physical reality** (objects, harvests, repaired
machines, buildings), with AI as the **mediator** doing the design
and analysis, while the hand that touches reality remains a human
hand. Who belongs here:

- **Makers and digital fabrication** (AI design + 3D print, laser,
  CNC)
- **Embedded engineers and robotics designers** (microcontrollers,
  PLCs, ROS2)
- **Precision agriculture and agritech** (sensors, drones, local
  LLMs running in the field)
- **Manufacturing-floor technicians** (having AI rewrite the factory
  automation)
- **Physicians using AI imaging and diagnostics; mechanics and
  repair technicians**
- **Carpenters, architects, craftspeople using AI design tools**

Chapter 9's "**maker types and field technicians enter embedded**"
was precisely about new entry into this middle layer. The labor
demand created by "**physical goods become scarcer**" (Chapter 10)
will be absorbed here too — the coders flowing out of the SIer
industry won't all rejoin pure software; a path **sideways into
the middle layer** opens here as well.

> The middle layer is the contemporary form of those who **gain
> power by touching reality**. The strongest form of the AI-era
> free person appears here.

Japan, with deep manufacturing, town-factory, natural-farming,
electronics-tinkering, and repair-culture foundations, holds a
**structural advantage** in the move to this layer. As the
**alternative path** to the "become a specialized engineer" advice
in the next section, this gives us a second route alongside
"sideways onto the liberal arts": **"sideways into builders who
hold physical reality."** Both are roads out of the lord's manor.

### "Become a specialized engineer" misreads the structure

There is a widely circulated piece of advice — "in the AI era,
become a specialized engineer, hold a deep specialty AI cannot
take, like security or ML." It **misreads the structure**.

What AI is absorbing is **the whole layer** of software engineering,
not a particular subdomain inside it (Chapters 1 and 3).
**Going deeper into a specialty only shifts the date by which the
specialty itself is overtaken** — the underlying structure does
not change. The medieval analogue would be telling a serf, "become
a more specialized serf and you will be free." Freedom does not
come from going deeper into the specialty; it comes from **stepping
out of the lord's structure of control**.

The path to becoming a "free person" of the AI era is the same.
The right move is not to deepen within engineering. It is to step
sideways onto the **liberal-arts axis — judgment, verbalization,
ethics, systems thinking**. That is the structurally correct
direction of motion.

> The road to becoming a free person is not deeper specialization.
> It is **stepping out of the lord's structure of control**. The
> AI era is no different.

## This is the beginning of the Second Renaissance

The structural change this sub-series has been tracking — from
coder to builder, from software engineering to the liberal arts,
from employment to self-employment, from the lord's manor to the
free city, from pure software to a middle layer that holds physical
reality — lines up, item for item, with the structural change of
the **First Renaissance (14th–17th centuries)**.

| Element | First Renaissance | Second Renaissance (AI era) |
|---|---|---|
| The classics being recovered | Greek and Roman classical learning | The liberal arts (Chapter 4) |
| The polymath ideal | Leonardo da Vinci | The builder, one person + AI (Chapter 4) |
| Individual subjectivity | The humanist "I" | One's own tools, one's own data, one's own judgment |
| Vernacular liberation | Dante's Italian, Luther's German | Natural language becomes "the programming language" |
| Free cities and guilds | Florence, Venice, the craft guilds | The AI-era free person, professional guilds (Chapter 9) |
| The accelerator | The printing press (1450s) — democratizing **reading** | The LLM — democratizing **making** (this chapter) |
| Reformation | Religious decentralization (against the Roman church) | Anti–vendor-concentration, anti–employment-centric, anti-SIer (this book) |
| The new rising class | The bourgeoisie (commerce, banking, manufacturing) | The AI-native builder, the self-employed judgment professional |
| New forms of art | Perspective, anatomy, naturalism | AI-assisted creation under human judgment |

Nine items, all corresponding. This is not metaphor — it is
**structural similarity**.

And just as the First Renaissance did not begin one morning — the
self-governance of 12th–13th-century cities, the formation of the
guilds, scholastic philosophy, and the rediscovery of classical
texts through the Crusades accumulated as the underlying ground,
which the printing press of the 1450s **accelerated** — the Second
Renaissance is following the same pattern. The personal computer,
the Web, open source, maker culture, the revival of natural and
organic farming, the data-sovereignty movement, the AI ethics
conversation have accumulated as the ground; **the LLM (from 2022
onward) is now the accelerator**.

> The five-year structural transition this sub-series describes is
> **one cross-section of the Second Renaissance**. The sub-series
> covered the software domain, but the same structural change is
> proceeding in other domains of life at the same time.

### The AI revolution is the completion of the IT revolution

Treating "the AI revolution" as a new, separate revolution is another misreading. **The AI revolution is the completion of the IT revolution** — seventy years of the IT revolution finally fulfilling its original promise.

The IT industry, until now, has had **humans hand-writing the code that automates work**. The original IT promise was "computers do the work, humans are freed." Yet for seventy years, **the side that implements the automation has been doing it by hand** — a strange structure. The consequences: programmer became one of the highest-paid professions; the cost of automation often exceeded the cost of doing the work manually; a massive industry of "manual labor for automation" emerged — SIers, consultancies, SaaS.

Logically odd. **If automation is the goal, making the automation should also be automated.** The LLM dissolves the twist by writing the code itself. **The AI revolution is not the beginning of a new revolution; it is the completion of the IT revolution.**

The completion functions as the strongest accelerator of the Second Renaissance. SIer contraction and the software-engineer → builder replacement are **inevitable consequences**, not sudden shocks.

### The LLM is a powerful statistical-processing tool, not a superintelligence

Coolly viewed, the LLM (Claude, GPT, Gemini, etc.) is **large-scale statistical processing of data** — predicting the most probable next token in context. An overwhelmingly powerful tool, but it is not, in itself, "superintelligence."

The pitch that "AGI is coming, white-collar work will be fully automated in 12–18 months" (Suleyman/Microsoft AI) **deliberately stages the LLM as a superintelligence parable** to push "hand judgment over to AI" and "buy Copilot."

Structurally wrong: statistical-processing tools cannot bear judgment or responsibility. The LLM makes **writing, looking up, organizing** orders of magnitude faster, but **deciding what to build, evaluating whether it is right, taking responsibility** stay on the human side. This is the **logical basis of the builder role**.

Read the AI revolution as "**the tool got strong, so the human role shifts to the judgment side**" — simple, structurally clear, no need for AGI mysticism. The SIer contraction, the builder's rise, the foundational shift from software engineering to the liberal arts — all are explained by this simple structure.

> The LLM is a powerful statistical-processing tool, not a superintelligence.
> **Judgment and responsibility stay with the human** — this is the
> logical ground beneath every argument in this sub-series.

### Apps do not disappear, the way of making them does — app-making comes to resemble film-making

Stated precisely, the structural change is this: **software development as an engineering craft disappears, but apps do not disappear**.

The most precise analogy is film-making. A film is made by many independent specialist roles coming together (cinematography, editing, sound, lighting, costume, set design, VFX, scoring, acting). The audience is not aware of any of these. **Only one artifact — the film — appears.** At the center are not the people handling each technical task, but the **director and the screenwriter** — those who carry creative judgment.

App-making in the AI era takes on the same structure.

| Film-making | AI-era app-making |
|---|---|
| Director — overall vision and judgment | Master builder / user — judging what to build |
| Script (manuscript) — natural language | Natural-language source — what, for whom, how it behaves |
| Cinematography, editing, sound, VFX — specialist crew | AI — picks up the engineering layer as a whole |
| Cast, set, costumes | AI-generated UI, logic, data structures |
| The film (artifact) | The app (artifact) |

**A director does not learn the camera. A screenwriter does not learn lighting. The audience does not know how the film was made.** Even so, the film exists and carries value. App-making takes the same shape — the user does not learn engineering, AI picks up the engineering work, end users do not know how it was made; apps still exist.

Just as the printing press eliminated the scribe but not the book, the LLM shrinks the software engineer but not the app. **Only the way of making changes** — and the new way is closer to film-making than to book-printing.

> Engineering-as-craft for software disappears; apps do not.
> **App-making comes to resemble film-making** — creative judgment at
> the center, with technical crew (= AI) gathered around it.

Film-making, however, has an enormous range. **A Hollywood blockbuster still requires massive crews, hundreds of millions of dollars, and years of work**, while **a YouTube video can be made by one person with a smartphone in a few hours**. AI-era apps will have the same range.

| Scale | Video production | AI-era app-making | Built by | Trend |
|---|---|---|---|---|
| Monolithic large-scale | Hollywood blockbuster | SIer mega-project ERPs, monolithic core enterprise systems | (formerly SIer) | **Declines** — decomposed into mid-scale |
| Mid-scale | Streaming series, theatrical film | Focused systems, specialized SaaS, industry-wide systems | **Master builder** | **Grows** — more apps, fewer workers per app |
| Personal | YouTube, TikTok | Everyday personal tools | The user | **Explodes** |

**Monolithic large-scale is structurally a poor fit for the AI era** — no single master builder can hold the whole, lock-in is created (Chapter 8), maintenance is intractable, the chain of judgment is dispersed. These systems are decomposed into combinations of mid-scale focused systems.

**Mid-scale is the master builder's home territory** — the scale at which the chain of judgment closes within one person (Chapter 4), the same position as lawyers and doctors (Chapter 9). Mid-scale apps themselves **do not shrink — they grow**: business apps that previously could not be cost-justified now get built in large numbers.

**Personal is the user as director and crew**.

What declines, then, is **not the number of apps but the total number of workers building them** (especially the monolithic SIer-project labor model). Apps themselves continue to exist across all three scales, and grow at mid-scale and personal.

This is the most precise statement of the structural change this sub-series has been arguing — the SIer labor model shrinks dramatically, master builders thrive **at mid-scale as the directors of the AI era**, and the personal scale is **absorbed into the user**.

### Not only the AI revolution

We have been calling this "the AI era," but trying to capture the current structural change through AI alone **misses half of it**. The transitions running in parallel:

- **The end of fossil resources** — collapse of the premises of oil-dependent society (Structural Analysis 02, 14)
- **Geopolitical multipolarity** — the end of US unipolarity, Trump, Ukraine, Iran, China
- **A generational shift in defense industry** — large platforms → drones + AI (Structural Analysis 11)
- **The reconstruction of agriculture** — limits of chemical fertilizer; rise of regenerative agriculture (Structural Analysis 03)
- **Collapse of finance and trade premises** — dollar standard, global supply chains
- **Simultaneous breakdown of demographics, cities, healthcare, and pensions** (Structural Analysis 11)
- And the **AI revolution** — the **accelerator** for all of the above

Just as the First Renaissance had to be understood as a **composite** of the printing press, the age of discovery, the Reformation, the scientific revolution, the rise of the nation-state, the rise of the commercial bourgeoisie, and the labor shifts after the Black Death, the Second Renaissance cannot be captured by **the AI revolution alone**. Multiple independent transitions converge; their convergence point is what makes "an era that is no longer the same." AI is the strongest accelerator among them, but not the cause of all.

### An age of creation, and an age of upheaval

The Renaissance is in textbooks as a luminous age of creation — Leonardo, Michelangelo, Galileo, Gutenberg. The same age was also an **age of violent upheaval**: the Reformation and the wars of religion (the Thirty Years' War cut Central Europe's population by ~30%), papal corruption and schism, recurring plague, populist demagogues like Savonarola staging the "bonfire of the vanities" in Florence, strongman politicians like Cesare Borgia who became Machiavelli's model in *The Prince*. **While the old order is collapsing and the new one has not yet stood up, people seek refuge in strong men and extreme words.**

The Second Renaissance's upheaval side is already unfolding. **Trump** is the canonical figure — direct attack on the expert class, judiciary, scientific consensus; ad-hoc swings on tariffs, immigration, science budgets; streams of executive orders that override congressional checks; "I decide everything alone" governance.

Placed next to Nadella's Copilot strategy, the structure becomes visible. **Nadella concentrates corporate judgment into a single AI; Trump concentrates national judgment into a single president.** Different means, but both **push the old era's logic of judgment-concentration to its absolute limit** (see [Microsoft's Nadella and Hegel's Philosophy](/en/blog/nadella-hegel-cunning-of-reason/)).

Just as the Renaissance-era populist demagogues in the end disappeared, figures pushing judgment-concentration to the extreme will not fit the new structure (distribution, the free person, judgment held by the individual) and will exit. But the interim is turbulent — this too is the same pattern as the First Renaissance.

> The Renaissance is an age of creation and an age of upheaval at the same time.
> Looking only at the creation side misreads the era. The upheaval side
> — Trump, Nadella, the runaway concentration of judgment — is also a
> symptom of the same transition. Both sides must be read together.

## In closing

Compress the conclusion of the Software sub-series, all eleven
chapters, into one passage here.

**AI has reached human-top execution capability. This happened
because the domain has explicit rules and verifiable correctness. As
a consequence, the role called "coder" (the role centered on coding)
goes away, and the builder (the judgment-side role) takes its place.
The SIer commission model cannot structurally hold, and within
roughly five years, the mainstream of the industry moves to AI-native
in-house development — irreversibly.**

But this is the story of one specific area: **"coding" inside
software development**. The other parts of software development
(requirements, design, operations, incident response, stakeholder
coordination) carry the same structural 1% problem as self-driving
and Shinkansen — this is where the builder remains. And the same
speed of complete replacement is not claimed for other domains either
(desk work, self-driving, robotics). In those, AI operates as a
productivity tool — it does not reach complete replacement.

And during the same few years that AI advances, **society as a whole
moves toward physical goods becoming scarce** (Chapter 10). AI
data-center construction, manufacturing reshoring, the shift to
natural farming — all generate physical-labor demand. Coders flowing
out of the SIer industry are absorbed both inside and outside the
industry.

What aiseed.dev has argued across the eleven chapters of this
sub-series is:

**A structural transition centered on "coding" inside software
development completes in roughly five years. The transition is
irreversible. And the conclusions from this specific area (= coding)
must not be casually extended to the rest of software development or
to other domains**.

And the other current named in Chapter 4 — **the foundational
discipline of the technical profession shifts from software
engineering to the liberal arts**. Because what AI has taken is the
core of software engineering (algorithms, languages, frameworks,
design patterns), what remains on the human side is judgment — the
craft of logic, verbalization, ethics, systems thinking, and history
that the liberal arts have always been. The medieval *artes
liberales* were defined as **the arts of the free person — one who
is not enslaved**. The builder is **the person who does not hand
judgment over to AI** — the contemporary form of that craft.

Hold those four, and the IT industry's AI narrative no longer sweeps
you along. You can read what is actually happening, structurally,
calmly. And from the position you stand in — customer commissioning
software, coder, builder candidate, SIer executive — you can decide
what to do over the next few years.

Thank you for reading to the end.

aiseed.dev will continue to publish articles that read the structure.

---

## Related articles

- [Chapter 1: AI Solves the World's Hardest Coding Problems](/en/ai-native-ways/software/coder-top/)
- [Chapter 3: The Coder's Job Goes Away](/en/ai-native-ways/software/coder-end/)
- [Chapter 4: The Builder Role](/en/ai-native-ways/software/builder/)
- [Chapter 10: Japan's SIer Industry Transition and Labor Mobility](/en/ai-native-ways/software/japan-transition/)
- [Phosphorus Depletion and Natural Farming](/en/phosphorus-and-farming/)
- [Structural analysis 08: Subtracting the enterprise-IT tax](/en/insights/enterprise-tax/)
- [Structural analysis 12: AI and the sole proprietor](/en/insights/ai-and-individual/)
