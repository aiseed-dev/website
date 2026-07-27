---
slug: nadella-yang-what-to-do-now
title: "Hailed as Prescient for Leading AI-First — Nadella, Yang Zhilin, and What to Do Right Now"
subtitle: "Nadella, who buys the frontier model and shipped no product that survives AI-driven attack, and Yang Zhilin, who opened the Mythos-grade Kimi K3 for free — what the shop floor does on the day attacks became free"
date: 2026.07.27
description: Moonshot AI announced Kimi K3 on 16 July 2026 and promised the full weights on 27 July under a modified MIT licence — 2.8 trillion parameters, a one-million-token context. Overall it trails Fable 5 and GPT-5.6 Sol, but it beats Opus 4.8 and GPT-5.5 and took first place in blind frontend-coding comparison: the frontier of a short while ago is about to be opened for free. No individual can run it even then (loading alone takes eight H100 80GB cards), but the premise still changes, because the attacking side is not an individual. Working out what to do about it, almost all of it turned into what to do about Microsoft. Moving the Windows machines to Linux and managing them properly is the best answer, but it cannot be done immediately — so this piece sets down what can be done now, layer by layer. Network (segments, no client-to-client traffic, egress deny by default, your own name resolution), identity (leave Active Directory), documents (turn off macros), applications (make the website static), recovery (an immutable backup). Then it shows that on Windows the premise of containment itself breaks down, because the hardware is tied to the cloud. Setup compels a connection, the key the TPM sealed is deposited in the cloud, and in April 2026 the seller's own update stopped machines from starting. Malware that turns BitLocker itself into ransomware exists, and whether keys escrow to AD or to the cloud, both are concentrations. These restrictions are waived for the large contracts, so there is no reason to expect market pressure to change the direction. Which leaves one conclusion: anyone responsible for a company's information should hold a migration to Linux as a plan.
lang: en
label: Blog
category: Structural Analysis Notes
---

# Hailed as Prescient for Leading AI-First

## Planning Against K3 Turned Into Planning Against Microsoft

On 16 July 2026 Moonshot AI announced Kimi K3: 2.8 trillion total parameters, a one-million-token context. Its author is Yang Zhilin, the company's founder. Moonshot has promised the full weights on 27 July under a modified MIT licence.

At the time of writing, K3 does not appear in the company's listing on Hugging Face. **The deadline is today.** Whether it ships on time, slips, or arrives with conditions attached does not change the premise of this piece.

The performance deserves stating precisely. Overall it trails Fable 5 and GPT-5.6 Sol. But it beats Opus 4.8 and GPT-5.5, and it took first place in blind comparison on frontend code. **The frontier of a short while ago is about to be opened for free.**

Even once the weights are out, no individual can run this. Loading it alone takes eight H100 80GB cards. **The premise still changes.** The attacking side is not an individual — criminal groups have compute on that scale, and so do states.

Working out what to do about it, **almost all of it turned into what to do about Microsoft.**

Moving the Windows machines to Linux and managing them properly is the best answer. But it cannot be done immediately. That is the reality, so what follows is what can be done now.

## The Target Is Not Being Untouched but Not Being Knocked Over

[The previous piece](https://aiseed.dev/en/blog/three-conditions-ai-era/) laid out the structure: software got cheap, so attacking and verifying both got cheap, and a cheap attack lands on whatever is concentrated. This one is the implementation.

Start by resetting the target. **The goal is not to avoid being attacked.**

It is to be attacked periodically, take damage, and keep the business running — the same standing as fire or theft. Shops get burgled sometimes and do not close over it, because there are locks, insurance, and an arrangement that survives a loss.

Security alone has long been discussed against an unreasonable standard: breached once, finished. That standard produces two failures. Either it is unreachable, so people give up; or a single breach is taken to mean everything was wrong.

**Not untouched, but not knocked over.** Reset the target there and the work becomes definable.

## What to Do Right Now — Decide How Far Things Reach, Layer by Layer

There are two kinds of thing you can do about an attacker: limit **what they can do**, and decide **how far they can go.**

The second is what sets the blast radius. So start with the network.

### Network — What Can Reach What

Most small and mid-sized company LANs are flat today. Every endpoint can talk to every other endpoint, and outbound traffic is unrestricted. That was not a design choice; it is what shipped.

Four things to decide.

**Split into segments.** Office, production, servers, guests, and devices like cameras and copiers. Don't put everything on one LAN. The moment you split, what one intrusion reaches goes from "everything" to "that compartment." Two IT staff can do this.

And **traffic crossing a compartment boundary is HTTPS or SSH only.** The path is not trusted, so it has to be encrypted. The effect does not stop there. That one line of rule shuts out every protocol that assumes a flat LAN: SMB, name lookups, printer discovery — none of them cross a boundary anymore. **Deciding the one form that may pass is shorter, and easier to check, than enumerating everything to stop.**

A company with a handful of machines does not need it — the reach is already narrow. And **the more Linux you run, the less it is needed.** Windows endpoints trust each other by default, allow credentials to be reused, and ship with sharing and remote-operation paths already open. Segmentation is partly the work of undoing that default at the network layer. When endpoints do not trust each other to begin with, there is less for a compartment to block.

**Don't let endpoints talk to each other. This is where you start.** There is almost no operational reason for PCs to communicate directly. They talk to the file server; they do not talk to the desk next door. Ransomware spreading inside a company usually travels this path. **Whether one machine falling means one machine or all of them is decided by whether SMB was contained.**

**And this one is not easy on Windows.** File sharing and lateral movement ride the same SMB, so you cannot stop the protocol outright. You have to split by destination, and pushing that rule to every endpoint requires central management — either AD or a cloud administration platform. **The very thing this piece says to leave.** Printing and remote-administration tools also assume endpoints can reach each other, so you cannot read in advance what breaks when you cut it.

**On Linux the problem does not arise.** Nothing is listening on 445 by default. It is not a matter of closing something; it is a matter of never opening it.

**Deny outbound by default.** Even after an intrusion, a machine that cannot reach its external controller receives no instructions and exfiltrates nothing. **Whether you stay standing is decided by endpoint isolation; whether your data leaves is decided here.** Allowing only the destinations you need looks tedious; the list of destinations you need is shorter than you expect.

**Hold your own name resolution.** Run and filter internal DNS. Set SPF, DKIM, and DMARC on your own domain — spoofed mail remains one of the largest entry paths. And clean up CNAMEs still pointing at retired services; an abandoned record is an entry point for subdomain takeover.

In short: **decide for yourself what can reach what.** As the previous piece put it, what cannot be explained cannot be defended. Very few small companies could draw their current LAN and explain it.

### Identity — Leave Active Directory

AD is a monolith with the domain administrator at its apex. By design, breaking one place takes everything. The techniques that abuse reused credentials or forge tickets exist as consequences of that structure.

What a small company actually needs is login to devices, authorization to files, and login to a handful of SaaS products. **That can be assembled without a directory.**

Moving to a cloud identity platform does not change the structure. The concentration moves from the building to the cloud; one break still takes everything.

### Documents — Turn Off Macros

Open a document and arbitrary code runs. That design is the anomaly, but it was decided in the 1990s and compatibility keeps it from being withdrawn. Macros remain a classic path for initial access.

The practical obstacle has been that operations depend on existing macros. So it stopped at "migration is too expensive to switch them off."

**That wall has come down.** AI reads a macro, explains what it does, and rewrites it into another form. Not being able to switch them off is no longer a reason not to.

And the same shape is being stacked on right now. An AI built into the document **follows the instructions written in the document.** Thirty years ago a document was also a program. Now a document is also an instruction.

Slip an instruction for the AI into a received email or a shared file — indirect prompt injection, and it is not a solved problem. Meanwhile an AI embedded in the product can read the whole tenant. **The wider what it can read, the more a single injection carries out. Concentration is being stacked on concentration.**

And what it means for the two to sit on the same surface runs deeper. **VBA reaches the OS.** File operations, launching external programs — it does not stay inside the document.

So an AI that follows instructions and an execution engine that reaches the OS are living in the same place. The only thing separating them is the defense against injection. And that defense **stands on an unsolved problem.** An unsolved problem is being used as the sole partition.

And there is a path by which outsiders place things on that surface. **Email.**

The inbox is the one place where a stranger can put content inside your company. Open an attachment and the associated application starts, and the macro engine is right there. The body and the attachment are also read by an AI that reads the tenant. **One entrance, two execution engines behind it.**

And the entrance itself is badly designed. **Opening and executing are the same action.** The recipient clicks, and whether the result is "look at the contents" or "run it" is decided by the file, not by them. There is no way to tell the two apart before pressing.

Mechanisms to block dangerous extensions have been added. But they block by list, and **a list always catches up afterward.** As long as the design assumes that pressing runs it, the blocking side is condemned to chase.

That is three times now. A document is also a program, a document is also an instruction, and an attachment does not separate reading from running. **The principle of not mixing data with execution has never once been applied to this path.**

The order is wrong too. **Macros should have been switched off before Copilot was brought in.** A second path of execution from documents was added while the first one was still open. And the reason the first one stayed open was "migration costs too much." **The organizations that could not find that budget found one for the second.** It was never a shortage of capacity. The capacity was pointed at opening something new rather than closing something old.

The previous piece's "don't settle for the AI your vendor bundled in" was never only about the quality of verification. It is also about attack surface.

### Applications — Make the Website Static

A company brochure does not need a dynamic CMS. A static site has no database, no server-side execution, no admin console, and no plugin-update treadmill.

**If it is breached, the files change.** There is no data to take and no runtime to pivot from. The blast radius is structurally small.

### Recovery — An Immutable Backup

The four above decide the extent of the damage. **This one decides whether you are knocked over.**

Keep one copy offline or in a form that cannot be rewritten. Actually rehearse a restore and measure how many hours it takes. With that in place, ransomware becomes a loss rather than a death.

The component that finally makes "attacked periodically, damaged, still running" true is this one.

## Windows Becomes the High-Maintenance Option

**Against AI-driven attack, the gap widens by another step.**

The attacker does not need to read your configuration. Reading the product is enough — the same product sits in the same shape everywhere, so reading it once works anywhere. **That advantage is identical on Windows and on Linux.**

The defender is the opposite: what decides the outcome is **whether you can hand your own state over to be read.** On Linux, configuration is very nearly all text. Everything under /etc, the service definitions, the traffic rules — you can pass them to an AI as they are, have them explained, diff them, and have the rewrite drafted. On Windows, much of the state lives in the registry, in policy objects, and behind screens. It can be extracted, but getting it into a readable form is itself a job.

**With the same AI in hand, the defender receives less.** The equilibrium the previous piece described — attack and defense becoming equals — arrives first on the foundation whose state can be read.

On top of that, lining the five up shows something else. **Most of the effort goes into undoing defaults.**

Endpoint-to-endpoint traffic is hard to stop because file sharing and lateral movement ride the same SMB. Segments become attractive because endpoints trust each other by default. Distributing a rule requires central management because no other road is provided. Turning off macros takes work because a document is also a program.

On Linux most of that column does not arise. There is no work in closing what was never open.

The same happens to the previous section's rule that only HTTPS and SSH cross a boundary. On Linux, keys, scp, and rsync are the native vocabulary of the environment; on Windows you start by adding the client, and neither generating a key nor distributing one is established practice. **The gap is not whether it runs; it is whether it is the standard road.** Running a tool born in the Unix world on Windows requires a port, and a port trails upstream and never catches up with the surrounding tooling. Since most of the people building tools today are in the Unix world, **the port standing between you and everything that world produces is a cost that never goes away.**

And settling one rule settles another. **If HTTPS and SSH are the only things that cross a boundary, there is no reason left to run a Windows server.** Its role as a file server stands on SMB, and SMB cannot cross. Move the exchange to HTTPS and boundaries are crossed naturally — but nothing about that shape requires Windows, and once you leave AD the domain-management role is gone too.

Look back over what has been laid out and one thing stands out. **Almost every specific name given, layer by layer, belongs to the same company.** The SMB that makes endpoint-to-endpoint traffic hard to block, the AD required to distribute the rules, the VBA that makes documents executable, the Copilot stacked on top of it, the attachment that runs when pressed, and the sending infrastructure whose treatment varies with the size of your contract. They were listed as separate problems, but they come from one design lineage.

This is what the Mythos era means. Once AI can find zero-days in a matter of hours, a target's worth is set by **how uniformly it is deployed** and **how little of it can be inspected**. Windows is at the maximum on both. The same thing sits in the same shape all over the world, and those who use it have no way to check what is inside.

In the interval between disclosure and fix, an open base lets you determine whether you are affected and act first. On a closed base you can only wait. **The length of that wait is set by the seller, not by you.**

So the abstract talk of preparing for the era comes down, in practice, to a single line. **Mythos-grade countermeasures means dealing with Windows.**

## Windows Ties the Hardware to the Cloud

Up to here it has been a question of labor. Labor can be paid. **What comes next cannot.**

The principle fits on one line. **Windows ties the hardware to the cloud.** The TPM is a component inside the machine, and sealing and unsealing were designed to complete locally. Then an account was wired to it. What follows are the three forms that binding takes.

**One. The freedom not to connect disappears.** Windows 11 setup demands an internet connection and a Microsoft account. The ways around it have been closed one by one: `bypassnro` was removed in March 2025, and `ms-cxh:localonly` in October. Microsoft's explanation is that users "need to complete OOBE with internet and a Microsoft account, to ensure device is setup correctly." Some shipping versions still have a working route, but there is only one direction of travel. What remains are unattended deployment through answer files, and the domain-join path — **both tools of an organization that has provisioning machinery.** Neither remains for an individual or a small business that wants to keep one machine unconnected. The surest form of containment was not connecting, and it was retained only for the larger side.

**Two. The disk key leaves.** From 24H2 onward, a clean install on a machine with TPM and Secure Boot, signed in with a Microsoft account, turns on disk encryption automatically. Home editions included. The recovery key is then deposited with that account automatically. The user chose neither the encryption nor the deposit; both happen by default. In January 2026 Microsoft confirmed that it hands those keys to the FBI on a valid legal request — around twenty a year, held in unencrypted form, with no obligation to tell the person whose key was handed over. The disk is encrypted. **The key, however, is not on your side.**

The difference in depth is worth pausing on. **A service going down and a machine not starting are different accidents.** Lose your cloud credentials and mail and documents stop opening; that hurts, but the machine in front of you still boots and what is stored locally still opens. One layer stopped. BitLocker is not like that. A machine that has entered recovery will not start without the 48-digit recovery key. And recovery is not an accident — **it happens during ordinary maintenance.** UEFI updates, TPM firmware updates, Secure Boot configuration changes, replacing a component involved in boot: each alters the measurements the TPM recorded, and the TPM stops releasing the key. In April 2026 this happened at scale: Microsoft's own update changed Secure Boot validation, machines with older firmware could not get back from the recovery screen, and the fix came only with the following month's update. **The seller's update stopped the machine, and the seller holds the key that opens it.**

And by default the key lives only inside the account. You need another device, an internet connection, and a successful sign-in to that account before the machine in front of you will start. An organization has the key in AD or Entra, where an administrator can retrieve them in bulk; individuals and small businesses have no such path. If the account is frozen, or taken over, or belonged to the person who set it up and has since left — **that machine does not start again.** Containment meant keeping an accident inside its layer. Here the opposite happens. **A problem with a cloud account reaches all the way down to whether a physical machine will start.**

**Three. Authentication becomes reachable from everywhere.** With a local account, only someone who can reach the machine can make an attempt. Splitting into segments, refusing endpoint-to-endpoint traffic, denying outbound by default — everything done so far **was also work to narrow who is able to attempt authentication.** None of it applies to an online account. **Given the ID, the attempt can be made from any device in the world.** And the ID is not a secret: usually an email address, printed in signatures and on business cards, and present in past breach dumps.

This is quietly terrifying. Against a local account, the number of attempts available to a distant stranger was **zero** — they could not reach the machine. The moment it goes online that number stops stopping. From everywhere, every day, out of sight. **A local account was never protected by a strong password. It was protected by being out of reach.** Lockouts exist, but attackers go around them: one attempt against many IDs, or a single attempt using a combination straight out of a breach dump. **A lockout guards one entrance; it does not stop attempts made across the whole surface.** And a short password becomes a matter of time. **The password did not change. Only the danger did.** Multi-factor authentication is added on top: it works, but it does not narrow reach. **Narrowing by layer and stopping at a gate are not the same thing.**

And the recovery key from a moment ago sits in that same account. **A path now exists that reaches the key to the disk without ever touching the machine.**

All three are one and the same binding. The key that unseals is deposited outside, the first step of putting a machine into service now runs through outside, and an update from outside breaks the seal. **Whether the machine in front of you runs is now determined by a state held elsewhere. The boundary has stopped being on your side.**

## Pull It Back Onto the Machine

This binding even changes the attacker's motive.

Ransomware has been laborious work: break in, obtain an execution environment, run the encryption, evade detection, hold the key. **The encryption is already done now.** It is on by default, and the key sits inside a single account. The job is no longer to touch the machine; it is to get into that account. This is not hypothetical. Malware that encrypts using BitLocker itself, **deleting the default protectors so that no route to recovery remains**, has been observed since 2024. What appears on an infected machine is the message that there are no more BitLocker recovery options on this PC. **The attacker no longer needs to bring the encryption.**

The damage also arrives differently. Deleting the key does nothing on the spot; the machines keep booting normally. They break the next time firmware is updated, a component is replaced, or the Secure Boot configuration changes. **Over months, one by one, they stop starting.** By then nobody connects it to the intrusion. The previous piece said attacks get cheaper because tools get cheaper; what is happening here is a different markdown. **What the attacker would have had to build, the seller installed in advance.**

Escrowing to your own side is no way out either. **Keys deposited in AD can be read with domain administrator rights**, and taking domain administrator is the standard destination for an intruder — the keys have been gathered where one breach yields all of them. Keep it in-house and it gathers somewhere poorly defended; keep it outside and the defense is solid, but you cannot move it and it is open to legal demand. **The only choice is which weakness to take on.**

So what do you do? **Using the cloud is not the problem.** If Google Workspace were compromised outright, the machine in front of you still starts. What is stored locally still opens. What stops is the service layer, and **the boundary is drawn there.** The problem is binding hardware to cloud, not the cloud itself — and it is this contrast that pulls the two apart.

And the service layer can be closed. Passkey-only sign-in is available on every contract tier and costs nothing. The guessable secret disappears, and so does handing a key to a counterfeit entrance. The remaining route is to take the endpoint itself — and **that is exactly where the measures in this article work.** Pull the attacker back onto the machine and segments, blocking, and default-deny outbound all mean something again. Start with the administrator accounts.

**What must not be tied together is hardware and cloud.** With that one line held, everything else goes back to being a question of layers.

There were three reasons to choose Windows anyway: the line-of-business application exists only there, document compatibility is required, and nobody can handle the alternative. **All three have weakened.** Applications can now be built, document formats are published, and configuration is something AI reads and writes. This is not a claim that Windows becomes unusable. It is a **demotion.** It moves from the default you choose without thinking to an option that has to justify its management overhead each time. If you can answer that, choose it.

For the near term that is enough. Over a longer horizon, something firmer can be said. **The ways out are disappearing one per year.** The means to set a machine up unconnected, the default that kept the key on your own side — both have been removed in turn. And the side doing the removing has no reason to stop, because the pain is carried by the smaller contracts. **As long as the large customers are exempt, there is no reason to expect market pressure to change this direction.**

So waiting is not a policy. **Anyone responsible for a company's information should hold a migration to Linux as a plan.** This is not a call to replace everything at once. There is an order. Make new servers Linux. When you split into compartments, make the equipment at the boundaries Linux. For endpoints, start where the dependency on a line-of-business application has been broken. **Migration can advance on the schedule of replacement** — not an expensive simultaneous upgrade, but the work of deciding a direction at each renewal. What needs deciding is not a deadline but a direction, which way you go the next time you buy something. **An organization that has not decided that in advance will be decided for, without ever feeling that a decision was made.**

## Why None of This Was Done Before

Start with the honest answer. **Because it was difficult.**

Running your own mail server meant, for years, a running fight with mail that doesn't arrive: SPF, DKIM, DMARC, blocklists, the filters of the large providers. One setting wrong and your company's mail never reaches the customer. Identity was the same — AD was solving a real problem, and nothing else at the time bound a fleet of Windows machines under one administration. Office alternatives left real compatibility gaps in complex spreadsheets and in documents that circulate outside the company.

**Choosing the vendor was a rational decision.** Nobody was fooled.

That said, the difficulty has a second layer. Stacked on top of the part that was genuinely hard is **a part that did not have to be hard.**

**The defaults ship connected.** Everything arrives interconnected, and disconnecting is the customer's job. Defaults are policy. Choosing a design in which doing nothing leaves the most-connected state is a decision made by the seller.

**Complexity consumes the attention budget.** When two IT staff are full up with identity, mail, and device management, network design never gets reached. A neglected network is not an independent failing; it is a consequence of complexity.

**Bundling removes the occasion to design.** When identity, mail, and name resolution all live in one tenant, the moment where you would design them never occurs. Whatever the wizard wrote stays, and so does the record pointing at a service you retired.

And here is the structural core. **What the customer cannot do for themselves is the product.** Difficulty is not a side effect; it is the thing being sold. What the previous piece said about systems integrators applies here unchanged.

## Why It Can Be Done Now

Two things changed.

One is that **the genuine difficulty came down.** Identity has mature open standards and usable implementations. Document formats are published, and AI handles conversion and repair. Network design can be surfaced by having the configuration read back to you. The grounds on which "we can't do this ourselves" was decided no longer hold.

The other is that **reading complexity got cheap.** Have it explain your network configuration. Have it read what a macro does. Have it surface which service depends on what. Have it propose which destinations to open and which to close. All of that used to take weeks and an outside specialist. Now it runs in your own hands.

**Mail is not hard anymore either.** The large providers publish their acceptance requirements, and SPF, DKIM, and DMARC can be verified in minutes. Packaged implementations exist; you do not assemble it from parts.

Getting the configuration right, however, is not the same as arriving. **The same rules are applied in different shapes according to size.**

Azure blocks outbound port 25 from virtual machines — but not for everyone. On the large enterprise contracts, EA and MCA-E, it is not blocked. On pay-as-you-go, MSDN, free trial, education, and CSP it is blocked, and requests to lift it are **documented as not granted.** Same platform, same technical hazard; the only difference is the size of the contract.

Authentication has the same shape. Microsoft automatically DKIM-signs its own onmicrosoft.com domain. From the first day a tenant exists, it can send with SPF, DKIM, and DMARC all aligned. No track record required. **Being inside substitutes for one.** This property is actually abused: fraudulent mail sent from tenants created through the ordinary signup process has been documented passing every authentication check.

Do the same thing outside and, with all three configured correctly, a low volume of mail from an address with no history is still treated as suspect. The rules are identical; passage is not. **What is left here cannot be bought with correctness.**

So there is only this one thing to move outside. The remaining external dependency is delivery reputation, and **that is handled by moving only the outbound relay outside.** Authenticated relay on port 587 is unrestricted even on Azure, and Microsoft itself directs customers to use it. The mailboxes, the accounts, and the archive stay in-house; only the act of delivering passes through someone else. A relay holds neither your identity nor your accumulated correspondence, so no concentration forms. The part that was hardest turned out to be the part that separates most cleanly.

Which sets the order. **You do not have to do all of it at once. Start by containing SMB** — that is what decides whether one machine falling means one machine. Then deny-by-default outbound, then segmentation. Identity migration is the heaviest, so it can come last.

As the previous piece said, the near-term task is not removal but containment — and the line of containment is drawn at the unit where responsibility can sit.

## Observation Points

**Network.** When a breach happens, what fraction of operations stopped. The share of companies running deny-by-default on outbound traffic.

**Identity.** The share of small companies operating without a directory.

**Recovery.** The share of companies that rehearse a restore even once a year. A restore procedure that is never exercised is not a procedure; it is a wish.

And the condition under which this piece is wrong: **if organizations that applied these measures ended up fully down at the same rate as those that did not**, the argument does not stand. If I'm wrong, I'll write that I was wrong.

---

## Related

- Blog [Who the AI Era Needs — Cheap Software Means Cheap Attacks](https://aiseed.dev/en/blog/three-conditions-ai-era/) — the preceding piece; the structural side
- Blog [Autonomy, Distribution, Diversity — The Shape of Systems to Come](https://aiseed.dev/en/blog/autonomy-distribution-diversity/) — the design argument for dividing things
- Blog [Self-Hosting the Equivalent of Microsoft 365](https://aiseed.dev/en/blog/self-hosting-microsoft-365/) — putting identity and mail on your own side
- Blog [The Danger of the Windows Account](https://aiseed.dev/en/blog/windows-account-danger/) — what concentrated identity means
- Blog [Microsoft's CEO Nadella and Hegel's Philosophy](https://aiseed.dev/en/blog/nadella-hegel-cunning-of-reason/) — what this piece describes as structure, argued from the side of who is choosing it
- Blog [When Fable 5 Returns, Do This First](https://aiseed.dev/en/blog/verification-shock/) — what it means for verification to be free
- Blog [IT Ends as an Industry, and the Age of Materials and Assembly Begins](https://aiseed.dev/en/blog/after-it-industry/) — why self-sufficiency becomes structurally favorable

## References

1. The preceding piece, "Who the AI Era Needs" — https://aiseed.dev/en/blog/three-conditions-ai-era/
