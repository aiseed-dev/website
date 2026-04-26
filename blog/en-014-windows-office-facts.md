---
slug: windows-office-facts
title: Will You Continue Using Windows and Office?
subtitle: Copilot Is Not Being Used — Yet the World's Resources Keep Being Drained
description: In the enterprise AI market, Anthropic has surpassed Microsoft. Copilot's active usage rate sits at 35.8%, with an NPS of -19.8. Due to the architectural limits of LLMs (O(N²·d)), hallucinations are mathematically unavoidable. Yet Microsoft continues to embed Copilot into the deepest layers of the OS, while its data center build-out drains the world's memory, electricity, and naphtha. This piece argues for an urgent migration to Linux.
date: 2026.04.26
label: Blog
category: Structural Analysis Notes
hero_image: 014-IMG_3437.jpg
---

# Will You Continue Using Windows and Office?

## Executive Summary

**First, the enterprise market verdict is already in.** Companies are choosing Anthropic's Claude (ARR exceeding **$30 billion**, adopted by 70% of Fortune 100 companies), while Microsoft Copilot's active usage rate sits at just **35.8%**, with an NPS of **-19.8** in deeply negative territory.

**Second, due to the architectural computational limits of LLMs (the O(N²·d) constraint), hallucinations in complex business tasks are mathematically unavoidable.** Microsoft's design posture of integrating this fundamentally flawed system into the deepest layers of Windows OS while making it nearly impossible to disable forces every industry — particularly healthcare and finance — to bear an **unauditable compliance risk**.

**Third, this unrecoverable AI investment is destroying physical reality.** As the February 2026 Iran war's blockade of the Strait of Hormuz triggers a naphtha crisis, life-sustaining resources for medical infrastructure, memory chips for consumer electronics (with abnormal DRAM price surges), and even local power grids are being relentlessly consumed to maintain underutilized AI data center infrastructure.

With Windows 10's end of support in October 2025, enterprises now face exponentially escalating ESU (Extended Security Updates) costs. Yet hardware refreshes force them to purchase needlessly high-spec systems (Copilot+ PCs) precisely when AI demand has driven memory prices to historic highs. And once they migrate to the new OS, they encounter AI surveillance and processing pathways that are extraordinarily difficult to opt out of and carry serious legal risks.

Corporate and government IT leaders, along with CISOs (Chief Information Security Officers), must clearly recognize that Microsoft's platform is **no longer the neutral, stable infrastructure that supports business operations** — it has transformed into **"a high-maintenance, high-risk agent that drains corporate budgets without limit and threatens compliance and social responsibility."**

---

## Windows PC Hardware Requirements

Microsoft's progressive escalation of hardware requirements to align with AI integration has rendered PCs around the world "unusable."

**The PCs progressively cut off**

- **Windows 11 (2021)**: PCs purchased before 2017 became unusable (TPM 2.0, Intel 8th gen / Ryzen 2000 or later required)
- **24H2 (2024)**: TPM bypass methods were also blocked (SSE4.2, POPCNT now required)
- **Copilot+ PC (2024)**: All PCs purchased before mid-2024 cannot fully use Copilot features (40 TOPS NPU, 16GB DDR5, 256GB SSD required)

**Copilot+ PCs require purchase, not upgrade**

- Existing PCs cannot be upgraded; new purchase only
- 40 TOPS on NPU alone (CPU/GPU combined performance not accepted)
- Compatible CPUs limited to Qualcomm Snapdragon X, Intel Core Ultra 200V, AMD Ryzen AI 300 series

**The reality users worldwide face with Windows 10's end of support**

- October 14, 2025: Support ended
- **240 million PCs** classified for disposal (Canalys estimate, ~20% of all Windows devices worldwide)
- 480 million kilograms of waste = equivalent to 320,000 cars
- To keep using them, pay ESU (Extended Security Updates): Year 1 $61 → Year 2 $122 → Year 3 $244. **$427 per device over three years**

**Where the discarded PCs go**

- 80–85% of discarded PCs end up in landfills
- Lead, mercury, cadmium, and flame retardants leach into soil and groundwater
- Most are PCs that simply don't run Windows — they could run Linux for years

---

## Nadella's Copilot Integration Strategy

### Mandatory AI Use Inside Microsoft

Satya Nadella has implemented the following internally:

- AI adoption metrics built into employee performance KPIs
- Internal memo to all employees: "Using AI is no longer optional"
- Removal of executives who resisted AI integration
- The CEO personally reviews prototypes and reallocates budget directly

Furthermore, executives have implemented mass layoffs and reorganizations, justified by claims that AI integration has dramatically improved coding productivity. The "voluntary separation program" for U.S. employees functions as a mechanism to remove employees who cannot transition to AI-native roles.

In an organizational environment where the CEO himself proves "people are replaceable by AI" and uses this to justify workforce reductions, it is extremely difficult for frontline engineers and salespeople to report uncomfortable truths upward — such as "Copilot is not trusted by customers, and actual usage is low." **The feedback loop from the bottom of the organization to the top has broken down, forming a rigid silo where plans are pushed forward in disconnect from reality.**

### Auto-installation Without User Consent — Mozilla's Criticism

The M365 Copilot app was auto-installed on Windows devices running Microsoft 365 desktop apps, without prompts or user consent.

Mozilla VP Linda Griffin publicly criticized Microsoft for installing the M365 Copilot app on Windows devices without user consent, and for placing a dedicated Copilot key on physical keyboards while making remapping difficult. She condemned this as **"a textbook dark pattern that strips users of choice and prioritizes Microsoft's own interests."**

### Default Pinning to the Taskbar

Copilot was pinned to the Windows 11 taskbar by default. Plans are progressing to embed it directly into the most fundamental surfaces of the OS — the notification center, settings app, and File Explorer.

### Only EEA Users Are Excluded

Microsoft has excluded the European Economic Area (EEA) from Copilot's auto-installation.

EEA gets exempted because of regulation. Everywhere else, it goes ahead. **Users in Japan, the U.S., Asia, Latin America, and Africa are not protected by regulation.** Microsoft itself recognizes this is not in users' interest and is legally problematic.

### Opt-out Is Extremely Difficult After 24H2

When IT administrators attempt to disable Copilot through Group Policy or registry settings, the system is deeply routed to maintain the AI processing pathway through Edge browser components, **making complete opt-out structurally extremely difficult**.

### Legal Liability for Healthcare and Financial Institutions

Healthcare IT administrators have testified that they had to completely disable Copilot via Group Policy. Patient information processing by AI cannot be permitted without explicit, documented consent and proper auditing. **If they overlook the disabling, the hospital bears legal liability.**

Financial institution compliance officers similarly worry that Copilot may analyze sensitive financial data or generate unauthorized communications. **If a leak occurs, it is the financial institution — not Microsoft — that bears the responsibility.**

The default-on integration of an AI processing pathway into industries where explicit consent and audit trails are legally required, without users' knowledge, **fundamentally obscures the locus of legal liability**. **Local governments, hospitals, banks, schools — all are forced to bear the same risk.**

---

## What Is the Data Center Build-Out Actually For?

Microsoft is concentrating global resources on building data centers. The scale is **comparable to the annual budget of many mid-tier nations**.

**Microsoft's CapEx**

- FY2026 capital expenditure: **$100–120 billion**
- Q1 alone: $34.9 billion (of which $11.1 billion was data center leases); Q2: $37.5 billion
- Nadella's declaration: "Double our data center footprint in two years"

**Existing global footprint**

- 400+ sites, 70 regions, 40 countries
- Cost structure of $25 billion per 1 GW

**Flagship project: Fairwater**

- Mount Pleasant, WI (the site Foxconn failed to complete): $7.3 billion → ultimately $13.3 billion, 9 million square feet
- A single supercomputer integrating hundreds of thousands of NVIDIA GB200 GPUs
- Connected to Fairwater 2 in Atlanta via AI WAN to form a virtual supercomputer

**Relationship with OpenAI/Stargate**

- January 2025: Exclusivity with OpenAI was relaxed
- March 2026: Microsoft absorbed 700 MW abandoned by OpenAI/Oracle in Abilene, Texas

**$10 billion flowing into Japan as well (announced April 2026)**

- **$10 billion (about ¥1.6 trillion), four years (2026–2029)**
- Partnership with SoftBank and Sakura Internet
- Linked with METI's multi-trillion-yen AI investment strategy
- Forms the core of Japan's national project to build **"Sovereign AI" infrastructure** keeping data within Japan
- Cybersecurity collaboration with the National Police Agency and the Cabinet Secretariat

The Japanese government predicts a shortage of **3.26 million** AI/robotics professionals by 2040, and has committed nationally to fully depending on Microsoft's technology ecosystem as the foundation for reskilling and social implementation.

**Funding flows from the Middle East**

- $100 billion fund formed with BlackRock + MGX (UAE) + Global Infrastructure Partners
- A pathway for Middle Eastern capital to flow into U.S. AI infrastructure

**Problems Nadella himself acknowledges**

- Azure backlog exceeds $80 billion (caused by power shortages)
- "GPUs are in stock, but we can't find the power to install them"

**The nature of this build-out**

This is not "hoarding" — not a deliberate market manipulation. Annual capital expenditure exceeding $100 billion creates a **crowding-out effect** through market purchasing power. Microsoft is simply the strongest buyer, and that fact alone is fundamentally distorting global supply chains.

Japan does not have the regulatory distance the EEA enjoys. As we will see below, the side effects of this build-out are directly hitting other industries and ordinary citizens worldwide.

---

## Side Effects of the Data Center Build-Out

### Semiconductor Memory Shortage and Price Surge — Electronics Worldwide Are Getting More Expensive

In October 2025, OpenAI signed a letter of intent with Samsung and SK Hynix for approximately **40% of global DRAM (900,000 wafers per month)**. Although there is no legal obligation to purchase, both companies reallocated their production lines.

Microsoft is also finalizing a multi-trillion-won three-year DDR5 long-term contract with SK Hynix. Samsung, Google, and AMD have all moved to long-term contracts. Samsung and SK Hynix together account for approximately 78% of global DRAM.

**More than half of global DRAM has been locked up for AI data centers.**

For AI servers in data centers, HBM (High Bandwidth Memory) and large-capacity enterprise SSDs are essential. Semiconductor manufacturers (Samsung, SK Hynix, etc.) have shifted their production lines significantly toward AI in response to hyperscaler long-term contracts. This reallocation of supply capacity has caused extreme tightness in the supply of DRAM and NAND flash memory used in general consumer electronics.

**Counterpoint Research's DRAM price tracking**

| Period | Trend |
|---|---|
| Q3 2025 | DRAM prices up **172% year-over-year** |
| Q4 2025 | Up **~50% quarter-over-quarter** |
| Q1 2026 | Further **40–50% increase** |
| Q2 2026 | Standard DRAM forecast: another **58–63% increase** |

**Specific price trajectory of 64GB RDIMM**

- Q3 2025: **$255**
- Q1 2026: **over $450** (76% increase in six months)
- Q4 2026 forecast: **$700–$1,000** (up to 4x within a year)

**NAND Flash similarly surging**

- TLC NAND device prices doubled in six months
- SLC and MLC NAND in some cases **400–500% higher**
- 2026 full-year forecast: combined DRAM + SSD up **130%** (Gartner)

**Who is being hit**

- **Individual users**: PC building and repair are effectively price-prohibitive
- **PC and smartphone manufacturers (HP, Lenovo, Xiaomi, etc.)**: Unable to absorb sharp BOM cost increases, forced to **raise retail prices 15–25%**
- **Xiaomi**: Budgeting **25% more** DRAM cost per phone for 2026 models; a $500 phone becomes $625
- **Dell**: "Costs are moving at speeds we've never experienced" (earnings call)
- **HP**: Lowered full-year guidance
- **Cisco**: Margins squeezed by memory prices; biggest stock drop since 2022
- **IDC forecast**: 2026 global smartphone shipments down **12.9%**, PC market down **11.3%** — double-digit market contractions

**Counterpoint Research's summary:**

> Memory companies are telling smartphone makers to get in line behind the hyperscalers.

**Japan's retail front line**

- Tsukumo and Sofmap in Akihabara have purchase limits (max 2 SATA SSDs, 2 NVMe SSDs, 4 SO-DIMMs per customer)
- "Memory reservation certificates": deposit-based reservation system locking 2025 prices for 2026 delivery
- Retail rationing for panic-buying prevention has returned for the first time since the COVID era

**How long will this last?**

- Counterpoint Research: Supply-demand balance will not normalize **until 2028**
- Supply meets only 60% of global demand
- Micron: DRAM scarcity may continue through 2028

**Memory factories cannot be built quickly. Electronics users worldwide will continue to bear the brunt of Microsoft's CapEx for another 2–3 years.**

---

### Material Scarcity — Even the Data Centers Themselves Cannot Be Completed

#### More than half cannot be completed

Of the 12–16 GW of data center capacity scheduled to come online in the U.S. in 2026, only **about one-third is actually under construction**. The rest is stalled awaiting electrical equipment delivery.

Industry analysis predicts that **30–50% of 2026 plans will slip beyond 2028**. **Microsoft is securing global resources for facilities that cannot be completed.**

#### What's happening in the transformer scramble

Data centers don't plug into wall outlets. Stepping high-voltage transmission lines down to usable voltage requires **transformers weighing hundreds of tons**.

- Custom-designed, hand-wound manufacturing (cannot be automated)
- Large transformer lead times: typically **3–5 years**, up to **120 weeks (over 2 years)** at maximum
- Prices: **4–6 times** 2022 levels
- Companies worldwide capable of manufacturing large transformers: **only 5–6**

Hyperscalers are reserving transformers **3–4 years before** breaking ground. **As a result, U.S. utilities are forced to defer their aging-transformer replacement programs.** More than half of U.S. high-voltage distribution transformers are over 33 years old, near or past end-of-life. **Outage risk is structurally increasing in communities worldwide.**

#### Grain-Oriented Electrical Steel (GOES), Copper, Helium, Bromine

Across all materials, data centers receive priority supply, while everything else gets pushed back.

- **GOES** (transformer core material): Cleveland-Cliffs is the sole U.S. producer; 80% of large transformers are import-dependent; prices doubled, lead times 12–18 months. **Renewables, EVs, and grid modernization are pushed back**
- **Copper**: 27–33 tons consumed per data center MW; 304,000-ton shortage in 2025; record high of $6/lb. **EV industry, renewable transmission grids, and residential wiring are getting more expensive**
- **Helium**: Prices doubled after attacks on Qatar; **rationing at semiconductor plants in Taiwan and Korea**. Net chip production may decline
- **Bromine**: Israel's ICL Group controls 40% of global supply; surged to $12,000/ton

#### Grid interconnection queue — power contracts now 3–7 year wait

The U.S. grid interconnection queue has swelled to **over 2,100 GW** — exceeding total U.S. transmission grid capacity. The grid interconnection process now takes **3–7 years**.

**New factories, new hospitals, new schools, new homes — all are queued behind data centers.** Power availability constraints alone are extending construction timelines by **24–72 months** in reported cases.

---

### Massive Fossil Fuel Use — De Facto Withdrawal of Climate Commitments

To secure power for data centers, Microsoft pivoted aggressively in 2026 toward direct large-scale investment in fossil fuel infrastructure. **Climate progress has been substantially set back by a single tech giant.**

#### $7 billion contract with Chevron

In April 2026, Microsoft entered an exclusive agreement with energy giant Chevron and investment firm Engine No. 1 to jointly build **a 2.5 GW massive natural gas power plant** in the Permian Basin of West Texas — a deal worth **$7 billion**.

- Scale: 2,500 MW (expandable up to 5,000 MW)
- Equivalent to power for approximately 4 million U.S. households
- Operational target: late 2027
- Design: **"behind-the-meter"** delivery directly to the data center campus to bypass grid congestion

**4 million U.S. households' worth of power, dedicated solely to one company's AI.**

#### CO₂ emissions and the de facto collapse of the "carbon negative by 2030" pledge

Microsoft has reported that its CO₂ emissions are already **23.4% above 2020 levels**. The ambitious environmental pledge it had made — "achieve carbon negativity by 2030" — has effectively collapsed.

When the massive Texas gas plant comes fully online, this figure will certainly continue rising. According to Stand.earth Research Group's analysis, Microsoft proposed a combined **4.75 GW** of new fossil fuel generation in just the first few months of 2026 alone.

**Industry-wide context**: According to Goldman Sachs' analysis, the explosive growth of AI is projected to drive a **160% increase** in data center power demand by 2030.

#### Data centers swallowing more than a third of natural gas infrastructure

At the end of 2024, data centers accounted for 5% of methane gas generation demand. By the end of 2025, this had jumped to **39%** — roughly an 8-fold increase in one year.

**Home heating, industrial boilers, electricity generation — all natural gas demands are now competing for the same pipelines as data centers.**

---

### The Iran War Oil Shock and the Scramble for Naphtha and Energy

Just as Microsoft committed to large-scale investment in natural gas power plants, the world entered an energy crisis. **Microsoft's construction plans are colliding head-on with a war-driven supply shock.**

#### February 28, 2026: Operation Epic Fury and the Strait of Hormuz Blockade

On February 28, 2026, U.S. and Israeli coalition forces launched a massive air operation (codenamed **"Operation Epic Fury"**) against Iranian military facilities and government command centers. The strike killed Iran's Supreme Leader Ali Khamenei and numerous high-ranking officials.

In retaliation, Iran launched thousands of missiles and drones against U.S. military bases throughout the Middle East and Israel, and effectively **blockaded the Strait of Hormuz** — the world's energy artery.

Cargo passing through the Strait of Hormuz:

- **~20%** of seaborne crude oil trade
- **~20%** of LNG (liquefied natural gas) trade
- **30%+** of urea fertilizer
- **~45%** of sulfur supply (Gulf states)

The International Energy Agency (IEA) characterized this as **"the largest supply shock in the history of the world oil market."**

#### Gasoline and electricity prices rising worldwide

- Gasoline prices: up **30% within weeks**
- Brent crude: from $72/barrel before the war to nearly $120 at peak (over 55% increase)
- Asian LNG spot prices: **140%+ surge**, compounded by attacks on Qatar's Ras Laffan facility
- Qatar's LNG production capacity: down 17%, full recovery in 3–5 years

**Households worldwide are paying more for electricity, fuel, and heating.**

Natural gas power plants are designed assuming continuous fuel supply. Microsoft's $7 billion investment decision presumes **a world of cheap, stable fossil fuels**. That premise collapsed on February 28, 2026. Yet construction continues.

#### The Naphtha Crisis — the Cutoff of an Irreplaceable Chemical Feedstock

The Hormuz blockade hit not only crude oil and LNG but also **naphtha**. Naphtha is a basic petrochemical feedstock obtained through crude oil distillation — the starting point for plastics, synthetic fibers, pharmaceutical packaging, and semiconductor manufacturing. **It has no substitute.**

**Catastrophic naphtha price surge**

- Immediately after February 28, 2026 (war start), spot prices nearly doubled from approximately **$600 to $1,190 per ton**
- Up **60% in one month** from the war start; reached **$1,000 per metric ton** in Asian markets
- Indian PVC prices up **78% in March alone**

**Japan, Korea, Malaysia — the extreme dependence on the Middle East**

- Japan's domestic naphtha inventory: a critical level of **only 10–20 days**
- **About 80%** of Japanese tankers transit the Strait of Hormuz; Middle East crude dependency exceeds 95%
- Over **70%** of Korea's crude imports pass through the Strait of Hormuz
- Japanese government: released **80 million barrels** from strategic reserves (a drop in the bucket)
- **Idemitsu Kosan**: warned trading partners of ethylene plant shutdowns if the Hormuz blockade persists. Tokuyama (620,000 tons/year) and Chiba (370,000 tons) plants are shutdown candidates — about **16% of Japan's ethylene production capacity**
- **Tosoh Corporation**: announced major price increases for MDI products
- **Mitsubishi Chemical**: assessing naphtha inventory durability
- **Korea**: emergency imports of Russian naphtha; export ban on naphtha

**Production halts under force majeure declarations**

- Indonesia's largest chemical company Chandra Asri Pacific
- Singapore's PCS (Petrochemical Corporation)
- Korea's Yeochun
- **More than 10 petrochemical plants** halted production across Asia

#### Medical Infrastructure vs. AI Infrastructure — Naphtha Triage

The extreme shortage of naphtha has triggered an ultimate **"triage (selective allocation of resources)"** in global supply chains.

| Naphtha-derived end products in competition | Healthcare / general industry | AI / data center infrastructure |
|---|---|---|
| Polyvinyl chloride (PVC) | Dialysis circuits, blood tubing, IV bags | Data center cable insulation, large piping |
| Polyethylene (PE) | Syringes, sterile packaging, pharmaceutical containers | Fiber optic cable jackets, immersion cooling specialty piping |
| Polyurethane / specialty resins | Medical valves, clamps, catheters | Server chassis plastic parts, motherboard coatings |

As the National Kidney Foundation of Malaysia and others have warned, modern medical systems are completely dependent on disposable plastic medical devices — dialyzers, syringes, and the like.

Normally, market mechanisms ensure that materials needed for medical infrastructure are secured. But in the 2026 crisis, hyperscalers like Microsoft — with annual CapEx budgets exceeding $100 billion — moved to lock in upstream raw materials (PVC, PE, etc.) at any price for the cables and cooling equipment essential to their data centers under construction.

**Medical device manufacturers and small packaging firms, with vastly inferior buying power, cannot pass the surging raw material costs to product prices and have been physically squeezed out of the procurement market.**

The recognition that **"dialysis patients are being sacrificed for an AI no one is using"** is not a literary metaphor. It is **an accurate description of the medical supply chain crunch unfolding across Asia in spring 2026**.

99% of German packaging manufacturers are receiving price hikes, with only some able to pass the costs through (March 2026, German Plastics Processing Association survey). **The risk of small and mid-sized manufacturer bankruptcies is rising worldwide.**

---

## Embedding Copilot Was Nadella's Failure

All the harm described above exists for the sake of integrating Copilot into the foundation of society. Even though Copilot has been rejected by employees, lost user trust, and been defeated in market share, Nadella will not stop the integration.

But **Copilot is not being used.** Microsoft's own data shows this.

### Usage rate — the massive gap between provisioned licenses and actual use

The largest structural challenge in Microsoft's AI rollout is the enormous gap between provisioned seat count and actual usage rate.

- **Microsoft 365 Copilot paid seats**: 15 million (Q2 2026)
- **Of employees with access, only 35.8% actually use it** (Recon Analytics, U.S. survey of 150,000 people, 2026)
- The remaining roughly two-thirds either don't use it despite having access, or have migrated to other platforms

In other words, even when companies pay for Copilot licenses, **two-thirds of their employees aren't using it**.

### Trust score (NPS) collapse

Copilot's NPS (Net Promoter Score) for accuracy:

- July 2025: **-3.5**
- September 2025: **-24.1** (severe deterioration)
- January 2026: **-19.8** (partial recovery, still deeply negative)

An NPS this deeply negative means **users who tried it not only refuse to recommend it to colleagues — they actively warn others away**.

In a survey of users who discontinued Copilot, **44.2% cited "distrust in answers" as the primary reason for stopping** — a level of distrust strikingly higher than for competing AI tools.

The unparalleled distribution advantage of being default-integrated into the OS and Office applications has not translated at all into product trust or actual usage.

### Anthropic Has Overtaken Microsoft in the Enterprise AI Market

In the enterprise AI market, Microsoft is no longer the winner. Anthropic's Claude has taken control.

**Anthropic vs. Microsoft Copilot, as of April 2026**

| Financial / Adoption Metric | Anthropic (Claude) | Microsoft (Copilot Enterprise) |
|---|---|---|
| Annual recurring revenue (ARR) | Exceeded **$30 billion** | Not disclosed (estimated $1.5–2.5 billion from 15M seats) |
| Growth rate (last 15 months) | ~30x ($1B → $30B) | Stalled at 35.8% utilization |
| Fortune 100 adoption | **70% adopted as primary model** | High deployment via Office bundle, but limited active use |
| Fortune 10 adoption | **8 out of 10 are customers** | — |
| Developer NPS | 54 (Claude Code, January 2026) | -19.8 (general business use, January 2026) |

**Anthropic's growth trajectory — fastest in enterprise software history**

- January 2025: ARR $1 billion
- Within 2025: reached $9 billion
- February 2026: $14 billion (Series G, $380 billion valuation)
- April 2026: **exceeded $30 billion** — surpassed OpenAI's estimated $25 billion
- As a B2B software company, three consecutive years of 10x annual growth — neither Slack, Zoom, nor Snowflake has matched this

**Claude Code's rise**

In software development, Claude Code's surge is striking. Claude Code alone has reached **ARR of $2.5 billion**, growing into a tool **used daily by 45% of professional software engineers**.

In development environments, the **"multi-tool stack"** has settled in as the standard 2026 paradigm: using Claude Code or Cursor for high-reasoning tasks like autonomous agent functions, complex refactoring, and architecture design.

**Examples of large-scale Claude deployments**

- Cognizant: Claude deployed to 350,000 employees
- Accenture: 30,000 trained on Claude; dedicated Anthropic Business Group established
- Deloitte: Rolled out to 470,000
- Salesforce Agentforce: Claude is the preferred model

**Unrecoverable CapEx**

- Microsoft Copilot estimated ARR: **$1.5–2.5 billion**
- Microsoft CapEx: **$100–120 billion**
- CapEx is **more than 50x Copilot revenue**

Meanwhile, in the same AI market, Anthropic is achieving **$30 billion** ARR with a fraction of Microsoft's CapEx. **The problem is not lack of demand for AI — it's that Microsoft's Copilot is not being chosen.**

### Microsoft's Own Pilot Failure Rate

Gartner survey: **Of Copilot pilot deployments, only 24% successfully scaled to 20%+ of employees.** The remaining 76% are stuck in pilot.

### The Structural Point

Nadella has executed a massive integration strategy, pulling in employees, users, partners, and nation-states. But the substance of that strategy (Copilot) is **a product not chosen by humans given a choice**. 8 of the Fortune 10 and 70% of the Fortune 100 are choosing Claude.

The structure "enterprises are buying AI, but not buying Copilot" is in complete agreement with objective market data.

---

## What Happens in Word, Excel, and PowerPoint — Mathematically Unavoidable Breakdown

In July 2025, Varin Sikka and others at Stanford University posted a paper to arXiv.

**Varin Sikka, Vishal Sikka, "Hallucination Stations: On Some Basic Limitations of Transformer-Based Language Models" (arXiv:2507.07505)**

Vishal Sikka is the former CTO of SAP, former CEO of Infosys, and a board member at Oracle, BMW, and GSK.

The paper proves that hallucinations (the generation of plausible-sounding false information) by large language models (LLMs) are not merely products of insufficient training data or probabilistic errors — they are **unavoidable physical and mathematical phenomena rooted in the "computational complexity mismatch" inherent to the Transformer architecture**.

**The paper's theorem:**

The inference process (self-attention mechanism) used when a standard Transformer-based LLM generates text always operates under the strict fixed-budget constraint of **O(N²·d)** computational time, where N is input token count and d is vector dimension.

Yet many practical tasks enterprises ask LLMs to perform have computational complexity far exceeding this budget:

- Extracting specific logical contradictions from a corpus of long documents — **O(n³)**
- Relational join operations across multiple databases — **O(n³)**
- Matrix multiplication — **O(n³)**
- Strict verification of optimal solutions to the Traveling Salesman Problem — **(n-1)!/2** (factorial order)

The moment a task's intrinsic computational complexity exceeds the model's reasoning ceiling of O(N²·d), it becomes physically impossible for the LLM to take the computational steps needed to perform the task correctly. But because **LLMs have no mechanism to explicitly declare computational failure**, they shift into a mode of blindly generating "the most probable next token" given the context.

The result is **a confidently delivered wrong answer that is grammatically perfect but substantively shattered** — a hallucination.

This cannot be overcome by scaling up. It is a ceiling inherent in the architecture.

### What Happens with Copilot

For tasks beyond a certain complexity, Copilot will either fail or confidently produce wrong answers. Long-form Word editing, complex Excel aggregation, PowerPoint structuring, Outlook email summarization — all silently break down the moment complexity exceeds threshold.

Copilot does not announce that it has broken down. **The essence is that failure and correct answers are externally indistinguishable.**

**The content Copilot generates is not verbatim-verified by humans.** "Things I didn't write" and "things I can't explain" accumulate inside corporate documents, government documents, medical records, and financial records.

**One day, an error in a residence record is discovered. A nonexistent transaction is found in a financial report. An incorrect prescription is found in a medical record.** Whether it came through Copilot or human error — no one can tell.

### Verification Is Impossible Even with Agentic AI

The Sikka paper also points out the difficulty of verification in autonomously operating "agentic AI." Tasks where one AI verifies whether another AI's generated solution is correct often **involve even higher computational complexity than generating the solution itself**.

This means that even by combining multiple AI agents, it is fundamentally impossible to guarantee correctness on advanced tasks.

---

## The Attack Surface — The Compliance Crisis from OS Deep Integration

Despite the existence of these mathematically proven, unavoidable limits, Microsoft chose a strategy of integrating Copilot into the deepest parts of Windows 11 and Microsoft 365 — its OS and platform.

The biggest problem here is that when the system silently breaks down (exceeding computational limits and producing wrong answers), **there is no mechanism to externally distinguish failure from success**.

The Windows + Office + Copilot stack creates a state where AI processing pathways are constantly open from the deepest parts of the OS. In a system where you cannot tell what passed through AI, **you cannot identify attacker intervention traces either**.

For an AI that cannot be audited to be placed in default access to sensitive patient data or financial information at the OS level **fundamentally obscures the locus of legal liability**. The risks of AI-generated incorrect prescription summaries, financial reports containing fictitious transactions, accumulating inside systems — these are no longer theoretical concerns but **cybersecurity vulnerabilities directly threatening real-world business infrastructure**.

**Local governments, hospitals, banks, schools — all critical infrastructure is in an unauditable state.**

Against the speed of Mythos-class attacks, completely auditing AI processing pathways is impossible — for both outsourced and in-house IT departments. Legally and physically. **Even when a breach occurs, the likelihood is high that no one will notice.**

---

## Why Nadella Cannot Stop Embedding Copilot Anyway

Even after being rejected by employees, distrusted by users, and defeated in market share, Nadella cannot stop Copilot integration. The reason is simple: the moment he stops, multiple premises collapse.

### The Reasons He Cannot Stop

**(1) The premise of stock price**

Microsoft's market cap exceeds $3 trillion. This level rests on the narrative that **"AI is the next growth driver."** The moment Nadella admits "Copilot is not being adopted" or "we are reducing CapEx," the stock price will plummet.

The bulk of FY2026's $100–120 billion CapEx is being financed through stock issuance and debt. **If the stock falls, financing costs spike, and data centers under construction cannot be completed.**

**(2) Strategic position with OpenAI**

Although the exclusivity was relaxed in January 2025, Microsoft Azure remains the exclusive cloud for OpenAI's stateless API. As OpenAI builds its own infrastructure (Stargate), **Microsoft must continue CapEx to maintain its position as "the cloud provider that has OpenAI."**

**(3) Long-term contract lock-in**

In 2026, Microsoft has signed a multi-trillion-won three-year DDR5 contract with SK Hynix, a $7 billion natural gas contract with Chevron, a long-term DRAM contract with Samsung, and a $100 billion fund with BlackRock + MGX. **These contracts impose payment obligations whether Copilot succeeds or fails.** Stopping mid-stream locks in losses.

**(4) Sovereign AI integration into national security**

The $10 billion contract with Japan (2026–2029) is not merely data center expansion. It is the core of a national project — collaborating deeply with domestic telecom and cloud providers like SoftBank and Sakura Internet — to build **"Sovereign AI" infrastructure** keeping data within Japan.

It is fully aligned with METI's multi-trillion-yen AI investment strategy and includes close cybersecurity collaboration with the National Police Agency and the Cabinet Secretariat. The same applies to Saudi Arabia's Sovereign Cloud, the linkage with UAE capital (MGX), and U.S. police's Copilot partnerships.

**Microsoft is no longer simply a corporation — it is entangled in treaty-like relationships with multiple nations on national security matters.** Mid-stream withdrawal would mean breaking those relationships.

**(5) Forced hardware refresh cycle**

Combining the Copilot+ PC requirements (40 TOPS NPU, 16GB DDR5, 256GB SSD) with Windows 10's end of support has **pushed a substantial portion of the world's Windows users into purchasing new PCs**. If Copilot integration stops, the justification for that forced purchase collapses. The 2026 sales plans of Dell, HP, Lenovo, Acer, ASUS, and other PC makers collapse with it.

**(6) Nadella's personal record**

Nadella has been celebrated for transforming Microsoft into a cloud and AI company since becoming CEO in 2014. Copilot is his largest strategic bet. **Withdrawing here turns the verdict on his entire CEO tenure into "failure."**

### What This Produces — A Self-Destructive Negative Loop

Because he cannot stop, the enforcement deepens. To keep performing the growth narrative as "the leading AI company" and to keep the massive financing flowing, the alternative is not just stock collapse but the collapse of treaty-like relationships with multiple nations on security matters. **The result is a self-destructive negative loop in which unwanted investment and OS feature integration accelerate further.**

- Further raising hardware requirements → users worldwide replace PCs again
- Deeper OS integration of Copilot → fewer options to opt out
- Forced Copilot use for individual users (auto-installation has already begun)
- Increased sales pressure on local governments, healthcare, finance → continued legal liability transferred to organizations
- Forced migration to Microsoft 365 E3 ($432/year) → subscription costs triple
- Continued ESU price escalation for Windows 10
- Expansion in less-regulated emerging markets (Japan, Southeast Asia, Middle East) → harm spreads in regions outside the EEA's regulatory protection

And simultaneously, the world's memory, electricity, copper, helium, bromine, and naphtha continue to be consumed **for the sake of running an unsold Copilot**.

Hospitals can no longer secure dialysis equipment packaging materials. Auto plants face component supply disruptions. Semiconductor plants run on rationed helium. Households pay more for electricity. Smartphones and PCs get more expensive. Climate progress reverses. Small and mid-sized manufacturers go under.

---

## Conclusion — An Organization That Cannot Stop Its CEO Will Physically Break Down

What happens to a Microsoft whose CEO cannot be stopped — Nadella will keep going until he is forcibly stopped. This is a pattern humanity has repeated.

Because Microsoft was such a large and excellent company, the harm already being scattered worldwide is immeasurable. From here, that harm will accelerate.

Will you continue using Windows and Office anyway?

You will suffer through PC replacements, Office subscription price hikes, and rising cybersecurity defense costs.

Microsoft's platform is no longer the neutral, stable infrastructure that supports business operations. It has transformed into **"a high-maintenance, high-risk agent that drains budgets without limit and threatens compliance and social responsibility."**

A staged migration to open-source operating systems (Linux and others) for desktop environments, de-Microsoftization of office suites, and limited, verifiable adoption of AI through APIs from independent vendors (such as Anthropic) — these are the most reliable, rational technology strategies for protecting an organization's self-determination and budget from this complex global crisis.

**Migrate to Linux as soon as possible.**

---

## References

### LLM mathematical limits
- Varin Sikka, Vishal Sikka, "Hallucination Stations: On Some Basic Limitations of Transformer-Based Language Models", arXiv:2507.07505 (July 2025)
- WIRED, "A research paper suggests AI agents are mathematically doomed to fail. The industry doesn't agree." (January 2026)

### Microsoft / Copilot enforcement
- Mozilla Blog, Linda Griffin, "Old habits die hard: Microsoft tries to limit our options, this time with AI" (April 2026)
- The Register, "Mozilla calls out Microsoft over Copilot push in Windows" (April 2026)
- AI Business Weekly, "Accenture Ties Promotions to AI Use; KPMG, Meta Follow"
- Microsoft Internal Memo, "Using AI Is No Longer Optional" (2025)
- HRD America, "Microsoft offers to buy out 7% of its workforce as it pivots towards AI"
- TNW, "Meta cuts 8,000 jobs and Microsoft offers first-ever buyouts as Big Tech converts payroll into AI capital expenditure"

### Copilot adoption and failure rates
- Recon Analytics, "AI Choice 2026: Why Licenses Don't Equal Adoption" (U.S. survey of 150,000, January 2026)
- Stackmatix, "Microsoft Copilot Adoption Statistics & Trends (2026)" (April 2026)
- AI Business Weekly, "Microsoft Copilot Statistics 2026: Users & Adoption" (March 2026)
- Avantiico, "The Definitive Microsoft 365 Copilot Adoption Guide for Businesses [2026]" (April 2026)
- Adoptify AI, "Why Microsoft Copilot Adoption Often Stalls" (January 2026)
- Whatfix, "Microsoft Copilot Adoption: From Enterprise Rollout to Habitual Usage" (January 2026)
- Gartner Copilot pilot scaling rate study

### Enterprise AI market — Claude / Anthropic adoption
- Medium, David C., "Anthropic Just Passed OpenAI in Revenue. Here Is Why It Matters." (April 2026)
- AI Business Weekly, "Claude AI Statistics 2026: Users, Revenue & Market Share" (April 2026)
- Searchlyn, "Claude Statistics: Users, Revenue & Growth in 2026" (April 2026)
- Second Talent, "Claude AI Statistics and User Trends for 2026" (April 2026)
- The AI Corner, "Claude AI in 2026: Stats, Workflows, and Resources" (March 2026)
- Thunderbit, "Claude Gemini Adoption Trends and Statistics for 2026" (March 2026)
- IdeaPlan, "AI Coding Assistants Market Share 2026"
- Uvik Software, "AI Coding Assistant Statistics 2026: 50+ Key Data Points"
- systemprompt.io, "Claude Code vs Cursor"
- Menlo Ventures, "2025 Enterprise LLM Spend Report"
- Anthropic Series G announcement (February 2026)
- Anthropic ARR $30 billion announcement (April 2026)

### Windows hardware requirements and disposal
- Microsoft, "Windows 11 Specs and System Requirements"
- Canalys, "End of Windows 10 support could turn 240 million PCs into e-waste" (December 2023)
- Tom's Hardware, "Microsoft's draconian Windows 11 restrictions" (December 2024)
- Microsoft Learn, "Extended Security Updates (ESU) program for Windows 10"
- Brytesoft, "Windows 10 ESU Cost in 2026: 3-Year Pricing Breakdown"
- Microsoft Learn, "Windows 11, versions 25H2 and 24H2 required diagnostic data events and fields"

### Microsoft data center build-out plans
- Network World, "Microsoft will invest $80B in AI data centers in fiscal 2025" (May 2025)
- Data Center Dynamics, "Microsoft spent $11.1bn on data center leases alone in Q1 2026" (February 2026)
- Introl Blog, "Hyperscaler CapEx Hits $690B in 2026" (February 2026)
- Microsoft On the Issues, "Made in Wisconsin: The world's most powerful AI datacenter" (September 18, 2025)
- Microsoft Blog, "Inside the world's most powerful AI datacenter"
- Data Center Frontier, "Microsoft Builds for Two Worlds: Sovereign Cloud and AI Factories" (2026)
- Microsoft Source Asia, "Microsoft deepens its commitment to Japan with $10 billion investment" (April 3, 2026)
- Windows Forum, "Sakura Internet Rises as Japan Sovereign AI Gets a $10B Boost"
- Dark Reading, "Microsoft Bets $10 Billion to Boost Japan's AI, Cybersecurity"
- RCR Wireless, "Five key things to know about AI infra investments in Japan"

### CO₂ emissions and climate
- NYC Comptroller, NYCERS Annual Climate Report FY2025 (Microsoft 23.4% increase vs. 2020)
- Energy Platform News, "Microsoft carbon emissions jump as AI and cloud demand rises"
- Goldman Sachs, "AI is poised to drive 160% increase in data center power demand"
- Stand.earth Research Group, "160% data center carbon footprint increase" (April 2026)
- IT Pro, "Gas-powered data centers could more than double Microsoft's emissions" (April 2026)

### Memory and storage
- Counterpoint Research, "Memory Prices Soar by 50% in Q4, Rally to Continue in 2026" (January 2026)
- BuySellRam, "Samsung's 100% DRAM Price Hike and Why Even Apple Had to Pay Up"
- SmarterArticles, "Priced Out by AI: The Memory Chip Crisis Hitting Every Consumer"
- SoftwareSeni, "DRAM Prices in 2026 Have Doubled and the Numbers Are Getting Worse"
- Tom's Hardware, "OpenAI's Stargate project to consume up to 40% of global DRAM output" (October 2025)
- Open Markets Institute, "OpenAI's RAMpage" (February 2026)
- TrendForce, "From Annual Deals to 3–5 Year LTAs: Samsung and SK hynix" (April 2026)
- IDC, "Global Memory Shortage Crisis" (February 2026)
- IEEE Spectrum, "AI Boom Fuels DRAM Shortage and Price Surge" (April 2026 issue)

### Data center completion failure and materials
- Manufacturing Dive, "The great data center delay" (April 2026)
- Tom's Hardware, "Half of planned US data center builds have been delayed or canceled" (April 2026)
- Tom's Hardware, "AI data-centre buildout pushes copper toward shortages" (December 2025)
- Power Magazine, "Transformers in 2026" (January 2026)
- The Invading Sea, "Supply-chain delays threaten power grid" (December 2025)
- Sandstone Group, "More than half of the Data Centers may be delayed" (April 2026)

### Chevron contract and fossil fuels
- Fortune, "Microsoft and Chevron enter exclusivity deal" (April 1, 2026)
- IDC Nova, "Microsoft, Chevron, and Engine No. 1 Forge Landmark Gas-to-Power Partnership"
- Energynow, "Microsoft in Talks With Chevron, Engine No. 1 Over $7 Billion Texas Power Plant"
- Motley Fool, "Chevron Could Build a $7 Billion Gas Plant to Power Microsoft's AI Ambitions"

### Iran war and the Strait of Hormuz
- Wikipedia, "2026 Iran war"
- Wikipedia, "Reactions to the 2026 Iran war"
- Wikipedia, "Economic impact of the 2026 Iran war"
- Britannica, "2026 Iran war: Explained, United States, Israel, Strait of Hormuz"

### Naphtha crisis and medical infrastructure
- CNN, "Noodles, kidney dialysis, condoms – the global oil crisis is turning into an everything crisis" (April 2026)
- CNBC, "Iran war Strait of Hormuz petrochemicals oil plastics" (March 2026)
- Inbound Logistics, "The Invisible Shortage: How Petrochemical Shortages Could Impact Packaging" (April 2026)
- Plastmatch News, "Hormuz Strait Blockade Sparks Shortage of Plastic Raw Materials" (April 2026)
- Financial Content, "Naphtha Surges to $1,000: The Petrochemical Crisis of 2026 Explained" (March 2026)
- Iran International, "Strikes on petrochemical hubs leave Iran short of plastics" (April 2026)
- PUdaily, "Japanese MDI Suppliers Forced to Raise Prices as Upstream Supply Risks Persist" (Idemitsu Kosan, Tosoh)
- Japan NRG Weekly 20260406
- CodeBlue, "Malaysia Faces Emerging Shortage Of Dialysers, Haemodialysis Components"
- ICIS, "INSIGHT: Asia petrochemical demand muted amid feedstock shortage" (April 2026)

### Windows / Microsoft 365 user counts
- Microsoft official Windows Experience Blog (June 2025)
- Microsoft Q2 2026 earnings call (January 28, 2026)
- StatCounter Global Stats (February 2026)
- Expanded Ramblings, "Microsoft Office Statistics (2026)" (February 2026)

### Existing data centers and grid impact
- arXiv:2509.07218, "Electricity Demand and Grid Impacts of AI Data Centers"
- World Resources Institute, "Powering the US Data Center Boom"

---

[Gemini Verification Report](014-windows-office-facts.pdf)

*aiseed.dev*