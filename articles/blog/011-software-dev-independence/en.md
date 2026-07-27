---
slug: software-dev-independence
title: Desk Work and System Design in the AI Era — Claude Mythos and Gemma 4
subtitle: Half a year to a year until Mythos goes public. The response is urgent — build your own scan-and-patch environment now.
description: In April 2026, Claude Mythos and Gemma 4 arrived. Half a year to a year until Mythos is released publicly. The moment it is, attackers gain the same capability. Windows/Office dependency, internal-system black boxes, CMS — the response is urgent. Start today or it's too late.
date: 2026.04.13
lang: en
label: Blog
category: Structural Analysis Notes
hero_image: IMG_3415.jpg
---

# Desk Work and System Design in the AI Era — Claude Mythos and Gemma 4

## April 2026: The Tools Have Arrived

In April 2026, two breakthrough tools arrived.

On April 7, 2026 (US time), Anthropic announced the restricted preview of its latest model, Claude Mythos Preview, through Project Glasswing. This release was unique in the history of AI. The official announcement was backed by the following facts.

* **Withheld from general release:** As a byproduct of its general reasoning and coding ability, Mythos exhibited an "emergent" capacity to autonomously discover and chain together unknown zero-day vulnerabilities in the Linux kernel and major operating systems and browsers — on the order of thousands.
* **Why access was limited:** The potential damage if the capability were used by malicious actors (economic, public safety, national security) was judged catastrophic, and general release was canceled.
* **Formation of Glasswing:** In its place, the project launched in partnership with more than ten initial partner companies — AWS, Google, Microsoft, Apple, CrowdStrike, and others — providing access strictly limited to "defensive security work (vulnerability discovery and remediation)."

Gemma 4 is a high-efficiency, high-performance model that Google released as fully open source (Apache 2.0 license) on April 2, 2026, just before Mythos. Its essence is that top-tier reasoning capability is now available in an offline environment on your own machine.

* Complete confidentiality (zero-leak): because it never communicates with an external cloud, personal information, undisclosed financial data, and government-confidential information can all be processed safely.

* Overwhelming speed and lightness: designs that minimize memory use (MoE architecture and similar) let it complete text parsing and code verification instantly on a local PC.

* CLI-centric practicality: it rejects black-box agents and functions perfectly as a part of a "pipeline (Unix-style approach)" — text is piped directly through the terminal.


## Urgent Warning for the Mythos Era — Break Dependency Now

A decisive event made the seriousness of the situation clear. On the same day Project Glasswing was announced, leaders of the US Treasury and the Federal Reserve convened the top executives of Wall Street's largest banks at Treasury headquarters in Washington and directly warned them about the catastrophic cybersecurity risks that Anthropic's Claude Mythos Preview could create.

Anthropic's measure restricting Mythos to 12 initial partners and over 40 infrastructure organizations is only a temporary breakwater. Once the selected infrastructure set completes its vulnerability remediation, Mythos will inevitably be released publicly. At that moment, both defenders and attackers gain exactly the same capability. For organizations outside Glasswing, the grace period before systems begin to fall — the countdown — is only half a year to a year.

The most fatal risk in this countdown is dependency on systems carrying decades of legacy code, like Windows and Office. These are internal black boxes, and once Mythos begins scanning, the volume of vulnerabilities to fix will be too large to patch in time for public release. Further, Microsoft's push for "automation via Copilot agents" carries structural defects — vulnerability to prompt injection, loss of data sovereignty — and becomes a massive entryway in the face of Mythos-level attack capability.

In other words, continuing to entrust your organization's security to a giant vendor's fragile ecosystem means you will be "working on an unpatched attack surface, defenseless" for a long time after public release.


## Concrete Steps and Environment Migration for the Mythos Era

For organizations outside Glasswing's protection, the public release of Mythos is an imminent threat. The moment it goes public, you must already have an environment in which you can scan your own systems and fix vulnerabilities immediately. Mythos-level code analysis and defense capability already surpasses human security specialists, so outsourcing this work to an external vendor is a fatal delay. With the current Claude (Opus 4.6, Sonnet 4.6, etc.), building this defensive environment yourself is by no means difficult. Below are the migration processes to begin immediately for each of three domains.

### Local PC: Return to Text, Leave Office

The current office environment is dominated by the "black box" of Windows and Office products. Binary files like Excel and Word cannot be diffed with Git, so the history of "who changed what, when, and why" exists only in people's heads. On top of that, non-creative manual work — adjusting formulas and macros — consumes enormous amounts of time. Even more serious are the zero-day vulnerabilities that trigger merely on opening a file, and the cascading risks inherent to the tightly coupled Windows + Entra ID + Azure ecosystem. With Copilot integrated on top, the attack surface has expanded to an unprecedented scale.

The best way out of this crisis is to move the desktop environment from Windows to Linux. Convert business documents to plain text — Markdown, CSV, JSON — and put everything under Git, enforcing "Doc as Code." For existing Excel workflows, observe the procedure, extract the logic, and have Claude rewrite it into code such as Python. Routine processing that includes confidential information should not be handed to a resident Copilot; run the local Gemma 4 as a CLI, one-shot per invocation, to complete the work.

### Internal Systems: End SI-Vendor Dependency, Achieve Deterministic Independence

Many internal systems (legacy ERP, Access, on-premise apps) have become black boxes delivered by SI vendors, with no one understanding what's inside. No internal staff can explain the structure, and when a vulnerability is found, it takes weeks to months to re-engage the vendor and apply a fix. External API integrations and VPN access paths also remain, and the assumption that "it's safe because it's on the intranet" has already collapsed — VPN appliances themselves become attack targets, and intrusion through them will accelerate after Mythos goes public. Also, the recent trend of embedding AI agents inside internal systems under the banner of "efficiency" is a foolish move that only multiplies external attack paths (prompt injection, etc.).

What is required is to break dependency on SI vendors and rebuild the systems yourself, openly, through dialogue with Claude. With AI support, even legacy systems can be replaced with modern code in a short time. Automate only "deterministic logic that a human has approved (Python, SQL, shell scripts)"; do not let AI agents reside inside systems and make autonomous judgments. Manage data simply in local SQLite and keep dependence on any central database to a minimum. Keep the source code under Git locally and keep understanding of the structure in your own hands — then, even if Mythos uncovers an unknown vulnerability, you can apply the patch yourself immediately. Design the intranet with the same defensive assumptions as a public-facing system.

### Public Systems: Eliminate the Attack Surface Through Static Sites

The single largest vulnerability on the web is the existence of CMSs like WordPress and the databases attached to them. Plugin vulnerabilities and unauthenticated exploit paths never stop appearing, and even with a WAF (Web Application Firewall) deployed, the majority of sophisticated attacks pass right through. The recent fashion of integrating AI chatbots and AI search into public systems only adds more attack targets.

The only correct answer is to "physically reduce the attack surface to zero." Completely discard CMSs and dynamic databases from production, and serve only "static HTML" generated by Markdown and a build tool. Keep the server configuration as simple as possible — Linux + Nginx + static files — with "one app per server" as a strict rule of loose coupling. Naturally, remove AI integrations from production entirely. The strongest defense in the coming era is to create a state in which, even when Mythos scans it, "no dynamic element is found to attack."

For the parts that must receive information — order and inquiry processing systems — the following design is the optimal solution.

**1. Design it as a "one-way valve (Write-Only API)"**

Do not colocate the order and inquiry processing system with the website (static HTML). Stand up a small, independent API server dedicated solely to input processing.

- Static site side: place a form inside the HTML. When the submit button is pressed, use JavaScript's `fetch` or similar to "throw" the JSON data at an API on a different domain (or subdomain / different port) — nothing more.
- API server side (receiving): run a minimal application written in Python (FastAPI etc.) on an independent Linux server. This server is specialized to a **single function (one app): "receive JSON of a specified format, write it to local SQLite or similar, and return 200 OK."**

**2. Enforce deterministic validation**

This receiving API becomes the attack target, but its attack surface is on an entirely different order of magnitude from a CMS.

- Strict input limits: validate the type and length of the incoming data (name, email address, order content, etc.) precisely with Python code (Pydantic etc.). Unexpected characters and oversized payloads are immediately discarded at the gate (HTTP 4xx errors).
- Do not expose reads from the DB externally: this API server can be "written to" from outside, but it has zero capability to "look up database contents and return them" in response to external requests. This cuts SQL injection and data-leak risk off at the root.

**3. Asynchronous processing and connection to local AI (Gemma 4)**

The received data should not be left for long on the web-facing server.

- After orders and inquiries accumulate in SQLite, periodically pull the data from a safe internal network (or an offline local PC).
- Pass the pulled data to Gemma 4 (CLI) in the internal local environment and have it perform tasks like "spam classification," "summarizing the inquiry content," and "converting order data into the core-system format (CSV, etc.)."

## Principles for Using AI in Business

The core of AI use in business is preventing "the abdication of responsibility under the name of efficiency."

**Principle 1: Completely exclude autonomous agents (the non-autonomy principle)**

In business, you must never grant AI the power to "judge on its own and operate systems on its own" (the autonomous agent function). AI's role is strictly limited to "translation and visualization" — organizing messy data, drafting code, and so on. The final execution functions — writing data, sending it externally, changing the system — must be physically isolated from AI's reach.

**Principle 2: Localize responsibility, keep human primacy absolute (the decision principle)**

Leaving the flow of work to an autonomous AI turns accountability into a black box and collapses organizational governance. AI is at best a machine that produces "highly plausible predictions" — it cannot make "decisions" that carry business risk or ethics. By always interposing a process in which a human reviews the AI's draft or analysis and "approves it by their own will (pressing Enter, etc.)," the final accountability for the work stays 100% in human hands.

**Principle 3: Reject black boxes and defend (the vulnerability-exclusion principle)**

The invisible reasoning loops repeated inside autonomous AIs, and the tight coupling with massive external ecosystems like Copilot, bring uncontrollable vulnerabilities into the system (prompt injection, data leakage). To prevent this, AI use must be limited to "pipelines where input and output are fully traceable (CLIs, etc.)." AI output must always be emitted as plain text (Markdown or source code), and its change history must be physically recorded in Git or similar, so humans can always audit and correct it.

**Principle 4: Return to deterministic automation (the execution principle)**

AI should intervene only in the phase that translates a human's "ambiguous intent" into logic. Once a human has approved a procedure as the "correct answer," it is immediately separated from the AI and fixed as "deterministic code (Python, SQL, etc.)" with 100% reproducibility. Once fixed, routine processing leaves no room for AI (probability) to enter; it is operated as clean, machine-level automation.

## Prepare for the Mythos Release — Start Today

Half a year to a year until public release. **Start today or you won't make it.**

Recover the spirit of the builder — who thinks for themselves, writes their own code, and makes their own decisions. It is fine for AI to write the code. What matters is taking responsibility for the result.

Start by using a Linux PC.

---

Join the discussion in the Facebook group: [AISeed — Biodiversity, Food, and Life with AI](https://www.facebook.com/groups/vegitage)
