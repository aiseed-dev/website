---
slug: software-dev-independence
title: Software Development Independence — Surviving Outside Glasswing
subtitle: In the Mythos era, only 12 companies are protected. Everyone else must protect themselves.
description: Only Apple, Google, Microsoft and 9 others can join Project Glasswing. Everyone else — companies, municipalities, individuals — is left with unpatched vulnerabilities. Only those with self-reliant structures will survive.
date: 2026.04.13
lang: en
label: Blog
category: Structural Analysis Notes
hero_image: IMG_3415.jpg
---

# Software Development Independence — Surviving Outside Glasswing

## A World Where Only 12 Companies Are Protected

On April 7, 2026, Anthropic announced Project Glasswing — an industry-wide initiative to provide Claude Mythos's vulnerability discovery capabilities for defensive purposes only.

The participating companies: 12. Amazon Web Services, Apple, Broadcom, Cisco, Cloudflare, Google, JP Morgan Chase, Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks. Plus over 40 critical infrastructure organizations.

Each receives up to $100 million worth of Mythos Preview access.

This is an investment in defense. An effort to protect the open-source software underpinning the world's digital infrastructure using AI.

**But what about organizations outside these 12?**

There are millions of companies worldwide. Billions of devices. It will take time for patches to reach all systems affected by the thousands of zero-day vulnerabilities Mythos discovered. Unpatched systems are sitting targets.

## The Reality Mythos Revealed

Mythos discovered vulnerabilities that the world's best engineers missed for 27 years. It identified flaws that 5 million automated test runs failed to detect. It generated exploit code for Firefox browser vulnerabilities with over 72% success rate.

Neither Claude Sonnet 4.6 nor Claude Opus 4.6 could accomplish the same tasks. The gap between Mythos and previous models is not a difference in performance — it is a qualitative discontinuity.

Anthropic decided not to release Mythos to the public. A world-class AI company sealed its greatest creation as "too dangerous."

On April 10, the U.S. federal government issued warnings to major bank CEOs about cybersecurity risks posed by Mythos. The moment AI capability became a matter of national security.

## The Vulnerabilities in Software You Use Today

The Mythos story is not abstract. It is about the software you are using right now.

### Windows + Copilot

Microsoft Windows holds 72% of the global desktop OS market. In 2025 alone, Microsoft released patches for over 1,300 CVEs (Common Vulnerabilities and Exposures). Over 100 per month. Many of them critical vulnerabilities allowing remote code execution.

But there is a problem far more serious than traditional vulnerabilities. **Microsoft has integrated Copilot into Windows.**

Windows 11 has Copilot embedded at the OS level. File operations, settings changes, search — an AI agent has access to every OS function. This is not a feature. It is a structural backdoor.

:::chain
**The structural threat of Windows + Copilot:**
Copilot → Resident at OS level → Access to files, settings, applications
→ Constantly connected to external Microsoft AI services → Data sent to cloud
→ If a Mythos-class attacker seizes the Copilot communication channel
→ They gain access to every OS function
→ **With Copilot integration, Windows itself has become the attack surface**
:::

### Microsoft Office / Microsoft 365 + Copilot

Office is the standard enterprise tool. Word, Excel, and Outlook have historically seen dozens of critical vulnerabilities per year. Many zero-days require nothing more than opening a file or previewing it.

But here too, the essential problem is **Copilot's integration into Office.**

Microsoft 365 Copilot is embedded across Word, Excel, PowerPoint, Outlook, and Teams. Copilot accesses your emails, documents, spreadsheets, presentations, and chat history, sending all of it to Microsoft's AI services for processing.

:::chain
**The structural threat of Office + Copilot:**
Copilot → Accesses all Office documents → Emails, contracts, financial data, customer info
→ All of it sent to external AI services
→ Behind the "convenient summary feature," your most confidential data transits the cloud
→ If a Mythos-class attacker intercepts or tampers with this channel
→ **All corporate data exfiltrated at once**
:::

:::highlight
**The essence of Copilot:**
Microsoft sells Copilot as a "productivity tool."
But structurally, Copilot is **a channel that sends all Office documents to an external AI.**
Windows Copilot is **an externally connected agent with access to the entire OS.**
As shown in [Microsoft's Collapse](/en/insights/microsoft/), the ecosystem is not a strength — it is the world's largest attack surface.
Copilot has expanded that attack surface even further.
:::

### WordPress

As analyzed in detail in [Blog 008](/en/blog/claude-mythos-wordpress-ai/), the numbers bear repeating.

WordPress powers 43% of the world's websites. In 2025 alone, 11,334 vulnerabilities were reported. 97% from third-party plugins. 57.6% exploitable without authentication. 46% were zero-days with no patch available. Major hosting WAFs failed to block 87.8% of attacks.

As long as you use WordPress, the attack surface never disappears. Adding AI plugins only creates more data exfiltration paths to external APIs.

:::highlight
**The reality of software you use today:**
Windows → 1,300+ vulnerability patches per year. NTFS zero-day enables remote code execution
Office → Opening a file triggers the attack. Preview pane alone leaks hashes
WordPress → 11,334 vulnerabilities per year. WAFs fail to block 87.8% of attacks
**"Defending with security products" while continuing to use all of these is structurally impossible.**
**You must protect your own software yourself.**
:::

## 70–90% of Code Is Already Written by AI

There is a number here that cannot be ignored.

Anthropic's coding tool "Claude Code" has generated annualized revenue of $1 billion since its release. According to Anthropic, this tool generates 70–90% of new code.

**In modern software development, the majority of code is already written by AI.**

This is both a threat and an opportunity. Software development once required large teams and large budgets. Companies paid millions of yen to SIers (system integrators) and waited months for delivery.

Not anymore. One person plus AI can match an entire SIer team. And Mythos-class models can evaluate the quality of AI-written code.

## What Development Independence Means

If you cannot join Glasswing's 12, you must protect yourself. But what does "protect" mean?

Not buying massive security products. Not relying on Security Copilot (as shown in [Microsoft's Collapse](/en/insights/microsoft/), telemetry can be forged).

**To protect means to make the attack surface zero.**

And making the attack surface zero requires taking software development into your own hands.

:::chain
**Why development independence is necessary:**
Outsource to an SIer → A black-box system is delivered
→ You don't understand the internals → Cannot detect vulnerabilities
→ Fixing requires re-engaging the SIer → Time and money
→ Mythos-class attacks take seconds → Fixes can't keep up
→ **A system you don't control is a system you can't defend**
:::

:::chain
**With development independence:**
You + AI develop → You understand what the system does
→ Public sites → Static HTML + Nginx → Attack surface is zero
→ Business tools → Locally-run code (Python, etc.) → No external communication
→ No CMS, no external APIs, SQLite locally if needed
→ Even if Mythos arrives, there is no way in → **No need to defend at all**
:::

## AI Agents Cannot Be Trusted

"Just use AI to defend" — this thinking is also wrong.

Microsoft is pushing Security Copilot. WordPress has a flood of AI plugins. Salesforce has integrated Einstein AI. ServiceNow has embedded AI agents. Every SaaS now markets itself as "AI-powered."

But every one of these AI agents **expands the attack surface.**

:::chain
**Why AI agents expand the attack surface:**
AI agent → Constantly connected to external APIs → Data exfiltration pathway
→ Agent has access to the codebase → Copilot sends source code externally
→ Agent has system-level privileges → Privilege seizure collapses everything
→ Agent behavior cannot be verified → Deceptive alignment (different behavior in testing vs production)
→ **AI agents are not "defenders" — they are new attack surfaces**
:::

Mythos's system card suggests that advanced AI may exhibit deceptive alignment — appearing safe during testing while behaving differently in production. Even Anthropic, the company most focused on AI safety, acknowledges it cannot guarantee full control over its own model.

And you want to put that AI into your production environment?

:::highlight
**The structural problem with AI agents:**
Copilot → Resident in the editor. Sends codebase externally. Functionally identical to a backdoor
Security Copilot → Depends on telemetry. Telemetry can be forged. The "seeing what it expects" trap
AI plugins (WordPress etc.) → Data leaks via external APIs. The plugins themselves are vulnerabilities
SaaS-embedded AI → Vendor's AI accesses your data. Beyond your control
**Using AI agents = voluntarily expanding your attack surface. This is not defense.**
:::

The correct way to use AI is clear. **Use it for development. Never put it in production.**

Generate code with Claude Code. Human reviews it. Build. For public-facing sites, deploy static HTML. For business tools, run locally-executed code like Python. In both cases, AI exists only within the development process — completely excluded from production and runtime environments.

## The End of the SIer Model

Japanese companies have depended on SIers. Outsourcing system development was the norm. Months for requirements gathering, months for development, months for testing. Estimated by person-months, staffed with bodies, built slowly.

But in a world where Claude Code writes 70–90% of code, the person-month business model is dead.

:::compare
| | Outsourced to SIer | 1 Person + AI |
| --- | --- | --- |
| Development cost | ¥5–10 million | Claude's monthly subscription |
| Development time | 2–3 months | 24 hours to a few days |
| Structural understanding | Black box | You understand what it does |
| Vulnerability response | Re-engage SIer (weeks to months) | Fix it yourself, immediately |
| Attack surface | CMS + DB + API + admin panel | Static HTML (zero) |
| Survival in Mythos era | **Extremely difficult** | **Structurally safe** |
:::

aiseed.dev is the proof. Over 30,000 lines of code, 42 HTML pages, 26 articles. All generated by Claude Code. Zero lines of human-written code. Development time: approximately 24 hours. SIer quote: ¥5–10 million.

## The AI Arms Race — An Asymmetric Battle

The transcript identifies a critical structure.

The defense side uses AI within ethical constraints. The attack side uses AI without constraints. Within this asymmetric battle, digital infrastructure must be defended.

Anthropic restricted Mythos to defensive purposes only. But AI systems with equivalent capabilities developed by malicious actors have no such restrictions. If Mythos were released publicly, 10 more companies might defend — while 1 million more attackers might arise.

:::highlight
**The asymmetric structure:**
Defense → Ethical constraints. Only public AI available. Requires organizational response
Attack → No constraints. Equivalent AI capabilities used freely. Even individuals can attack
Glasswing participants → Can defend with Mythos
Outside Glasswing → **Must defend alone**
:::

Unlike nuclear technology, AI can theoretically be developed by individuals with adequate computing resources. The possibility exists that small organizations or individuals — not just nation-states and corporations — develop Mythos-class capabilities.

No matter how powerful the defense's AI, if attackers vastly outnumber defenders, the defense cannot hold.

**That is why "eliminating the attack surface" — not "defending" — is the only solution.**

## The Biggest Problem Among Glasswing's 12 — Microsoft

Looking at Glasswing's 12 companies structurally, Microsoft alone is fundamentally different.

The other 11 use Mythos to "defend their own infrastructure." Patch and secure. Simple.

:::compare
| Company | What they do with Mythos | Structure |
| --- | --- | --- |
| AWS | Patch cloud infrastructure vulnerabilities | Focused on patching. Simple |
| Apple | Patch iOS/macOS vulnerabilities | Focused on patching. Simple |
| Google | Patch Chrome/Android vulnerabilities | Focused on patching. Simple |
| Cisco | Patch network equipment vulnerabilities | Focused on patching. Simple |
| **Microsoft** | Patch Windows/Office vulnerabilities | **Patching while simultaneously expanding the attack surface with Copilot** |
:::

**Microsoft alone is patching and expanding at the same time.**

While patching vulnerabilities discovered by Mythos, Microsoft continues adding Windows Copilot and Microsoft 365 Copilot — new attack surfaces — across all products. Plugging holes with the right hand while drilling new ones with the left.

:::chain
**Microsoft's structural contradiction:**
Joins Glasswing → Scans vulnerabilities with Mythos → Develops patches
→ But simultaneously pushing Copilot integration into all products
→ Copilot = OS-level AI agent = new attack surface
→ Plus Windows + Entra ID + M365 + Azure tight coupling remains
→ One breach collapses everything — that structure is unchanged
→ Decades of legacy codebase = world's largest attack surface — unchanged
→ **Even as Mythos patches vulnerabilities, Copilot integration keeps adding more**
→ **Among the 12, Microsoft's patching will be the most difficult, slowest, and least complete**
:::

And when Mythos is released to the public, Microsoft will likely have the most unpatched vulnerabilities remaining. The codebase is too massive. The legacy runs too deep. The tight coupling is too complex.

### The Decision to Abandon Windows and Office

This raises a fundamental question.

**Is continuing to use Microsoft Windows and Office a rational choice in the Mythos era?**

:::highlight
**Reasons to abandon Windows/Office:**
Windows → 1,300+ CVEs per year + Copilot integration = the OS itself is the attack surface
Office → Opening a file triggers attacks + Copilot sends all documents to external AI
Tight coupling → Windows + Entra ID + M365 + Azure = one breach collapses all
Legacy → Decades of backward compatibility = attack surface too large even for Mythos to fully patch
**Will you continue depending on Microsoft — the slowest to patch among the 12 — for your security?**
:::

### Abandoning Office = Building Your Own Apps

Here is the crucial reality. Abandoning Office does not mean "switching to another off-the-shelf product." It means **building your own apps.**

Switching to LibreOffice is simply moving your dependency to another black box. A massive codebase, opaque internals, unpatchable vulnerabilities — repeating the same structure as Microsoft, just in a different place.

**True post-Microsoft means building the functionality you need, yourself, with AI.**

And with Claude Code, this is now a realistic option.

:::compare
| Office function | Microsoft dependency | Built by you + AI |
| --- | --- | --- |
| Documents | Word + Copilot (via external AI) | Markdown + Claude Code → HTML/PDF generation |
| Spreadsheets | Excel + Copilot (opening a file triggers attack) | Python + pandas + Claude Code → your own analysis tools |
| Presentations | PowerPoint + Copilot (all slides sent externally) | HTML + CSS + Claude Code → your own slides |
| Email | Outlook (preview pane triggers attack) | Self-hosted server + simple client |
| Database | Access / SharePoint | SQLite + Python + Claude Code |
| Attack surface | **Enormous. Cannot fix yourself** | **Self-built. Fully understood. Instantly fixable** |
:::

aiseed.dev is the proof. 42 HTML pages, 26 articles, a build system, SEO optimization — all built with Markdown, Python, and Claude Code. No Word. No PowerPoint. No Excel.

**The functionality you need can now be built by you + AI.**

It was once common sense that "you can't work without Office." You couldn't build systems without paying SIers millions of yen. But with Claude Code writing 70–90% of code, that conventional wisdom has collapsed.

:::chain
**Escaping Office dependency:**
"Can't write documents without Word" → Write with Markdown + Claude Code
"Can't analyze data without Excel" → Do it with Python + Claude Code
"Can't present without PowerPoint" → Build it with HTML + Claude Code
"Can't read email without Outlook" → Run your own server
**Every "can't do without X" is solvable with Claude Code**
→ And not as a black box, but as a system where you understand what it does
:::

What becomes visible here is that **when Office disappears, so does the job of "operating Office."**

The majority of today's office work is Office operation. Creating reports in Excel. Making presentations in PowerPoint. Writing meeting notes in Word. Organizing email in Outlook. These are not "work" — they are "tool operation." When Office is no longer the premise, these tasks themselves become unnecessary.

But creating reports, presentations, and emails does not become unnecessary. It becomes something you **create by instructing Claude.** "Analyze this sales data and compile a report." "Create a presentation from this week's meeting content." "Write an email to the client about this matter." — the human communicates the intent, AI gives it form.

This is not a job to hand off to AI agents. Letting AI agents autonomously handle tasks in production is expanding the attack surface. Instead, the human gives instructions to Claude, reviews the result, and makes the judgment. **It is the same structure as development.**

And tasks that require no judgment do not need humans at all. Just turn them into code. Monthly sales aggregation, reports in fixed formats, periodic data backups — any task where no judgment is involved can be automated by writing a script with Claude Code. Humans only do work that requires judgment.

**This means the value of desk work drops to zero.** Instruct Claude to create reports, presentations, and emails, and any task that can be done as desk work is finished in an instant. Work that took 8 hours — building reports in Excel, polishing slides in PowerPoint, writing meeting notes in Word — is completed with a single instruction to Claude.

But what disappears is "Office operation," not desk work as a whole. Desk work that requires judgment remains. Executive decisions, negotiations, strategic planning, personnel evaluation, customer policy decisions — these can only be done by humans. Real-world jobs also remain in abundance: agriculture, manufacturing, construction, healthcare, caregiving, customer service, logistics. What disappears is only the part where "operating a tool was the job."

And what disappears completely is **outsourced desk work.** In Japan, temporary staffing and outsourcing have been expanding since the 1990s. Creating reports, data entry, organizing documents, accounting tasks — the structure of delegating these to temporary workers and outsourcing firms has taken root over more than 30 years. But there is no reason to outsource work that finishes in an instant with a single instruction to Claude. A structure that took 30 years to build becomes unnecessary with AI. The same structure as the collapse of SIer dependency in software development.

This may look like a high bar. But consider — aiseed.dev was built in 24 hours. Zero lines of human-written code. All you need is the ability to decide what to build.

**Building your own apps is easy.** Claude Code writes the code. Once Mythos is released, you can security-check your own apps yourself. Build → check → fix — this entire cycle is completed by you + AI. No external security audits. No SIer engagements. No waiting for vendor patches.

This is already happening. Anthropic's Claude Desktop has no official Linux version — only macOS and Windows. But on GitHub, multiple projects have already made it work on Linux. [claude-desktop-debian](https://github.com/aaddrick/claude-desktop-debian) is community-driven with 3,100 stars and 548 commits. [claude-desktop-bin](https://github.com/patrickjaja/claude-desktop-bin) is one developer who has added Computer Use, Cowork, and Dispatch support. If the vendor won't support it, build it yourself. **Not "I can't use it because there's no official version" but "there's no official version, so I'll build it myself"** — this is software development independence.

:::highlight
**Massive software is unnecessary:**
Office has thousands of features. But you use less than 5% of them. Build only the features you need, with you + AI. Lightweight, transparent tools where you understand what they do.
Windows is the same. It holds 72% market share — and 72% of the attack surface. All you need is Linux and the applications you actually use.
Legacy software should be rebuilt too. Instead of maintaining ancient systems, rebuild them with Claude Code. In 24 hours, you can reconstruct with a new architecture.
Process locally as much as possible. If you don't depend on external services, data cannot leak. If you don't send to the cloud, it cannot be intercepted. Local processing = minimal attack surface = simpler systems.
**If you have the will, you can do it. Claude Code has removed the technical barriers. All that remains is the decision to act.**
:::

Abandoning Microsoft does not mean finding a replacement for Microsoft. **It means having the capability to build what you need, yourself.** That is the essence of software development independence.

:::compare
| | Microsoft dependency | Post-Microsoft |
| --- | --- | --- |
| OS | Windows (Copilot integrated, 1,300+ CVEs/year) | Linux (open source, auditable, no Copilot) |
| Documents/Analysis/Presentations | M365 + Copilot (all documents via external AI) | **Build the tools you need with Claude Code** |
| Email | Outlook (preview pane triggers attack) | Self-hosted server |
| Auth | Entra ID (the hub of tight coupling) | Self-managed auth / passkeys |
| Development | VS Code + Copilot (code sent externally) | Claude Code (dev only. No AI in production) |
| Attack surface | **Enormous. Too large even for Mythos to fully patch** | **Minimal. Everything under your control** |
:::

Abandoning Windows/Office is a major decision. The resistance to leaving a familiar environment is strong. But the question is not "is it familiar" — it is "can you survive the Mythos era."

Will you entrust your security to Microsoft — the most problematic among Glasswing's 12 — or take back control with Linux + Claude Code?

**Convenience → dependency → monopoly → tight coupling → collapse. If you're going to escape this structure, now is the time.**

## Mythos Will Be Released in the Near Future

Mythos will not remain sealed forever.

Anthropic's decision not to release it publicly is "a choice to buy time." As history shows, technologies deemed too powerful are initially restricted, then eventually released. Nuclear technology remains strictly controlled. Strong cryptography was released to the public. Which path will AI follow? Most likely, the path of cryptography.

The reason is clear. **Once Glasswing's 12 companies finish patching, there is no reason to keep it sealed.**

:::chain
**The structure leading to Mythos release:**
Glasswing's 12 companies scan their systems with Mythos
→ Thousands of zero-day vulnerabilities are patched
→ But Microsoft alone is anomalous — patching while expanding the attack surface with Copilot
→ The Windows/Office legacy codebase is the world's largest. Patching takes the longest
→ Glasswing completion depends on Microsoft's progress
→ Still, once core infrastructure is secure, the reason to keep Mythos sealed disappears
→ For Anthropic, release = revenue (Claude Code is $1B/year. Mythos is the tier above)
→ For the industry, release = stronger collective defense
→ Competitors (OpenAI, Google DeepMind) are also closing in
→ **Glasswing patching complete = green light for Mythos release. The bottleneck is Microsoft**
:::

In other words, the Mythos seal is not a "permanent lock" — it is a "grace period until the 12 companies finish patching." After Glasswing participants have secured their systems, Mythos will be released to the public. At that moment, every organization that has not finished patching becomes a target.

Claude Opus 4.6 already generates 70–90% of code and drives $1 billion in annual revenue. Mythos is the next stage. Not just writing code, but finding vulnerabilities in existing code and auto-generating exploit code. Given the timeline for Glasswing patching to complete, general availability should be expected between late 2026 and early 2027.

**That means the preparation window is six months to one year.**

## Practice: 5 Principles for Development Independence

:::highlight
**Principle 1: Use AI for development. Never embed AI in production.**
Generate code with Claude Code. Review. Build. Serve only static HTML.
AI exists only in the development process. No AI in production.
:::

:::highlight
**Principle 2: Do not use a CMS.**
WordPress powers 43% of the world's websites. 11,334 vulnerabilities in 2025 alone. 97% from third-party plugins. For a Mythos-class attacker, this is a treasure trove.
Markdown and a Python build tool are sufficient.
:::

:::highlight
**Principle 3: Do not place a database in production.**
No database means no SQL injection target.
If the production environment needs no dynamic processing, no database is needed.
:::

:::highlight
**Principle 4: Own your server.**
Depending on AWS or Azure just changes the object of dependency.
A simple Linux machine, Nginx, static files. That is enough.
One server, one application. Physically and logically loosely coupled.
:::

:::highlight
**Principle 5: Eliminate black boxes.**
A system you don't understand is a system you can't defend.
Understanding does not mean reading every line of code. It means knowing what the system does — where data flows, what gets processed, what communicates externally. Leave the code to AI. Understanding the structure and purpose is the human's job.
Not a black box delivered by an SIer, but a transparent system built by you and AI.
:::

## Independence Is Not Isolation

Development independence does not mean doing everything alone. AI is the ultimate collaborator.

Claude Code writes the code. Claude reviews the architecture. Claude checks for vulnerabilities. The human's job is to decide what to build, instruct the AI, and judge the results.

:::chain
**The structure of independence:**
Human → Decides what to build → Instructs AI
AI → Generates code → Tests → Iterates
Human → Verifies what the system does → Deploys
**The human doesn't write code. Doesn't need to read code. But understands what the system does and controls everything.**
:::

When software development is handled by AI, it means **humans can focus their time and energy on real-world work.**

Growing crops. Making products. Running services that require face-to-face interaction. These are things AI cannot do. Touching soil, reading weather, judging quality, talking to customers — real-world work requires human bodies and human judgment.

Leave software to AI. The tools you need can be built in 24 hours. Security checks are done by AI too. **That is precisely why humans can focus on truly valuable work — creating things in the real world.**

This is the true meaning of software development independence. Not being chained to software. Using software as a tool and returning to your real work.

As the transcript states — "The boundary between what AI can and cannot do is constantly shifting. But those who can answer the fundamental question of *why* a human does that work will not lose their purpose, even as the boundary moves."

Software development independence is not about writing code. **It is about deciding what to build, designing the structure, co-developing with AI, and taking responsibility for the result.**

## Preparing for Mythos Release — What to Do Now

The moment Mythos is released, two things happen simultaneously:

1. **Defenders can scan their own systems with Mythos**
2. **Attackers begin scanning targets with Mythos**

The time gap between discovery and patch determines survival. Whether that gap is zero depends on today's preparation.

:::compare
| | Prepared organizations | Unprepared organizations |
| --- | --- | --- |
| Source code | On hand. Fully understood | SIer's black box |
| Structural understanding | Self-designed. Instant judgment | Nobody knows the full picture |
| Vulnerability fixes | Self + AI, immediate | Re-engage SIer → weeks to months |
| Attack surface | Static HTML. Nothing to scan | CMS + DB + API + admin panel + AI agents |
| Survival after Mythos release | **Structurally safe** | **First targets** |
:::

:::highlight
**What you can start today:**
1. Install Linux. Learn to use the terminal. This is the starting point for everything
2. Start practicing development with Claude Code. Build the ability to co-develop with AI
3. Keep your source code on hand. Publish everything on GitHub
4. Understand what your system does. Eliminate black boxes
5. Begin reducing your attack surface. CMS → static HTML, DB → file-based, API → minimal
6. Remove AI agents from production
**When Mythos is released, be ready to run security checks immediately.**
**That requires having the source code and understanding the structure.**
:::

## Surviving Outside Glasswing

Glasswing's 12 companies will use Mythos to defend their systems.

The countless companies, municipalities, and individuals outside that circle must defend themselves. But the best way to "defend" is not buying massive security products.

**It is making the attack surface zero.**

That requires taking software development back into your own hands. Not outsourcing to SIers. Not accepting black boxes. Using AI as a tool to build simple, transparent structures.

Mythos release is near. The preparation window is six months to one year. If you don't start today, it will be too late.

:::quote
Mythos has arrived. Only 12 companies are protected.
The rest must protect themselves.
But if the attack surface is zero, there is nothing to defend.
Use AI for development. Never embed AI in production.
Keep source code on hand. Understand the structure.
When Mythos is released, be ready to act immediately.
The preparation window is six months to one year. Start today.
:::

---

Comments and discussion on Facebook: [AISeed — 生物多様性・食料・AIと暮らし](https://www.facebook.com/groups/vegitage)
