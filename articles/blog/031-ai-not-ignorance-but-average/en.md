---
slug: ai-not-ignorance-but-average
title: "AI Isn't Wrong Because It's Ignorant — What One Bad Answer Teaches About Working With AI"
subtitle: "What comes back is the commercially weighted average of public discourse — and once you know how it errs, you know how to use it"
date: 2026.07.21
description: I asked a generative AI about exchanging text data between systems, and it answered that "zero trust strangles operations — the most robust option is physical isolation with a data diode." Plausible-sounding, and upside down. The AI was not ignorant of the subject. It traced the center of gravity of the vendor discourse that fills the web around the words "zero trust" — a commercially weighted average of public discourse. This piece dissects one wrong answer to locate the mechanism of the error, then draws out five rules for use — hand it primary sources, choose your own canon, read plausibility and correctness separately, use it where you can verify, and throw the opposing view at it.
lang: en
label: Blog
category: Structural Analysis Notes
---

# AI Isn't Wrong Because It's Ignorant

## It Started With One Wrong Answer

I had asked a generative AI about exchanging text data between systems. The answer that came back looked plausible at first glance. It opened by explaining the zero-trust idea correctly, went on to argue that implementation is difficult and strangles operations, and finally landed on the conclusion that "the most robust option is to place a data diode (a one-way communication device) between physically isolated wired networks." Better to restrict communication at the physical layer, it said, than to build complex software defenses — safer and easier to operate.

The answer does line up some genuinely valid concerns. Parser vulnerabilities are real, and DDoS is a real threat to public endpoints. Even so, the conclusion was upside down. And the way it was wrong expressed the nature of AI so well that I want to put it on record.

## Where It Went Wrong

The definition of Zero Trust Architecture (ZTA) is written clearly in NIST SP 800-207. The core is this: never use network location as the basis of trust. Even inside the corporate LAN, every request is authenticated, authorized, and encrypted, every time. It is a question of how trust is decided, not of which path the traffic takes.

Yet that answer, having stated this definition correctly at the top, quietly rewrote it in the body into "ZTA = exposing things to the internet." It then attacked that substitute and concluded, "therefore physical isolation is better." ZTA is about the criteria for judging trust, not about the path. You do ZTA over a leased line too, and nothing requires a public endpoint. By swapping the premise, the conclusion came out 180 degrees off.

The individual points fail the same way. "To do zero trust you are forced to depend on a giant cloud IdP" is wrong: that is needed only when you must dynamically evaluate an open-ended population of people and devices. In system-to-system integration the peer is a known, fixed machine, so mutual TLS with your own CA, or WireGuard key pairs, is all it takes. It runs offline, with zero external dependencies. The "it degenerates into cloud dependence" storyline is not a consequence of ZTA; it is merely a consequence of buying a vendor product.

## Why It Went Wrong — Not Ignorance, but the Average

Here is the heart of the matter. The AI was not ignorant about any of this. The contents of the NIST document, the mechanics of mutual TLS — all of it must have been somewhere in the training data. It erred anyway, because **the center of gravity of the text that fills the web around the words "zero trust" lies not in the standard's definition but in the market's usage.**

There is exactly one NIST SP 800-207. Meanwhile, there are tens of thousands of security-vendor product pages, case studies, trade-show reports, and content-marketing articles wearing the words "zero trust." Training is pulled by frequency. So the center of gravity of the meaning of "zero trust" that the AI absorbed is not the standard's definition but a commercially weighted average of public discourse. The association "zero trust = buying a cloud IdP product = heavyweight and externally dependent" is precisely the skeleton of vendor discourse; the AI inhaled it as an unquestioned premise, and then swung toward physical isolation as a reaction against that premise. Both the outbound leg of the error and the return leg followed the ruts worn into the web's discourse.

In other words, what the AI returned was neither ignorance nor a lie, but **the commercially weighted average of public discourse**. This is not a defect peculiar to one product. It is a structural property common to every AI of this kind, arising from the mechanism itself: choosing the next word probabilistically from a mass of text.

Ask in Japanese about Japanese topics, and the effect gets stronger. The prose style of government-facing proposals that call three-tier network separation "robust," the field wisdom that "not connecting anything is safest" — a dozen-plus years of accumulated IT discourse has been absorbed as-is, so the received ideas whose failure Japan's public-sector IT spent years confirming can come back wearing the most plausible face of all.

## So How Should We Use It?

I don't want the conclusion to be "AI gets things wrong, so don't use it." Once the mechanism of the error is understood, the way to use it follows. There are five points.

### 1. Don't make the model's memory your basis of trust

This is the one that matters most. What an AI speaks from memory is "the average of public discourse," not the correct answer. So for decisions that matter, hand it primary sources yourself: NIST or the RFCs for standards, the statute text itself for law, official documentation for products. Have the AI reason over that text, and it turns from a machine that recalls the average into a machine that reads the material you gave it and organizes it. The former is unreliable; the latter is remarkably capable.

Built into a system, this is RAG (retrieval-augmented generation). Even at the level of personal use, simply pasting in a document and saying "answer based on this" cuts wrong answers dramatically.

### 2. Choose your own canon

Decide for yourself which document counts as authoritative, rather than accepting the web's majority vote. In a world where vendor volume keeps rewriting what words mean, standing a standards document up as the canon is a technical policy and, at the same time, a policy for how to use AI. Never surrender the choice of what counts as the basis of trust.

### 3. Read plausibility and correctness separately

In AI prose, fluency and correctness do not correlate. That answer, too, from "the practical optimum for the field" onward, was written with the practiced fluency of an SIer's proposal. But the more skilled the prose, the harder it is to notice a swapped premise. With well-written text, read what it does not say rather than what it says: what it silently assumes, what it manages never to touch. That is where the errors hide.

### 4. Use it where you can verify

AI is a powerful partner in fields where you have knowledge, and a dangerous adviser in fields where you have none. The reason is the same: what comes back is "the average." Only someone who knows the field can judge whether the average happens to be correct. So AI shows its real worth precisely where you can verify the answers instead of swallowing them. Conversely, in a wholly unfamiliar field, use the answer as a starting point and always check it against primary sources.

### 5. Throw the opposing view at it

AI tends to fall in with your premises. So when you get one answer, prompt it: "argue against this from the opposite position." In this very case, one question in reply — "can a data diode do bidirectional data exchange?" — immediately exposed the contradiction with its by-definition one-way nature. Use AI as a partner in argument, and keep the subject who draws the conclusion yourself.

## Closing — Zero Trust for AI, Too

The irony is that the right way to use AI resembles nothing so much as the zero-trust idea that the wrong answer failed to explain. **Do not make the output's origin (inside or outside, AI or human) the basis of trust; verify the content, every time.** Do not trust it because the model speaks with confidence. Admit into your decisions only what has passed the authentication called primary sources.

As a machine for recalling the average, AI is unreliable; as a tool that reads the documents you give it, organizes them, builds counterarguments, and multiplies perspectives, it is superb. Make it use reasoning, not memory. Hold the canon in your own hands. Never let go of verification. Keep those three, and AI becomes something that aids judgment rather than something that takes it away.

One wrong answer showed the limits of AI — and at the same time traced the outline of its proper use. To know how it errs is to know how to use it.

---

## Related

- Blog [The Copilot Problem — Code That Looks Right but Is Wrong](https://aiseed.dev/en/blog/copilot-correct-looking-but-wrong/) — another case where plausibility and correctness diverge
- Blog [With AI, You Can Build an App Through Dialogue Alone](https://aiseed.dev/en/blog/building-apps-through-dialogue/) — AI as a tool that gives you speed, not correct answers
- Blog [When Fable 5 Returns, Do This First — Verify Every System You Run](https://aiseed.dev/en/blog/verification-shock/) — the organization-scale flip side of "never let go of verification"

## References

1. NIST SP 800-207, Zero Trust Architecture — https://csrc.nist.gov/pubs/sp/800/207/final
