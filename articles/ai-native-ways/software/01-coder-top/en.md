---
slug: coder-top
number: "01"
lang: en
title: AI Has Reached Human-Top-Class Capability in Writing Code
subtitle: Codeforces 2700 tier — the world's top coding ability, for a few tens of dollars a month
description: AI's code-writing ability has matched human top-class on public competitive-programming ratings. Two facts matter — the capability level reached, and the fact that anyone can access it for a few tens of dollars a month. The whole sub-series argues outward from those two.
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

## A few tens of dollars a month buys access to the world's top

This is where the sub-series' argument starts.

The paths to access top-tier coding ability used to be narrow — be
hired by Google, Meta, or Anthropic; spend years climbing the
competitive-programming ladder; or pay seven-figure salaries.
**Capability above the threshold was a scarce resource**.

The paths to access AI models look like this today:

- Claude Pro / ChatGPT Plus / Google AI Pro — **about $20 a month**
- Claude / OpenAI / Google APIs — pay-as-you-go, a few cents per
  ~10,000 tokens
- Most IDE integrations (Cursor, Claude Code, Copilot) call the same
  models on your behalf

In other words, **the world's top-tier coding ability is reachable for
a few tens of dollars a month**. One credit card and one browser, and
you have access within minutes.

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
    N1["Subscribe for tens of dollars a month"]
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
> It is now a **subscription costing tens of dollars a month**.

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
**top-tier coding ability is available for a few tens of dollars a
month**. This chapter exists only to plant that point.

One more frame for what follows. This sub-series covers **structural
change inside software development**. It does not entertain the extreme
positions — "leave everything to AI, humans aren't needed" or "AI has
no creativity, so the impact is bounded." The practical question, the
one this sub-series answers chapter by chapter, is: **once AI above the
threshold has been in the market for some years, how do the commissions,
the outsourcing, the employment, and the prices of software development
rearrange?**

> Compressed to one line, this is the sub-series:
> **if top-tier coding costs tens of dollars a month, the
> outsourcing-centered structure of software development can no longer
> hold**.

The next chapter takes up what is, structurally, the most overlooked
consequence of cheap coding — the shift in the unit of maintenance.

---

## Related articles

- [Prologue: AI's Native Tongue Is Python and Markdown-Shaped Text](/en/ai-native-ways/prologue/)
- [Chapter 11: Verifying Narratives with AI](/en/ai-native-ways/verify-narratives/)
- [Structural analysis 08: Subtracting the enterprise-IT tax](/en/insights/enterprise-tax/)
- [Structural analysis 12: AI and the sole proprietor](/en/insights/ai-and-individual/)
