---
slug: claude-debian-server-02-where-to-run
lang: en
number: "02"
title: Chapter 2 — Where to Put Your Server
subtitle: Old PCs, your home, VPS — a map of costs and responsibilities
description: This book's premise is a home server — your data managed on your own machine at home. We still map all three options (home, VPS, major cloud) by cost and responsibility: to put numbers behind "why home," and to fix, together with Claude, the right roles of VPS and cloud — practice rig and publishing entrance.
date: 2026.06.10
label: Claude × Debian Server 02
prev_slug: claude-debian-server-01-what-is-a-server
prev_title: Chapter 1 — What Is a Server
next_slug: claude-debian-server-03-minimal-install
next_title: Chapter 3 — The Minimal Install
cta_label: Learn with Claude
cta_title: Decide the place, and you decide the responsibility.
cta_text: The body stays home; the entrance comes later, if at all. Who carries power, the line, and physical failure changes the scope of your responsibility. Spread out the map of cost and responsibility, and ground the home-server premise in your own numbers.
cta_btn1_text: Continue to Chapter 3
cta_btn1_link: /en/claude-debian/server/03-minimal-install/
cta_btn2_text: Back to Chapter 1
cta_btn2_link: /en/claude-debian/server/01-what-is-a-server/
---

## Why "Where to Put It" Is the First Design Decision

When people hear "start a server," most first think "what kind of machine should I buy?" But that is the wrong order. **Before you choose hardware, you need to decide where to put it.**

That is because, once the location is decided, the three structures riding on top of it are decided automatically — cost (up front and monthly), responsibility (who fixes it when it breaks), and network (how you connect, whether you can publish). Putting it on an old PC at home versus on a VPS across the net changes all three wholesale. Choosing the machine's model number comes after that.

As declared in Chapter 1, this book's premise is a **home server**. We still turn the three location options into a map in this chapter — to put numbers behind "why home," and to fix the right roles for VPS and cloud: a practice rig, and the publishing entrance handled in Chapter 9. By the end, you will be able to state "it lives at home" as your own decision, with reasons behind it.

## Section 1 — A Map of the Three Options

Where to put a server splits, broadly, into three.

- **(a) A machine at home.** An old PC you stopped using, a mini PC, a Raspberry Pi, and so on. Placed physically in your house.
- **(b) A VPS.** A virtual private server. You rent a virtual machine in a provider's data center for a monthly fee. From a few hundred yen a month.
- **(c) A major cloud.** Metered billing. You pay for what you use. Flexible, but if you are careless the cost is hard to predict.

Let us line up the three differences in a single table.

| Aspect | (a) Home machine | (b) VPS | (c) Major cloud |
|---|---|---|---|
| Up-front cost | 0 for an old PC (tens of thousands of yen for a new mini PC) | 0 | 0 |
| Monthly | 0 (excluding the machine) | A few hundred to a few thousand yen | Per usage (hard to read) |
| Electricity | On you (see below) | Provider's burden | Provider's burden |
| Noise / placement | You secure it | Not needed | Not needed |
| Line | Depends on your home line | Provider's fat line | Provider's fat line |
| Who fixes failures | All you | Physical not you, OS internals you | Physical not you, OS internals you |
| Physical location of data | Your house | Provider's data center | Provider's data center |

The most important rows in this table are the bottom two. **A home server means "all the responsibility is yours" but "the data is physically in your own hands."** A VPS or cloud means "physical failures and the line are looked after by the provider" but "the data sits in someone else's data center." As declared in Chapter 1, this book puts data sovereignty first — so the body lives at home. Where a VPS shines is in the roles where you may hand most of the responsibility away: the practice rig, and the publishing entrance.

The stance repeated in the main edition — **"bring an old PC back to life"** — connects naturally here. An old PC that cannot run Windows 11 and has retired as a desktop is **ideal as a server machine.** It has performance to spare, and you give a second life to something that was headed for the trash.

### Ask Claude ①: Diagnose Your Machine's Fitness as a Server

> I have an old PC at hand that I might repurpose as a server. Its specs are:
> [paste the my-system.md you made in Chapter 3 of the main edition if you have it; if not, bullet the CPU, memory, disk, year, and power draw as far as you know]
>
> Please diagnose this machine's fitness for use as a Debian server. Against the "what I want to run" I sorted in Chapter 1 [paste it here], is the performance enough? If not, what could I add to improve it? Also point out concerns when running it around the clock (heat, lifespan, power draw).

The `my-system.md` you made in the main edition can be reused as-is. This is the carry-over of the main edition's craft, working here in the server edition too.

## Section 2 — The Reality of a Home Server

A home server is appealing, but it comes with several realities a desktop did not have. Face them squarely before you start.

### Estimating the Electricity Bill

A server runs around the clock. So its power draw becomes the monthly electricity bill directly. An old laptop's idle draw is a few watts; a desktop or mini PC is in the ballpark of ten-something to tens of watts.

Let us do a very rough calculation.

```
10 W for 24 hours × 30 days = 7.2 kWh/month
At 31 yen/kWh, about 223 yen/month

At 30 W, about 670 yen/month
```

So, a low-power machine runs a few hundred yen a month. This becomes a number you can compare directly against a VPS's monthly fee. Settle from the start that **"home is not zero yen" but "there is a monthly fee called electricity."**

### The Line and the Router

A home server hangs off your home's line. For LAN-only use, it runs today as long as you have a router. The problem comes when you want to connect from outside.

Recent home lines are often **CGNAT** (a setup where multiple households share one global IP), and in that case "connecting to your home server directly from outside" is, as a rule, not possible. Whether you have a static global IP assigned depends on your contract and line type. Since this "connect from outside" problem is about publishing, we handle it in Chapter 9 alongside solutions like tunnels. **If you use it LAN-only, this problem is entirely irrelevant. You can start safely today.**

### Power Outages, Heat, Dust

Once you place a physical machine in your home, all physical trouble becomes your responsibility.

- **Power outages.** If the power cuts, the server goes down. If you load important data, consider a UPS (uninterruptible power supply) eventually.
- **Heat.** A machine running around the clock generates heat. Avoid poorly ventilated spots and sealed cabinets.
- **Dust.** Dust building up on the intake fan worsens cooling. A cleaning every few months is needed.

These are not reasons to "give up on a home server." **For a LAN-only experimental machine, you can rebuild it if it goes down in an outage, and heat and dust are well handled by sensible placement.** Think seriously about it again at the stage of loading real data.

### Ask Claude ②: Consult on Where to Put It

> I want to start a Debian server. My situation is:
> - Purpose: [the "what I want to run" I sorted in Chapter 1]
> - Monthly budget: [e.g., ideally within 1,000 yen including electricity]
> - Machine at hand: [have an old PC / not; if so, its specs]
> - Line: [home line type, and whether I have a static IP if I know]
> - Want to publish: [LAN-only for now / want to use it from outside eventually]
>
> Starting under this book's premise (the body is a home server; I manage my own data), please recommend how I should set up my stage-one experimental machine — use the old PC I have / buy a used or mini PC / rent a VPS for a few days as practice. Give reasons, and compare pros and cons if there are several options.

The trick is to hand over the four points of budget, purpose, line, and publishing policy. With these four in hand, Claude can return a recommendation tailored to you rather than a generality.

## Section 3 — Where a VPS Fits: Practice Rig and Publishing Entrance

If you want to avoid the physical care of a home machine, a VPS is a strong option.

### What Gets Easier

A VPS is a setup where you rent a virtual machine in a provider's data center. **Power, the line, and physical failure are all looked after by the provider.** You do not have to worry about outages or dust. A fat line is attached from the start, and a global IP is assigned (on most plans), so the "connect from outside" problem of Chapter 9 is far easier than at home. What you are responsible for is only "the OS internals" of the virtual machine you rent.

### What You Lose

There are things you lose in exchange. **The data sits in the provider's data center, not in your house.** From the data sovereignty perspective of Chapter 1, this is a step back. And of course, a monthly fee keeps accruing. Since it is not physically in your hands, it may feel unsatisfying to those seeking ultimate independence.

So under this book's premise, **putting the body — your apps and data — on a VPS is not a path we take.** The VPS has exactly two roles here: the "break it and rebuild it" practice rig, and the publishing entrance handled in Chapter 9 (it relays traffic while the data stays home). Read the axes below with those two roles in mind.

### Axes for Choosing

When choosing a VPS, think roughly along these axes.

- **Domestic or overseas provider.** Choose by response latency (domestic is faster if you use it from Japan), price, and support language.
- **Memory.** For something like the "file sharing, photos, notes" from Chapter 1, **2 GB of memory is plenty to start.** Raise it once you run short.
- **Disk.** If you store lots of photos or video, check capacity and the price of additional disks.
- **Billing form.** Flat monthly, or hourly.

### Excellent as a "Break and Rebuild" Practice Rig

A VPS has one more advantage not to overlook. Many providers offer **hourly billing** or **easy re-creation**, so you can casually repeat building a server, wiping it, and building again. You can prepare the "machine you can afford to break" from Chapter 1 without physically dirtying your own machine. You can even rent one for just a few days, practice the minimal install of Chapter 3, and wipe it when you are satisfied.

### Ask Claude ③: Compare Electricity vs. VPS Monthly Fee

> I want to estimate, for my case, whether a home server or a VPS is cheaper.
> - Power draw of the candidate home machine: [watts if you know; the model number if not]
> - Electricity rate in my area: [e.g., 31 yen/kWh; "general Japanese household rate" if unknown]
> - VPS plan under consideration: [e.g., 2 GB memory, 50 GB disk, ___ yen/month]
>
> Assuming around-the-clock operation, calculate the home server's monthly electricity cost and line it up against the VPS monthly fee. Add a word on the non-cost differences too (scope of responsibility, location of data).

Turning electricity, a "hard-to-see monthly fee," into a number lets you compare home and VPS fairly for the first time. Have Claude do the calculation, and there is no risk of getting an order of magnitude wrong.

## Section 4 — Conclusion: How to Decide

Given the map so far, the path this server edition recommends is clear.

**First, place an experimental machine inside your home LAN and run Chapters 3 to 8 there.** LAN-only carries no danger of exposure, the electricity cost is small, and you can rebuild it no matter how many times you break it. Use an old PC if you have one; if not, rent a VPS for a few days as a practice rig. The basics of a server — minimal install, user management, SSH, running services — can all be learned on this experimental machine.

**Only at the stage of publishing (Chapter 9) do you choose how to build the entrance — dig a tunnel from home, or rent a VPS as the entrance.** Either way, **the body and the data do not leave your home.** This is where the CGNAT problem of Section 2 and the VPS roles of Section 3 come into play. Publishing is a heavy decision, one you should step into only after understanding the threat model (Chapter 5). So this path — which lets you defer the entrance decision until the publishing stage — is the safest and the deepest in learning.

In other words, there is nothing you must rush to decide. **The body lives at home — that was settled as a premise from the start.** Start experimenting on the LAN, and decide only the "entrance" when publishing comes around. This two-stage stance minimizes the risks of cost and responsibility.

### Ask Claude ④: Build Your Own Two-Stage Plan

> As the conclusion of Chapter 2, a two-stage stance was recommended: "the body and the data stay home; first run Chapters 3 to 8 on an experimental machine inside the home LAN, then choose the entrance (home tunnel / VPS entrance) at the publishing stage."
>
> Tailored to my situation [paste again the budget, purpose, machine, line, and publishing policy you handed over in Section 2 ②], please turn this two-stage stance into a concrete plan. Show, with reasons, the machine I should use in stage one (the experimental machine) and the options available in stage two (publishing).

Copy this plan into the "Network" and "Publishing policy" fields of `my-server.md`, and Chapters 3 onward will not wobble. The draft you made in Chapter 1 gets one notch more concrete here.

## Summary

What you did in this chapter:

1. Understood that the location is the first design decision, settling all three of "cost, responsibility, and network."
2. Lined up the three — home machine, VPS, major cloud — in a comparison table.
3. Faced the reality of a home server squarely (estimating electricity, the line and CGNAT, outages / heat / dust).
4. Sorted out the pros and cons of a VPS and the axes for choosing one.
5. Built, together with Claude, a two-stage plan of "the body stays home; the entrance is chosen at the publishing stage."

What you hold now:
- A comparison table of the three options (applied to your own situation).
- A cost estimate for home vs. VPS.
- The two-stage plan copied into `my-server.md`.

In Chapter 3, on the experimental machine you decided on, we finally do the **minimal install**. What differs from the desktop edition's install, what to choose for a server, and what not to install — together with Claude, we stand up one screenless Debian.

---

The server sub-series can be navigated from [Learning Debian with Claude — Server Edition](/en/claude-debian/server/). The main desktop series is at [all chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
