---
slug: coder-top
number: "01"
lang: en
title: AI Has Reached Human-Top-Class Capability in Writing Code
subtitle: Codeforces 2700 tier — the world's top coding ability, for $200 a month on Claude Max
description: AI's code-writing ability has matched human top-class on public competitive-programming ratings. Two facts matter — the capability level reached, and the fact that anyone can access it via Claude Max for around $200 a month. The whole sub-series argues outward from those two.
date: 2026.06.01
label: Software 01
title_html: AI now sits on the side<br>that solves <span class="accent">the hardest problems</span>.
prev_slug:
prev_title:
next_slug: maintenance-shift
next_title: Maintenance-Phase Shift Is the Real Story
---

# AI Has Reached Human-Top-Class Capability in Writing Code

**Start with one fact — AI now sits on the side of the table that solves
the world's hardest coding problems**.

The parent series' prologue made the case that AI's native tongue is
Python and Markdown-shaped text. This sub-series goes one step further —
not the question of language, but the question of **capability level**.
Once AI's code crosses a certain threshold, the structure of software
development itself rearranges. This chapter establishes where that
threshold sits.

## Competitive-programming rating as a yardstick

There is exactly one mechanism in the world that **assigns objective
numbers to coding ability**: the public ratings of competitive
programming. Codeforces, AtCoder, ICPC — all of them accumulate, over
years, whether you can solve set problems in time, how many you solve,
and how correct your solutions are. Each participant ends up with a
number.

Codeforces rating bands distribute roughly like this:

| Band | Title | Participant position |
|---|---|---|
| Below 1200 | Newbie | Beginner |
| 1600–1899 | Expert | Top ~10% |
| 2100–2399 | Master | Top few percent |
| **2400–2599** | **International Grandmaster** | **~Top 1%** |
| **2600 and above** | **Legendary Grandmaster** | **A few dozen worldwide** |

The numbers have **threshold steps** baked in. The gap between 1500 and
1800 closes with study. **The gap between 2400 and 2700 does not close
with study alone** — past that point you need speed, design intuition,
a nose for the hardest problems. The world's top sits between roughly
2700 and 3900, and contains around fifty people.

> This is the one place in the world where coding ability is compared by
> number. And here, the bands you can reach by study and the bands you
> cannot are clearly separated.

## AI has reached the 2700 tier

Through late 2024 and into 2025, the situation changed. OpenAI's
publicly reported estimated Codeforces rating for the o3-series models
came in at **around 2727** (announced at the o3 launch). Google
DeepMind's AlphaCode 2, a step before, demonstrated top-15% Codeforces
performance, and later research models have pushed further. Anthropic
has reported continuous improvement in coding ability for the Claude
family.

There is room to argue about the numbers and how they are measured, but
**the fact that AI has entered the 2700 tier** is now confirmed by
multiple independent announcements moving in the same direction. This
is not "useful assistant now"; it is **"sitting on the side that solves
the hardest problems."**

What matters is not the rank, but the **structural change of crossing a
threshold**.

- Up to 2400 is "a strong specialist can reach this with enough drill."
- 2700 is "fewer than a few dozen people in the world."
- AI entered that tier **via a different path** than the one human
  competitors climb.

For a human to reach this band requires thousands of hours of practice
starting young, and then passing a talent filter on top. AI got there
**without taking that path**. The earlier objection — "but the training
data contained the same problems" — no longer holds; Codeforces runs
live contests with **fresh problems**, and AI models have repeatedly
been observed returning 2700-tier solutions there.

> A band humans reach **one person at a time, over a decade-plus**, was
> entered by AI **all at once, by multiple paths**.

## $200 a month buys access to the world's top

This is where the sub-series' argument starts.

The paths to access top-tier coding ability used to be narrow — be
hired by Google, Meta, or Anthropic; spend years climbing the
competitive-programming ladder; or pay seven-figure salaries.
**Capability above the threshold was a scarce resource**. Palantir's
FDE (Forward Deployed Engineer) model — embedding top-tier engineers
inside the customer's organization on year-long, eight-figure contracts
— is the extreme upper end of that legacy path (mechanics covered in
detail in Chapter 8).

Access to AI models comes in tiers, depending on how hard you intend
to use them.

- **Chat-grade use** — Claude Pro / ChatGPT Plus / Google AI Pro at
  around $20 a month. **Not enough for serious coding**, though — you
  run into usage limits, context length, or model selection before
  long.
- **Coding-grade use** — **Claude Max ($200 a month)** is the current
  standard anchor. It lets Claude Code, Cursor, and IDE integrations
  call Sonnet and Opus at production volumes; a builder can have AI
  writing code for eight hours a day without hitting the wall.
- API pay-as-you-go — wiring the same usage through the API directly
  lands in the same few-hundred-dollars-a-month range. The Max
  subscription is essentially that invoice averaged out.

In other words, **the world's top-tier coding ability is reachable for
$200 a month**. One credit card and one browser, and you can start the
same day.

```mermaid
flowchart LR
  Top["World-top<br/>coding ability<br/>(Codeforces 2700+)"]

  subgraph Legacy["The old path"]
    direction TB
    H1["Get hired by a global tech firm"]
    H2["Pay seven-figure salaries"]
    H3["Compete for a few dozen people"]
  end

  subgraph Native["The AI-native path"]
    direction TB
    N1["Subscribe to Claude Max ($200/mo)"]
    N2["Access starts the same day"]
    N3["No headcount limit"]
  end

  Top ==>|reaches few people| Legacy
  Top -.->|reaches anyone| Native

  classDef good fill:#e8f5e9,stroke:#7a9a6d,color:#3a4d34
  classDef bad fill:#fef3e7,stroke:#c89559,color:#5a3f1a
  class Native good
  class Legacy bad
```

This is not "prices dropped." **The very axis of pricing changed**.
Before: scarce capability multiplied by large fixed cost. Now:
comparable capability multiplied by something close to zero marginal
cost. The two are not the same spreadsheet at two prices; they are
**different supply curves**.

> Top-tier coding used to be a **scarce resource of a few dozen people**.
> It is now a **$200-a-month subscription**.

## This is where the IT revolution actually completes

What the facts above describe — top-tier coding ability reaching anyone
for $200 a month — is not just "AI got faster" or "AI got useful." It
is the moment in which **what has long been called the "IT revolution"
finally completes**.

Look at what the term "IT revolution" named, in structural terms.

- Industrial revolution — production of physical goods moved from
  human hands to machines.
- First wave of computing — calculation moved from human hands
  (abacus, human computers) to machines.
- "IT revolution" — business processing moved from paper and pen to
  software.

In the first two, the core of the revolution (mechanization,
automation) reached the object of the revolution fully. **The third
did not**. Software itself was still being written by human hands.
The revolution's tool (software) kept being produced by hand-labor —
which means the revolution's core had not yet reached the production
of its own tool. What was called the "IT revolution" was, in fact, an
**incomplete form of revolution**.

The industrial-revolution parallel: the power loom exists, but the
loom's own parts are still hammered out by hand at the blacksmith's.
The revolution's loop does not close **until production of the tool
itself is mechanized**.

Now that AI has taken execution completely, the loop finally closes.
**The act of producing software is itself taken over by machines**.
The revolution's tool is built by the revolution's own process. That
is what "the IT revolution actually completing" means.

> The decades called "the IT revolution" were a revolution that
> **mechanized business using software**.
> What is happening now is **the revolution that mechanizes the
> production of that software itself** — the revolution's core
> finally reaching the revolution's own tool.

With that frame, the changes this sub-series covers — the coder role
ending, the structural uneconomy of the SIer model, the order-of-
magnitude price gap, the rearrangement of employment and industry —
read not as isolated phenomena but as **a long-delayed revolution
finishing the work it had left incomplete**.

## Everything else in this sub-series follows from one fact

Every chapter that follows is **deduced** from this one fact.

- Chapter 2 — once the coding itself becomes cheap, where does the
  **unit of maintenance** move?
- Chapter 3 — what happens to roles whose center is "writing code"
  (coders)?
- Chapter 4 — what role takes their place (the builder)?
- Chapter 5 — when customers themselves pair with AI, what happens to
  the structure of outsourcing?
- Chapter 6 — can the SIer commission model compete with **AI sitting
  above the threshold**?
- Chapter 7 — when one side has a different cost structure entirely,
  how large is the gap?
- Chapter 8 — where do existing commission relationships act as
  **lock-in**?
- Chapters 9–11 — hiring builders, the transition of the SIer
  industry, the time horizon over which the transition completes.

These are not independent observations. They all derive from one point:
**top-tier coding ability is available for $200 a month**. This chapter
exists only to plant that point.

One more frame for what follows. This sub-series covers **structural
change inside software development**. It does not entertain the extreme
positions — "leave everything to AI, humans aren't needed" or "AI has
no creativity, so the impact is bounded." The practical question, the
one this sub-series answers chapter by chapter, is: **once AI above the
threshold has been in the market for some years, how do the commissions,
the outsourcing, the employment, and the prices of software development
rearrange?**

> Compressed to one line, this is the sub-series:
> **if top-tier coding costs $200 a month, the outsourcing-centered
> structure of software development can no longer hold**.

The next chapter takes up what is, structurally, the most overlooked
consequence of cheap coding — the shift in the unit of maintenance.

---

## Related articles

- [Prologue: AI's Native Tongue Is Python and Markdown-Shaped Text](/en/ai-native-ways/prologue/)
- [Chapter 11: Verifying Narratives with AI](/en/ai-native-ways/verify-narratives/)
- [Structural analysis 08: Subtracting the enterprise-IT tax](/en/insights/enterprise-tax/)
- [Structural analysis 12: AI and the sole proprietor](/en/insights/ai-and-individual/)
