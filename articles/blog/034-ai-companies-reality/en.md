---
slug: ai-companies-reality
title: "The Reality of AI Companies, and What Kimi K3 Does to It"
subtitle: "The revenue is real. The losses and the infrastructure promises are larger — and the tower of debt stands on the single fact that there are only two borrowers"
date: 2026.07.25
description: The claim that there is no demand for AI does not survive contact with the top two companies. OpenAI is at a $24 billion annual run rate, Anthropic at $30 billion. But the losses and the infrastructure commitments are larger still, and beneath them sits a layer of data-center SPV debt whose total no one can state with confidence. The economic life of a GPU is two to three years; the debt against it runs five to twenty. And the decisive weakness is borrower concentration — almost all of the rent is paid by two companies. This piece establishes that structure in numbers, then shows Kimi K3 acting on it in four directions: compressing pricing power, possibly creating a third class of borrowers, the reverse case where margins erode faster than that class forms, and the politics of who controls distribution. With the DeepSeek shock as precedent, it narrows the verdict to three indicators. Second of five.
lang: en
label: Blog
category: Structural Analysis Notes
---

# The Reality of AI Companies, and What Kimi K3 Does to It

[The previous piece](https://aiseed.dev/en/blog/kimi-k3-what-to-watch/) laid out what to watch when Kimi K3's weights drop on July 27. This one takes the question underneath it — what is the actual state of the AI companies — checks it in numbers, and then considers how K3 acts as a variable on that state.

## The Revenue Is Real

Start with this: the claim that there is no demand for AI does not hold, at least not for the top two. OpenAI has disclosed $2 billion a month, a $24 billion annual run rate. Anthropic has reached a $30 billion annualized figure. A year ago Anthropic was around $1 billion and OpenAI somewhere near $6 billion. There is no precedent for this rate of growth in the history of the software industry.

## But the Losses and the Infrastructure Promises Are Larger

For OpenAI, the original picture was a $14 billion loss in 2026, $44 billion cumulative across 2023–2028, and profitability no earlier than 2029–2030. What actually happened was roughly $7 billion in operating losses in Q1 2026 alone — an operating margin around negative 122 percent — and the most recent estimates put the single-year 2028 loss as high as $85 billion. Revenue is climbing fast; costs are climbing faster.

Heavier still are the commitments on the infrastructure side. At a revenue scale of roughly $20 billion a year, OpenAI committed to $1.4 trillion in infrastructure spending, later revised down to about $600 billion through 2030. Industry-wide, capital expenditure for 2026 alone is projected at $690 billion, with Google accounting for $185 billion of it. However fast the model companies' revenue grows, the total they have promised to pay grows faster.

## Two "AI Companies," Two Divergent Balance Sheets

Anthropic disclosed to investors $10.9 billion in Q2 2026 revenue and a first operating profit of $559 million. Its training costs run about a quarter of OpenAI's, and it projects full-year profitability around 2028. One company has begun demonstrating the turn to profit; the other cannot cover even its hardware costs from revenue and is heading toward an $85 billion single-year loss in 2028. Eighty percent enterprise revenue on one side; on the other, a consumer shape in which only a fraction of 900 million weekly users pay anything. The difference in business model became, directly, the divergence in the financials.

Both are heading toward IPOs in the second half of 2026. The funding source for these losses is moving from venture capital to the public markets — and ultimately to household savings.

## The Substructure: Data-Center Debt

Below these two companies sits a layer that is much harder to see. Data centers are structured through SPVs, with a substantial share of the debt held off balance sheet. The total is put at $1.65 trillion, or double that if you count the off-book portion; no one knows precisely. The only source of repayment is the rent paid by customers, primarily the model companies, and much of it is non-recourse. The collateral asset, the GPU, is carried at a five-to-six-year useful life for accounting purposes — a figure each company stretches and compresses to manage earnings. The economic life is shorter. H100 rental prices fell from $8–10 an hour in early 2024 to $2–3.50 by 2026, reaching the edge of payback about two and a half years after launch. Secondhand prices halve within two years, and the inference-cost gap against a new generation exceeds tenfold. On an earning-power basis the life is two to three years; the debt against it runs five to twenty. Pension and insurance money has entered through private credit, and where the risk actually sits has become impossible to trace.

And the decisive point is borrower concentration. The entities actually paying GPU rent are essentially OpenAI, Anthropic, and a handful of hyperscalers. If those two companies' gross margins thin, the repayment source for the entire tower thins with them.

## How K3 Acts on This Structure

Kimi K3, released on July 16, is a 2.8-trillion-parameter MoE model that independent evaluations place just behind the top closed models, with full weights promised for the 27th. An open model has closed to within a few months of the closed frontier. Its effect on the structure above runs in more than one direction.

First, it compresses the model companies' pricing power over the long run. If waiting a few months gets you something roughly equivalent in the open, there is a ceiling on the premium a closed model can charge. That said, the fact that K3 itself priced its API at $3 in and $15 out — Claude Sonnet territory — shows that no one escapes the weight of inference costs. Going open is an abandonment of training-cost recovery, and K3's existence is, if anything, corroboration that the frontier is expensive no matter who attempts it.

Second, it may ease the demand concentration. The greatest weakness of data-center debt was that there were only two borrowers. If the weights are public and companies move to self-hosting or cloud inference, a third class of borrowers could emerge for the first time. K3 did hit its own compute ceiling within 48 hours and stopped taking new contracts — the demand doesn't vanish, it disperses as inference demand. There is corroborating evidence. At the end of 2025, Hopper-generation rents were expected to collapse as Blackwell spread; instead they firmed, on the back of open-weights adoption and accelerating inference demand, and the one-year reserved price for H100s rebounded roughly 40 percent off its October 2025 floor. What is extending the economic life of last-generation GPUs is precisely open-model inference demand. And a recommended configuration of 64-plus accelerators means that demand lands on data-center-class hardware, not consumer machines.

Third, it cuts the other way as well. If open models erode the two companies' gross margins faster than the third borrower class forms, the sole source of repayment simply thins and nothing replaces it. It is a race between the two, and the answer isn't in yet.

Fourth, politics added a variable. The US government asserted by name that K3 was built by distilling Anthropic's Fable, and raised sanctions and an Entity List designation. No evidence has been published, but if the distribution channel closes — Hugging Face is an American company — the formation of that third borrower class fragments. Conversely, it gives Moonshot a motive to scatter the weights while it still can.

## Precedent and Criteria

The DeepSeek shock of January 2025 is the precedent. The market wobbled for a day, and hyperscaler capex went up afterward, not down. A single day of stock prices decides nothing. What decides is only whether inference demand actually flows into the SPVs as rent.

So there are three indicators worth watching. The trajectory of gross margins at the two model companies — when the pricing pressure from open models shows up in the numbers. Total GPU leasing by parties other than hyperscalers — whether the third borrower class clears a multi-billion-dollar threshold. And the first data-center default: many contracts treat three months of customer non-payment as a breach, and these cluster around 2027.

An open model of K3's class is the only variable that touches all three. It can be the needle that bursts the bubble or the pillar that widens the borrower base and extends the structure's life. The weight release on the 27th is the starting point of that divergence.

A disclosure: this analysis was developed in dialogue with an Anthropic model (Claude). Anthropic is a beneficiary of the building boom this piece describes and a party to the K3 distillation allegations. Read it with that discounted.

---

## Related

This is the second of a five-part series.

- Blog [What to Actually Watch When Kimi K3's Weights Drop on July 27](https://aiseed.dev/en/blog/kimi-k3-what-to-watch/) — part one: the checklist for the 27th, and the empty tier
- Blog [What to Watch in Microsoft's July 29 Earnings](https://aiseed.dev/en/blog/microsoft-earnings-verdict/) — part three: the day this structure gets judged by the market
- Blog [Three Reckonings Are Closing In, All in the Same Week](https://aiseed.dev/en/blog/three-fronts-same-week/) — part four: three limits outside AI arriving the same week
- Blog [IT Ends as an Industry, and the Age of Materials and Assembly Begins](https://aiseed.dev/en/blog/after-it-industry/) — part five: what grows after it ends
- Blog [The Beginning of the End of American AI Hegemony](https://aiseed.dev/en/blog/end-of-us-ai-hegemony/) — the geopolitical backdrop to the rise of Chinese open-weights models

## References

1. OpenAI And Anthropic Are Testing Two Very Different AI Business Models (Forbes, 2026-05-21) — https://www.forbes.com/sites/paulocarvao/2026/05/21/anthropic-openai-enterprise-ai-profitability/
2. Anthropic Just Passed OpenAI in Revenue. While Spending 4x Less to Train Their Models (SaaStr) — https://www.saastr.com/anthropic-just-passed-openai-in-revenue-while-spending-4x-less-to-train-their-models/
3. Sam Altman's OpenAI is burning billions (European Business Magazine) — https://europeanbusinessmagazine.com/sam-altmans-openai-is-burning-billions-most-users-pay-nothing-as-anthropic-closes-in/
4. Anthropic revenue, valuation & funding (Sacra) — https://sacra.com/c/anthropic/
5. Better Offline / The Tech Report (Ed Zitron) — analysis of data-center SPVs and private credit (show transcript)
6. Kimi K3 popularity strains GPUs; new subscriptions suspended (ITmedia, 2026-07-21) — https://www.itmedia.co.jp/news/articles/2607/21/news099.html
7. US government names Moonshot AI, alleging Kimi K3 distillation and GB300 use (XenoSpectrum) — https://xenospectrum.com/moonshot-kimi-k3-distillation-accusation/
8. Kimi K3: The open-weights escalation (Nathan Lambert, Interconnects) — https://www.interconnects.ai/p/kimi-k3-the-open-weights-escalation
9. Kimi K3's open weights arrive July 27. The catch is 1.4TB (TECHi) — https://www.techi.com/kimi-k3-open-weights-inference-economics/
10. AI Chip Lifespans: A Note on the Secondary Market (CITP, Princeton, 2025-12-18) — https://blog.citp.princeton.edu/2025/12/18/ai-chip-lifespans-a-note-on-the-secondary-market/
11. H100 GPU Cost In 2026: Buy, Rent, And Cloud Pricing Compared (CloudZero) — https://www.cloudzero.com/blog/h100-gpu-cost/
12. The Great GPU Shortage – Rental Capacity (SemiAnalysis) — https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity
13. Is the AI Chip Shortage Over in 2026? (Value Add VC) — https://valueaddvc.com/blog/is-the-ai-chip-shortage-over-in-2026-gpu-pricing-and-what-comes-next
