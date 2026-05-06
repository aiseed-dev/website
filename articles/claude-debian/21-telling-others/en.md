---
slug: claude-debian-21-telling-others
lang: en
number: "21"
title: Chapter 21 — Telling Those Around You
subtitle: Family, friends, colleagues — show the use, don't try to convince
description: To tell people close to you about Debian, "showing how you use it" works better than persuasion. Tailor the message to family, friends, and colleagues. Use Claude to put together explanations that fit the listener.
date: 2026.04.23
label: Claude × Debian 21
prev_slug: claude-debian-20-community
prev_title: Chapter 20 — Engaging with the Community
next_slug: claude-debian-22-organization-adoption
next_title: Chapter 22 — Adoption in an Organization
cta_label: Learn with Claude
cta_title: Examples, not arguments.
cta_text: Insisting "Linux is better" moves no one. When they see you running daily life comfortably on Debian, the curious ones come forward. That's where it starts.
cta_btn1_text: Continue to Chapter 22
cta_btn1_link: /en/claude-debian/22-organization-adoption/
cta_btn2_text: Back to Chapter 20
cta_btn2_link: /en/claude-debian/20-community/
---

## The Difficulty of Telling

Just because you find something good doesn't mean someone else will receive it the same way. **Debian fitting you doesn't mean it will fit your family or colleagues.**

In this chapter we cover how to avoid the failures common when telling, while handing it precisely to those who do show interest.

## Section 1 — Why Persuasion Doesn't Work

### Few People Move on Logic

"Debian is free software, secure, long-term stable, free of cost, and revives old PCs." — Listing this rarely moves anyone. Why?

For most people, a PC is **a tool that already works**. Changing what works has unclear payoff against the cost (time, learning, anxiety). Logically listed advantages stay abstract; they aren't felt.

### "Showing" Works Better

What works instead is **showing** what you actually do on Debian.

- When family asks "How do you organize photos?", answer with `digiKam`.
- When a colleague is stuck on "I want to edit this PDF," demo with `Xournal++`.
- When a kid says "I want to play games on the parent's PC," pick games that run via Steam Proton together.

**Interest comes first; the migration conversation follows.**

## Section 2 — Telling Family

### Don't Rush

Telling family deserves the most care. Suddenly changing the PC environment of someone you live with disrupts daily life. **Move only after the person themselves develops interest in Debian.**

### For Kids: Give Them an Experience

If you have kids, putting Debian Xfce on an old laptop and giving it to them as their PC is an option.

- Separate from the parents' Windows machine — a "lab" PC for the kids.
- Minecraft, Scratch, Code.org, Krita — educational software is well-stocked.
- The experience of "building your own game" together with Claude.

Kids have fewer preconceptions about what an environment "is." If anything, they find Windows-specific rituals (accounts, ads, consent screens) puzzling. **It is fine if Debian is "the normal" for them.**

### For Older Family: Simplify

If an older parent's PC is full of trouble, Debian + Xfce + a minimal app set can actually be easier to use.

- Browser, mail, Zoom, photo viewer — that's enough for many.
- Zero Windows updates, antivirus pop-ups, or ads.
- Usable until it physically breaks.

That said, **be prepared to be the support person**. Have a way for them to reach Claude (so the family can ask Claude themselves), or make yourself easy to contact.

### Ask Claude ①: A Proposal Tuned to Your Family Composition

> My family setup: [age of children / how the spouse uses a PC / situation of parents]
> Without it being coercive, propose three opportunities for introducing Debian to family members in ways that make them think "I'd like to try it."
> Add the expected reactions and the preparation on my side for each.

## Section 3 — Telling Friends

### Tech-Inclined Friends

With a tech-curious friend, conversation happens naturally. Share dotfiles, show how you use Claude, let them try the apps you built — that's enough.

### Non-Tech Friends

For non-tech friends, what works is "the story of getting easier," "the story of saving money," "the story of an old PC coming back to life." Don't preach.

"Office 365's annual fee is gone now." "I'm running Debian on an old ThinkPad as my daughter's PC." Short, no boasting, draw out questions.

### Ask Claude ②: How to Tell a Friend

> Suppose I introduce Debian to my friend [tech level, interests]. Propose:
> (1) Conversation hooks.
> (2) Topics to avoid ("Windows is bad," etc.).
> (3) The next step when the friend shows interest.

## Section 4 — Telling Colleagues

### Be Careful Because Work Is Involved

A company PC environment is, often, not yours to change. **Conversations about migrating a work PC connect to formal organizational topics (Chapter 22).** Here we limit to **a colleague's personal PC**, separate from work.

### Start from a Shared Pain

Start where a colleague is grumbling.

- "Windows Update reboot waits are too long" → faster on Debian.
- "Office 365 is expensive" → **switch the content to Markdown and Word becomes optional — convert to .docx with pandoc only when you have to.**
- "Excel is slow, the macros keep breaking" → **CSV + Python (pandas) does the math in seconds, and the code keeps working next month too.**
- "I can't part with my old PC" → extend its life with Debian.

Speak as your own experience. "Doing this resolved it for me," without forcing.

### Show the Quality of Your Work

When a colleague notices the speed of your work, the lack of mistakes, the tidiness of your documents, they ask "how do you do it?" Then, and only then, talk about Debian + Claude.

**Results first, tools second** — this order doesn't change.

## Section 5 — People to Whom You Shouldn't Tell

You don't need to tell everyone. The following are best not told.

- **People not interested in tech.** Waste of time.
- **"Everything should be the same" types.** They dislike differences in environments.
- **People who expect you to support them.** They will come to you forever when something goes wrong.
- **People moved by authority.** Microsoft's brand is the basis of their trust.

Not telling isn't coldness. **It is respecting where they are.**

## Section 6 — Mindset of the One Teaching

### Don't Teach Everything

When you introduce someone to Debian and install it together, drop the "I will teach all of it myself" stance. **Hand them the same form of "learning together with Claude" you used.**

"I asked Claude all along when I started too. Open Claude yourself and let's ask together when you get stuck."

This reduces dependency on you and supports the other person's autonomy.

### Hand Over This Textbook

This textbook you read can be handed off as a URL. The person reads at their own pace and dialogues with Claude on their own. You only run alongside.

### Allow Failure

If they give up partway, don't blame them with "but I introduced it to you." The timing just wasn't right. Six months or a year later, they may come back asking again.

### Ask Claude ③: Things to Watch When Teaching

> When I introduce Debian to family or colleagues, organize the typical failures and how to avoid them, on these axes:
> (1) Don't show off knowledge.
> (2) Respect the other person's pace.
> (3) Don't take on too much support.
> (4) Don't blame them for giving up.
> (5) Don't break the relationship.
>
> For each, give concrete examples of what to say and not to say (good vs. bad).

## Section 7 — "Continued Use" Is the Strongest Message

The strongest message is **that you keep using Debian and enjoy it**.

- Ten years later your PC is still alive.
- ¥10,000 a month freed up; you started something with it.
- You build your own tools with Claude, and work got easier.
- When trouble happens, you fix it without panic.

People around you watch this and, eventually, someone says "I want to do that too." Until that day, just keep using it, with pleasure.

## Summary

What you did in this chapter:

1. Adopted the strategy of "show the use, don't argue."
2. Sorted out how to tell family, friends, and colleagues differently.
3. Identified people not to tell.
4. Confirmed the teacher's mindset (don't teach everything, allow failure).
5. Picked up the way to hand off "learning with Claude" to others.

What you hold now:
- A policy for whom to tell, and how.
- The setup to hand over this textbook.
- The posture of "continued use is the message."

In Chapter 22, we go beyond the individual to **adoption in an organization**. The political and organizational challenges, not just technical ones, of using Debian on a team or company — sorted out with Claude.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
