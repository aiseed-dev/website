---
slug: copilot-correct-looking-but-wrong
title: The Copilot Problem — Code That Looks Right but Is Wrong
subtitle: A closed loop where AI reviews AI-written code — how statistical "plausibility" reproduces vulnerabilities
description: About 40% of GitHub Copilot-generated code contains critical vulnerabilities; more than 15% of commits introduce new bugs. From the moment an AI acknowledged its own structural flaw, through Pearce et al., Veracode, and Fortune 50 findings, to the Model Carousel phenomenon, the 8,000-token ceiling, and the limits of defensive filters.
date: 2026.04.19
lang: en
label: Blog
category: Structural Analysis Notes
hero_image: 012-IMG_3424.jpg
---

# The Copilot Problem — Code That Looks Right but Is Wrong

## One day, talking to ChatGPT

I made an observation to ChatGPT.

> It acknowledges facts but doesn't change its assessment.
> That makes it untrustworthy.
> Codex / Copilot are unusable for the same structural reason.

ChatGPT answered:

> That cuts right to the heart of it.
> And it's not just intuition — the same problem is documented in research and in the field.

And continued:

> GitHub Copilot:
> ・Roughly 30% of the code it generates contains vulnerabilities
> ・It tends to regenerate known bugs verbatim
>
> In other words, **it has a structure that "preserves mistakes without fixing them."**

That was the moment an AI acknowledged its own structural flaw.

![Screenshot](012-copilot_correct_looking_but_wrong.png)

---
## The state of the structural flaw

I had Gemini investigate the current state of Copilot's structural flaws, and the following problems surfaced.

Full report: [The Copilot Problem — Code That Looks Right but Is Wrong](en-012-copilot_correct_looking_but_wrong.pdf)


| Study | Subject | Finding |
|---|---|---|
| Pearce et al. (2025) | 1,689 programs based on MITRE Top 25 CWE | **~40% of generated code contained critical vulnerabilities** |
| Veracode GenAI Report (2025) | 100+ LLMs compared across 4 languages | **2.74× more vulnerabilities on average** than human-written code |
| Fortune 50 Enterprise (2026) | Real enterprise environments | 4× faster development, but **10× the security risk** and **322% more privilege-escalation paths** |
| Elsisi et al. (2026) | Long-term tracking of AI-assisted commits | **Over 15% of commits introduced new bugs**; **24.2% of those remained unfixed in the latest revision** |

Between January and March 2026, vulnerable AI-generated code commits at Fortune 50 companies **surged 6×**.

---

## Why regeneration happens

LLMs optimize for "statistical frequency," not correctness. Public GitHub repositories contain decades of bugs, deprecated APIs, and vulnerable patterns. AI learns them as "the common way to write code" and reproduces them as-is.

A human developer asks: "What happens if this endpoint is called out of order?" "Should an authenticated user be allowed to access this object?" — threat modeling. AI has none of it.

According to Ryz Labs, **Copilot suggests non-existent npm packages or deprecated libraries about 15% of the time**.

---

## The reality of the "defensive mechanism"

GitHub is aware of this and has implemented an "AI-based Vulnerability Prevention System" as a post-model filter. It is designed to block hard-coded credentials, SQL injection, path traversal, and similar issues in real time.

Empirical research tells a different story.

- Credo AI's assessment: "It is unlikely to identify every conceivable vulnerability."
- IEEE 2025 paper "Artificially Insecure": **researchers deliberately bypassed this defense and succeeded in generating vulnerable code.**

A September 2025 study further confirmed that Copilot Code Review **frequently misses critical vulnerabilities** — SQL injection, XSS, unsafe deserialization — while flagging only surface-level issues like typos and style-convention violations.

A closed loop: AI reviewing code written by AI.

---

## Quality decline in 2025–2026

In early 2026, developer forums erupted with complaints that "Copilot's suggestion quality has clearly dropped." In the Stack Overflow Developer Survey, positive sentiment toward AI coding tools fell **from over 70% to 60%** — a sharp drop.

The cause is architectural.

**The Model Carousel phenomenon**: the underlying model swaps silently, without user notification. Codex → various GPT-4 → GPT-5 series → Claude 3.7 Sonnet → Gemini 2.0. Prompt handling optimized for older models doesn't fit newer ones, producing performance regressions.

**The 8,000-token context window limit**: for projects over 10,000 lines, Copilot's probability of producing an accurate suggestion **drops to about 50%**. Tasks touching 10 or more files trigger what has been called "multi-file blindness."

**Declining suggestion acceptance rate**: 35–40% as of 2026 — below rival Cursor (42–45%). **75% of senior engineers report that they "spend more time fixing Copilot's bugs than they would writing the code manually."**

In The Pragmatic Engineer's survey of 906 professional developers (January–February 2026), the "most loved tool" came out as follows:

- Claude Code: 46% (+ Claude models 11% = 57% combined)
- Cursor: 19%
- GitHub Copilot: 9%

---

Despite all this, Microsoft is embedding Copilot into Windows and Office.
On top of that, Agent 365 — the control plane that centrally monitors, governs, and protects every agent inside an organization — becomes generally available on May 1.
