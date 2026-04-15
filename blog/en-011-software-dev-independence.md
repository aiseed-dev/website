---
slug: software-dev-independence
title: Desk Work and System Design in the AI Era — Rebuild the Three Domains
subtitle: Before Mythos goes public, rebuild desktop, internal systems, and public systems with Claude and Gemma 4.
description: In April 2026, Claude Mythos and Gemma 4 arrived. Half a year to a year until release. Three problem domains — Windows/Office, internal systems, public systems — rebuilt with role-split AI and approved-logic-as-code.
date: 2026.04.13
lang: en
label: Blog
category: Structural Analysis Notes
hero_image: IMG_3415.jpg
---

# Desk Work and System Design in the AI Era — Rebuild the Three Domains

## April 2026: The Tools Have Arrived

In April 2026, two breakthrough tools arrived.

- **Claude Mythos** (April 2026, restricted preview from Anthropic via Glasswing): advanced logical reasoning, abstract thinking, policy, strategy, and coding.
- **Gemma 4** (April 2026, released by Google under Apache 2.0): a high-performance open-source model that **runs on your own machine with zero external communication.** Fast processing, routine tasks, full privacy. Free.

Claude turns logic into code. Gemma 4 handles routine processing on your machine. **Together, they replace your work with code.**

## Urgent — Finish Before Mythos Goes Public

### Glasswing — Inside and Outside the 12

On April 7, 2026, Anthropic announced Project Glasswing. Claude Mythos is restricted to 12 companies and 40-plus infrastructure organizations. **Everyone else must protect themselves.**

Mythos will not stay locked up forever. As the 12 Glasswing companies finish their remediation, Mythos gets released. The moment that happens, **defenders and attackers start using Mythos at the same time.**

### Windows / Office Won't Make It in Time

Windows and Office carry decades of legacy code, and Copilot is now integrated across the OS and every Office product. Even with Mythos scanning, the surface to patch is too large to finish before public release. **If you keep relying on Microsoft for your security, you will be working on an unpatched attack surface long after Mythos goes public.**

### Copilot-Style Automation Won't Work in the Mythos Era

Microsoft is trying to solve the Excel / Word operation burden with **Copilot agent automation.** Structurally, this direction will not hold in the Mythos era.

- **Prompt injection**: instructions hidden in documents hijack Copilot.
- **Loss of data sovereignty**: internal documents are sent to an external AI.
- **Thinking atrophy**: outsourcing judgment erodes human judgment.

Copilot multiplies "convenient but fragile, unverifiable automation." Once Mythos is public, all of it becomes an entryway.

### Countdown

:::chain
The 12 Glasswing companies finish remediation → Mythos released publicly
→ Attackers gain the same capability
→ Windows / Office legacy, internal systems, public sites — all get scanned
→ Systems that can't patch in time fall first
→ **You have half a year to a year. After release is too late.**
:::

## Split AI by Role

Don't rank AIs by capability. **Split them by role.**

- **Claude Mythos**: thinking work. Coding, structural analysis, strategy, writing. Send only material.
- **Gemma 4 CLI**: processing work. Summaries, aggregation, transformation, routine analysis. Zero external communication. Runs on your own machine. **Not resident. One shot per invocation.**
- **Gemini**: research work. Source gathering, earnings analysis, deep research.
- **Production**: no AI. Static HTML, Python, SQLite. **Zero attack surface.**

:::chain
**Four principles:**
Think → Claude Mythos
Process → Gemma 4 CLI
Research → Gemini
Run → No AI
**Human is the hub. Don't auto-chain AIs.**
:::

## Rebuild the Three Problem Domains

For organizations outside Glasswing, there are three domains to defend. The shape of the problem differs, so the shape of the rebuild differs.

### 1. Windows / Office Problem (Desktop)

**Problem:**

- Binary files (Excel, Word, PowerPoint). `git diff` produces nothing.
- No history. Who changed what, when, and why lives only in people's heads.
- Manual at the core. Filling cells, fixing formatting — non-judgment operation eats the workday.
- Hundreds of CVEs a year. Zero-days that fire on open or preview.
- Tight coupling (Windows + Entra ID + Azure + SharePoint). One breach cascades through everything.
- Copilot integration expands the attack surface further.

**Rebuild:**

- **Move to Linux.** Get your desktop off Windows.
- **Binary → text:** Markdown, CSV, Python, JSON. Everything in Git (Doc as Code).
- **Observe Excel / Word work → extract logic → ask Claude to turn it into code.**
- **Hand routine processing — including confidential data — to Gemma 4 CLI, one shot at a time.** Not resident.
- Don't use Copilot agents.

### 2. Internal Systems Problem

**Problem:**

- Legacy line-of-business systems, ERP, core operations, Access DBs, on-prem apps.
- An SI vendor's black box. No one knows what's inside.
- No one in-house can explain the structure.
- When a vulnerability surfaces, re-engaging the vendor takes weeks to months.
- External API links, VPN access, remote desktop — external paths remain.
- AI agents are being pushed inside under the banner of "efficiency."

**Rebuild:**

- **Don't leave it to an SI vendor. Rebuild it yourself with Claude.** Something working in 24 hours.
- Observe the workflow → **turn only the logic a human approves into code** (Python, SQL, shell).
- **Data lives on your own machine as SQLite. Keep the central DB to the minimum.**
- Manage source code in Git. Understand the structure yourself.
- **No AI agents inside internal systems.** No Copilot, no resident Gemma 4. What runs is only the code a human approved.
- **When Mythos arrives, having the source in hand means you can fix it yourself.**

### 3. Public Systems Problem

**Problem:**

- Public sites on CMS (WordPress etc.). 11,000+ CVEs per year.
- 97% in third-party plugins. 57% exploitable without authentication.
- Public APIs, admin consoles, databases — wide attack surface.
- AI agent integrations (chatbots, AI search) widen it further.
- WAFs let 87.8% of attacks through.

**Rebuild:**

- **Drop the CMS.** Markdown + a build tool + static HTML.
- **No DB in production.** Local SQLite if needed.
- **No AI in production.** Retire chatbots and AI search.
- Keep the server simple. **Linux + Nginx + static files,** nothing else.
- One server, one app. Loosely coupled.
- **Drive the attack surface to zero.** Build a state where a scan finds nothing.

## Three Principles

:::highlight
**1. AI is used only by those with authority and responsibility.**
AI cannot take responsibility — a human takes responsibility for the result of any judgment. And AI is **itself a source of vulnerability** — external communication, prompt injection, unverifiable judgment. So an organization must decide *who* uses AI. The person with authority picks the material, judges the result, and carries the responsibility. **AI left to no one in particular diffuses accountability and widens the attack surface.**
:::

:::highlight
**2. Leave binary. Adopt Doc as Code.**
Markdown, CSV, Python, JSON. Everything in Git. A shape both AI and humans can diff.
:::

:::highlight
**3. Stay in a state where Mythos can scan and you can patch.**
Build a system where, the moment Mythos is public, you can scan your own code and patch what it finds yourself. Three things have to be true at once: the source code is in your hands, the structure is understood, and the code is small and transparent. Only then can you act on Mythos findings in hours to days. **Don't keep what you can't patch yourself — CMS, AI agents in production, SI-vendor black boxes.**
:::

## Independence Is Not Isolation

Claude Mythos writes code. Gemma 4 CLI processes locally. Gemini researches. **The human decides what to build, instructs the AI, and judges the result.**

You don't write code. You do understand the structure.

Leave the software to AI, and humans focus on real-world work. Grow food. Build things. Face other people. **That is what lies on the other side of rebuilding the three domains.**

## Preparing for the Mythos Release — Start Today

You have half a year to a year before release. **Start today or you won't make it.**

:::highlight
**Start today:**
1. Install Linux. Get comfortable with the terminal.
2. Practice development with Claude Code.
3. Run Gemma 4 locally as a CLI.
4. Build the habit of researching with Gemini.
5. Observe your Excel / Word work and replace routine parts with code.
6. Plan the rebuild of your internal systems. Keep an option that doesn't rely on an SI vendor.
7. Make the public site static. Drop the CMS and the production DB.
8. Put your source code on GitHub.
9. Remove AI agents from production.
:::

## Independence Begins the Moment You Split the Roles

**Think with Claude Mythos. Process locally with Gemma 4 CLI. Research with Gemini. Keep AI out of production.**

Windows / Office, internal systems, public systems — drive the attack surface to zero in each of the three domains. **That is the only approach that works in the Mythos era.**

:::quote
Leave Windows / Office.
Rebuild internal systems yourself with Claude.
Make the public site static HTML.
Think → Claude Mythos
Process → Gemma 4 CLI
Research → Gemini
Run → No AI
**Half a year to a year until Mythos goes public. Start today.**
:::

---

Join the discussion in the Facebook group: [AISeed — Biodiversity, Food, and Life with AI](https://www.facebook.com/groups/vegitage)
