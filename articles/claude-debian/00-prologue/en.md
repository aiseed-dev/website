---
slug: claude-debian-prologue
lang: en
number: "00"
title: Learning Debian with Claude — Prologue
subtitle: What "learning with Claude" means. Why this approach. What you can expect.
description: A new kind of textbook you read with Claude beside you. Not a one-way "book that teaches," but a dialogue-based way of learning where the answer changes according to your own situation. The prologue lays out why this approach was chosen and what you can expect.
date: 2026.04.22
label: Claude × Debian Prologue
prev_slug:
prev_title:
next_slug: claude-debian-01-what-you-lose-and-gain
next_title: Chapter 1 — What You Lose, What You Gain
cta_label: Learn with Claude
cta_title: Not "reading" but "dialoguing"
cta_text: Open Claude beside the textbook as you read. Type your situation into Claude and get an answer fitted to you. The same book becomes different learning for every reader — that is the premise of this book.
cta_btn1_text: Go to Chapter 1
cta_btn1_link: /en/claude-debian/01-what-you-lose-and-gain/
cta_btn2_text: All chapters
cta_btn2_link: /en/claude-debian/
---

## Why Start with a Prologue

The usual textbook begins at Chapter 1. A long preamble before getting into the technical content is considered a waste of time.

This book takes the opposite position. **Unless we first share the method of learning itself, this book does not work.** So the prologue lays out three things: what "learning with Claude" means, why this approach was chosen, and what you can expect.

If you skip the prologue and jump into Chapter 1, the "Ask Claude" boxes at the end of each chapter will look like just reference material. They are not. These boxes are the body of the book; the running prose of each chapter only supplies the context for the question you throw into the box.

This prologue exists to make that clear.

## Section 1 — What "Learning with Claude" Means

### A "Book You Read" vs. a "Book You Dialogue With"

This book is not designed to be read alone from start to finish.

Into the prose of each chapter, **sample dialogues with Claude** are woven in. They are not "this is how Claude should answer"; they are **the skeletons of answers I actually got when I put the same questions to Claude**. If you ask the same questions, answers of a similar shape will come back. But once you add your own circumstances, the answer becomes tailored to you.

In addition to the running prose, each chapter has an "**Ask Claude**" box. It is a template. You fill in the [your situation goes here] portions with your own words and send the whole thing to Claude. The answer that comes back becomes *your* conclusion for that chapter.

Put another way, only half of the book's content is printed. The remaining half is completed by the dialogue between you and Claude.

### The Moment "Teacher" and "Learner" Flip

The usual textbook is a one-way medium: the author conveys what they know to the reader. The author does not know the reader's situation, so the writing becomes abstract — "in general this," "typically that."

Once Claude sits beside you, that relationship changes.

You tell Claude your situation — the software you use, the vintage of your PC, the size of your organization, what you are worried about. Claude returns an answer matched to your situation. **At that moment you shift from being the recipient of the book to being the leader of the dialogue.**

The book's role shrinks to providing the "first question" and the "framework of the dialogue." The textbook becomes not a map but a compass.

### Author, Reader, and Claude — Three Roles

There are three characters in this book.

**The author (me)** actually uses Debian and has learned through dialogue with Claude. The author's role is to lay out **what questions to ask so that learning deepens**. Not to hand over the answers themselves.

**The reader (you)** is the only person who knows your situation best. The reader's role is to **convey that situation to Claude accurately, and to weigh the returned answer with your own judgment**. A stance of passively waiting for answers will not make this book work.

**Claude** holds technical knowledge and can adjust its answers based on the dialogue. Claude's role is to **translate the book's questions into concrete answers fitted to the reader's situation**. Claude is not omniscient — it makes mistakes, and it may not know the latest information. So the reader's judgment has the final say.

Only when all three play their parts is this book complete.

## Section 2 — Why This Approach

### The Premises of the Technical Book Have Broken

The technical book was traditionally a medium for "fixing the latest correct information onto paper and delivering it to many readers." That premise has broken down in two ways.

**First: the speed of technical change overtook the speed of paper updates.** Debian has several minor releases a year, and the surrounding tools change faster still. Locking information onto paper has lost much of its meaning when that information goes stale the moment it is written.

**Second: readers' circumstances are too varied.** Migrating from Windows 11 is a different story from migrating from macOS, which is different again from migrating from a Chromebook. The nature of the work, the size of the organization, the software in use — all differ from person to person. A single book cannot give the optimal answer for every case.

With Claude's arrival, both premises can be sidestepped. **Ask Claude for the latest information; let Claude match the individual situation.** The book only has to carry "how to form the question" and "the underlying stance."

### From "Learning to Remember Answers" to "Learning to Form Questions"

As I wrote in [Chapter 9, "AI and the Individual"](/en/insights/ai-and-individual/), for an individual in the AI era the most important skill has become the ability to form the right question. Remembering answers now takes a few seconds with Claude. Conversely, if you do not know what to ask, even Claude cannot take you anywhere.

This book trains that question-forming ability, using Debian as the subject. Learning Debian is certainly a goal, but so is acquiring **the craft of using Claude as a learning partner**.

That craft transfers to other domains — another OS, another technology, another field entirely. After finishing this book, you will be able to "learn something together with Claude." As a by-product, this may matter more than the Debian knowledge itself.

### Alignment with the Mythos Era

As I wrote in [Chapter 5, "Mythos Has Arrived"](/en/insights/mythos/), we have entered an era in which AI can discover zero-day vulnerabilities in a few hours. In this era, continuing to use a black-box OS is dangerous.

Put the other way: **pairing a transparent OS like Debian with a transparent thinking-aid like Claude** is the most rational configuration for the Mythos era. The OS lets you see inside, and if necessary, fix it yourself. Claude assists your judgment, but the decision remains yours. Both are designed so that they do not take your initiative away.

This book's approach — "learning with Claude" — is the style of learning most aligned with the structure of this era. That is why this approach was chosen.

### Why Linux Now — Which Architectures the AI Era Rewards, Which It Doesn't

I just wrote that "a black-box OS is dangerous." There is a deeper reason behind it. **In the AI era, the structural difference between Linux and Windows is, for the first time, taking on decisive weight.**

#### 1. AI's acceleration is not symmetric

AI — Claude and other LLMs — has made every OS task easier. At first glance, Linux and Windows seem to benefit equally. They don't.

- Linux's strength is **transparency and operability**. It was always the "powerful if you know it, unusable if you don't" kind of strength — its only weakness was **the cost of the on-ramp**. In an era where Claude explains `journalctl` in seconds, that on-ramp cost is effectively zero.
- Windows's strength is **completing tasks through a GUI**. The on-ramp was already cheap. AI cannot make it any cheaper.

In other words, **AI dropped the price tag on Linux's strengths**, and only Linux's. This asymmetric acceleration starts to bite in the next few years. That this book is written *now* is largely because of that.

#### 2. Fused stack vs. layered stack

Another asymmetry sits inside the OS architecture itself.

Windows has, layer after layer, been inserted in a way that **cannot be separated from the layers below it**.

```
[new ] Copilot / Recall / Windows Copilot+
[    ] Telemetry (DiagTrack / Windows Update)
[    ] Bundled apps (Edge / Store / OneDrive / Teams)
[    ] Shell (Explorer.exe / taskbar / Start)
[    ] Win32 / WinUI (welded to DWM)
[    ] NT kernel
```

"You can't remove Cortana," "You can't remove Edge" — for the same reasons, **Copilot and Recall cannot be removed**. This is not Microsoft being malicious; it's that the stack was never designed for separation in the first place.

Linux is the opposite. Each layer is independently replaceable.

```
[user picks] Claude Code / Zed / local LLM …  (bolted on)
[user picks] GNOME / KDE / Xfce / none
[user picks] Wayland / X11 / none
[          ] kernel
```

AI runs only when the user invokes it. The kernel doesn't know AI exists; neither does the shell. **The structure itself lets you say "I want it here, but not there."** It is this layer separation that lets Chapters 6 and 9 say "the DE can be thin, and you can swap it," and that lets Chapters 17 and 19 say "revive an old PC."

#### 3. Recall isn't an accident — it's the natural endpoint

This is the part to look at coldly. Microsoft's Recall — which takes screenshots every few seconds and indexes them with AI — is not an "overreach mistake." On a fused stack with AI welded in, **it is what was bound to emerge**.

- Every layer can see every other layer → a privileged process holds, from day one, the right to see the entire screen.
- AI is embedded in the OS → that privileged process now has a pipe to hand what it sees to the AI.
- A Microsoft account and the cloud are already wired in → no guarantee that what was handed over stays local.

**Trying to build the same feature on Linux is technically difficult.** Wayland structurally restricts cross-application peeking, the kernel doesn't know about screens, and the culture keeps AI bolted on from outside — so no one starts with the privileges that would aggregate it all. **The fact that it cannot be built** is not ideology; it is the consequence of the design.

#### What this book assumes

In short, this book quietly assumes three things.

1. In the AI era, the cost of Linux's strengths (transparency, operability) collapsed.
2. Linux's layered architecture lets you keep AI as **a tool the user calls**, bolted on from outside.
3. Windows's fused architecture cannot help but embed AI as **a pipeline the user cannot opt out of**.

Every concrete migration step in Chapter 1 and beyond stands on those three premises. **"Switching to Linux" is a structural choice for keeping your initiative in the AI era** — not a matter of taste or ideology. That is the ground this book stands on.

## Section 3 — What You Can Expect

### What You Hold When You Finish

When you have read this book to the end and filled every "Ask Claude" box with your own situation, you will hold four things.

**One: a PC that runs Debian.** Because you move your hands as you read, by the time you finish all 24 chapters including the prologue, your main working environment should be Debian.

**Two: notes tailored to you.** You will end up with as many text files as there are chapters, each holding the results of a dialogue. Taken together, they become *the documentation of your Debian environment*. When something goes wrong, these notes will help you.

**Three: the craft of dialogue with Claude.** How to form a question so that a good answer comes back, how to convey a situation so that precise advice is returned, where to trust Claude and where to doubt it — these become second nature.

**Four: an independent stance.** Keeping distance from vendor lock-in, eliminating black boxes, widening the range of what you can fix with your own hands — these are no longer abstract words but experience you carried out with your own hands.

### What You Will Not Hold

To be honest, here is what this book will not give you.

**Perfect technical knowledge.** This book does not explain every Debian command, every configuration option, every package. That is the job of the official manuals and of Claude.

**An environment identical to anyone else's.** The dialogue results differ from person to person, so the final environment does too. This is not a flaw; it is part of the book's design. Your environment gets optimized to your situation.

**A procedure that completes without Claude.** If you read only this book without opening Claude, only half of it works. Please accept that going in.

### Time and Cost

Budget 30 minutes to 1 hour per chapter. All 24 chapters take 12 to 24 hours — a volume you can finish over two or three weekends.

Cost is close to zero. Debian is free; most applications are free. Claude's free tier is enough to work through almost all of the exercises in this book. If you want to go deeper later you can upgrade to the paid plan ($20/month), but it is not required.

### Hardware and the "Dual-Boot Trap"

For hardware, the PC you already have is enough. At this point many introductory books recommend dual-boot (keeping Windows and Debian side by side on the same machine), but this book does not take that road.

Laptop dual-boot in particular has too many practical problems. Windows Update periodically overwrites the bootloader (GRUB) and Debian stops booting; suspend/resume becomes unstable on one side; power management breaks and the battery drains abnormally; disk space runs short and both sides end up cramped; the combination of BitLocker and encryption makes the machine unbootable — these are the first landmines a beginner steps on, and the leading cause of people ending up hating Debian itself.

**Move your data safely onto a separate drive, and then wipe Windows without hesitation.** In the end this is easier, more stable, and the learning goes deeper. If you ever want to turn back, keep an old PC around, or clone Windows onto an external SSD beforehand. Reviving an old PC is in fact an ideal use case for this book.

The decision to wipe may feel big, but it is the very stance I wrote about repeatedly in [Chapter 14, "Subtraction Design"](/en/insights/subtraction-design/). Instead of half-heartedly holding onto both, commit to one side. This whole book is built from choices of that kind.

### One Preparation Before You Begin

Before you close the prologue and move on to Chapter 1, there is one thing to prepare.

**Open [claude.ai](https://claude.ai) in your browser.** Create an account if you don't have one. That's it.

From Chapter 1, "What You Lose, What You Gain," the dialogue with Claude begins.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
