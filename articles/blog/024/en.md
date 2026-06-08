---
slug: self-hosting-microsoft-365
title: "Can You Build a Microsoft 365 (Standard + Copilot) Equivalent Yourself?"
subtitle: "Nadella's 'contradiction' and the collapse of the enclosure — taking control back into your own hands"
date: 2026.06.08
description: Microsoft CEO Satya Nadella wrote on his personal blog about "model overhang — capability outrunning our ability to put it to real-world use." But if that diagnosis is right, the place to invest is not $190 billion a year of infrastructure but the side that uses the capability we already have. AI chief Suleyman has openly said the goal is to "ultimately eliminate" what Microsoft pays Anthropic — exposing a structure in which the intelligence running underneath can be silently swapped out. Ironically, the very "intelligence that can replace an engineer" they spent so much to build has become the best partner for users who want to leave the cloud and self-host. With ONLYOFFICE, Ryzen AI Max, and open-weight models, this piece asks whether you can take a Microsoft 365 (Standard + Copilot) equivalent back into your own hands.
lang: en
label: Blog
category: Structural Analysis Notes
hero_image: pxl.jpg
---

# Can You Build a Microsoft 365 (Standard + Copilot) Equivalent Yourself?

Microsoft CEO Satya Nadella has started a personal blog, "sn scratchpad." So far there is exactly one post: "Looking Ahead to 2026."

One passage in it caught my eye. He writes that we are in "the first few miles of a marathon," and in the same paragraph he writes about "model overhang — capability outrunning our ability to put it to real-world value."

At first glance this looks like a contradiction. But in his own framing the two coexist. "The first few miles" is not about capability; it means that diffusion and implementation are still early. Capability is already in surplus (overhang), and the side that turns it into real-world value has not remotely caught up — that is his diagnosis. The problem is that, if the diagnosis is correct, the conclusion points the other way.

If capability is already in surplus, the place to invest now is not gigantic infrastructure that adds still more capability, but the side that puts the existing capability to use. Yet Microsoft is pouring $190 billion a year — an enormous sum — not into the side that is in surplus but into the side that adds still more capability. His diagnosis and his wallet point in opposite directions.

## Where Nadella Is Right, and the Trap In It

There is a part where he is right. "What matters is not the power of any individual model, but how people use it." The value lies in building the "scaffold" that binds multiple models and agents together, handles memory and entitlements, and lets tools be used safely. How you deploy intelligence into your own work matters far more than the raw cleverness of the model. This is true.

But the more honestly he states the value of that "scaffold," the more he digs the grave of his own enclosure. If the essence of the scaffold is engineering you can write in Python — flexible orchestration, entitlement management, moving data around — then it is something you can build yourself.

A scaffold is specific to each organization's work. A general-purpose scaffold can only ever be "80 out of 100 for everyone." A scaffold that scores 100 for my work can only be built by me, the person who knows my work. What a vendor can sell is the general-purpose scaffold; what is truly valuable is the one tailored to your own environment.

The lower layer — the models — is already open (Gemma, Qwen). And the upper layer — the scaffold — may become something you can write yourself, working alongside AI. In fact, AI has already reached the stage of helping develop AI itself. There is no layer left, above or below, for Microsoft to enclose.

## The Asymmetry of "Hard Problems," and the Public's Over-Extrapolation

Why do people keep expecting so much from general-purpose AI? Because they misjudge the line between the "hard problems" AI is good at and the "hard problems" it is bad at.

AI is extremely good at solving "hard problems in a closed world." Problems where the boundaries are defined, the necessary information is all present, and the answer can be verified instantly — for example, autonomous target acquisition by drones in the war in Ukraine, or fixing bugs in tangled source code. Here AI overwhelms humans, and the effect is visible and vivid.

But it is structurally hard for AI to solve "strategic hard problems" — ones that require weighing many factors, depend on tacit knowledge that is never put into words, and whose answers cannot be verified for years. In domains that involve the value judgment of "what should be prioritized," AI does not work. Because a human has a history: four billion years as a living organism, five million years as a species, and a lifetime as an individual. AI, by contrast, has no history — only the knowledge it acquired through learning and training.

The problem is that, because success in the former "closed world" is so effective and dramatic, ordinary people **over-extrapolate the capability into the invisible region of its limits** — "if it can do that with drones, surely it can be handed the whole war's strategy," "if it can summarize Excel and email this well, surely it can be a perfect sounding board for corporate strategy."

A drone's results are visible and dramatic, but AI's limits in strategy are invisible and unglamorous. So people inflate the capability from visible success into the invisible region of its limits. Those who hype it merely ride this natural over-extrapolation. Present only the fact that "this worked," and the listener will convince themselves that "so it must be a magic wand that can do that too." Of course the over-extrapolation does not hold up in practice, and the moment you actually use it, disillusionment sets in.

## The Cost of Dependence: Intelligence Taken Away Without Notice

And there is a decisive risk in depending on the Office ecosystem.

Mustafa Suleyman, Microsoft's AI chief, said this in a Bloomberg interview in June 2026:

> "We pay a lot of money to Anthropic, so our goal is to reduce and ultimately eliminate that cost."

Earlier in the same interview he also said, "Anthropic is extremely expensive, and I think many people are urgently looking for alternatives."

Their strategy is this. First gather users with an excellent third-party model (Claude and the like); once the lock-in has set, peel away the intelligence running underneath to protect their own margins, and swap it out for a cheap in-house model — counting on the fact that users cannot leave.

The problem is: **if you cannot promise continuity as a product, it has failed as a product.** Either you guarantee it will be usable for a reasonable period and build it in, or you don't put it in at all. One or the other. "Attach it, and quietly remove it whenever" — selling something whose availability is uncertain as a continuous service does not deserve the name of a product. Users build their workflow on that feature, train people, and create dependence. That investment rests on the implicit promise that "it will be stably usable for a reasonable period."

What is deeper still is that this is also a self-negation of strategy. By now AI, not Office, is the main thing. The competition is fought on AI capability. Yet Microsoft's MAI is not aiming squarely at the frontier. Microsoft claims its new MAI-Thinking-1 matches Claude Opus on coding, but Suleyman himself admits Anthropic is ahead, and what he sells is not capability but "cost efficiency." In other words, the real face of MAI is a fast follower that chases the frontier from a few months behind, cheaply.

In a world where the main battlefield has shifted to capability, to declare that you will "bring to zero" your dependence on the frontier means deliberately pinning your main product to a cheap model that is a few months behind, and stripping users of the priority right to choose the frontier. There may be a commodity tier you can win on price. But the high-value tier, differentiated by capability, you would be handing over yourself. It looks like a declaration of efficiency; in truth it is a declaration of abandoning the main battlefield.

And these risks are merely the manifestation of one large shift. Microsoft has moved its center of gravity from a company that provides tools to a company that earns by having you entrust your data to it. Once, if you bought Windows or Office, you processed your own data, on your own PC, by yourself. The tool was subordinate to you. Now it is the reverse. Files go to the cloud, conversations to a hidden folder in Teams, processing to Microsoft's models. The data moves to their side, and the tool that uses it is held by their side too. That they can silently swap the model running underneath, and that they can openly declare they will bring the cost to zero — all of it rests on this single point: "users can no longer leave."

It is not coercion by force. Lure with convenience, make it the standard, and before you notice the cost of escaping has become high — an inducement with no way out. And this is not personal malice. In an era where the tools themselves are commoditizing — the OS flowing to free Linux, the models to open weights — a company that can no longer earn from tools has simply moved to where it can earn: having you entrust your data.

## The Logic Reverses: AI Broke the Wall of Operations

Here a delicious reversal of logic occurs.

There is one domain where AI is so "superb" that it can fully take a human's place. It is precisely the world of software engineering — a "closed hard problem."

According to a report from Challenger, Gray & Christmas, tech-sector layoffs have reached their highest level in about two years, and the largest factor behind them is AI. Vendors, paying the bill for excessive infrastructure investment, are cutting their own engineers.

But the knowledge of the engineers they let go — programming, infrastructure setup, debugging, the "intelligence of the closed world" — has already come down into our hands in the form of open AI.

Once, the biggest barrier to hosting an environment like M365 yourself was not the cost of hardware but the "advanced engineering expertise" needed to operate it safely and stably. What the cloud vendors were really selling, too, was less the compute itself than that wall: "taking the operational knowledge off your hands."

That wall of knowledge was broken by none other than AI itself. Installing Debian and swapping the kernel, resolving AMD ROCm dependencies, Docker routing — AI helps with all of it, right beside you. We have entered an era in which the infrastructure produces, by itself, the advice for operating itself.

The "intelligence that can replace an engineer," which they grew with enormous investment, has ironically become the best partner for users who want to break out of their cloud and self-host.

## So, Here Is What I Will Do

If you are an individual, just install ONLYOFFICE Desktop Editors. You get something nearly equivalent to Word, Excel, and PowerPoint. LibreOffice is fine too. But if, as an organization, you want collaborative editing as well, then to match Microsoft 365 Business Standard, install ONLYOFFICE DocSpace Community on a server.

And with a PC powered by the **Ryzen AI Max+ 395 / 128GB LPDDR5x — with unified memory on par with Apple Silicon — open-source AI (Gemma 4, Qwen 3.6, and the like) runs locally. Of course it does not yet have Claude's capability, but it is worth trying.

What matters is **holding the initiative in your own hands.** If Claude's new model is good, switch to it and use it. If you want to close everything off for free, run an open-source model on the power of a local Ryzen AI Max, on top of 128GB of high-bandwidth memory. Which intelligence, for which task, when to use it and when to drop it — that is decided by you, not by a vendor. Bind it all together with Python and hold the control. Your data does not leave. The cost is only electricity. The model can be swapped at any time.

## A Second Renaissance — As a Starting Point

I want to call the era ahead "the age of a Second Renaissance," because it looks set to be an age of both upheaval and creation.

What set off the Renaissance was the printing press. Before it, knowledge was enclosed as manuscripts, and value was concentrated in the handful who could copy them. Printing broke the cost of copying, made knowledge impossible to enclose, and moved authority to a new layer.

Now AI, a powerful means of processing information, is coming down into the hands of individuals in the same way. Knowledge and open-source assets, once out in the commons, cannot be recalled. The know-how I assemble and accumulate will, in time, become someone's stepping stone too. That is why open-source AI will not disappear.

Nadella pointed accurately at where AI's value lies. And with the same finger, he pointed at the place where his own enclosure no longer holds.

I will set up my own server.
