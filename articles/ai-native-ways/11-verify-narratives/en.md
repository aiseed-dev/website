---
slug: verify-narratives
number: "11"
lang: en
title: "Verifying Narratives with AI"
subtitle: "Don't get carried by convenient stories — this is the essential work of the AI era."
description: The workplace is surrounded by narratives — executive briefings, vendor pitches, industry common sense, news articles, politicians' words. With AI, you can verify a narrative structurally, against past statements, public records, contracts, and third-party verifiable facts. As case studies, four governance-failure patterns — WordPress (excessive concentration in one person, the main case), Node.js (no one is in charge, Example 1), Linux distributions / CentOS (corporate stewards rewriting their promises, Example 2), and Microsoft's "return to native apps" (the gap between strategic slogan and actual implementation scope, Example 3).
date: 2026.05.02
label: AI Native 11
title_html: Verify narratives,<br><span class="accent">with AI</span>.
prev_slug: ai-delegation
prev_title: "Knowing What Work to Hand to AI"
next_slug: one-plus-ai
next_title: "One Person + AI — The New Unit of Work"
---

# Verifying Narratives with AI

The workplace is surrounded by narratives.

Executive briefings, vendor pitches, industry common sense, news articles, politicians' words, social media trends, earnings calls, performance reviews, job postings, contract preambles — most of the information we receive every day is a **narrative** that someone has shaped with intent.

And most narratives are **constructed to suit the side that tells them**. This is not a story about malice. Humans build narratives to justify their actions, to organize context, to maintain relationships. It is the standard operating mode of a social animal.

The problem is that **getting carried by a narrative leads to bad judgment**.

You sign an expensive vendor contract because the sales pitch swept you along. You make an investment because you believed the inflated industry report. You hire someone by taking the resume's narrative at face value. You vote by accepting a politician's account without checking it.

This chapter is about the essential work of the AI era — **verifying narratives**. This is not work you "hand off" to AI; it is work that **humans do** together with AI.

## Why AI is well-suited for verifying narratives

Verifying narratives used to be the work of specialists — reporters, researchers, investigators, lawyers. Ordinary people had neither the time nor the capacity, so they had no choice but to believe without checking.

This is where AI enters.

**1. It can read across enormous volumes of text**

What would take a human a week to read — speech transcripts, meeting minutes, social media posts, articles — Claude can scan in minutes. "Arrange Mr. X's statements about Y over the last five years in chronological order" — even just this shortens human research time by orders of magnitude.

**2. It is good at pointing out contradictions**

"In 2020, Mr. A said this; in 2024, he said that. Are these consistent?" — this kind of structural comparison is AI's strong suit. It can extract the substance of a claim, ignore variations in phrasing, and compare them.

**3. Unbiased perspective (it sees the whole training data)**

Humans tend to read only the articles they want to read (cognitive filter bubbles). AI's training data contains articles from opposing positions on both sides. Asked well, it will lay out both sides' claims even-handedly.

**4. It doesn't tire, and it doesn't curry favor**

AI has neither "deference to the boss" nor "standing in the industry" to worry about. It responds frankly about facts. This is something humans cannot do.

> AI is good at "creating narratives." It is also good at "verifying narratives." In an era when **AI is on both the creating side and the verifying side**, we need to put AI on the verifying side.

## Case study: WordPress and Matt Mullenweg

Let's look at a concrete case.

Matt Mullenweg — co-founder of WordPress and CEO of Automattic — has been publicly feuding since 2024 with **WP Engine**, a major hosting company. There are many public statements, court filings, blog posts, conference talks, and podcast appearances.

This is a **prime case** for verifying a narrative with AI. Because:

- The party in question (Matt) has left a vast quantity of public statements
- His statements over many years can be tracked chronologically
- Court filings (claims from plaintiff and defendant) are public
- Third-party testimony (community, press, developers) is plentiful
- The boundaries between three organizations — WordPress.org, Automattic, the WordPress Foundation — are at stake
- There are **legally verifiable points** like GPL licensing, trademarks, and contractual rights and obligations

### The narrative's main claims (surface)

Matt's main public claims can be summarized roughly as follows `[unverified: specific quotes and dates]`.

1. **"WP Engine free-rides on the WordPress ecosystem"** — improperly using the trademark, contributing markedly little upstream
2. **"WP Engine is distorting the true form of WordPress"** — deliberately impoverishing user experience, e.g., disabling revisions by default
3. **"WordPress.org is my personal property"** — the domain and infrastructure are personally owned, and I decide who gets blocked
4. **"The injunction against WP Engine is a legitimate act to protect the community"**

### Steps for verifying with AI

How do you verify these claims together with AI?

**Step 1: Extract and classify the claims**

Have Claude read Matt's statements and the public documents:

> From the following body of text, extract Mr. Mullenweg's main claims. Classify each claim as (a) a claim about objective fact, (b) opinion / evaluation, or (c) metaphor / rhetoric.

Just this exposes the structure of the argument. "Free-riding" is opinion; "improper use of the trademark" is a factual claim (verifiable); "protecting the community" is evaluation — the parts come apart.

**Step 2: Match factual claims against verifiable sources**

"WP Engine is improperly using the WordPress trademark" — this is a factual claim, so it can be verified.

> Who owns the WordPress trademark? Under the WordPress Foundation's trademark policy, to what extent are service names containing "WordPress" allowed? Over the past 10 years, did Matt or Automattic publicly object to WP Engine's use of the trademark?

Claude can build an answer by referring to the WordPress Foundation's trademark policy page, past community discussions, statements at WordCamps, and so on. **When verifiable sources exist, AI can put the facts in order.**

**Step 3: Check the consistency of statements over time**

This is where AI is particularly strong.

> Arrange Matt's mentions of WP Engine over the past 10 years chronologically. From 2014, when WP Engine brought in CEO Heather Brunner, through 2018 when Lee Wittlinger from Silver Lake joined the WP Engine board, up to the 2024 injunction.

At which point, have it organize:

- In the past, did he welcome WP Engine as a WordCamp sponsor?
- During what period was WP Engine listed on the WordPress.org recommended-hosting page?
- When did the "free-riding" claim begin to appear?
- Has the basis for the claim shifted over time?

**When past statements diverge sharply from present statements, either there is new information, or the narrative has been retrofitted.** One or the other.

**Step 4: Cross-check with verifiable third-party records**

In court documents (WP Engine v. Automattic, the litigation that began in October 2024), each side's claims are filed under oath. This is **third-party verification** that can be compared against Matt's solo narrative.

Have Claude:

> Summarize WP Engine's preliminary injunction motion (October 2024), Automattic's response, and the judge's preliminary order (December 2024). Identify the parts that match Matt's public claims and the parts that contradict them.

The fact that the preliminary order found that **Automattic's blocking of WP Engine from WordPress.org is subject to injunction** is not consistent with Matt's claim that "WordPress.org is my personal property, so I can decide freely."

**Step 5: Catalog the remaining open questions**

Not every contradiction can be resolved. Finally, organize:

- Which factual claims are still unverified?
- Which points lack public primary sources?
- Which points have the parties' claims and third-party testimony in conflict?

**Clearly separating "what is known" from "what is not known"** is itself essential work for not getting carried by a narrative.

### What comes into view

Through this process, of Matt's narrative:

- **Objectively verifiable factual claims (GPL violation, trademark violation) have thin grounds**, or at minimum are not unique to one interpretation
- **The boundaries between the individual and the foundation** (WordPress.org, Automattic, WordPress Foundation) **shift conveniently** in each iteration of the narrative
- There were periods when WP Engine was **actively treated as a collaborator**
- Behind the normative claim of "protecting the community" there is a commercial motive: **market competition between Automattic and WP Engine**

These things, with AI, become visible **even to an individual**.

This is not a conclusion that "Matt is a bad person." **Every human tells a narrative shaped to their situation.** And the more of a leader or public figure they are, the more social weight that narrative carries. That is why it has to be verified.

> Telling a narrative and believing a narrative are different activities.
> With AI, you can do the latter **structurally**.

## Case Study 2 (separate page): Should you adopt Node.js for production work? — The reality of "no one is managing it"

The WordPress case was governance failure as **excessive concentration in one individual**. Now let's verify the opposite governance failure — **no one is managing the whole** — through a near-at-hand technical decision. The subject is **whether to adopt Node.js for production work**.

The verification reveals:

- The Node.js runtime is owned by the OpenJS Foundation; the npm registry is owned by Microsoft — at odds with "vendor neutral"
- Founder Ryan Dahl gave a 2018 talk titled "10 Things I Regret About Node.js" and walked away to build Deno
- Supply-chain incidents — event-stream, ua-parser-js, colors, SAP — **recur almost yearly**
- Behind the slogan "supported by major companies" is a structure where **a billion-dollar business is sustained by 1–2 unpaid volunteers**

WordPress is "**one person carrying too much responsibility**"; Node.js is "**no one carrying responsibility**" — both are governance failures, but in opposite directions.

For the detailed five-step verification, see the **Example 1** page at the end of this chapter. From extraction of the surface narrative to primary-source matching, chronological consistency, cross-checking against third-party records, and finally organizing "what is known / what is not known," it is laid out in walkthrough form.

## Case Study 3 (separate page): How should you choose a Linux distribution? — When "free, perpetual, neutral" breaks down

What we have seen in the WordPress and Node.js cases were two governance failures:

- **Concentration in one person** (WordPress / Mullenweg)
- **Distributed with no one in charge of the whole** (Node.js)

Now we add a case showing another typical failure mode — **the corporate steward changes the promise mid-way**. The subject is **choosing a Linux distribution** for server use.

The verification reveals:

- **CentOS 8 EOL** (December 8, 2020): "supported until 2029" was the promise, but it was changed to **end at the close of 2021, eight years early**
- **Red Hat statements**: 2014 "we will protect CentOS's independence"; 2019 "independence is preserved even after the IBM acquisition"; 2020 "CentOS 8 is ending" — the timeline of the promises is not consistent
- **Ubuntu / Canonical**: the forced Snap rollout (from 2020), the Ubuntu Pro registration requirement (from 2022), the Mir / Unity independent-path detours and their abandonment — repeated direction changes driven by a private company's business decisions
- **Debian**: the 1997 social contract, the 1998 constitution, no owning company, SPI as the non-profit holder of assets — **for over 30 years, structurally protected from corporate acquisition**, a uniquely positioned Linux

WordPress is "**one person carrying too much responsibility**"; Node.js is "**no one carrying responsibility**"; Linux distributions are "**the corporate steward rewriting the promise**" — all governance failures, but in different directions.

For the detailed five-step verification, see the **Example 2** page at the end of this chapter. The ground-level chaos on the day of the CentOS EOL announcement, Canonical's 5-to-10-year direction reversals, Debian's structure, the perpetual-availability verification of AlmaLinux / Rocky Linux, and the implications by time horizon for adoption decisions — all laid out in walkthrough form.

> Debian is a uniquely positioned Linux that lets you plan in 20-year units. What promises that is not the technology, but the **governance structure**.

## Case Study 4 (separate page): Is Microsoft's "return to native apps" real? — The actual scope of "100% native"

What we have seen across the WordPress, Node.js, and Linux distribution cases were three governance failures:

- **Concentration in one person** (WordPress / Mullenweg)
- **Distributed with no one in charge of the whole** (Node.js)
- **The corporate steward rewriting the promise** (CentOS / Ubuntu)

Now we add a case showing a fourth typical failure mode — **the gap between strategic slogan and actual implementation scope (a partial truth presented as the whole)**. The subject is the **"return to native apps" strategy** that Satya Nadella announced on April 29, 2026.

The verification reveals:

- **The OS shell layer (Start menu, taskbar, File Explorer)** — Rudy Huyn's team is moving forward with WinUI 3 + .NET 10 Native AOT to make this "100% native," with proof-of-results in the May 2026 Windows 11 update (KB5083631)
- **The Microsoft 365 division (Outlook, Teams)** — the new Outlook (Project Monarch) is a WebView2 wrapper; Teams 2.0/3.0 is also WebView2 — within the same Microsoft, **the direction is the exact opposite**
- **Enterprise pushback delayed the classic Outlook migration by a year** (April 2026 → March 2027), with support continuing through 2029
- **The third-party layer**: Microsoft itself is strengthening "React Native for Windows" with the 0.81/0.82 releases in 2026 — until the developer economics change, Electron / React Native will continue
- **Precedents from WPF / UWP**: a "history of zigzags" in which loudly announced frameworks were abandoned within a few years — the developer community is cautious about investing in WinUI 3, too

WordPress is "**one person carrying too much responsibility**"; Node.js is "**no one carrying responsibility**"; Linux distributions are "**the corporate steward rewriting the promise**"; Microsoft's "return to native" is "**the slogan's reach hides the implementation's reach**" — all governance failures, but in different directions.

For the detailed five-step verification, see the **Example 3** page at the end of this chapter. Pinning down the actual scope of "100% native," the Microsoft 365 division's choice of WebView2, measured resource consumption of web-wrapper apps, the proof-of-results for .NET 10 Native AOT, the third-party developer economics, and Microsoft's "OS-as-transparent" strategy for the AI PC era — all laid out in walkthrough form.

> Microsoft is, in fact, returning to native — but **only within an extremely limited scope, the OS shell layer**.
> When you hear "100% X" or "return to Y," ask AI first: **"What is the actual scope of the 100%?"** The strength of a slogan and the scope of its truth are often inversely correlated.

## General practices for narrative verification

From the WordPress case, here are five practices that generalize.

### 1. Extract and classify the claims

Before believing a narrative as is, **explicitly write out "what does this narrative claim?"** Have Claude help:

> From the following text, extract the main claims. Classify each claim as
> (a) a claim about objective fact
> (b) opinion / evaluation
> (c) metaphor / emotional expression

Only (a) is the target of verification. (b) and (c) are debatable (or do not require verification) territory.

### 2. Match factual claims against primary sources

Take the extracted factual claims and put them up against **primary sources**.

- Executive statements → earnings reports, disclosure documents, SEC filings
- Vendor pitches → contract text, SLA, past case studies
- Politicians' statements → minutes, voting records, past testimony
- Legal disputes → court documents, judgments
- Industry reports → primary data, methodology, sample size

Hold the awareness that **"news articles are secondary sources"**. When possible, verify quoted statements and numbers against the originals. Asking AI "tell me the source of this article's quote" makes the original easier to find.

### 3. Check chronological consistency

Are past statements consistent with present ones?

- Have the claims changed between two years ago and today?
- If they have, has the change been explained?
- Has the change been acknowledged, or feigned ignorance?

> The greatest vulnerability of any narrative is the time axis. People build narratives to fit the convenience of the present moment, but their past statements remain on record.

### 4. Apply third-party verifiable records

Beyond statements from the parties involved, apply **third-party testimony** and **public records**.

- Internal whistleblowing, exit interviews
- Court filings in litigation
- Audit reports
- Legislative or committee testimony
- Citations and critique in academic papers

A third-party perspective surfaces the **blind spots** in a narrative.

### 5. Separate "what is known" from "what is not known"

At the end of verification, organize:

- Facts that were confirmed
- Facts that could not be confirmed (information not public, etc.)
- Points where the opposite claim has weight
- Points where there is not enough information to conclude

**Don't rush to a conclusion.** If information is missing, write "missing." This is intellectual honesty.

## Why this practice matters in real work

Verifying narratives is not merely a tool for op-ed commentary. **It plays an essential role in every situation in real work.**

**Vendor selection**

Sales pitches, white papers, case study collections — these are all narratives. "1,000 customer companies," "average 300% ROI," "industry No. 1" — verify these factual claims together with Claude.

> What is the basis for "industry No. 1"? Which research firm, which category, as of when? What is included in the comparison set, and what is excluded?

A numerical narrative changes drastically depending on how the definitions are operated. Factor it apart with AI.

**Executive judgment**

Industry reports, consultant recommendations, competitive analyses — these are narratives too. "The market is growing 30% annually," "the threat of new entrants is high" — together with AI, verify the primary data, methodology, and assumptions behind them.

**Hiring interviews**

Resumes are narratives. "I led the project and grew revenue by 50%" — how many people were on the team that was led, and what is the "50%" measured against? Use AI to break down the structure, then ask specifically in the interview.

(Note: hiring is a legally protected area, so be cautious about using AI to "evaluate" individuals. Use AI **to raise the precision of your questions**.)

**Investment judgment**

Earnings releases, IR materials, CEO statements — all narratives. The footnotes on the accounting figures, deviations from past guidance, peer comparisons — verify broadly and deeply with AI.

**Contract negotiation**

The other side's claims, industry custom, past case law — together with AI. When you're told "this is the going rate," check whether it really is.

**Public policy and civic decision-making**

This is not work, but as a citizen it is the most important area. As a voter, verify what politicians, agencies, and industry bodies say. With AI, even without being a full-time reporter, you can do a meaningful amount of verification.

> Get carried by narratives, and people lose time and money.
> Build the habit of verifying, and you can reduce that loss by orders of magnitude.

## Caveats — AI is not perfect either

To say "verify narratives with AI" can sound omnipotent, but there are caveats.

**1. AI also produces incorrect information**

Claude and ChatGPT can, due to training-data bias or hallucination, output incorrect information "with confidence." **Always re-verify factual claims against primary sources.** AI proposes hypotheses; humans verify the facts. Hold to that division of labor.

**2. The training data itself is biased**

AI training data is centered on English, on Western sources, on online discussion. Japanese-language industry context, local politics, records that exist only in print — these are easily distorted. When possible, ask the same question of multiple AIs (Claude, Gemini, ChatGPT) and compare answers.

**3. Beware the AI vendor's own narrative**

AI vendors (Anthropic, OpenAI, Google, etc.) also have narratives about their own products. Letting an AI verify those creates a circular reference. For claims about the AI industry in particular, verify against third-party sources.

**4. The final judgment is human**

Even when AI says "this is contradictory," that judgment is not necessarily right. Treat AI's output as a **hypothesis**, then check it against the originals yourself. "AI said so" is not a basis for judgment.

**5. Don't turn it into a tool for personal attack**

Verifying narratives is done not to denounce the parties involved, but **to keep your own judgment from going wrong**. Be careful not to drift toward using verification results as ammunition on social media. This is intellectual work, not emotional activity.

## In summary

The AI-native way of working is not just about **handing things to** AI. **Thinking together with AI** — and especially **verifying narratives** — is an essential role for humans in the AI era.

- The workplace is surrounded by narratives
- Most narratives are constructed to suit the side that tells them
- Get carried by a narrative and judgment goes wrong
- With AI, you can verify narratives structurally — against past statements, primary sources, and third-party testimony
- Five practices: **extract claims → match primary sources → check chronological consistency → apply third-party testimony → separate what is known from what is not known**
- Caveats: AI is not perfect, the final judgment is human, don't make it a tool for personal attack

> Creating narratives — AI is good at it.
> Verifying narratives — AI is good at it, too.
> Putting AI on the verifying side is a human **choice**.

Don't take narratives at face value. Use AI to see the structure. Whether you can do this or not will sharply divide the quality of work in the AI era.

In the next and final chapter, we combine all of these tools and practices and look at how the new unit of work — **one person + AI** — comes together.

---

## Related

- [Chapter 10: Knowing What Work to Hand to AI](/en/ai-native-ways/ai-delegation/)
- [Chapter 12: One Person + AI — The New Unit of Work](/en/ai-native-ways/one-plus-ai/)
- [Structural Analysis 14: The Design of Subtraction](/en/insights/subtraction-design/)
- [Structural Analysis 12: AI and the Individual Business](/en/insights/ai-and-individual/)
