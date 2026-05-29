---
slug: microsoft-power-and-environment
title: "The Power and Environmental Problems Microsoft Is Causing"
subtitle: "The cost of the AI-first strategy — five-year support, AI PCs in name only, data centers doubled"
date: 2026.05.28
description: Microsoft's AI-first strategy is creating two problems. The first is internal to Windows 11 PCs — long-term support is not guaranteed past 2029, and the "AI PC" branding is largely cosmetic. The second is the bigger one this strategy itself produces: explosive data center expansion driving electricity demand and emissions. Windows 10's October 2025 end-of-support could push up to 400 million PCs into the e-waste stream, around 88 million tonnes CO2e from manufacturing alone. Microsoft's electricity use is up 168% since 2020 and total emissions are up 23.4%. Doubling data centers in two years while pledging carbon-negative by 2030 is structurally incompatible.
lang: en
label: Blog
category: Structural Analysis Notes
---

# The Power and Environmental Problems Microsoft Is Causing

The reception of Microsoft's flagship AI product, Copilot, has been harsh. Even though it is bundled into Windows and Office, fewer than 1 in 30 of the eligible users actually pay for it. The single largest complaint is accuracy — Copilot hallucinates facts. Of the users who churned, 44.2% gave "distrust of the answers" as the reason. Internal leaks called the integration "not actually working." Salesforce's Benioff has said publicly that customers prefer ChatGPT and are disappointed by Copilot, and reports have surfaced of Microsoft employees themselves preferring competing tools.

An OS, by its nature, should be a boring and stable foundation. Its value is in combining mature, verified technology and then not changing behavior for years. Windows 11 instead bolted experimental AI of uncertain quality onto that foundation, redesigned the hardware requirements around it, and is now pushing users to buy new machines. Users are being sold an unfinished AI product as if it were a finished one. Anything unfinished cannot be guaranteed over the long term, and the support-window shortening described below is the natural consequence. And yet Microsoft cannot stop its massive infrastructure investment — it has bet on AI at a scale it can no longer back out of. This is the source of the larger problems that follow.

## The Windows 11 PC Problem

Windows 11 PCs, plainly stated, have two problems.

First, **support is not guaranteed on any machine past 2029**. Even Enterprise LTSC 2024 — the SKU explicitly intended for long-term stable operation — has no extended support window and ends on October 9, 2029, halving the previous 10-year cycle to 5. The general release assumes you accept yearly feature updates; from 24H2 onward, CPU requirements have been raised without prior notice, and machines that fall short simply do not boot. Neither the "freeze it" crowd nor the "always latest" crowd has a long-term guarantee.

Second, **the NPU-equipped PCs sold as "AI PCs" (Copilot+ PCs) are not actually fast at AI inference**. The requirement is a 40 TOPS+ NPU, but local AI inference speed is determined by memory bandwidth, not raw compute (TOPS), and integrated chips are structurally short on bandwidth. In real measurements, a 40 TOPS NPU runs a 1.5B-parameter model at roughly 6.9 tokens/second, with LPDDR memory bandwidth as the bottleneck. Most Windows laptops cannot run LLMs above the 1–3 billion parameter range at usable speed. The premium you pay for an "AI PC" buys you Recall and Live Captions — not serious local inference performance.

## And the Larger Problem Is the Environmental Cost

These two problems are not separate. Both flow out of Microsoft's AI-first strategy, and the largest problem that strategy creates is environmental.

### The E-Waste Windows 11 Generates Directly

With Windows 10 support ending on October 14, 2025, up to 400 million PCs could become electronic waste. 43% of Windows 10 machines cannot move to Windows 11. If all of them are scrapped, that is up to 700 million kilograms of waste. Because laptops emit 70–80% of their lifetime CO2 during manufacturing — about 219 kg CO2e per unit — discarding a working PC for a new one adds several times more carbon at manufacturing than you could have saved by extending its use. At 400 million units, that is on the order of 88 million tonnes CO2e.

And this is not a one-time event. With the 5-year support window and unannounced requirement hikes now permanent fixtures, physically functioning machines will be cycled out of support periodically, and the waste wave will repeat. Most of the affected PCs are used for web-based work and need no new device; the reason they are out of scope is not performance but the line Microsoft drew (TPM 2.0, CPU generation).

### AI-First Drives Up Power and Emissions

"AI PC"-ification and AI integration into the OS are the downstream end of Microsoft's AI-first strategy. The strategy's main body sits in the upstream — extraordinary data center investment.

In fiscal 2025 alone, Microsoft spent roughly $80 billion on data center construction, more than half of it in the United States. This is the largest infrastructure investment in the company's history. As a result, its electricity use rose 168% from 2020.

The investment is still accelerating. Capex in Q1 of fiscal 2026 alone was $34.9 billion, of which $11.1 billion went to data center leasing. Nadella has said the company will grow AI capacity by more than 80% through fiscal 2026 and roughly double its data center footprint over the next two years. Fiscal 2026 capex is expected to exceed $120 billion.

Doubling data centers in two years and the carbon-negative target do not coexist structurally. Construction investment on the order of hundreds of billions of dollars itself produces enormous manufacturing and construction emissions, and once operating, consumes enormous electricity. This is what produces regional power shortages and large carbon increases.

### Running Forward While the Contradiction Stays Unresolved

Nadella has simultaneously announced two contradictory plans: an AI-first strategy that has explosive electricity demand built into it, and carbon-negative by 2030. The company's own sustainability lead has stated that "the goal was always a moonshot, but the moon has moved farther away," and yet the target has not been withdrawn. And the top page of Microsoft's sustainability site, "Explore our impact," lists only the metrics that have gone down, structurally omitting the fact that total emissions are up 23.4%.

That physical actual emissions have doubled in four years, and that the company has now restarted the previously shuttered Three Mile Island reactor on a 20-year contract to power AI data centers from 2028, shows the scale of energy demand this strategy creates.

## Summary

The two Windows 11 PC problems — unguaranteed support and the in-name-only "AI PC" — are both expressions of the same AI-first strategy, the one that is rebuilding Microsoft from "provider of a long-term, stably operated OS" into "company that funnels customers into AI and cloud subscriptions." That strategy cycles working machines into e-waste, drives data-center electricity demand upward, and has taken the company's own emissions to 23.4% above 2020. Microsoft is sprinting in a direction incompatible with the carbon-negative banner it still flies. This is the largest problem Windows 11 and the AI-first strategy are creating.

And here one question arises. **Is that much data center capacity actually necessary in the first place?** As we saw at the outset, fewer than 1 in 30 of the eligible users actually pay for the flagship product, Copilot. For something whose real demand is that uncertain, Microsoft is restarting a nuclear reactor, scrapping usable PCs, and stacking up enough infrastructure to double its own emissions. At the root of the power problem and the environmental problem is a structure in which supply at a scale that does not match demand was built first, in a form that cannot be undone.

---

*Related: [PCs Just Got Much More Expensive — Install Linux on the PC You Already Have](/en/blog/windows-10-to-debian/)*

*Related: [Windows is Breaking Down — How Nadella has given up on Windows](/en/blog/windows-breaking-down/)*

*Related: [Are You Still Going to Keep Using Windows and Office? — Detailed structural analysis with primary sources](/en/blog/windows-office-facts/)*
