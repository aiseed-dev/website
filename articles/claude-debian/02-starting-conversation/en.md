---
slug: claude-debian-02-starting-conversation
lang: en
number: "02"
title: Chapter 2 — How to Begin a Dialogue with Claude
subtitle: The shape of a good question, examples of bad ones, and how to break out of stalled dialogue
description: The basic craft of using Claude as a learning partner. The difference between vague and specific questions, how to hand over context, how to press further, and how to spot mistakes. Before learning Debian, this chapter lays out the techniques of dialogue itself.
date: 2026.04.23
label: Claude × Debian 02
prev_slug: claude-debian-01-what-you-lose-and-gain
prev_title: Chapter 1 — What You Lose, What You Gain
next_slug: claude-debian-03-telling-environment
next_title: Chapter 3 — How to Tell Claude About Your Environment
cta_label: Learn with Claude
cta_title: Claude is a tool. How you use it changes the result.
cta_text: Just as some people can hammer a nail and some cannot, Claude too has a way of being used well. What you acquire in this chapter transfers beyond Debian to everything else you will ever learn in the AI era.
cta_btn1_text: Continue to Chapter 3
cta_btn1_link: /en/claude-debian/03-telling-environment/
cta_btn2_text: Back to Chapter 1
cta_btn2_link: /en/claude-debian/01-what-you-lose-and-gain/
---

## Where This Chapter Fits

In Chapter 1 we took stock of "what you lose and what you gain." That already involved calling on Claude three times. Some of you will have felt it click; others will have been rattled when a thin answer came back.

In Chapter 2 we set out **how to use Claude itself**. Debian steps aside for now. This is because the quality of your dialogue with Claude determines the quality of every remaining chapter in this book. If you carry bad dialogue habits into Chapter 3 and onward, Claude's answers will thin out steadily.

The craft you acquire here transfers to domains beyond Debian — cooking, languages, law, parenting, business design — all of them. **The craft of learning with Claude is a foundational literacy for the AI era.**

## Section 1 — Good Questions vs. Bad Questions

### Typical Bad Questions

The following four are classic cases where Claude returns only useless answers.

**Bad question 1: "What is Debian?"**
Too broad. Claude can only return a textbook-style abstraction. Your situation is nowhere in the question, so nothing surfaces that means anything to you.

**Bad question 2: "Is Debian good?"**
There is no criterion for "good." Claude can only dodge by listing both sides.

**Bad question 3: "I got an error."**
The content of the error, what you did before and after, and your environment are all missing. Claude is not a mind-reader.

**Bad question 4: "Tell me how to do it."**
What the procedure is for, which environment it is for, how far you have already gotten — none of that is clear. Claude returns a generic procedure, and half of it misses your situation.

### The Shape of a Good Question

Good questions, by contrast, share a common shape. Include three elements.

**Element A: Context (your situation).**
What OS; what you are trying to do; how far you have gotten; what you did just before.

**Element B: Specifics (facts and errors).**
The error message in full, without abbreviating; file names; commands; versions; timestamps.

**Element C: Purpose (what you want to get out of it).**
Not just "I want it to work," but "I use this every morning for work, so I want it to start in under 10 seconds" — add the criterion you are judging against.

Once these three are in place, Claude's answer becomes far more concrete.

### Ask Claude ①: Have Your Own Question Edited

> I am about to start learning Debian. Is the following a good question?
>
> "I'd like to install Debian. How should I do it?"
>
> If it is a bad question, point out what is bad about it and rewrite it into a good question. Then, show me the answer to the rewritten question.

Claude will edit it for you. This approach works in every area of learning. "Rewrite my question into a good question" is a powerful prompt.

## Section 2 — How to Hand Over Context

### All at Once vs. Bit by Bit

In dialogue with Claude, the order in which you hand over context affects the outcome. There are two approaches.

**Bulk style: a long self-introduction at the start, then every following exchange builds on it.**
Pro: Claude answers from the same premise every time.
Con: the initial setup takes time.

**Drip style: attach only the context you need with each question.**
Pro: easy to start.
Con: you end up rewriting the same context over and over, and pieces slip out along the way.

This book recommends **bulk style**. Once, at the start, organize your environment in a text file and send it to Claude. That file becomes your "profile for Claude."

### Ask Claude ②: Build Your Profile

Create a text file called `my-claude-profile.md` and fill in the following.

```markdown
# My Profile (for Claude)

## Machine
- PC: [maker, model, year]
- CPU / Memory / Storage
- Current OS

## Work
- Industry / role
- The core of a day's work (writing, coding, design, etc.)
- Frequency and format of external communication

## Software I Use
- Daily essentials (browser, mail, office)
- Occasional but important
- Industry-specific

## What I Am Uneasy About
- The specific things I fear going wrong during migration
- What I'd be in trouble without

## Goal
- Where I want to be in six months
```

Once you have filled it in, send it to Claude like this.

> This is my profile. [paste the file content]
>
> From now on, when I ask questions about learning Debian, please answer with this profile as the premise. If there is anything you cannot judge from the profile, ask me before answering.

This one-time setup changes the quality of every later exchange significantly.

## Section 3 — The Craft of Pressing Further

### Don't Stop at the First Answer

The single biggest way beginners lose out in dialogue with Claude is **settling for the first answer**. Claude's first answer is often a textbook-style generalization. Once you press further from there, the answer suddenly gets deeper.

### Patterns for Pressing Further

**Pattern 1: Demand concreteness.**
> "Please be more concrete. For my environment [paste again], lay out the steps one by one."

**Pattern 2: Demand trade-offs.**
> "What are the drawbacks of this choice? Who would it be a bad fit for?"

**Pattern 3: Make it argue the opposite side.**
> "If you had to recommend Ubuntu over Debian, what reasons would you give?"

**Pattern 4: Demand units and numbers.**
> "Put 'fast' and 'light' into numbers. How much faster does it get? By how many MB does memory usage drop?"

**Pattern 5: Ask for confidence level.**
> "In this answer, how far can you say things with confidence? Where has speculation crept in?"

Pattern 5 is especially powerful. Claude answers honestly: "This part is a general tendency; the current situation may have changed."

### Ask Claude ③: Experience the Follow-Up

> For the question "What is the best desktop environment for Debian?", first give me an ordinary answer. Then show how the answer would deepen if I pressed further using the following five patterns: (1) concreteness (for my environment [paste again]); (2) trade-offs; (3) the opposite stance; (4) units and numbers; (5) confidence level.

Running through this exercise once makes the feel of pressing further second nature.

## Section 4 — Spotting Claude's Mistakes

### Claude Gets Things Wrong Sometimes

Claude is powerful, but not perfect. In particular, watch for these three.

**A. Stale information.** Claude's knowledge stops at some point in time. The very latest Debian version, the latest state of packages, and recent vulnerability information are all suspect.

**B. Hallucinations.** Claude can confidently produce commands that don't exist, package names that don't exist, and URLs that don't exist.

**C. Over-generalization.** Answers that begin with "in general" or "usually" may fail on your specific situation.

### Three Principles of Verification

Three habits that keep you from swallowing Claude's answers whole.

**Principle 1: Double-check before running.**
Especially for destructive commands like `sudo rm`, `dd`, `mkfs`, or `parted`, ask Claude again before running: "What does this command do? Is it definitely safe?"

**Principle 2: Cross-check against official documentation.**
The Debian official manuals, package descriptions via `apt show`, the `man` command. Confirm that these primary sources and Claude's answer do not contradict each other.

**Principle 3: When you point out a mistake, check whether it retracts properly.**
When you say to Claude "that answer is wrong, the truth is X," does it retract cleanly, or argue back with grounds? Either is fine. But Claude sometimes retracts where it shouldn't — accommodating you even though you are actually wrong — so when you are not sure who is right, ask "Show the grounds for both sides."

### Ask Claude ④: A Verification Prompt

> I am going to verify what you answered earlier.
>
> (1) In that answer, which parts are sure to match the current state as of 2026?
> (2) Which parts may be stale?
> (3) Among the commands and package names, are there any whose existence you cannot confirm (possible hallucinations)?
> (4) For points I should not take on your word alone, give me primary-source URLs or commands I can check against.

Using this prompt regularly lowers the risk of hallucination and stale information.

## Section 5 — Breaking Out When Dialogue Stalls

### Common Stalls

- Claude repeats the same answer.
- In a long dialogue, context drops out and answers go off-target.
- You keep asking small questions until you lose sight of the whole.

### Patterns for Breaking Out

**Pattern 1: Reset.**
Start a new conversation, paste the profile again, and rewrite your question as a better one. It takes courage to let go of a conversation that has grown too long.

**Pattern 2: Ask for a summary.**
> "Please summarize our conversation so far, separating it into the conclusion, the grounds for it, and any questions that remain open."

This brings the overall picture back.

**Pattern 3: Step back.**
> "What was my original purpose behind this discussion? Is the option we are currently discussing really relevant to that purpose?"

This is also a question worth asking yourself.

**Pattern 4: Write on paper.**
Step away from Claude and write out the key points by hand. The dialogue's partner is Claude, but the decision is yours. Sort things out on paper, then come back and ask Claude again.

## Summary

What you did in this chapter:

1. Learned the three elements of a good question (context, specifics, purpose).
2. Established the bulk-style habit of handing your profile to Claude.
3. Experienced five patterns for pressing further.
4. Learned three principles for spotting Claude's mistakes.
5. Prepared four ways to break out when dialogue stalls.

What you hold now:
- `my-claude-profile.md` (your profile)
- A template of question shapes, for reference when you need it

In Chapter 3 we go one step deeper into the profile and cover **concrete ways to tell Claude about your hardware and software environment accurately**. How to use basic commands like `lscpu`, `lsblk`, and `dpkg -l`, and how to hand their output to Claude effectively.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
