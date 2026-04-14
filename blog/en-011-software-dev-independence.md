---
slug: software-dev-independence
title: Software Development Independence — Claude + Gemma 4 and the Four-Role AI Split
subtitle: Think, process, research, run. Split AI by role, and your attack surface can be zero.
description: Claude, Gemma 4, Gemini — split your AIs by role and keep the production environment AI-free. Even outside Glasswing, a structurally safe development stack is available today. A four-quadrant model for surviving the Mythos era.
date: 2026.04.13
lang: en
label: Blog
category: Structural Analysis Notes
hero_image: IMG_3415.jpg
---

# Software Development Independence — Claude + Gemma 4 and the Four-Role AI Split

## The Tools for the Mythos Era Have Arrived

On April 7, 2026, Anthropic announced Project Glasswing — providing Claude Mythos's vulnerability discovery capability to 12 companies and 40-plus critical infrastructure organizations, for defensive use only. Once Glasswing participants reach a certain level of remediation, Mythos will be released publicly. At that moment, every unpatched system becomes a target.

But this is not a story of fear. It is the story that **the tools to develop for yourself have arrived at exactly the same time.**

Anthropic's coding tool "Claude Code" has reached $1 billion in annualized revenue since launch, and Anthropic states that this tool now generates 70–90% of new code. Google has released Gemma 4 as open source (Apache 2.0), making a high-performance model runnable locally by anyone. Gemini is integrated with Google's search infrastructure and has reached a level where one person can do deep research.

**Claude + Gemma 4 + Gemini. Use these three by role, and keep AI out of production.** That alone builds a structurally safe development stack outside Glasswing.

## Four Roles for AI

Don't rank AIs by capability. **Split them by role.**

### Claude — Thinking Work (external connection)

Coding, report writing, structural analysis, blog writing. Work that requires complex judgment and creativity.

Develop with Claude Code. Review designs. Write documentation. Structure articles.

You communicate with Anthropic's servers. In return, you get state-of-the-art reasoning and agentic development support via Claude Code. What you send is only **material that deserves to be thought about** — structures, outlines, code for review — not raw data or secrets dumped wholesale.

### Gemma 4 CLI — Processing Work (fully local)

Document summarization, data aggregation, text transformation, routine analysis.

Zero external communication. Runs on your own server. Free under Apache 2.0.
**Do not run it as a persistent agent. Invoke it via CLI and let each call complete in one shot.**

Summarize today's sales log. Reshape a CSV. Turn meeting notes into bullet points. Normalize, classify, fill templates — hand routine information processing to a local Gemma 4, one shot at a time. No daemon. No privileges. Input → process → output, round trip finished. This is the key to keeping the attack surface from forming.

### Gemini — Research Work (Google search infrastructure)

Source gathering, earnings analysis, deep research.

Google owns the world's largest search and crawl asset. Gemini plugs directly into it. "Five-year earnings trend for this industry." "Country-by-country comparison of this regulation." A model fused with search infrastructure is overwhelmingly faster for this kind of work.

A human reads the research output. Once useful material is extracted, Claude analyzes it and Gemma 4 CLI reshapes it if needed.

### Production Environment — No AI

Static HTML, Python execution code, SQLite. **Zero attack surface.**

No AI agents in the public site. No AI agents resident in internal tools. Production runs only code that a human has read and understood (i.e. code that Claude Code generated and a human reviewed). No inference calls to external APIs. No decisions delegated to an LLM.

The temptation to run AI in production is strong. "Let's add a chatbot." "Let AI summarize it." But that is the same thing as opening an entryway for a Mythos-class attacker. Always-on external communication. System-level privileges. Judgments that cannot be verified. Structurally, it is attack-surface expansion.

**Use AI during development. Not in production.** Hold this line and the attack surface stays at zero.

## Why the Four-Way Split Works

This split is not arbitrary. It is a design that **uses each AI in the shape it is good at and keeps it out of the shapes where it is not.**

:::compare
| AI | Shape of use | Data flow | Attack surface |
| --- | --- | --- | --- |
| Claude | Agentic. Dialog and iteration | Only thinking material leaves | Dev only. None in production |
| Gemma 4 CLI | One-shot. Input → output, done | Never leaves the local box | Zero (no external comms) |
| Gemini | Search-integrated. Research queries | Public information primarily | Only during research |
| Production | No AI | Static / local-only | Zero |
:::

:::chain
**The rule of the four-way split:**
Think → Claude (borrow top-tier reasoning; send only material)
Process → Gemma 4 CLI (complete locally; never resident)
Research → Gemini (a model fused with search infrastructure)
Run → No AI (production is static / local; zero attack surface)
**Don't design around "which AI"; design around "which job goes to which AI."**
:::

Each AI's output is received by a human and passed to the next AI. **Don't chain AIs together automatically.** AI agents calling other AI agents expands privileges and communication paths quickly, widening the attack surface. **The human is the hub.** That is the operating rule that keeps the four-way split safe.

## 70–90% of Code Is Already Written by AI

One number not to miss.

Claude Code generates 70–90% of new code. Software development used to require large teams and large budgets. Millions of yen to an SI firm, months of build time.

Not anymore. One person plus Claude matches what an SI team used to deliver. Local routine processing is carried by Gemma 4 CLI. Research is accelerated by Gemini.

:::compare
| | SI vendor | One person + Claude + Gemma 4 + Gemini |
| --- | --- | --- |
| Cost | ¥5M–10M | Claude subscription + your own server |
| Duration | 2–3 months | 24 hours to a few days |
| Understanding | Black box | Self-built, self-understood |
| Routine processing | Priced by man-month / SaaS dependency | Local with Gemma 4 CLI |
| Research | Outsourced | Instant with Gemini |
| Patching | Re-engage SI vendor | Fix yourself with Claude |
| Attack surface | CMS + DB + API + admin | Static HTML (zero) |
:::

aiseed.dev is the proof. Over 30,000 lines of code. 42 HTML pages. 26 articles. All generated by Claude Code. Zero lines written by a human. About 24 hours of build time. Quoted to an SI firm: ¥5M–10M.

## The Asymmetric Race

Defenders use AI under ethical constraints. Attackers use AI without. In this asymmetric fight, digital infrastructure still has to hold.

Anthropic restricted Mythos to defensive use. An equivalent AI built by malicious actors has no such limit. No matter how strong the defender's AI is, sheer numbers can overwhelm.

That is exactly why, **rather than "defend better," the only answer is "remove the attack surface."** And the four-way split is the design that gets you there — by keeping AI out of production, there simply is no AI-mediated entryway to exploit.

## Five Principles for Development Independence

:::highlight
**Principle 1: Split AI by role. Do not put AI in production.**
Think with Claude. Process locally with Gemma 4 CLI. Research with Gemini.
What runs in production is static HTML and local execution code. No resident AI agents.
:::

:::highlight
**Principle 2: Don't use a CMS.**
A public site is fine with Markdown, a build tool, and static HTML.
Claude Code will write the build script. With that, there is no reason to depend on a CMS.
:::

:::highlight
**Principle 3: Don't put a database in production. Use local SQLite when needed.**
No DB, no SQL injection.
Production serves static files. Data processing is completed locally with Gemma 4 CLI and SQLite.
:::

:::highlight
**Principle 4: Own your server.**
A simple Linux box, Nginx, static files. Run Gemma 4 on that same box as a CLI.
One server, one app. Physically and logically loosely coupled.
:::

:::highlight
**Principle 5: Eliminate black boxes.**
A system you don't understand is a system you can't defend.
Leave the code to AI. Understanding structure and intent is the human's job.
A human reads the code Claude Code produced and grasps the structure. That is the core of independence.
:::

## Independence Is Not Isolation

Independence does not mean doing everything alone. **Four AIs are your collaborators.**

Claude Code writes code. Claude reviews designs. Gemma 4 CLI handles daily local processing. Gemini accelerates research. The human decides what to build, instructs the AI, and judges the results.

:::chain
**The structure of independence:**
Human → decide what to build → instruct Claude
Claude → generate code → test → revise
Gemma 4 CLI → handle routine processing locally
Gemini → gather needed information
Human → verify results → deploy (no AI in production)
**The human writes no code — yet understands what the system does, and controls everything.**
:::

That software development can be completed with AI means **the human's time and energy can be concentrated on real-world work.**

Grow food. Build things. Run services that face other humans. AI can't do those. Real-world work requires a human body and judgment — feel the soil, read the weather, judge quality, talk to customers.

Leave the software to AI. The tools you need can be built in 24 hours. Routine processing runs locally. Research is accelerated. **That is exactly why a human can concentrate on the work that really matters — making things in the real world.**

This is what software development independence actually means. Not being bound by software. Using software as a tool and returning to your real work.

## Preparing for Mythos's Public Release

The moment Mythos is released publicly, two things happen at once.

1. Defenders gain the ability to scan their own systems with Mythos.
2. Attackers start scanning target systems with Mythos.

The gap before patches land decides who lives. Whether you can close that gap to zero is decided by what you do today.

:::compare
| | Organization that is ready | Organization that is not |
| --- | --- | --- |
| Source code | In your hands. Fully understood | An SI vendor's black box |
| Structural understanding | Self-designed | No one knows the whole |
| Routine processing | Gemma 4 CLI, fully local | Depends on external SaaS |
| Patching | Fix it yourself with Claude | Re-engage SI vendor (weeks to months) |
| Attack surface | Static HTML. Nothing to scan | CMS + DB + API + AI agent |
| Survival after Mythos release | **Structurally safe** | **First target** |
:::

:::highlight
**What you can start today:**
1. Install Linux. Get comfortable with the terminal. This is the starting point.
2. Start practicing development with Claude Code. Build the skill of co-developing with AI.
3. Get Gemma 4 running as a CLI on your own server.
4. Build the habit of researching with Gemini (search + deep research).
5. Keep your source code in your hands. Publish everything on GitHub.
6. Remove AI agents from production (CMS → static HTML, DB → file-based).
**Build the capability to run security checks the moment Mythos is released.**
**Prerequisites: your source code is yours, and the structure is understood.**
:::

## Independence Begins the Moment You Split the Roles

The 12 Glasswing companies will protect their systems with Mythos. The countless organizations, municipalities, and individuals outside must protect themselves.

But "protect yourself" is not "fight alone." **Use Claude + Gemma 4 + Gemini by role, and keep AI out of production.** This four-way placement is the structurally safe development stack outside Glasswing.

**Drive the attack surface to zero.** That is the best defense. Think with Claude. Process locally with Gemma 4 CLI. Research with Gemini. Keep production static.

Mythos's public release is close. You have half a year to a year to prepare. The tools are here. What remains is deciding the role split and starting today.

:::quote
Thinking work goes to Claude.
Processing work goes to Gemma 4 CLI.
Research goes to Gemini.
Production runs with no AI.
Split the four roles, and the attack surface becomes zero.
Even when Mythos arrives, you build a structure that needs no defending.
The tools are ready. What is left is the decision.
:::

---

Join the discussion in the Facebook group: [AISeed — Biodiversity, Food, and Life with AI](https://www.facebook.com/groups/vegitage)
