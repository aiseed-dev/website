---
slug: claude-debian-22-organization-adoption
lang: en
number: "22"
title: Chapter 22 — Adoption in an Organization
subtitle: Stack small wins. Don't make loud declarations.
description: A realistic path for adopting Debian on a team or in a company. Beyond technology — organizational politics, support, budget, internal approvals. Build with Claude a strategy of stacking small wins, not a large simultaneous migration.
date: 2026.04.23
label: Claude × Debian 22
prev_slug: claude-debian-21-telling-others
prev_title: Chapter 21 — Telling Those Around You
next_slug: claude-debian-23-passing-on
next_title: Chapter 23 — Passing It On to the Next Generation
cta_label: Learn with Claude
cta_title: Track record beats declaration.
cta_text: Declaring "the whole company will migrate to Linux" almost always fails. Start with one person, deliver results, and wait for allies to grow. This strategy fits Mythos-era organizations as well.
cta_btn1_text: Continue to Chapter 23
cta_btn1_link: /en/claude-debian/23-passing-on/
cta_btn2_text: Back to Chapter 21
cta_btn2_link: /en/claude-debian/21-telling-others/
---

## The Reality of Organizational Adoption

"The entire company will migrate to Linux" — this kind of large-scale project almost always fails. Business-app compatibility, internal support, user education, budget, internal approvals — the moment any one of them hits a wall, the project stalls.

What works instead is **starting with one person, building a track record, and waiting for allies to grow**. This chapter covers that realistic path.

## Section 1 — Start with Your Own Work PC

### A Fait Accompli, Rather Than an Approval

Begin by **starting to use Debian on your own work PC**. Whether this is allowed varies by your role, your work, and internal rules — but at many companies, even short of "OS choice is up to the individual," it is silently tolerated as long as the developer environment or work isn't disrupted.

- Developers: it isn't unusual to have a work PC on Linux.
- Data analysts: a Python / SQL environment feels natural on Linux.
- Web operations: server work often demands Linux anyway.
- Admin / sales: heavy Office dependence, but possible depending on the work.

### Alignment with the Mythos Era

As I wrote in [Chapter 11, "Claude Mythos — WordPress + AI"](/en/blog/claude-mythos-wordpress-ai/) and [Chapter 13, "Desk Work in the AI Era"](/en/blog/software-dev-independence/), **dependence on Windows is a high security risk in the Mythos era**. If the IT department is starting to understand this structure, migrating to Linux becomes a legitimate option.

### Ask Claude ①: Possibility in Your Own Work

> Based on my role [industry / role], main work [content], and organization size [headcount], if I replaced my work PC with Debian, organize:
>
> (1) Functions / apps that would obstruct work.
> (2) Alternatives or workarounds.
> (3) How to explain it and build agreement inside the organization.
> (4) Realistic probability of execution (high / medium / low).
> (5) A goal achievable in six months.

## Section 2 — Show Small Wins

### Speak with Deliverables

Once you've migrated to Debian, show the following.

- It got faster: boot time, app startup, processing speed.
- Fewer mistakes: documents managed as text, bugs traceable.
- Lower cost: license-fee reduction.
- New capabilities: tools you built with Claude, data processing.

**Show numbers.** Not "vaguely faster," but "boot went from 45s to 12s."

### Document on a Blog or Internal Wiki

Record your migration and operation on the internal wiki or your team's documents. When others read it, that itself becomes a sample.

## Section 3 — Build the Second and Third Person

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

## Section 4 — Relationship with the IT Department

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

### Ask Claude ②: A Proposal to the IT Department

> My affiliation: []. I want to propose to the IT department that I switch my work PC to Debian.
> For each category the IT department is likely to worry about (security, support, connections, licensing), put together a proposal of my response / handling.
> Tone is "consultation," not demand.
> Include a fallback plan (the steps to return to Windows) if it fails.

## Section 5 — Living with Business Apps

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

### Ask Claude ③: A Handling Map for Business Apps

> The business apps my organization uses are [list].
> Make a table for each app: the current state of Linux support, and the handling proposal (alternative / VM / separate machine / web version).
> Include handling for connections to internal systems (VPN, AD domain, certificates).

## Section 6 — Move It with Cost Analysis

### Organizational Decisions Move on Numbers

Organizations that don't move on logic do move on numbers. Build the calculation for Debian migration.

- **License-fee reduction.** Windows Pro, Office 365, security software.
- **Hardware life extension.** Old PCs no longer need replacement.
- **Support-cost reduction.** Less outsourced help on trouble (Claude-assisted self-resolution).
- **Risk reduction.** Reduced expected loss from Mythos-era zero-days.

A few tens of thousands to a hundred-plus thousand yen of savings per person per year is realistic. With 100 employees, that's millions to tens of millions of yen. **This is the number that lands with executives.**

### Ask Claude ④: A Cost Calculation for Your Organization

> Given my organization's size [headcount] and major licenses [Windows Pro, Office 365, security software], calculate annual savings if all or part of staff migrated to Debian + alternatives.
>
> (1) Direct savings (license fees).
> (2) Indirect savings (support, trouble handling).
> (3) Migration cost (training, migration work).
> (4) Cumulative profit / loss over five years.
>
> Give two scenarios: conservative and optimistic.

## Section 7 — Be Ready for the Long Game

### Organizations Change Over Five Years

For a small organization, 1–2 years; for a large company, 5 years. Simultaneous migration is impossible, but **a 10–20% increase per year** is realistic.

You as the first one, growing allies over 2–3 years, and after 5 years 30% of the organization is on Linux — this is the realistic picture of success.

### Build Something That Lasts

It's bad if "Linux culture in the company evaporates when you leave."

- Leave documents (internal wiki, operational procedures).
- Make it operable by multiple people.
- Present the migration option to new hires too.

**Grow it as a continuing system, not just one person's activity.**

## Section 8 — When It Fails, Withdraw

### Withdrawal Is a Strategy Too

Organizational Debian adoption can fail. IT policy changes, business apps update and stop working, the key person leaves, leadership changes — for many reasons.

When it fails, don't get emotional. Withdraw. **Just keep using Debian yourself.** The organization's direction and your own PC environment are separate things.

### Ask Claude ⑤: Criteria for Withdrawal

> If I am championing Debian adoption in an organization, what conditions, when met, should I judge as "time to withdraw"? Give five clear criteria.
> Also, when withdrawing, how to arrange the relationship with the organization so I can keep my own PC going.

## Summary

What you did in this chapter:

1. Understood why simultaneous organizational migration fails.
2. Set the strategy of starting from your own work PC.
3. Sorted out how to show small wins in numbers.
4. Confirmed how to keep IT not as the enemy.
5. Designed realistic compromises with business apps.
6. Got the practice of moving leadership with cost calculations.
7. Set the long-game posture and the criteria for withdrawal.

What you hold now:
- Debian operating in your own work.
- An internal proposal / documentation.
- Withdrawal criteria.
- Candidates for the second and third person.

In Chapter 23 — the textbook's final chapter — we cover **passing it on to the next generation**. How to hand what you've learned to your children and to those who follow. The shape of inheritance of learning, in an era of learning together with Claude.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
