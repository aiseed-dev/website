---
slug: end-of-us-ai-hegemony
title: "The Beginning of the End of American AI Hegemony — The Supreme Court Ruling and Five Layers of Structural US-Dependence Risk"
subtitle: "Legal foundation, oversight, technical base, supply, talent — one administration's decisions degraded five layers at once"
date: 2026.07.04
description: Starting from the US Supreme Court's June 29, 2026 ruling in Trump v. Slaughter, the structural risk of depending on US technology infrastructure surfaced across five distinct layers at once — the loss of FTC independence shaking the DPF, a dormant CSRB, the structural problems of Entra ID, VBA, and Copilot, the precedent of the Fable 5 export halt, and an 80% drop in AI researchers moving to the US. The conclusion is neither anti-American nor anti-vendor — a structure that entrusts your data, authentication, and operations to the policy decisions of one country or one company carries uncontrollable risk by design.
lang: en
label: Blog
category: Structural Analysis Notes
---

# The Beginning of the End of American AI Hegemony

## The Conclusion

Starting from the US Supreme Court's ruling of June 29, 2026 (Trump v.
Slaughter), the structural risk of depending on US technology
infrastructure surfaced simultaneously across five distinct layers: the
legal foundation, the oversight regime, the technical base, the supply
regime, and the talent base. The cause is not the United States as a
country but a series of policy decisions by the current administration.
And yet the very fact that one administration's decisions can reach this
far is what demonstrates the essential risk of concentrated dependence on
a single country or a single company.

And beneath the five layers of individual risk lies one deeper layer:
**uncertainty itself.** An individual risk can be estimated and prepared
for. But what this Court term produced was a 90-year precedent overturned,
a contradictory exception carved out the same day, and unexplained orders
arriving one after another — **no one can any longer predict which premise
falls next.** Measurable risk can be insured. Unmeasurable uncertainty
cannot. The greatest problem of US dependence is not the expected value of
any individual loss, but that **the calculation of expected value itself
no longer holds.**

The direction of response is clear: place data and authentication under
your own organization's control, and minimize dependence on any single
vendor or single country.

## Layer 1: The Legal Foundation — FTC Independence Lost, the DPF Shaken

### Facts

On June 29, 2026, the US Supreme Court held in Trump v. Slaughter
(No. 25-332), by 6 to 3, that the federal statute limiting removal of FTC
(Federal Trade Commission) commissioners to cases of "good cause" violates
the constitutional separation of powers. Explicitly overruling the 1935
Humphrey's Executor decision, the ruling means the president may remove
FTC commissioners without cause.

The decision reached the EU directly. The EU-US Data Privacy Framework
(DPF) is the arrangement that legalizes transfers of personal data from
the EU to the US, and the European Commission's 2023 adequacy decision
cites the FTC as an "independent enforcement authority" 259 times. EU law
(TFEU Article 16(2), Article 8(3) of the Charter of Fundamental Rights)
requires that data protection be supervised by an independent authority —
the loss of FTC independence strikes that premise head-on.

The privacy organization noyb (Max Schrems) sent the European Commission a
letter on June 30, the day after the ruling, demanding an orderly
withdrawal of the DPF adequacy decision, and announced preparations to
bring a case before the Court of Justice of the EU (CJEU). The European
Commission has said it will assess the implications.

After Safe Harbor (invalidated by Schrems I in 2015) and Privacy Shield
(invalidated by Schrems II in 2020), the third framework — the DPF — may
now follow the same path.

### The Precise Current State

As of July 2026 the DPF remains formally valid. The European Commission
has not withdrawn it and the CJEU has not invalidated it. DPF-certified
companies — Microsoft, Google, Apple, and others — continue to operate
lawfully. Based on past cases, a CJEU resolution is expected to take two
to three years.

### Inference

If the DPF is invalidated in the future, the impact will not take the form
of "US companies can no longer do business in the EU." It will appear as:

- Switching costs to the alternative instruments (SCCs: standard
  contractual clauses; BCRs: binding corporate rules)
- But the alternatives may not solve the root problem, because the
  redress body created by executive order (the DPRC) carries the same
  independence defect
- As a result, US operators will be pushed to build EU-contained data
  processing structures — arrangements the US parent cannot access
  technically or legally

The path of impact differs by revenue model. Microsoft's revenue rests on
subscription contracts and deep penetration of the EU public sector, so
its exposure runs through contract reviews — a direct path. Google's core
is advertising, so restrictions on cross-border personal-data processing
would arrive indirectly, as degraded targeting precision.

## Layer 2: The Oversight Regime — CSRB Dormant, CISA Shrinking

### Facts

The CSRB (Cyber Safety Review Board) was established under Executive
Order 14028 (2021) as the investigative body for major cyber incidents. It
holds no regulatory power and is modeled on the accident investigations of
the National Transportation Safety Board (NTSB). It published three
inquiries: the Log4Shell vulnerability (2022), the Microsoft Storm-0558
breach (2023), and LAPSUS$ (2023).

Its Storm-0558 report named Microsoft directly — a "cascade of avoidable
errors" and a corporate culture that "prioritized speed to market and
revenue targets" — as the cause that allowed Chinese state hackers to
breach the email of senior US officials, and it drove the company's
security-strategy overhaul.

On January 20, 2025, the Trump administration terminated the memberships
of all advisory committees under DHS, effective immediately. The CSRB was
at that moment investigating the breach of nine US telecom carriers by the
Chinese state group Salt Typhoon; the investigation was cut off. No new
members have been appointed since, and as of July 2026 the CSRB remains
dormant. The ACM (Association for Computing Machinery) issued a statement
in 2026 demanding its reactivation and a permanent statutory basis.

As for CISA itself, the FY2026 budget proposal announced in May 2025 cut
about $491 million, targeting the disinformation-response and
international-cooperation divisions for elimination. Specialist staff
reductions are underway, and former officials warn of devastating damage
to capability. CISA has, however, continued issuing directives into 2026
(BOD 26-02 and others) — this is not a total shutdown.

### Inference

The only government investigative body with a track record of criticizing
Microsoft by name has now been out of operation for a year and a half. At
present, the United States has no mechanism for independently examining
the security practices of its major vendors.

## Layer 3: The Technical Base — Entra ID's Structural Problem, VBA's Design Problem, Copilot's Embedding

### Facts

Microsoft Entra ID (formerly Azure AD) has had at least three serious
defects confirmed in the past three years.

- **2023, the Storm-0558 incident**: a single stolen MSA (consumer)
  signing key allowed token forgery against enterprise Exchange Online,
  breaching the email of dozens of organizations including the US State
  Department. One cause was a key-separation failure — a consumer key
  passing enterprise-side validation. The CSRB concluded it was a
  "cascade of avoidable errors" and that "Microsoft's security culture
  was inadequate and requires an overhaul."
- **2023–2024, the access-review API vulnerability**: Secureworks CTU
  research showed that unprivileged multi-tenant service principals could
  tamper with access reviews (the permission-audit mechanism) through a
  vulnerable API. Fixed in January 2024.
- **April 2026, the Agent ID Administrator vulnerability**: a role newly
  created for managing AI-agent identities could take ownership of
  arbitrary service principals outside its intended scope and inject
  credentials — a defect that could lead to directory-wide compromise.
  Now fixed.

VBA macros are a design that embeds executable code in Office files, and
they have been abused as a malware delivery channel since the 1990s.
Microsoft moved in 2022 to block macros in files from the internet by
default, but the root design — no separation between document and code
execution — is unchanged, and abuse continues with shifting techniques.

As for Copilot, its embedding into the OS and Office products has
proceeded along this timeline:

- November 2023: Microsoft 365 Copilot general availability. It references
  the organization's email, documents, and chat history via Microsoft
  Graph to generate responses — placing the organization's most sensitive
  data under AI processing.
- 2024: a dedicated Copilot key was added to Windows PC keyboards — the
  first change to the standard key layout in about 30 years, since the
  Windows key (1994).
- May 2024: the Windows Recall feature (continuous screenshotting of the
  screen, made AI-searchable) drew security researchers' criticism for
  inadequate protection of stored data, and was delayed and redesigned —
  opt-in, with strengthened encryption.
- January 2025: Copilot was bundled into consumer Microsoft 365
  Personal/Family plans and prices were raised. Choosing a configuration
  without Copilot required switching to "Classic" plans.
- The AI-agent identity scheme announced in 2025 (Agent ID) has been
  rolling out, and by 2026 AI agents are treated as principals on the
  Entra ID authentication foundation.

### Inference: Entra ID's Problem Is Structural, Not a Series of Implementation Mistakes

The three defects are not independent accidents; they arise from a common
structure.

1. **A single, centralized identity foundation**: authentication for
   organizations worldwide is concentrated on one cloud foundation hosted
   by one company, so a single defect's blast radius reaches every tenant.
   In Storm-0558, one leaked key translated directly into the breach of
   dozens of organizations. Failure domains that were independent per
   organization under on-premises Active Directory now chain across the
   whole, through cloud concentration.
2. **New features stacked on a legacy foundation**: two of the three
   defects (access review, Agent ID) were permission-scope gaps at the
   seam where new permission models were laid over the old
   service-principal foundation. The same class of defect repeats — a
   pattern rooted in development culture. The CSRB's "security culture"
   critique points here.
3. **Unverifiability**: as a closed cloud service, users cannot audit the
   key management or the implementation. The basis of trust is
   Microsoft's internal regime alone — and the only government body that
   judged that regime "inadequate" is, as Layer 2 showed, dormant.

VBA's design philosophy itself is the breeding ground of the
vulnerability, and it cannot be cured while compatibility with existing
macro assets takes priority. Moreover, the VBA assets accumulated inside
companies function as a barrier against migrating away from Microsoft —
security risk and vendor lock-in have become two faces of one thing.

Copilot's problem is not the performance or quality of the AI but the
delivery form — **embedding**.

1. **Inseparability**: Copilot is built into the standard configuration at
   each layer — the OS (keyboard layout, Recall), Office (default
   integration), pricing plans (bundled price hikes) — and the user's
   option to detach just the AI layer is limited. The design decision VBA
   made — no separation of document and code execution — is being repeated
   at the AI layer.
2. **The most sensitive data, permanently connected to cloud AI**: via
   Microsoft Graph, all of the organization's documents, email, and chat
   become AI-processable. This amplifies the Layer 1 DPF risk in the most
   confidential data domain. Unlike storing individual documents in the
   cloud, cross-cutting reference and processing happens by default —
   a qualitative difference.
3. **Expanded attack surface**: AI agents become principals on the
   authentication foundation (Entra ID), and the 2026 Agent ID
   vulnerability arose precisely at that new-on-old seam. Copilot's
   embedding works to enlarge Entra ID's structural problem. In addition,
   prompt injection via external documents adds a new attack class of the
   same shape as VBA macros — "executing instructions mixed into data."
4. **Deepening lock-in**: just as VBA assets have functioned as a
   migration barrier, workflows premised on Copilot will themselves become
   the next barrier once entrenched. And on the Graph-data side there is
   an asymmetric pricing structure. Microsoft Graph Data Connect (the
   service for large-scale extraction of Microsoft 365 data) is metered at
   $0.75 per 1,000 extracted objects, and its output destination is
   restricted to your organization's Azure tenant. The ordinary Graph API
   is unsuitable for large extractions due to throttling, so the practical
   means of pulling your own email, documents, and calendar data in bulk
   converges on Data Connect. Free to put data in, metered to take it out
   at scale, and the exit is Azure-only — the cost of moving data is built
   into the pricing design.

Entra ID, VBA, and Copilot differ in era and technology, but they share
one design decision: **prioritizing convenience and compatibility over the
separation of things that should be separated.** VBA fused documents with
executable code; Entra ID fused every organization's authentication;
Copilot fused business data with cloud AI processing.

The analysis of this "no value unless embedded" structure is developed in
[Structural Analysis Part 1, Chapter 12 "The Lord Class Self-Destructs"](/en/insights/lord-class-collapse/)
and [Part 3, Chapter 4 "Independence from the Cloud"](/en/insights/cloud-independence/).

## Layer 4: The Supply Regime — Export Controls on Anthropic's Models

### Facts

Anthropic's Claude Fable 5 and Claude Mythos 5, released on June 9, 2026,
were suspended on June 12 in response to US Commerce Department export
controls. Commerce lifted the controls on June 30 and access was restored
on July 1. The halt lasted about three weeks. Following the US
government's tightened restrictions on foreigners' access to frontier AI,
allied countries reportedly moved to secure alternatives (Bloomberg,
June 16, 2026).

### Inference

The episode resolved quickly, but it demonstrated that a single US policy
decision can halt the overseas provision of US-origin AI services without
notice. Where the Layer 1 DPF risk for Microsoft and Google is still at
the "could happen" stage, a supply halt in AI is now a precedent that
**actually happened**.

The timeline of the halt and restoration — and what a company should do on
the day access returns — is covered in
[the previous post, "When Fable 5 Returns, Do This First"](/en/blog/verification-shock/),
and in installment 7 of the series "Fable 5 Is Back" (Japanese only).

## Layer 5: The Talent Base — The AI Researcher Exodus from the US

### Facts

According to the annual survey of Stanford University's Institute for
Human-Centered AI (HAI), published in April 2026, the number of AI
researchers and developers moving to the United States fell by about 80%
over the year 2025. Behind it are the Trump administration's visa
restrictions.

In a Nature survey of over 1,600 US researchers, 75% answered that they
were considering leaving the United States (about 79% among postdocs).
Student visa revocations, detentions of researchers, and green-card
denials of prominent AI researchers have been reported one after another.

The receiving side is moving concretely. The EU announced a €500 million,
three-year budget to attract researchers; in Japan, Tohoku University
announced a plan to invest ¥30 billion to hire about 500 researchers from
Japan and abroad. At NeurIPS in December 2025, Chinese AI researchers
returning home from the US were reported.

### Inference

US technological hegemony in AI has depended heavily on foreign-born
researchers (as of 2021, 43% of doctorate-holding scientists and engineers
in the US were foreign-born — NSF). If the 80% drop in inflow persists for
years, the superiority of US-origin technology and services itself erodes.
Unlike Layers 1–4, this is not a "user-side risk" — it is the degradation
of the supplier's own capacity.

## Synthesis: What Five Layers Degrading at Once Means

The five layers arise through different mechanisms: law (a judicial
ruling), administration (executive orders and budgets), technology (design
and implementation), regulation (export controls), and immigration policy.
What they share is that each traces directly or indirectly to decisions of
the US administration — and none can be controlled by the user's own
effort.

The practical conclusion this yields is neither anti-American nor an
attack on any particular company. **A structure that entrusts the
existence of your organization's data, authentication, and operations to
the policy decisions of one country or one company carries uncontrollable
risk by its very design.** This time it was the United States; the same
structure applies to concentrated dependence on any country or any
company.

Moreover, viewing the Supreme Court term that closed in June 2026 as a
whole shows that the problem does not stop at individual rulings (Axios's
term retrospective, July 2026). In the same term, the Court overturned a
90-year precedent (Humphrey's Executor) while carving out an "exception"
for the Federal Reserve that the same logic should have reached — a move
that conservative Justices Thomas and Barrett themselves called an
unprincipled "contradiction." Challenges to vote-diluting maps under the
Voting Rights Act became practically impossible; the withholding of
congressionally appropriated foreign aid was allowed to stand; and orders
keep arriving through the "shadow docket" — fast, unsigned, and often
unexplained. Constitutional scholars describe a court that reaches the
result first and selects the legal philosophy afterward. Even a legal
position considered outlandish a decade ago — denying birthright
citizenship — drew four votes, opening the road for the next "outlandish"
position to become mainstream.

What this state of affairs means is **the loss of legal predictability.**
Risk management presupposes that probabilities can be assigned to risks —
measurable risk can be insured, hedged, and planned around. A state in
which probabilities cannot be assigned — what economics has long
distinguished from risk and called **uncertainty** — admits none of those
instruments. More than any individual event in Layers 1 through 5, **the
fact that no one can predict what happens next, in which layer, is itself
the greatest risk of US dependence.** And the only preparation against the
unpredictable is a structure that makes prediction unnecessary — reducing
the dependence itself. That is the basis of the next section.

## The Direction of Response

1. **Map your data's location and exit cost**: inventory which country's
   and which operator's control your data sits under, and which
   jurisdiction's rules it answers to. Alongside, confirm the means, cost,
   and destination constraints of bulk extraction. When input is free but
   extraction is metered with destination restrictions (Microsoft Graph
   Data Connect and the like), that is a migration barrier by design.
2. **Move to infrastructure under your own control**: put personal and
   confidential data on infrastructure your organization controls
   physically and legally (on-premises, self-hosted). In Germany,
   Bitkom's 2025 survey found 74% of companies strengthening private-cloud
   use — the direction is already the practical mainstream.
3. **Adopt standard technology**: avoid dependence on vendor-proprietary
   technology (VBA, proprietary identity foundations) and compose from OSS
   and standard protocols. Do not create the sources of migration cost in
   the first place.
4. **Bring oversight in-house**: as Layer 2 showed, external (government)
   oversight and investigation can vanish by political decision. Keep the
   basic functions — logging, audit, vulnerability response — inside your
   own organization.

This is not an argument against using US technology and services. It
means: even if you keep using them, build first the structure in which
your organization survives when they stop — or lose their legal basis.
The concrete migration steps are covered by the independence part of
[AI-Native Ways of Working — Software](/en/ai-native-ways/software/), and
the judgment of where to place infrastructure by
[Structural Analysis Part 3, Chapter 4 "Independence from the Cloud"](/en/insights/cloud-independence/).

---

### Timeline of Key Facts

| Date | Event |
|---|---|
| Summer 2023 | Storm-0558. A stolen signing key breaches the email of dozens of organizations, including senior US officials |
| Nov 2023 | Microsoft 365 Copilot general availability |
| Jan 2024 | Entra ID access-review API vulnerability fixed (reported Dec 2023) |
| Apr 2024 | CSRB publishes the Storm-0558 report; finds Microsoft's security culture "inadequate" |
| May 2024 | Windows Recall announced; delayed and redesigned after security criticism |
| Jan 2025 | Copilot bundled into consumer Microsoft 365 with price increases |
| Jan 20, 2025 | All DHS advisory committee memberships terminated (CSRB included); CSRB dormant |
| Mar 2025 | President Trump fires FTC commissioners Slaughter and Bedoya without cause |
| May 2025 | FY2026 budget proposal reveals ~$491M cut to CISA |
| Apr 2026 | Entra ID privilege-escalation vulnerability reported (fixed). Stanford HAI reveals 80% drop in AI researchers moving to the US |
| Jun 9, 2026 | Claude Fable 5 / Mythos 5 released |
| Jun 12, 2026 | Models suspended under Commerce Department export controls |
| Jun 29, 2026 | Supreme Court rules in Trump v. Slaughter; Humphrey's Executor (1935) overruled |
| Jun 30, 2026 | noyb demands DPF withdrawal from the European Commission; Commerce lifts export controls |
| Jul 1, 2026 | Claude Fable 5 / Mythos 5 access restored |
