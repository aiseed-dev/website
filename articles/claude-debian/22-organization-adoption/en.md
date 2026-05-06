---
slug: claude-debian-22-organization-adoption
lang: en
number: "22"
title: Chapter 22 — Adoption in an Organization
subtitle: Change the tools before changing the OS.
description: A realistic path for adopting Debian on a team or in a company. Before pushing the OS swap, change the tools — Markdown / CSV / Python (uv) / Claude / Element. These work on Windows already. Once the substance moves to structured text, Linux migration becomes a small final step.
date: 2026.04.23
label: Claude × Debian 22
prev_slug: claude-debian-21-telling-others
prev_title: Chapter 21 — Telling Those Around You
next_slug: claude-debian-23-passing-on
next_title: Chapter 23 — Passing It On to the Next Generation
cta_label: Learn with Claude
cta_title: Tools first, OS later.
cta_text: Declaring "the whole company will migrate to Linux" almost always fails. What you do first is Markdown, Python, and Claude — these run on Windows. Change the tools first, then change the OS, and the friction drops to a minimum.
cta_btn1_text: Continue to Chapter 23
cta_btn1_link: /en/claude-debian/23-passing-on/
cta_btn2_text: Back to Chapter 21
cta_btn2_link: /en/claude-debian/21-telling-others/
---

## The Reality of Organizational Adoption

"The entire company will migrate to Linux" — this kind of large-scale
project almost always fails. Business-app compatibility, internal support,
user education, budget, approvals — the moment any one of them hits a
wall, the project stalls.

And **leading with Linux migration is the wrong sequence**. Swapping the
OS is the largest change there is. There's something else that should
go first.

## Section 1 — Change the Tools Before Changing the OS

The book's claim is simple — **before pushing an OS swap, change the
tools first**. This is exactly what [AI-Native Ways of Working](/en/ai-native-ways/)
spells out, and **you can start it today on Windows.**

### What "the tools" means

- Documents: Word → **Markdown** (export to .docx with pandoc only on delivery)
- Spreadsheets: Excel → **CSV + Python (uv + pandas)** (export .xlsx only on delivery)
- Slides: PowerPoint → **Markdown + Marp**
- Diagrams: Visio / PPT shapes → **Mermaid**
- Mail: Outlook → **Thunderbird** (same on both OSes)
- Chat: Slack → **Element / Matrix** (self-hostable, you own the data)
- Browser: Edge → **Firefox + Chrome** (same profile on both OSes)
- Editor: VS Code → **Zed** (runs on both OSes)
- Packaging: pip → **uv** (runs on both OSes)
- AI: → **Claude Code** (`curl https://claude.ai/install.sh | bash`, both OSes)

**All of these run on Windows.** You don't need to switch the OS yet.

### Why this order works

1. **Compatibility problems disappear.** Once the substance is Markdown
   and CSV, the OS doesn't matter. A vendor sends Word, you receive it
   as Markdown (via pandoc) and reply in Markdown.
2. **The cost of retreat is small.** Tool changes can be reversed
   ("I'll go back to Word"). OS swaps cannot, easily.
3. **No persuasion needed.** "I write faster than Word," "next month's me
   reruns the same aggregation in one command" — results land first. No
   approval cycle.
4. **No collision with IT.** "I'm not changing the OS, just how I write."
5. **It prepares the OS migration.** The same tools run on Linux. Once
   the substance has moved, swapping the OS is **just changing the
   desktop wrapper** — a small job.

### The map of stages

```
Stage 0 (status quo):
  Windows + Office + special-purpose apps

Stage 1 (change the tools — this book's main recommendation):   ← works on Windows
  Windows + Markdown + CSV + Python(uv) + Claude + Element + Zed
  Office shrinks to an import / export adapter

Stage 2 (change the OS — for those who want to):
  Debian + Flatpak + the same tools
  Stage 1 already runs, so this is just changing the wrapper

Stage 3 (one person + AI as the unit, organization changes):
  Each member is an autonomous unit; the organization coordinates
```

**90% of organizational adoption gets done at Stage 1.** Even without
forcing Stage 2 (the OS migration), **most of the productivity and
security gains arrive at Stage 1 alone.**

### Ask Claude ①: A Tool-Change Plan (No Linux Yet)

> Given my role [industry / role], main work [content], and organization
> size [headcount], scaffold a 90-day plan to introduce the following
> tools **while staying on Windows**:
> - Markdown (documents), CSV + Python uv (spreadsheets), Marp (slides), Mermaid (diagrams)
> - Thunderbird (mail), Element (chat), Firefox / Chrome (browser)
> - Zed (editor), Claude Code (AI alongside)
>
> For each week, give the tasks and the first deliverable (a small,
> visible internal win). Include the **import / export adapters** with
> existing Office / Outlook / Teams.

## Section 2 — Start with Your Own Work PC (Stage 2)

When the tool change has settled, **then** the people who still want
Linux move to Stage 2. Not by mandate; **by individual choice.**

### A Fait Accompli, Rather Than an Approval

Whether this is allowed varies by your role, your work, and internal
rules — but at many companies, even short of "OS choice is up to the
individual," it is silently tolerated as long as the developer
environment or work isn't disrupted.

- Developers: it isn't unusual to have a work PC on Linux.
- Data analysts: a Python / SQL environment feels natural on Linux.
- Web operations: server work often demands Linux anyway.
- Admin / sales: heavy Office dependence, but **once Stage 1 is done**
  the migration bar drops dramatically (the substance is already in
  Markdown / CSV).

### Alignment with the Mythos Era

As I wrote in [Chapter 11, "Claude Mythos — WordPress + AI"](/en/blog/claude-mythos-wordpress-ai/)
and [Chapter 13, "Desk Work in the AI Era"](/en/blog/software-dev-independence/),
**dependence on Windows is a high security risk in the Mythos era**. If
the IT department is starting to understand this structure, Stage 2
(Linux migration) becomes a legitimate option.

### Ask Claude ②: Should I Move to Stage 2?

> I've been running Stage 1 (Markdown / CSV / Python uv / Claude /
> Element / Zed) for [X] months. My role is [industry / role], my
> organization is [headcount].
>
> Is it worth migrating my work PC to Debian? Lay out:
> (1) Pain that remains under Stage 1 alone.
> (2) Pain that disappears on Linux.
> (3) New pain that appears on Linux.
> (4) A six-month achievable goal.
> (5) Realistic probability of pulling Stage 2 off (high / medium / low).

## Section 3 — Show Small Wins

### Speak with Deliverables

Once you've migrated to Debian, show the following.

- It got faster: boot time, app startup, processing speed.
- Fewer mistakes: documents managed as text, bugs traceable.
- Lower cost: license-fee reduction.
- New capabilities: tools you built with Claude, data processing.

**Show numbers.** Not "vaguely faster," but "boot went from 45s to 12s."

### Document on a Blog or Internal Wiki

Record your migration and operation on the internal wiki or your team's documents. When others read it, that itself becomes a sample.

## Section 4 — Build the Second and Third Person

### Support Those Who Show Interest

When someone sees your results and says "I want to try too," apply Chapter 21's "telling those around you."

- Hand them this textbook.
- Pick an install day together.
- Ask Claude together when stuck.
- Don't take on too much support.

**One person at a time, reliably.** Rushing into "an install party for everyone interested" fails.

### Three People Make a "Debian User Group"

Three Debian users inside the company makes an informal group possible.

- 15 minutes at lunch once a week.
- **An Element / Matrix room** (Slack works too, but this book recommends
  Element: self-hostable, E2EE, federated, you own the data — all of
  which fit a Mythos-era "support from below").
- Share trouble; accumulate know-how.

This becomes the internal "support from below."

> **Why Element over Slack**
> Slack is convenient, but the data lives under a cloud vendor's control.
> Element backed by a self-hosted Matrix server gives you **message
> history and search you own**. The Linux client installs cleanly via
> Flatpak; the same client can carry business messages and family chat
> on one machine. And there's no 90-day free-tier message expiry.

## Section 5 — Relationship with the IT Department

### Don't Make Them the Enemy

The IT department is the team responsible for stable operations. Adopting a new OS means **expanding their scope of responsibility**. Pushback is natural.

### Enter as "a Consultation," Not "a Permission Request"

If you ask "may I switch to Debian?", absent precedent the answer is no. Instead, ask "we have this work issue, and Linux looks like it could solve it — could I consult with you?"

### Understand Their Concerns

The IT department worries about:
- Security-patch application guarantees.
- Connections to internal systems (VPN, domain authentication, certificates).
- Support window (who looks after it).
- Incident response.
- License management (the company's legal responsibility).

Build, with Claude, proposals that defuse each one.

### Ask Claude ③: A Proposal to the IT Department

> My affiliation: []. I want to propose to the IT department that I switch my work PC to Debian.
> For each category the IT department is likely to worry about (security, support, connections, licensing), put together a proposal of my response / handling.
> Tone is "consultation," not demand.
> Include a fallback plan (the steps to return to Windows) if it fails.

## Section 6 — Living with Business Apps

### In-House-Only Apps

Many organizations have Windows-only apps used only inside the company. Handling:

1. **Investigate alternatives.** Ask Claude; actually try them.
2. **Run in a virtual machine.** A Windows VM under KVM / virt-manager.
3. **A separate PC (Windows kept).** A dedicated machine just for that app.
4. **Migrate to a web app.** Long-term, even internal systems shift to web.

### Microsoft 365 / Teams

If Teams meetings are required for work, it runs on Linux too. The official native app was discontinued, but the web version works. Installed as a PWA, the experience is close to a native app.

### Mail and Calendar

Exchange Online is reachable from Thunderbird with IMAP setup. Calendar (CalDAV) works depending on configuration.

### Ask Claude ④: A Handling Map for Business Apps

> The business apps my organization uses are [list].
> Make a table for each app: the current state of Linux support, and the handling proposal (alternative / VM / separate machine / web version).
> Include handling for connections to internal systems (VPN, AD domain, certificates).

## Section 7 — Move It with Cost Analysis

### Organizational Decisions Move on Numbers

Organizations that don't move on logic do move on numbers. Build the calculation for Debian migration.

- **License-fee reduction.** Windows Pro, Office 365, security software.
- **Hardware life extension.** Old PCs no longer need replacement.
- **Support-cost reduction.** Less outsourced help on trouble (Claude-assisted self-resolution).
- **Risk reduction.** Reduced expected loss from Mythos-era zero-days.

A few tens of thousands to a hundred-plus thousand yen of savings per person per year is realistic. With 100 employees, that's millions to tens of millions of yen. **This is the number that lands with executives.**

### Ask Claude ⑤: A Cost Calculation for Your Organization

> Given my organization's size [headcount] and major licenses [Windows Pro, Office 365, security software], calculate annual savings if all or part of staff migrated to Debian + alternatives.
>
> (1) Direct savings (license fees).
> (2) Indirect savings (support, trouble handling).
> (3) Migration cost (training, migration work).
> (4) Cumulative profit / loss over five years.
>
> Give two scenarios: conservative and optimistic.

## Section 8 — Be Ready for the Long Game

### Organizations Change Over Five Years

For a small organization, 1–2 years; for a large company, 5 years. Simultaneous migration is impossible, but **a 10–20% increase per year** is realistic.

You as the first one, growing allies over 2–3 years, and after 5 years 30% of the organization is on Linux — this is the realistic picture of success.

### Build Something That Lasts

It's bad if "Linux culture in the company evaporates when you leave."

- Leave documents (internal wiki, operational procedures).
- Make it operable by multiple people.
- Present the migration option to new hires too.

**Grow it as a continuing system, not just one person's activity.**

## Section 9 — When It Fails, Withdraw

### Withdrawal Is a Strategy Too

Organizational Debian adoption can fail. IT policy changes, business apps update and stop working, the key person leaves, leadership changes — for many reasons.

When it fails, don't get emotional. Withdraw. **Just keep using Debian yourself.** The organization's direction and your own PC environment are separate things.

### Ask Claude ⑥: Criteria for Withdrawal

> If I am championing Debian adoption in an organization, what conditions, when met, should I judge as "time to withdraw"? Give five clear criteria.
> Also, when withdrawing, how to arrange the relationship with the organization so I can keep my own PC going.

## Summary

What you did in this chapter:

1. Understood why a simultaneous organizational Linux migration fails.
2. Confirmed the strategy: **change the tools (Markdown / CSV / Python uv / Claude / Element / Zed) before changing the OS** — Stage 1 runs on Windows.
3. Treated Stage 2 (Linux migration) as an individual decision for those who want it.
4. Sorted out how to show small wins in numbers.
5. Confirmed how to keep IT not as the enemy.
6. Designed realistic compromises with business apps.
7. Got the practice of moving leadership with cost calculations.
8. Set the long-game posture and the criteria for withdrawal.

What you hold now:
- Debian operating in your own work.
- An internal proposal / documentation.
- Withdrawal criteria.
- Candidates for the second and third person.

In Chapter 23 — the textbook's final chapter — we cover **passing it on to the next generation**. How to hand what you've learned to your children and to those who follow. The shape of inheritance of learning, in an era of learning together with Claude.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
