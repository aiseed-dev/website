# Example 2 — Which Linux Distribution Should You Choose? Verifying Narratives with AI

A walkthrough that applies the practices from Chapter 11, "Verifying Narratives with AI," to a concrete operational scenario many organizations face: **choosing a Linux distribution for server use**.

## What this page demonstrates

"What should we run on our servers?" — this is a question every IT department, every SRE, every startup CTO, and every individual developer has to confront at some point. And **a great deal of narrative gets tangled up in that decision**.

- "**Servers? CentOS, of course.**" — the long-running default
- "**For business systems, RHEL.**" — the comfort of a paid commercial contract
- "**Our standard is Ubuntu.**" — the de facto standard
- "**Debian feels dated.**" — stable, but behind the times
- "**What matters is that it's Linux. The distro doesn't matter.**" — same kernel underneath anyway

Verify all of these together with AI in five steps and a third pattern of governance failure surfaces: **"corporate stewards rewriting their promises midstream."**

It is another failure mode, sitting alongside WordPress (overconcentration on one individual) and Node.js (distributed irresponsibility).

> They look like separate phenomena, but the common thread is **a fragile governance structure**. The surface narrative covers that fragility up. Verify with AI, and the cover comes off.

---

## The surface narratives (the usual reasons given)

Some of the narratives most often heard around server-OS selection:

1. **"CentOS lets you run RHEL for free, so it's safe."** — enterprise quality at zero cost
2. **"Red Hat is the great success story of commercial open source."** — major contributor to OSS too
3. **"Ubuntu is the de facto standard."** — desktops, servers — when in doubt, this
4. **"Debian is dated; this is the Ubuntu era."** — Debian is just too slow
5. **"What matters is Linux. Any distro is fine."** — the kernel is the same anyway

All of them sound reasonable. Let's put them through AI verification.

---

## Step 1: Extract and classify the claims

> Take the Linux-distro-selection narratives above and classify the claims into "objective fact," "evaluation," and "metaphor / rhetoric."

Key results:

| Claim | Classification | Verifiability |
|---|---|---|
| "CentOS lets you run RHEL for free" | Factual claim (true at one point in time) | Verifiable — but watch the time axis |
| "Red Hat is an OSS success story" | Mix of evaluation and fact | Partially verifiable |
| "Ubuntu is the de facto standard" | Evaluation (popularity fact + value judgment) | Partially verifiable |
| "Debian is dated" | Evaluation | Verifiable (release cadence, package count) |
| "Any distro is fine" | Evaluation + factual claim | **Verifiable, and seriously wrong** |

"Same kernel, so it doesn't matter" turns out, on inspection, to be **a fatally wrong claim**. The next step makes that visible.

---

## Step 2: Cross-check the factual claims against primary sources

### CentOS history on a timeline

"CentOS lets you run RHEL for free, so it's safe" — verify on a time axis.

> Lay out the history of CentOS from its founding in 2004 to the present in chronological order. Include the Red Hat acquisition, IBM's acquisition of Red Hat, the switch to CentOS Stream, and the impact.

What Claude lays out (highlights):

- **2004**: CentOS launches as a community rebuild of RHEL — "the same RHEL code, rebuilt for free, fully equivalent."
- **2014**: Red Hat absorbs the CentOS Project (employment relationship). But it is officially promised that "CentOS continues as a free RHEL-compatible distribution."
- **2019**: **IBM acquires Red Hat for roughly $34 billion.**
- **December 8, 2020**: Red Hat suddenly announces — **CentOS 8 support is shortened from 2029 to the end of 2021**. **It ends eight years earlier than promised.**
- "Use CentOS Stream (the unstable upstream of RHEL) instead of CentOS."
- For organizations running CentOS 8 in production all over the world, this was a shock that **forced migration to another distribution within months**.
- **AlmaLinux** (developed by CloudLinux) and **Rocky Linux** (started by CentOS founder Gregory Kurtzer) emerged to fill the gap.
- **June 2023**: Red Hat **restricts public access to RHEL source RPMs** — AlmaLinux and Rocky have to gather sources through alternative channels.

In short:

> The narrative "**CentOS lets you run RHEL for free, so it's safe**" **collapsed entirely as of December 2020.**

What sounded like a promise of "free," "permanent," and "neutral" was **rewritten overnight by the parent company's business decision.**

If someone is still proposing "let's go with CentOS" without knowing this, that narrative is just **dragging a five-year-old story along unchanged.**

### December 8, 2020: what happened on the day of the announcement

Reconstruct the chaos on the **day of** the CentOS 8 EOL announcement, on a timeline, with AI, and the fragility of governance becomes tangible.

> Reconstruct the enterprise community's reaction around Red Hat's December 8, 2020 CentOS 8 EOL announcement, drawing on Hacker News, Reddit, and major blogs.

The flow of major reactions (highlights):

- **Time of announcement (US time, December 8)**: Sudden announcement on the Red Hat blog.
- **Within a few hours**: Reaches the top of Hacker News, thousands of comments.
- **Within 24 hours**: Numerous reports of emergency meetings convened in large enterprise IT departments.
- **Within 48 hours**: Gregory Kurtzer (CentOS founder) announces the **Rocky Linux** project.
- **Within a week**: CloudLinux announces the **AlmaLinux** project.
- **Within a month**: Oracle ramps up a campaign promoting migration to Oracle Linux ("we keep our promises").
- **Within months**: Reports surface of organizations under long-term maintenance contracts considering class action against Red Hat.

> **A live sense of "sudden death of governance"** — this is valuable learning material that AI lets you reconstruct from past events.

### Ubuntu / Canonical's history of unilateral decisions

"Ubuntu is the de facto standard" also needs a different reading on a longer time scale.

> Lay out, on a timeline, Ubuntu's and Canonical Ltd.'s major shifts in direction. Include cases like the Snap mandate, the Amazon Lens controversy, Ubuntu Pro registration requirements, Mir, and the abandonment of Unity.

Claude's summary (highlights):

- **2010**: Introduces the Unity desktop environment (decision to drop GNOME).
- **2012**: The Amazon Lens controversy — desktop search results are sent to Amazon for monetization. Heavy criticism over privacy.
- **2013**: Announces **Mir** (its own display server) — going its own way despite Wayland being the industry standard.
- **2017**: Drops Unity, returns to GNOME — seven years of investment go to waste.
- **2020 onwards**: **Snap packages are mandated** — `apt install firefox` internally calls `snap install`, breaking the meaning of `apt install`.
- **2022 onwards**: **Ubuntu Pro registration requirements** — a growing number of security patches require registration (creating an Ubuntu One account), even for individuals and small users.

> **Ubuntu's direction has shifted significantly many times based on Canonical's business judgment.** What looked like a stable "standard" gets rewritten on a 5-to-10-year cycle.

### Debian's structure, via primary sources

In contrast, look at the organizational structure of **Debian** and you can see a design that is hard to rewrite.

> Lay out Debian's organizational structure, release history, past ownership changes, license, and social contract.

The Debian structure Claude describes:

- **Founded 1993**, by Ian Murdock (the "Deb" in Debian comes from his wife Debra; the "ian" from himself).
- **1997**: Adopts the **Debian Social Contract** and the **Debian Free Software Guidelines (DFSG)**. Constitution-grade public documents.
- **1998**: The **Debian Constitution** is established — decisions made by developer vote, the project leader is elected annually, an independent technical committee.
- **Over 30+ years**: **No owning company. No parent.** Assets are held by the non-profit SPI (Software in the Public Interest).
- Releases happen "when it's ready." Stable approximately every 2–3 years; LTS for 5 years; ELTS extends another 5.
- Many major distros are Debian-based (Ubuntu, Linux Mint, Raspberry Pi OS, Tails, Kali Linux, Devuan, PureOS, Tails).

> Debian is **the rare Linux distribution that has organizationally maintained, since the 1990s, a structure that "cannot be bought by a corporation" and "does not suddenly change direction."**

This contrasts sharply with Ubuntu. Ubuntu is **owned by Canonical Ltd., a private company**, with Mark Shuttleworth as the major shareholder and final decision-maker.

---

## Step 3: Check coherence on a timeline

Lay out Red Hat's official statements on a timeline, and contradictions surface.

> Lay out Red Hat's and IBM's public statements regarding CentOS and RHEL, on a timeline from 2014 to the present. Show where promises and reality diverge.

Highlights:

- **2014 (CentOS absorption)**: Official statements of "we will protect CentOS's independence" and "the free RHEL-compatible distribution will continue."
- **2019 (IBM acquisition)**: The CEO explicitly states that "Red Hat's independence will be preserved" and "IBM will not change the open-source strategy."
- **December 2020**: "CentOS 8 ends at the end of 2021. We are concentrating on CentOS Stream." — inconsistent with prior promises.
- **2021 onwards**: Claims that "CentOS Stream is production-grade" — but in reality it is the upstream (unstable) of RHEL.
- **2023**: Restriction on public RHEL source RPMs. Justified as "legitimate business practice" — many community developers push back.

> **The same organization has unilaterally rewritten its promises on a 5-to-10-year cycle.** This is not "malice" — it is **rational as a business decision** (revenue strengthening after the IBM acquisition). But the user side has to plan on the assumption that "**it could be rewritten again, and you don't know when.**"

### Canonical's statements on a timeline as well

> Lay out Mark Shuttleworth's and Canonical's official statements on Snap strategy, on a timeline from 2018 to the present.

Claude's summary (highlights):

- **2018**: Snap is messaged as "the universal package," "coexisting with Flatpak."
- **2020**: The framing is "Snap is **optional**."
- **Late 2020 onwards**: `apt install firefox` is changed so that **Snap is installed under the hood**.
- **2022 onwards**: The message shifts to "Snap is **the default**."
- **2024**: In response to criticism of the Snap Store's centralization, the framing becomes "**the most secure choice**."

> "Optional" → "default" → "the secure choice" — the official framing of the same technology has gone through **three stages of change in 5–6 years**. From the user's side, this too is an unpredictable change.

---

## Step 4: Cross-check against third-party verifiable records

### The scale of damage from CentOS 8 EOL

Check, against third-party records, **how much damage** this change actually caused.

> Lay out, drawing on reporting, surveys, and community testimony, how much migration cost the December 2020 CentOS 8 EOL announcement imposed on organizations worldwide.

Claude's summary (the major points only):

- Multiple US and European surveys: **10–20% of the world's Linux servers were CentOS-family** `[unverified]`
- From large enterprises down to SMBs, production-system migrations involved **months to a year of effort**.
- Compatibility verification, configuration rewrites, restructuring of maintenance contracts.
- Some organizations migrated to AlmaLinux / Rocky Linux, others to Ubuntu, others to SUSE — **the market fragmented**.
- Many commentators noted that trust in IBM / Red Hat dropped significantly within the enterprise community.
- Cloud providers like AWS, Google Cloud, and Azure rolled out official AlmaLinux / Rocky Linux images one after another.

### How permanent are AlmaLinux / Rocky Linux?

Verify the **long-term durability** of AlmaLinux and Rocky Linux themselves, the alternatives that emerged.

> Lay out the sponsors, funding structure, governance, and history from founding to the present for AlmaLinux and Rocky Linux.

Highlights:

| Item | AlmaLinux | Rocky Linux |
|---|---|---|
| Founded | March 2021 | April 2021 |
| Primary sponsor | CloudLinux | RESF (Rocky Enterprise Software Foundation) |
| Founder | Igor Seletskiy (CloudLinux CEO) | Gregory Kurtzer (CentOS founder) |
| Governance | AlmaLinux OS Foundation (independent) | RESF (Public Benefit Corporation) |
| Response to 2023 Red Hat source restriction | Eased CentOS Stream compatibility somewhat; focus on ABI compatibility | Rebuilt RPMs from UBI containers and public sources |
| Status (2026) | Operating relatively stably | Operating relatively stably |

> That said, **both have a short history (about five years)**, and whether they can withstand structural pressures like Red Hat's source restriction over the long term has not yet been demonstrated. For 20-year planning, the track record is still insufficient.

### Debian's long-term track record and derivative ecosystem

Verifying Debian's **long-term track record** against third-party records, the following becomes visible:

- **30+ years of continuous operation**: Founded in 1993, has continued without an owner change.
- **Number of derivative distributions**: According to Distrowatch, more than 100 distributions are Debian-based.
- **OS share**: In the server space, **Debian alone** (pure Debian, excluding Ubuntu) holds around 10–15% (W3Techs and similar data).
- **Infrastructure**: Debian package archive, bug tracking, social contract, technical committee, universe maintainership — **all functioning on a 30-year horizon**.

These are figures that contrast sharply with CentOS 8's **eight-years-early EOL**.

---

## Step 5: Sort what was learned vs. what is still unclear

| Item | Conclusion |
|---|---|
| CentOS is free and permanent | **A story from the past.** Ended in 2020. |
| Red Hat's neutrality | **Doubtful.** Clear shift toward revenue priority after the IBM acquisition. |
| Ubuntu's neutrality | **Limited.** Depends on Canonical's private corporate decisions. |
| Debian's neutrality | **Structurally protected.** Constitution and social contract. |
| AlmaLinux / Rocky permanence | **Unconfirmed.** Short history; future uncertain under Red Hat's source restriction. |
| Oracle Linux's neutrality | **Caution warranted.** By analogy with Oracle's licensing practices (e.g., Java commercialization). |
| openSUSE's neutrality | **Needs verification.** SUSE has been restructured multiple times under EQT (private equity) ownership. |
| "Any distro is fine" | **False.** Substance differs significantly by governance structure. |

And **what could not yet be verified**:

- AlmaLinux / Rocky Linux's track record 10 and 20 years from now.
- How Debian's slow decision-making will respond to modern security requirements.
- How far Debian can keep up in new domains like quantum computing and AI integration.

---

## The "corporate steward" problem that surfaces

In WordPress, **one individual** failed to take responsibility. In Node.js, **no one** took it. In Linux distributions, a third failure mode is visible: **corporate stewards (Canonical, Red Hat / IBM, SUSE, etc.) rewriting their promises based on their own business judgment.**

This is not a story about "bad companies." **Companies acting on business judgment is natural.** The problem is that the user side fails to recognize this, and treats corporate-stewarded projects as "neutral and permanent."

> "Free to use" is a promise only for now.
> "De facto standard" is a position only for now.
> "Backed by a corporation" is **support that can be withdrawn at any time.**

The CentOS incident demonstrated this most dramatically. The notice that it would **end eight years early** betrayed every organization that had been planning long-term. Red Hat / IBM presumably had no malice. But a structural fact emerged: **corporate stewards are simply like that.**

### Comparing the three governance-failure patterns

Lining up the three cases (WordPress / Node.js / Linux distros), the structural contrasts become clear.

| Case | Direction of failure | Typical damage | How verification reveals it |
|---|---|---|---|
| **WordPress / Mullenweg** | One individual carries too much responsibility (excessive concentration) | The whole organization is jolted by one person's mood and conflicts | Lay out one person's statements on a timeline and contradictions appear |
| **Node.js / npm** | No one manages the whole (distributed absence) | Supply-chain incidents, burnout, unclear locus of responsibility | Lay out the governance structure from primary sources and the responsible parties are fragmented |
| **CentOS / Red Hat / Ubuntu** | Corporate stewards rewrite their promises | Years-long plans suddenly collapse; migration costs | Lay out the past 5–10 years of policy changes on a timeline |

These look like separate phenomena, but they share **fragile governance structure.** The surface narratives ("the community supports it," "a corporation backs it," "it's the standard") cover the governance fragility. Verify with AI, and that cover comes off.

---

## Implications for adoption decisions

The questions that emerge from verification, regarding Linux-distro selection:

### Selection by time horizon

- **Systems ending in ≤5 years**: Ubuntu / RHEL is fine. You can take the benefit of commercial support.
- **Systems running 5–10 years**: Debian, or a paid RHEL/SUSE subscription. AlmaLinux / Rocky Linux: wait and see.
- **Systems running 10–20 years**: **Debian, no contest.** The constitution-and-social-contract structure is the rare guarantee that cannot be rewritten by a corporation's business judgment.

### Factor in exit costs

- **What if the next corporate steward changes direction?**
  - Migration cost (verification, rewriting, restructuring maintenance contracts)
  - Retraining cost (operations team)
  - Compatibility verification for third-party software
  - Cost-model on the assumption that you pay an exit cost once every five years.

### The risk of "the de facto standard"

- "Everyone uses it" is **not a guarantee of governance.**
- There is no guarantee that the "everyone uses it" state will last another five years.
- **Large share and long-term durability are different things.**

### The practical value of the derivative (Debian-derived) ecosystem

- When Ubuntu changes direction, **the path back to Debian is still open.**
- Mint, Pop!_OS, Devuan, and others function within the Debian ecosystem as "the option that does not go through Canonical."
- **Debian is also Ubuntu's insurance policy.**

The reason this book (aiseed.dev) recommends Debian, in the "Learning Debian with Claude" series, is exactly this. **Debian is the rare Linux you can plan around on a 20-year horizon.** It is not the technology that guarantees this — it is **the governance structure**.

---

## The power of narrative verification

> "Free," "the de facto standard," "backed by a major corporation" — these narratives sound attractive at adoption time.
> But verify with AI, and you see that they are **"promises that can be rewritten at any time."**
> Meanwhile, a structure like Debian's — **"unexciting, but unrewritable"** — is **dramatically more valuable for long-term decisions.**

The flashier the narrative, the more verification it needs. Whether you can see through to the "unexciting facts" decides the quality of long-horizon work.

This is the practical value of verifying narratives with AI. **Seeing the structure before adoption** changes the quality of work after adoption.

---

## Related

- Chapter 11 main text: [Verifying Narratives with AI](/en/ai-native-ways/verify-narratives/)
- Example 1: [Should You Adopt Node.js at Work?](/en/ai-native-ways/verify-narratives/example-1/)
- "Learning Debian with Claude" series: [/en/claude-debian/](/en/claude-debian/)
- Structural Analysis series: [Security Design for the Mythos Era](/en/insights/security-design/)
