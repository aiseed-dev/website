---
slug: claude-debian-01-what-you-lose-and-gain
lang: en
number: "01"
title: Chapter 1 — What You Lose, What You Gain
subtitle: Before deciding to wipe Windows, take stock together with Claude
description: Before you migrate to Debian and wipe Windows, take stock with Claude of what you lose and what you gain. Not in the abstract, but a concrete accounting tied to your own work, software, and habits.
date: 2026.04.23
label: Claude × Debian 01
prev_slug: claude-debian-prologue
prev_title: Prologue
next_slug: claude-debian-02-starting-conversation
next_title: Chapter 2 — How to Begin a Dialogue with Claude
cta_label: Learn with Claude
cta_title: Write what you lose and what you gain, in your own words.
cta_text: Not an abstract "Linux is wonderful," but a concrete table — "I lose feature X of Excel and gain Y in return" — kept close at hand. This table becomes the basis for every later decision.
cta_btn1_text: Continue to Chapter 2
cta_btn1_link: /en/claude-debian/02-starting-conversation/
cta_btn2_text: Back to Prologue
cta_btn2_link: /en/claude-debian/prologue/
---

## Why Begin with "What You Lose"

Many introductory books begin with "the wonders of Linux": freedom, speed, stability, zero cost. Reading them lifts your mood. But once you have actually migrated and notice "that doesn't run" or "I can't do this anymore," the initial excitement collapses fast.

This book starts from the opposite end. **First, lay out honestly what you will lose.** Only when you can still judge for yourself that what you gain outweighs that do you have a solid footing for migration.

The goal of Chapter 1, before you wipe Windows, is to build — together with Claude — a loss/gain table that is **yours personally**. Not in generalities, but a table tied to your work, your software, your habits.

## Section 1 — Face What You Will Lose Head-On

### Sort It into Four Categories

When thinking about "what you will lose," the worst thing is to worry about it vaguely. Work with Claude to break it into four concrete categories.

**A. Software that won't run as-is.**
Industry-specific applications, particular accounting software, CAD, some Adobe products, anti-cheat-enabled online games. These will not run on Debian as-is.

**B. Alternatives exist, but not fully compatible.**
Microsoft Office (→ LibreOffice, OnlyOffice), Outlook (→ Thunderbird), Edge (→ Firefox / Chromium). Alternatives exist, but complex Excel macros or Outlook's in-house server integration may need tuning.

**C. Habits you lose.**
"Press the Start menu and there's a search box," "Right-click to send to OneDrive," "Ctrl+Shift+Esc to open Task Manager" — muscle memory built up over twenty years. The first few weeks require deliberate replacement.

**D. Compatibility with those around you.**
Colleagues on Windows / Office, clients sending Excel files with macros, family members particular about Word formatting. Friction here is not your problem alone, so it takes time to resolve.

### Ask Claude ①: Take Stock of What You Will Lose

> I am currently on [your OS name and version], and I use the following software daily: [list your software, with purposes if possible]. My work is in [your industry / role], with [organization size, frequency of external communication].
>
> Given this, when I migrate to Debian, please lay out what I will lose, sorted into these four categories:
> A. Software that won't run as-is.
> B. Software for which alternatives exist but are not fully compatible.
> C. Habits I will lose.
> D. Compatibility issues with those around me (colleagues, clients, family).
>
> For each category, add severity (high / medium / low) and a short suggestion for how to handle it.

Claude's answer is tailored to your situation. **Save the returned table to a text file.** You will reference it many times in later chapters.

### If Even One "High" Severity Item Shows Up

If even one Category A item with "high" severity (business software with no alternative) shows up, do not migrate all your PCs at once. Take one of the following three options.

1. **Remove that use case from the migration target.** Keep the software on a separate PC (an old Windows machine) used only for that purpose, and move your main work to Debian.
2. **Run Windows in a virtual machine.** On Debian, run Windows through KVM or VirtualBox, and boot it only when needed. Note that software which leans heavily on the GPU will not perform well this way.
3. **Seriously explore alternatives.** Even software you thought was "absolutely irreplaceable" can surprise you: ask Claude to list alternatives, and unexpected options may appear.

Making this call is the core of this chapter.

## Section 2 — List What You Gain Without Exaggerating

### Avoid Abstract Praise

"Freedom," "fast," "stable," "free" — the adjectives commonly used in introductory books are too abstract to serve as decision material. Work with Claude to make concrete **how each of them shows up in your own life**.

### Ask Claude ②: Make "What You Gain" Concrete

> Based on the environment and work I laid out in the previous question, please organize — **concretely** — what I stand to gain from migrating to Debian, along the following axes:
>
> 1. Time savings (boot time, waiting for updates, frequency of restarts, app startup speed).
> 2. Monetary savings (OS, Office, security software, cloud storage subscriptions — as a yearly amount).
> 3. Mental gains (release from unwanted updates, forced restarts, ads, telemetry).
> 4. Skill gains (command line, package management, editing config files, dialogue with Claude).
> 5. Long-term independence (distance from vendor lock-in, extending the life of old hardware, reducing attack surface in the Mythos era).
>
> For each axis, answer with numbers or concrete examples. Do not use adjectives like "wonderful" or "comfortable."

Forbidding adjectives to Claude is a trick. Once abstract expressions are blocked, the answer turns concrete.

### Verify "Do I Really Gain This?"

Don't swallow Claude's answer whole; doubt it and push back.

> Among the answers just now, please separate those you can confidently say "will definitely be gained by migrating to Debian" from those that "may not be gained depending on the person or the use case." For the latter, explain under what conditions they would not be gained.

This question makes Claude honest. For example, "monetary savings" is solid, but "performance improvement" is pronounced on old hardware and slight on top-end new PCs — you get conditional answers like that back.

## Section 3 — Combine into a Single Table

### Put It in a Table, Keep It Close at Hand

Compile what you lose and what you gain into a single table you can take in at a glance. The format looks like this.

```
# My Debian Migration — Loss / Gain Table  (created: 2026-04-23)

## What I Lose
| Category | Specifics | Severity | Handling |
| --- | --- | --- | --- |
| A Won't run | Adobe Premiere | High | Migrate to DaVinci Resolve (Linux version) |
| A Won't run | In-house △△ system | High | Keep an old Win10 machine for work |
| B Alternative | MS Office | Medium | LibreOffice; for complex files, ask a colleague |
| C Habit | OneDrive right-click menu | Low | Replace with an rsync script |
| D Compatibility | Monthly report as Excel macro | Medium | Python for my own work; Office Online only for submission |

## What I Gain
| Axis | Specifics (in numbers) | Conditions |
| --- | --- | --- |
| Time | Boot 30s → 8s; time spent waiting for updates 2h/month → 0 | The gap is even larger on an older SSD |
| Money | Office 365 ¥14,000/yr, Win Pro equivalent license, security software ¥6,000/yr → ¥20,000+/yr saved | Half that if I keep one license for business compatibility |
| Mental | No unexpected restarts, no ads, no stress from disabling Recall | — |
| Skill | Command line, package management, daily operational dialogue with Claude | Learning cost in the first month |
| Independence | Reviving a 10-year-old PC; able to patch myself in the Mythos era | Only if I keep learning |

## Conclusion
Overall judgment: [migrate / keep one Windows machine for work, main on Debian / hold off]
Decisive factor: [one line]
```

Keep this table as a text file (Markdown). Don't write it in Word. **Your first Debian document is born before you even start using Debian.**

### Ask Claude ③: Have It Draft the Table

> Please organize the content from the previous two questions into the Markdown table format below. Fill it with numbers and specifics. Do not include adjectives. [paste the format above]

This gives you a first draft. You then adjust what's left by hand.

## Section 4 — Make the Decision

### Four Conclusion Patterns

Looking at the loss / gain table, the conclusion settles into one of the following.

**Pattern 1: Migrate fully.**
What you lose is all low-to-medium severity, and there are alternatives. What you gain is clear. → Wipe Windows from your main PC and consolidate on Debian. You can proceed through the rest of this book as-is.

**Pattern 2: Main work on Debian, one Windows machine kept for work.**
You have one or two Category A items with "high" severity, and the work that uses them is limited to a portion of your day. → Main PC is Debian; a separate Windows machine handles part of the work. Most of this book still applies.

**Pattern 3: Postpone migration by six months.**
You have many Category A items you can't replace right now. First, spend time researching alternatives. → Read Parts 1 and 5 of this book first to prepare, and defer Part 2 (installation).

**Pattern 4: Don't migrate.**
Category A items are woven through the core of your work, and no path to replacement is visible. → Make that call honestly. The rest of this book is still worth reading as practice in "how to learn with Claude," but you won't be executing it.

Even in Pattern 4, the time spent on this chapter is not wasted. **A document that puts your environment into words** stays in your hands. It will be useful later, when your situation changes.

### You Can't Decide Without Writing It Down

The most important thing here is this: **do not settle for thinking it through in your head alone.** Always write it out. Put it into a table. Go back and forth with Claude to raise the precision.

Before you write it down, "I can probably do it" and "I'm vaguely uneasy" have almost nothing to do with fact. The moment you write it down, they become — for the first time — something you can base a decision on.

## Summary

What you did in this chapter:

1. Took stock of what you will lose, in four categories (together with Claude).
2. Made what you gain concrete, along five axes (asking Claude with adjectives banned).
3. Combined it all into a single Markdown table.
4. Chose one of four conclusion patterns.

What you hold now:
- `debian-migration-decision.md` (the loss / gain table)
- A one-line note of your decisive factor

In Chapter 2, we cover **how to begin a dialogue with Claude** itself. How to form a good question, examples of bad questions, how to break out when a dialogue stalls — the techniques of dialogue, laid out as a foundation for learning Debian.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
