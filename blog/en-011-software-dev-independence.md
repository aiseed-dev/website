---
slug: software-dev-independence
title: Desk Work and System Design in the AI Era — Turn Excel / Word Operations into Code
subtitle: Most desk work is Excel / Word operation. Systematize it with Claude and Gemma 4. Copilot-style automation won't work in the Mythos era.
description: Most desk work is Excel / Word operation. Replace it with code using Claude and Gemma 4. Office Copilot's agent automation is fragile and will not survive the Mythos era.
date: 2026.04.13
lang: en
label: Blog
category: Structural Analysis Notes
hero_image: IMG_3415.jpg
---

# Desk Work and System Design in the AI Era — Turn Excel / Word Operations into Code

## Most Desk Work Is Excel and Word Operation

Picture today's desk work.

- Paste data into Excel. Reshape it. Aggregate it.
- Write reports in Word. Fix the layout.
- Line up slides in PowerPoint.
- Sort mail in Outlook.

A large share of work hours goes to **manual work on binary files.** No judgment. Just operation.

**Systematize that directly.** That is the design of desk work in the AI era.

## Office Itself Won't Survive the AI Era

Before Copilot even enters the picture, **Office (Word / Excel / PowerPoint) itself** is structurally mismatched with the AI era.

- **Binary files**: hard for AI and humans alike to read. `git diff` produces nothing.
- **No history**: who changed what, when, and why lives only in people's heads.
- **Manual at the core**: filling cells, fixing formatting, adjusting layout — non-judgment operation eats most of the workday.
- **Hundreds of CVEs a year**: zero-days that fire just by opening or previewing a file appear year after year.
- **Tight coupling**: Windows + Office + Entra ID + Azure + SharePoint are so tightly bound that one breach cascades through the whole stack.

Office grew big while still wearing the "document-centric, personal-PC era" design. It is not a shape AI can read and write, and it does not match how modern development, auditing, or collaboration actually works.

**Copilot automation piles a fragile AI agent on top of this without fixing the underlying mismatch.** The foundation is wrong for the AI era, but convenience hides it. In the Mythos era, this structure will not hold.

## April 2026: The Tools Have Arrived

In April 2026, two breakthrough tools arrived.

- **Claude Mythos** (April 2026, restricted preview from Anthropic via Glasswing): advanced logical reasoning, abstract thinking, policy and strategy — and coding.
- **Gemma 4** (April 2026, released by Google under Apache 2.0): a high-performance open-source model that **runs on your own machine with zero external communication.** Fast processing, routine tasks, full privacy. Free.

Claude turns logic into code. Gemma 4 handles routine processing on your machine. **Together, they replace Excel / Word operations with code.**

## Urgent — Finish Before Mythos Goes Public

On April 7, 2026, Anthropic announced Project Glasswing. Claude Mythos is restricted to 12 companies and 40-plus infrastructure organizations. **Everyone else must protect themselves.**

**This is not "do it eventually." There is a deadline.**

Mythos will not stay locked up forever. As the 12 Glasswing companies finish their remediation, Mythos gets released. The moment that happens, **defenders and attackers start using Mythos at the same time.**

### The Biggest Problem — Windows / Office Won't Make It in Time

This is the main reason for the urgency. Windows and Office, which most organizations depend on, carry decades of legacy code, and Copilot is now integrated across the OS and every Office product. Even with Mythos scanning, the surface to patch is too large to finish before public release.

### Copilot-Style "AI Automation" Won't Work in the Mythos Era

Microsoft is trying to solve the Excel / Word operation burden with **Copilot agent automation.** Structurally, that direction will not hold up in the Mythos era.

:::chain
**The shape of Copilot automation:**
Office documents (mail, spreadsheets, contracts) → Copilot reads all of them
→ Sent to an external AI service → response flows back into Office
→ Instructions hidden in a document can hijack Copilot (prompt injection)
→ **Attack surface grows with every document. When Mythos goes public, this becomes an immediate target.**
:::

- **Prompt injection**: instructions hidden in documents hijack Copilot.
- **Loss of data sovereignty**: internal documents are sent to an external AI.
- **Thinking atrophy**: outsourcing judgment erodes human judgment.

Reducing Excel / Word operation is the right goal. But **the method matters.** Copilot multiplies "convenient but fragile, unverifiable automation." Once Mythos is public, all of that becomes an entryway.

### Time Remaining

:::chain
**Countdown:**
The 12 Glasswing companies finish remediation → Mythos released publicly
→ Attackers gain the same capability
→ CMS, legacy DBs, Copilot-integrated documents — all get scanned
→ Systems tied to Microsoft legacy and Copilot automation become the first targets
→ **You have half a year to a year. After release is too late.**
:::

## Split AI by Role

Don't rank AIs by capability. **Split them by role.**

### Claude Mythos — Thinking Work (external connection)

Coding, structural analysis, strategy, writing. Complex judgment and creativity. Develop with Claude Code. Send only **material that deserves to be thought about.** No raw data, no secrets.

**Observe an Excel task → extract the logic → ask Claude to turn it into code.** This systematizes most of desk work.

### Gemma 4 CLI — Processing Work (fully local)

Summaries, aggregation, transformation, routine analysis. **Zero external communication. Runs on your own machine.**

**Do not run it as a persistent agent. Invoke via CLI and finish in one shot.** No privileges. Input → process → output, done.

Daily sales aggregation, meeting-note summaries, CSV reshaping, draft email bodies — hand routine processing (including confidential data) to Gemma 4 CLI, one shot at a time. Unlike Copilot, it is not resident, so it does not form an attack surface.

### Gemini — Research Work

Source gathering, earnings analysis, deep research. Fast because it's plugged into Google search. A human reads the output.

### Production Environment — No AI

Static HTML, Python, SQLite. **Zero attack surface.**

No AI agents in production. Always-on external comms + system privileges + unverifiable judgment — that is opening a door for a Mythos-class attacker.

:::chain
**Four principles:**
Think → Claude Mythos (send only material)
Process → Gemma 4 CLI (local; never resident)
Research → Gemini (search-integrated)
Run → No AI (production is static / local)
**Human is the hub. Don't auto-chain AIs.**
:::

## Systematize Desk Work

### Leave Binary — Doc as Code

Excel and Word binaries are hard on both AI and humans.

:::compare
| Binary-centric | Text-centric |
| --- | --- |
| Excel aggregation macro | Python script |
| Word report template | Markdown + generation script |
| Boilerplate email | Email body generated by Gemma 4 CLI |
| Manual reshaping | Intent → code → artifact (PDF etc.) generated directly |
| Diffs invisible | Full history in Git |
:::

Manage documents in Git like code. **Who changed what, when, and why** — all preserved.

### System Design — Approved Logic Becomes Code

:::chain
**The design rule:**
Observe today's Excel / Word work → separate judgment from routine processing
→ Let Claude turn the routine part into code (Python, SQL, shell)
→ Execute with 100% reproducibility → record in Git
→ **Claude does the coding. This is not hard.**
:::

- **Don't let an AI agent decide.** What runs is only the logic a human approved.
- **What can't be automated, a human does.** AI assists during that work.
- **The human takes responsibility.** AI is a tool. Judgment and accountability stay with the human.

This is the essential difference from Copilot automation. Copilot delegates judgment to a black-box agent. Here, a human's approved logic runs as transparent code.

## Five Principles

:::highlight
**1. Split AI by role. No AI in production.**
Think with Claude Mythos. Process with Gemma 4 CLI. Research with Gemini. Production stays static.
:::

:::highlight
**2. Leave binary. Adopt Doc as Code.**
Markdown, CSV, Python, JSON. Everything in Git.
:::

:::highlight
**3. No CMS, no DB in production.**
Use local SQLite if needed. No DB, no SQL injection.
:::

:::highlight
**4. Keep the public site static.**
Linux + Nginx + static files is enough. Run Gemma 4 locally as a CLI on your own machine.
:::

:::highlight
**5. Eliminate black boxes.**
Leave code to AI. Understanding structure and intent is the human's job.
Don't bring in "invisible automation" like Copilot.
:::

## Independence Is Not Isolation

Claude Mythos writes code. Gemma 4 CLI processes locally. Gemini researches. **The human decides what to build, instructs the AI, and judges the result.**

You don't write code. You do understand the structure.

Leave the software to AI, and humans focus on real-world work. Grow food. Build things. Face other people. **That is what lies on the other side of systematized desk work.**

## Preparing for the Mythos Release — Start Today

You have half a year to a year before release. **Start today or you won't make it.**

:::highlight
**Start today:**
1. Install Linux. Get comfortable with the terminal.
2. Practice development with Claude Code.
3. Run Gemma 4 locally as a CLI.
4. Build the habit of researching with Gemini.
5. Observe your Excel / Word work and start replacing routine parts with code.
6. Put your source code on GitHub.
7. Remove AI agents from production (CMS → static HTML, Copilot integration → retire).
:::

## Independence Begins the Moment You Split the Roles

**Think with Claude Mythos. Process locally with Gemma 4 CLI. Research with Gemini. Keep AI out of production.**

Don't hand desk work to a Copilot agent. **Turn approved logic into code.** That is the only approach that works in the Mythos era.

:::quote
Most desk work is Excel / Word operation.
Think → Claude Mythos
Process → Gemma 4 CLI
Research → Gemini
Run → No AI
Copilot automation won't work in the Mythos era.
Approved logic becomes code.
**Half a year to a year until Mythos goes public. Start today.**
:::

---

Join the discussion in the Facebook group: [AISeed — Biodiversity, Food, and Life with AI](https://www.facebook.com/groups/vegitage)
