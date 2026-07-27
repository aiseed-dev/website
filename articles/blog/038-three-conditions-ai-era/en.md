---
slug: three-conditions-ai-era
title: "Who the AI Era Needs — Cheap Software Means Cheap Attacks"
subtitle: "One change made both building and attacking cheap — and a cheap attack lands on whatever is concentrated"
date: 2026.07.26
description: Part five said the AI revolution drove the cost of software toward zero, and derived self-sufficiency from it. But attacking is software too, and so is verifying. One change produces three things at once — anyone can build, anyone can attack, anyone can check. A cheap attack lands on whatever is concentrated, and delegation is the arrangement that concentrates the judgment to defend at the furthest point available. Microsoft and the systems integrators face the same wall: hold compatibility and you cannot defend, break it and customers leave; if AI can do the maintenance the fee loses its basis, and if it cannot, the labor cost cannot be justified. So take on responsibility, rebuild the structure, and then you need people who can defend — which means the opposite of "specialize in security." The conclusion of the zero-trust trilogy.
lang: en
label: Blog
category: Structural Analysis Notes
---

# Who the AI Era Needs

## The Starting Point Is That Software Got Cheap

[Part five](https://aiseed.dev/en/blog/after-it-industry/) put it this way:

> Design, procedure, documentation, standards — the entire informational component of a product. The AI revolution is the event that drove the cost of that component toward zero all at once.

Self-sufficiency followed from that. But **attacking is software too. So is verifying.** One change produces three things at once.

**Anyone can build.** That is self-sufficiency, and it was part five's subject.

**Anyone can attack.** AI takes over the slowest part of attacking — reading the structure of the target. The distributed weights cannot be recalled. And as the number of builders rises, so does the number of targets. As the number rises, one of them lands: at low volume you can get away on luck, at high volume the luck runs out. And it is fast.

**Anyone can verify.** That becomes the premise of the second condition below.

Part five was a piece about the first of the three. The second comes from the same cause, on the same day.

## Cheap Attacks Land on What Is Concentrated

So where does a cheap attack strike? **Whatever is concentrated.**

If everything rides on one system, one hole lets all of it out. If the same vendor's same configuration sits in a hundred companies, one vulnerability takes all hundred. If judgment sits at the center, the site stops until the center answers. From the attacker's side, concentration is **the place where a single success yields the most.**

None of this is new. As [part four](https://aiseed.dev/en/blog/three-fronts-same-week/) put it, in an age when the cost of attack has collapsed, concentration is not an asset but a target. The concentration was always there and so was the danger. While attacking was expensive, the bill could simply be deferred.

## AI Works for Defense Too

There is no need to tip into pessimism here. **The same change that made attacking cheap has made defending cheap.**

In [an earlier piece](https://aiseed.dev/en/blog/verification-shock/) I put it this way:

> To attack is to understand a system's structure more deeply than its designer did, find the weak point, and press on it. A capability that can understand structure that deeply is, unchanged, the capability to design and the capability to verify. They are not separate abilities — they are three faces of one thing: understanding structure deeply.

What made attacking cheap makes verifying cheap. Defects in a specification, the hollowness inside a contract, the weak points in your own systems — an AI reads them in a few hours. What used to take weeks and an outside specialist now runs in your own hands.

The tool exists on both sides. What separates them is not whether you have it, but **whose hands it runs in.**

There is one more premise this argument has been resting on: **that the defensive tool stays cheap.** [Kimi K3](https://aiseed.dev/en/blog/kimi-k3-what-to-watch/) is what supports it — a frontier-class model at 2.8 trillion parameters, distributed as open weights.

The significance is on the price side. When equivalent capability is available for nothing, there is a ceiling on what a commercial model can charge. And distributed weights cannot be recalled. **The path by which the defensive tool gets expensive has closed.** If verification alone became costly, only the attacker would hold a cheap tool and the asymmetry would return. There is now evidence that it won't.

And the far end is visible too. **Once AI becomes smarter than a person, attack and defense become equals, and it stabilizes there.**

Attacking held the advantage because the attacker needs one hole while the defender has to close all of them. But two separate causes sit underneath that asymmetry.

One is that **the defender runs out of hands.** Checking everything takes more people than anyone has, so things get missed. This one disappears once verification is free.

The other is **structure.** When everything is connected, a single miss becomes a total loss. No amount of cheap verification removes this one: finding more of the holes doesn't help if missing one still costs you everything.

So the equilibrium does not arrive on cheap verification alone. **It arrives when verification is cheap and the blast radius is small.**

And that equilibrium is not a state in which attacks have stopped. **It is a state in which you get attacked periodically, take damage, and the business keeps running** — the same standing as fire or theft. Not untouched, but not knocked over. That is where the target moves.

The second half of it is within reach for most companies — an ordinary business has no reason to be connected to everything.

The problem is whoever does have such a reason. **What should worry you is not the equilibrium. It is that some parties cannot move to it.**

And that is where delegation becomes the problem. **Delegation is the arrangement that concentrates the judgment to defend at a single point outside the company** — the furthest point available.

Delegation has a round trip built into it. Detect, contact the desk, get accepted, get investigated, get a recommendation back, approve, act. Hours or days fall away at every hop. It is the time that asking another company inherently costs. **Speed outruns that round trip. Volume clogs it.** A vendor's capacity is estimated in incidents per contract, and it is shared with their other clients. Attacks do not arrive politely spaced out.

A tool that makes verification nearly free sits in your own hands, and the judgment still gets sent to the furthest point available. That is the current shape.

## So the Organization Becomes Independent and Takes On Responsibility

If delegation cannot meet the clock, the organization has to carry it. But "independence" is usually misheard, because it sounds like shouldering a new burden. It is the reverse.

What most organizations buy today is not only a system. They also buy **the ability to say "that's the vendor's responsibility" when something happens.** It does not hold. Contracts carry liability caps, usually bounded by what was paid. The company that loses trust, the company that loses money when operations stop, and the company that has to explain it to customers are all yours. **Responsibility never moved. Only the work moved.** Confusing the two is how organizations ended up keeping the responsibility while giving away only the capacity to handle it — the worst of the available arrangements.

So **becoming independent does not mean taking on new responsibility. It means becoming able to handle responsibility you already carry.** The burden does not grow; what grows is only the fact that you can handle it. And that, as [part five](https://aiseed.dev/en/blog/after-it-industry/) argued, becomes a qualification for doing business and a condition of business continuity.

## The Microsoft Paradox

Deciding to carry the responsibility runs into the next wall. And that wall shows up most clearly at the largest scale.

Compatibility was Microsoft's strength. Something written decades ago still runs today. That is why it was chosen. But leave it as it is and it cannot withstand AI-driven attack; break it and customers leave. **What was promised protection is what prevents protection.**

The systems integrators stand at the same wall. Their assets are delivered systems and the maintenance contracts on them. If AI can do the maintenance, the fee loses its basis. If it cannot, people do it — at a labor cost orders of magnitude above AI's, and with lower accuracy. **Either way, today's maintenance fee cannot be justified.**

And among the systems delivered to small and mid-sized companies, there is essentially none an AI cannot read. There is really only one branch, and **the answer is already in.** Checking it costs an afternoon with the delivered code and a model.

The root runs deeper. **For a small company's work, COBOL and VB were enough.** Record an order, allocate the stock, print the invoice — the substance of the processing has not changed in thirty years. The systems were rewritten anyway, again and again, each rewrite adding another layer, and each layer leaving fewer people inside the company able to explain it. A rewrite is a cost to the buyer and revenue to the seller. No bad faith needs to be assumed. That was the shape of it.

And the main justification for rewriting was always "nobody works in that language anymore." **That justification is now gone. AI reads COBOL and VB.**

Nor is a successor contract waiting to take its place. A payment that has lost its basis does not get renamed. It **stops.**

## Rebuilding the Structure Is No Longer the Hard Part

Reading this far, you may have pictured restructuring as a huge project. It used to be. Not rebuilding was never negligence — it was expensive.

That cost has fallen. Read the current system, surface its dependencies, propose the compartment boundaries, write the migration steps — that is now AI's work. The cost drop this piece started from applies to attacking and verifying, and it applies to **rebuilding** in exactly the same way.

What blocks it is sitting on top of the shape described in the previous section. Windows, M365, the core system already delivered — knowing they are weak does not make them disappear next week. The near-term task is to contain them.

Containment means holding what the product connects to down to a minimum. Put it inside a compartment. Separate the credentials, so a breach there leaves the rest alive. Hold a separate path that keeps operations running when it stops. And don't stack anything new on top of it.

Concretely, it looks like this. What you need to write documents is Word and Excel, not Microsoft 365; a perpetual license covers it. The subscription persists **for email and file sharing** — and those two are what bind the credentials into one. Break a single account and the documents, the mail, and the shared files all come out together. That is what concentration means.

So the order follows. Documents can go back to a form that doesn't reach outside. File sharing **can be far simpler.** A scheme where hierarchies, groups, and share links are tangled together is one nobody inside the company can explain. **What cannot be explained cannot be defended.** Plain directories with plain permissions can be explained. For email, moving only the act of delivery outside leaves the mailboxes and the accounts in-house.

This is not a compromise. What you can do about something you cannot remove is not to remove it, but to **shrink what a single success yields.**

**Whether you can defend is determined less by the quality of the individual than by the shape of the structure.** Treat this as a problem of individual effort and it fails every time.

## And That Needs People Who Can Defend

Take on the responsibility, rebuild the structure. Running it takes people.

But the most widely circulated advice has to be dealt with first.

> To survive the AI era, hold a deep specialty AI cannot take. Security, for instance.

This misreads the structure. What AI absorbs is **the whole layer** of software engineering, not one subdomain inside it. Going deeper into a specialty only moves the date by which that specialty is overtaken. Transposed to the medieval case, it has the shape of telling a serf that becoming a more specialized serf will make him free.

Three things are needed instead.

### First Condition: Understanding the Structure of What You Built

Take the line quoted earlier — attack, design, and verification are three faces of one thing — and move it from the tool to the person. The answer changes. **A person who can respond to attacks is not a defense specialist. It is a person who understands the structure of what they built.** And a person who understands structure can, for the same reason, design and verify.

The precedent is quality assurance. That, too, was once the inspection department's job. When it became a condition on everyone who builds, quality stopped being the name of a department. Defense travels the same road. Its current state — separated out as a specialist profession — is a transitional stage, not a finished form.

One more thing, stated precisely. **This is not the highest value but the lowest qualification.** What generates value is judgment, materials, and the thing you built. But however fine your judgment, one breach takes all of it. That is why it comes first — not because it matters most. It is the floor, not the ceiling.

### Second Condition: Being Able to Check It Yourself, Against a Frontier Model

The second is the simplest. **Put your own work through the frontier AI you have, and check it.** That is all, and it takes no years of specialist education. What verification requires is not the ability to write large volumes of code but the ability to run your own systems through the model, read the findings, and judge which are genuinely dangerous.

Two parts of it must not be dropped.

**One is "frontier."** The quality of the tool sets the ceiling on the quality of the check. A weak model returns a weak check — and the troublesome part is that a weak check still leaves the feeling of having checked. Settling for whatever AI the vendor bundled into the product is usually where this goes wrong. In an era when the top-tier model costs a few thousand yen a month, there is no reason to economize here.

**The other is "yourself."** Having someone else run the verification and receiving their report is not verification; it is outsourced verification — and it rebuilds the round trip all over again. Read the findings yourself, then decide which are genuinely dangerous.

Choose what you feed it, too. Your own records of design decisions, the official standards, primary sources. The more the material is your own, the further what comes back sits from the general average. **First, check.**

### Third Condition: Being Able to Decide at the Edge

For the same reason the delegation round trip cannot meet the clock, **the round trip inside the organization cannot either.** All the information is gathered. The AI is deployed. And still, if approval travels to the center and back while the event finishes, the sensors at the edge are decoration. That is exactly how [Shanghai](https://aiseed.dev/en/blog/three-fronts-same-week/) flooded while holding 662 rainfall observation points. The sensors were sufficient; the average erased the local reading, and the judgment sat at the center.

So the third condition is **being able to decide yourself, from the information in hand, fast enough to keep pace with events.** And this is a property of the individual and simultaneously a question of whether the organization permits it — which returns the argument to the structural section.

There is another story in circulation that recommends the reverse: concentrate judgment in AI, in the platform, or in a single leader. But a statistical-processing tool cannot carry judgment or responsibility.

## Three Layers, Once You Sort It Out

| Layer | The question | What is not let go of |
|---|---|---|
| The organization's will | Who carries the outcome | Responsibility |
| The organization's structure | How much falls in one blow | Being divided |
| The person | Who understands, checks, decides | Understanding, verification, judgment |

These three are not separate requirements. **They are one act seen at three scales.** Responsibility is taken on, distributed inside the organization, and at the end of the distribution a person stands. Top to bottom, it is a single line.

## Observation Points

**Responsibility.** The share of contracts that carry security requirements as a term of trade. Whether the party that discloses an incident is the buyer or the supplier.

**Structure.** The number of companies that fall simultaneously in a single breach. When a breach happens, what fraction of operations stopped.

**Whether they can move.** Whether a major vendor decides to rebuild its structure even at the cost of breaking compatibility. Whether maintenance-contract prices and renewal rates start falling.

**People.** The share of companies that can explain their own system's composition in-house. The share whose staff can reach a frontier model in daily work.

And the condition under which this piece is wrong: **if maintenance fees hold without ever being asked for their basis, and concentrated systems go on unbroken**, the argument does not stand. If I'm wrong, I'll write that I was wrong.

## Related

This is the conclusion of the zero-trust trilogy, and the consequence of the five-part series.

- Blog [When Fable 5 Returns, Do This First — Verify Every System You Run](https://aiseed.dev/en/blog/verification-shock/) — the practical version of the second condition, and where "attack, design, and verification are three faces of one capability" first appeared
- Blog [AI Isn't Wrong Because It's Ignorant — What One Bad Answer Teaches About Working With AI](https://aiseed.dev/en/blog/ai-not-ignorance-but-average/) — zero trust for the user's side; why what you feed it matters
- Blog [What Was Kimi K3 Made From? — Zero Trust for the Maker's Side, Too](https://aiseed.dev/en/blog/kimi-k3-maker-side-zero-trust/) — zero trust for the maker's side; inheriting only what passed a verifier
- Blog [IT Ends as an Industry, and the Age of Materials and Assembly Begins](https://aiseed.dev/en/blog/after-it-industry/) — the final part of the five, and the piece that opened the hole this one closes
- Blog [Three Reckonings Are Closing In, All in the Same Week](https://aiseed.dev/en/blog/three-fronts-same-week/) — Shanghai's 662 points and the placement of judgment
- Blog [Autonomy, Distribution, Diversity — The Shape of Systems to Come](https://aiseed.dev/en/blog/autonomy-distribution-diversity/) — the design-side version of the structural layer
- Blog [Internal Business Systems Are No Longer Something You Outsource](https://aiseed.dev/en/blog/in-house-business-systems/) — the practice of moving from delegation to self-sufficiency
- Blog [Three Transitions in Software](https://aiseed.dev/en/blog/software-three-transitions/) — the structural reply to "become a specialized engineer"

## References

1. The five-part series (what to watch in the K3 weight release / the reality of AI companies and K3 / Microsoft's July 29 earnings / Ukraine, Iran, China / the end of IT as an industry) — part one at https://aiseed.dev/en/blog/kimi-k3-what-to-watch/
2. Record rainfall in Shanghai (2026-07-19; 104.5mm in one hour and 212.8mm in four and a half hours at Wujiaochang, Yangpu, against a citywide average of 29.7mm) — China Safety Information Bureau — https://www.alertchina.com/post-35388/
3. Kimi K3 Open Weights Drop July 27: The Developer Prep Guide (byteiota) — on open-weights distribution and irrecoverability — https://byteiota.com/kimi-k3-open-weights-july-27-developer-prep/
