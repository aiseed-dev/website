---
slug: cloud-independence
number: "04"
lang: en
title: Independence from the Cloud — AI Supports Only the Open Layers
subtitle: Vendor-specific management and identity layers sit beyond AI's reach. Standardized Linux environments sit within it. That asymmetry makes infrastructure independence possible.
description: Part of the public cloud's value proposition is being undermined by AI — not because cloud technology declined, but because vendor-specific management layers (proprietary consoles, APIs, identity foundations) sit outside AI's strong domain of "closed problems with stable specifications." The environments that receive the most AI support are VPS and local machines, standardized down to the provisioning layer. Practical choices for small operations, the structural problem of Entra ID, and the different exposures of AWS, Google, and Azure — organized not as "the fall of the cloud" but as "infrastructure independence."
date: 2026.07.04
label: Structural Analysis 4
part_title: Design and Practice
part: "3"
prev_slug: security-design
prev_title: Security Design for the Mythos Era
next_slug: nativism-observation
next_title: "Nativism and Observation — The Isomorphism of AI and Agriculture"
cta_label: Own It
cta_title: Rent the window. Keep the keys and the management in your own hands.
cta_text: Standardized resources can be rented. The moment you deposit them into a vendor-specific management and identity layer, you live where AI's support cannot reach.
cta_btn1_text: "Next: Nativism and Observation"
cta_btn1_link: /en/insights/nativism-observation/
cta_btn2_text: "Previous: Security Design for the Mythos Era"
cta_btn2_link: /en/insights/security-design/
---

## The Conclusion — Infrastructure Can Now Be Independent Too

[Part 2, Chapter 7](/en/insights/builder-emergence/) showed individuals
migrating to the free city (Linux + Python + AI) and standing as builders.
This chapter of the design part treats the ground under their feet —
**where to place infrastructure, what to rent, and what never to deposit.**

The conclusion first. Part of the public cloud's value proposition is being
undermined by AI. The cause is not a decline in cloud technology. It is that
**the vendor-specific management layer (proprietary consoles, proprietary
APIs, proprietary identity foundations) sits outside AI's strong domain —
"closed problems with stable specifications."**

The standardized parts — compute and storage — remain. The vendor-specific
management, identity, and operations layers are the parts that get replaced.
And this asymmetry carries one consequence for individuals and small
organizations: **infrastructure can now be independent.** The premise of the
old judgment — "we have no experts, so leave it to the cloud" — has
inverted.

## The Asymmetry of AI's Uplift — Linux vs. the Vendor Console

The more public knowledge a technology has, and the more stable its
specifications, the more AI raises a practitioner's implementation level.
This principle is the operational version of the "open accumulation" of
[Part 2, Chapter 4](/en/insights/two-layer-ai-revolution/), and the same
structure as the Oracle-tax argument of
[Part 1, Chapter 8](/en/insights/enterprise-tax/) (the PL/SQL vs. PostgreSQL
comparison) — and it applies directly to the infrastructure layer.

Linux operations (systemd, Caddy, PostgreSQL, Docker, and the rest) rest on
decades of accumulated public information; command and configuration syntax
is essentially stable. Error messages and log formats are standardized, so
AI locates causes easily.

Cloud vendors' management consoles and CLIs, by contrast, routinely change
menu layouts and API versions on a scale of months. For the same task —
"stand up a virtual machine" — console button placement and CLI options
differ by version. Vendor-specific concepts (Azure resource groups, Entra ID
tenants) accumulate poorly as general knowledge.

:::highlight
**The support-quality asymmetry:**
Linux operations → rich public knowledge, stable specs → **high-quality AI support**
Vendor-specific consoles → closed knowledge, fluid specs → **comparatively poor AI support**
The advantage the cloud held before AI — "anyone can operate it from the
management screen, no expertise required" — is being **inverted.**
:::

## What to Become Independent From — Lock-in Lives in the Management Layer

Cloud vendor lock-in, like Oracle's, has been sustained by the height of
migration costs. But its substance is concentrated not in the standardized
compute and storage but in **the vendor-specific management and
authentication layers.**

Take Microsoft Azure. Virtual machines and storage themselves can be built
from standard Linux technology, but access control (RBAC) and resource
management bind to Entra ID. Entra ID is an authentication foundation
designed around deep integration with Microsoft 365 and Copilot — carrying
the structural problem seen in
[Part 1, Chapter 12](/en/insights/lord-class-collapse/): it produces value
only when embedded.

The vulnerability of this class of authentication foundation follows a
published timeline: warned about internally by an engineer in 2016, deferred;
actually exploited in the 2020 SolarWinds attack; and in 2024 the US Cyber
Safety Review Board (CSRB) concluded that Microsoft's corporate culture
"deprioritized security investment."

:::chain
**Building the upper floors before the foundation — an error of sequence:**
2016 → the vulnerability in ADFS (the AD-federation ancestor of Entra ID) is flagged internally
→ response deferred; the integration ("embed everywhere") strategy accelerates
→ 2020 → actually exploited in the SolarWinds attack
→ 2024 → the CSRB report: a culture that "deprioritized security investment"
→ the after-the-fact Secure Future Initiative
→ **the deeper the integration, the more dependence is stacked on a known weakness**
:::

In housing terms: a multi-story structure (Copilot integrated into every
product) was stacked on top before the foundation (the robustness of the
authentication base) was set. Whether to deposit the keys of your own
infrastructure into this foundation — the question of independence starts
here.

## What Remains, and What to Rent

The resources themselves — compute and storage — look standardized, but
**the method of acquiring and managing those resources (provisioning APIs,
management consoles) is vendor-specific.** What AI is good at is not that
layer, but operating the standard Linux technology (systemd, Docker,
standard SQL) after acquisition.

So the estimate "the compute-provision part will remain" needs a correction.
Even if the resource itself is standardized, as long as the path to it — the
provisioning layer (VM creation, network configuration, permission grants) —
is vendor-specific, AI's support reaches it poorly. This layer carries the
same structural weakness as an authentication layer like Entra ID.

:::highlight
**The environments that receive the most AI support:**
Environments standardized down to the provisioning layer.
Forms like a **VPS (virtual private server)** — where a nearly standard
Linux environment is handed over as-is after signup — and **self-owned local
machines** hold the advantage here.
Whatever depends on a hyperscaler's proprietary provisioning APIs and
consoles should be treated as **part of the lock-in**, even when it is
resource provision.
:::

## The Practical Choice for Small Operations

For small operations — informational sites, community applications — this
structure translates directly into choices. If the load fits on one to a few
VPS instances, there is little reason to assume hyperscaler-specific
features (autoscaling, managed identity foundations) in the first place.

- For short-term or event-driven load spikes, a domestic cloud (Sakura Cloud
  and the like) handles it fine
- For steady load, a local machine (home or office) works — and stands
  independent of external cloud-failure risk
- In either case, authentication can be completed with a self-hosted
  identity foundation built on standard protocols like OIDC (PocketBase,
  Keycloak) — avoiding dependence on vendor-specific identity

This is the implementation of **independence**. It does not mean building
everything yourself. **Keep the keys (authentication) and the management in
your own hands, and rent what you rent in standard form** — rent the window,
keep the safe on your side. The full procedure for doing this across an
organization's entire suite is covered by the independence part of
[AI-Native Ways of Working — Software](/en/ai-native-ways/software/).

## Cloud-First Was a "Re-labeling of the Legacy"

Why could the cloud — Azure above all — grow this far? It did not create a
new market from zero. **It stood on existing assets.**

- Enterprise customers already on Windows Server, SQL Server, and Active
  Directory migrated as-is to the cloud versions (Azure VM, Azure SQL,
  Entra ID)
- Decades of relationships with corporate IT staff, procurement contracts,
  and license structures carried over unchanged
- The existing lock-in was simply re-labeled from "on-premises billing" to
  "cloud billing," so the customer's decision cost was near zero

Cloud-first, in substance, was not a new business but **a high-margin
remodeling of existing assets.**

There is a control experiment: **mobile-first lost because there was no
legacy.** Windows Phone had none of the accumulated enterprise legacy — app
assets, developer community, user habit — and had to fight the network
effects Apple and Google already held, from zero. In territory where the
legacy could not be re-labeled, Microsoft's essential strength (existing
customer lock-in) did not function at all.

:::highlight
**Success and failure explained by one principle:**
Cloud-first's success = the **re-labeling of legacy (lock-in)** worked
Mobile-first's failure = there was no legacy to re-label
And now the base of that success — the legacy lock-in itself — is, per the
general law of [Part 1, Chapter 7](/en/insights/nvidia/) (every lock-in was
protected by "nobody can read the closed asset"), **beginning to melt under
AI.**
:::

## The Three Companies Differ — If You Rent, What and How

The same "cloud" faces this structural risk differently at AWS, Google
Cloud, and Azure.

**AWS** has the character of a base widely used by outside businesses and AI
developers. Full-year 2025 revenue was $128.7B (+19% YoY), the largest of the three;
Bedrock carries models from multiple AI labs. Organizations already deep in
the AWS ecosystem (IAM, VPC) find AI adoption low-friction. Its in-house AI
chip (Trainium) is grown with external provision in mind. With a widely
distributed customer base, its dependence on any single lock-in structure is
comparatively thin.

**Google** weights internal use heavily. Google Cloud's standalone revenue
(about $59B for full-year 2025; an annualized run rate above $70B at
year-end) is growing, but against Alphabet's overall AI and data-center
investment ($91B actual in 2025, a 2026 plan doubled to $180–190B, and 2027
guided to increase significantly again), a substantial share of that
investment plausibly serves Search, YouTube, and Gemini itself. Its reliance on external cloud customers is lower than AWS's.

**Azure** depends most, among the three, on enterprise lock-in through deep
integration. Its revenue was disclosed for the first time in FY2025 (ended
June 2025): **over $75B** (+34% YoY). Its strategy foregrounds integration with Entra ID, Microsoft
365, and Copilot — pressing proprietary management and identity dependence
on customers hardest. That is why it stands most directly exposed to the
substitution pressure of AI solving "closed problems with stable
specifications."

:::compare
| | Structural character | Exposure to AI substitution pressure |
| --- | --- | --- |
| AWS | high customer diversity and dispersion | comparatively thin |
| Google | low dependence on external customers (the core is Search, YouTube, Gemini) | limited impact on the parent even if cloud struggles |
| Azure | deep-integration lock-in is the revenue pillar | **carries it most directly** |
:::

From the standpoint of independence: what may be rented is the part whose
character is "standard resources handed over in standard form"; what must
not be deposited is the part premised on "deep integration."

## Summary — What Falls Is the Closed Layer; Independence Stands on the Open One

The concept of the cloud itself is not ending. The part that provides
standardized technology (Linux, containers, standard SQL,
standard-protocol authentication) in standard form will remain. What gets
undermined is **the part whose very method of provision is vendor-specific
and therefore hard for AI to support.** That extends beyond the
authentication and management layers to compute provisioning itself. This
enclosure is fragile against the speed at which AI solves "closed problems
with stable specifications" — the same structural risk as Oracle DB's PL/SQL
lock-in.

:::quote
AI's support gathers on the open layers.
It does not reach vendor-specific management and identity layers.
"No experts in-house, so leave it to the cloud" — that premise has inverted.
Keep the keys and the management at hand; rent what you rent in standard form.
Infrastructure independence does not mean building everything yourself.
**It means living where AI's support can reach.**
:::
