<!--
投稿先: Medium
想定読者: 英語圏の技術・ビジネス読者
推奨タグ: Artificial Intelligence, Security, Legacy Systems, Enterprise Software, Technology
方針: 038中心。Microsoft paradox と保守料の話が英語圏には刺さる
-->

# Cheap Software Means Cheap Attacks — And the Maintenance Fee Loses Its Basis

Last week I published five pieces on AI's economy and geopolitics. The last one ended with a claim: the new manufacturing is self-sufficient in software, earns in the physical, and defends itself.

After publishing, I noticed the hole in my own conclusion. So I wrote a sixth piece.

## One change, three consequences

Part five put it this way: the AI revolution drove the cost of the software component toward zero. Self-sufficiency followed from that.

But I left something out. **Attacking is software too. So is verifying.** One change produces three things at once:

- **Anyone can build** — that was part five's subject
- **Anyone can attack** — AI takes over the slowest part of attacking, reading the structure of the target
- **Anyone can verify** — and this turns out to be the way out

Part five was a piece about the first of the three.

## Where a cheap attack lands

On whatever is concentrated. If everything rides on one system, one hole lets all of it out. If the same vendor's same configuration sits in a hundred companies, one vulnerability takes all hundred. From the attacker's side, concentration is **the place where a single success yields the most.**

But this is not a reason for pessimism. **The same change that made attacking cheap has made defending cheap.**

Attacking held the advantage because the attacker needs one hole while the defender has to close all of them. That asymmetry came not from a difference in capability — it came from **the defender running out of hands.** Checking everything takes more people than anyone has, so things get missed. When verification becomes free, that constraint disappears.

So the end state is an equilibrium in which attack and defense are both cheap and roughly equal. **What should worry you is not the equilibrium. It is that some parties cannot move to it.**

## The Microsoft paradox

Compatibility was Microsoft's strength. Something written decades ago still runs today. That is why it was chosen. **But leave it as it is and it cannot withstand AI-driven attack; break it and customers leave.**

What was promised protection is what prevents protection. That is the shape of the paradox.

## And the maintenance fee loses its basis

The systems integrators stand at the same wall. Their assets are delivered systems and the maintenance contracts on them.

- If AI **can** do the maintenance, the fee loses its basis
- If it **cannot**, people do it — at a labor cost orders of magnitude above AI's, and with lower accuracy

Either way, today's maintenance fee cannot be justified. And among the systems delivered to small and mid-sized companies, there is essentially none an AI cannot read. **There is really only one branch, and the answer is already in.** Checking it costs an afternoon.

The root runs deeper. **For a small company's work, COBOL and VB were enough.** Record an order, allocate the stock, print the invoice — the substance has not changed in thirty years. The systems were rewritten anyway, each rewrite adding a layer and leaving fewer people inside the company able to explain it. A rewrite is a cost to the buyer and revenue to the seller. No bad faith needs to be assumed; that was the shape of it.

And the main justification for rewriting was always "nobody works in that language anymore." **That justification is now gone. AI reads COBOL and VB.**

Nor is a successor contract waiting to take its place. A payment that has lost its basis does not get renamed. It stops.

## Microsoft 365 was never really necessary

Concretely: what you need to write documents is Word and Excel, not Microsoft 365. A perpetual license covers it. The subscription persists **for email and file sharing** — and those two are what bind the credentials into one. Break a single account and the documents, the mail, and the shared files all come out together.

So the order follows. Documents can go back to a form that doesn't reach outside. File sharing **can be far simpler** — a scheme where hierarchies, groups, and share links are tangled together is one nobody inside the company can explain, and **what cannot be explained cannot be defended.** Email is the hardest to move, and it can come last.

The near-term task is not removal but **containment.**

→ Full piece: [Who the AI Era Needs — Cheap Software Means Cheap Attacks](https://aiseed.dev/en/blog/three-conditions-ai-era/)

## The five that led here

**[One — What to Watch When Kimi K3's Weights Drop](https://aiseed.dev/en/blog/kimi-k3-what-to-watch/).** A 2.8-trillion-parameter frontier-class model distributed as open weights. This is what supports the premise that the defensive tool stays cheap: when equivalent capability is free, there is a ceiling on what a commercial model can charge, and distributed weights cannot be recalled.

**[Two — The Reality of AI Companies](https://aiseed.dev/en/blog/ai-companies-reality/).** The revenue is real. But the losses and infrastructure commitments are larger, and essentially two companies pay all the GPU rent.

**[Three — What to Watch in Microsoft's Earnings](https://aiseed.dev/en/blog/microsoft-earnings-verdict/).** Watch gross margin, not revenue. Free weights lower input costs, but when the price ceiling is set from outside, lower costs don't become profit.

**[Four — Three Reckonings in the Same Week](https://aiseed.dev/en/blog/three-fronts-same-week/).** Ukraine, Iran, China. Shanghai flooded while holding 662 rainfall observation points — the sensors were sufficient, but the average erased the local reading and the judgment sat at the center.

**[Five — IT Ends as an Industry](https://aiseed.dev/en/blog/after-it-industry/).** The volume of IT work doesn't disappear; what disappears is IT being bought and sold as an industry.

---

If I'm wrong, I'll write that I was wrong. All of it is on [aiseed.dev](https://aiseed.dev/en/blog/three-conditions-ai-era/), in English and Japanese.
