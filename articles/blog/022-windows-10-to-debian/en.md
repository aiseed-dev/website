---
slug: windows-10-to-debian
title: "If You Have a Windows 10 PC — Time to Install Linux"
subtitle: "In the AI era, Linux is the easier choice."
date: 2026.05.26
description: Windows 10 support ended in October 2025. Hundreds of millions of PCs worldwide are flagged as "not compatible with Windows 11." But the hardware is fine. Debian runs on the same hardware — and runs lighter. The "Linux is hard" reputation reversed twice in the AI era: first, AI is unusually good at teaching commands (and unusually bad at teaching GUI clicks); second, Flathub now provides a curated, ad-free, vendor-neutral GUI app store that is, in several ways, better-stocked than Microsoft Store. With AI beside you now, Linux commands are no longer hard. The time to try Debian is now.
lang: en
label: Blog
category: Structural Analysis Notes
hero_image: IMG_3482.webp
---

# If You Have a Windows 10 PC — Time to Install Linux

In October 2025, Microsoft ended support for Windows 10. Even with a year of ESU, individuals are about five months from the end. For businesses, $122 in October this year, $244 in October next year, and the door closes the following October.

Hundreds of millions of PCs worldwide are flagged as "not compatible with Windows 11." CPUs older than 8th gen, no TPM 2.0 — by Microsoft's standard, "no longer usable."

**For anyone who owns one of these "can't-upgrade-to-Windows-11" PCs, the answer of this article is clear-cut: you should absolutely migrate to Linux (Debian).** ESU is finite and expensive, buying a new PC is — as the next sections show — the worst possible timing, and Linux is free with the existing hardware untouched. There is, in practical terms, no other road to choose. The rest of this article is about how to carry out that "should."

Meanwhile, 2026 is the worst possible timing to buy a new PC. The AI bubble that **Microsoft itself helped trigger** has driven up memory and storage prices significantly over the past year, on the back of massive demand for AI infrastructure. One concrete number: **the same mini PC model the author uses for the hardware verification later in this post has gone up by ¥60,000 (about $400) within less than a year since purchase** — not "prices in general," but the same exact SKU, observed in real-time.

More serious than that: **the "16 GB RAM + 500 GB SSD" spec that was the standard entry-level configuration just a year or two ago is becoming hard to actually buy.** The bottom of the market has been drained by AI data-center demand, and what's left on the shelves is either "a step up from that," or a Copilot+ PC priced above ¥200,000 ($1,500). This bimodal split is not an accident.

### What is Microsoft Doing?

Lined up, Microsoft's strategy is **structurally identical to the medieval enclosure of the commons**.

1. **Chop off the bottom.** Windows 11 hardware requirements (TPM 2.0, 8th-gen CPU or later) declared hundreds of millions of working PCs "no longer usable" on paper. Copilot+ then set a new floor at NPU 40 TOPS.
2. **Drain the middle.** The AI bubble Microsoft itself stoked has pushed memory and SSD prices up, and the entry-level 16 GB / 500 GB tier is vanishing from shelves.
3. **Push only the top.** ¥200,000+ Copilot+ PCs are sold as "the next standard," with Copilot subscriptions and a Microsoft account chained to them.

Demolish the commons — working second-hand and entry-level PCs — and leave only the lord's designated, expensive plots. That is the same playbook as medieval enclosure. But every enclosure has an exit. In the medieval case it was the New World; in 2026 it is **migration to Linux**. What Microsoft wants to enclose is "Windows users," not "PC users." The hardware itself comes along to Linux untouched.

Microsoft has also created a new "Copilot+ PC" category with a fresh cutoff at NPU 40 TOPS. These machines start above $1,500 (¥200,000+).

But adding an NPU to a PC **does not change the fact that AI processing remains centralized in data centers**. Copilot's core features — drafting in Word, formula generation in Excel, summarization in PowerPoint, reply drafts in Outlook, agents — still call Azure and OpenAI's cloud. What the NPU actually runs locally is a narrow set of peripheral features: Recall, Studio Effects, parts of live captions. Despite the "AI on the edge" marketing, dependence on the Azure data centers — the actual core of the AI bubble — does not decrease.

And even after paying that much, you have no guarantee how many years a Copilot+ PC will be supported — or whether you can install Linux on it directly. In particular, **on Snapdragon (ARM) Copilot+ PCs, installing Linux is currently very hard** — the combination of bootloader, firmware, and GPU drivers leaves the community still in trial-and-error territory. You cannot just "burn an ISO and boot it" the way you can on x86 hardware. You end up paying $1,500+ for **a PC with no exit**.

Right now, the best move is to **not buy a new PC**. And in that case, Linux is the option.

## Debian as the choice

Linux has many distributions, but Debian — maintained by volunteers across the world for over 30 years — is one of the strongest candidates. It is structurally insulated from commercial vendor decisions to drop support.

Hardware that ran Windows 10 will, in most cases, run Debian 13 without issue.

## Real-hardware verification — the basis for this post

So this post isn't written in the abstract, here is the actual machine the author installed Debian 13 on and tested.

| Component | Model | On Debian 13 |
|---|---|---|
| Chassis | MouseComputer ISoDEi-I1MA (mini PC) | UEFI / TPM 2.0 left enabled |
| GPU | Intel Iris Xe Graphics (integrated) | Works out of the box on Mesa, no extra driver |
| Wi-Fi | Intel Wi-Fi 6E AX211 160MHz | `firmware-iwlwifi` bundled in netinst — **SSID list shows up right in the installer** |
| Bluetooth | Intel | Same iwlwifi package |
| Wired LAN | Realtek 2.5GbE + GbE (dual NIC) | Standard `r8169` |
| Storage | NVMe Kingston OM8TAP4512 (512 GB) | Standard `nvme` driver |
| Audio | Realtek HD + Intel SST | `snd-hda-intel` / `sof-firmware` |

Of the seven trouble categories Chapter 8 of [Learning Debian with Claude](/en/claude-debian/) lists (display, Wi-Fi, Bluetooth, audio, suspend, Japanese input, peripherals), **none of them required any work on this machine — all worked from first boot**. And because you skip every Windows 11 setup chore (Microsoft account requirement, Copilot opt-in, OneDrive push, the wall of consent dialogs), **the Debian 13 install was, if anything, faster than the Windows 11 setup that came on the same hardware**.

### Aside — I bought this PC to develop Windows apps

To be honest: **this mini PC was originally bought to develop Windows applications on**. Within six months of buying it, I'd reached the conclusion to **stop making new Windows apps**. The reasons are the ones this site has been writing about — there is no public roadmap for how many more years Windows will hold as a base, the structures that the AI era rewards lean to the Linux side, and users are walking away from Windows.

And the moment I installed Debian 13, **the hardware I bought for Windows app development turned into a "mini PC where everything except Windows runs"**. Every spec I chose for Windows (TPM, Wi-Fi 6E, NVMe, 2.5GbE) carries 100% over to Debian 13. None of the hardware was wasted. The only thing thrown away was the Windows layer on top.

One more thing worth adding: **the same mini PC model is now ¥60,000 (about $400) more expensive than when I bought it less than a year ago**. Replacing this exact spec today would cost noticeably more. So "**the value of switching to Linux now**" and "**the value of buying a new PC now**" are two different things — if you already have working hardware on hand, extending its life with Debian is a much better deal than buying new.

In a sense, this post is a hands-on demonstration of the "shift to the builder" argument from [**"In the AI Era, Become a Specialized Engineer" Misreads the Structure**](/en/blog/software-three-transitions/), carried out on the author's own bench.

## "Linux is hard" reversed in the AI era

The reputation that Linux is hard runs deep. The black screen with commands, the unfamiliar vocabulary, the lack of Windows-style click-through interfaces — all of that was true **when humans had to memorize everything alone**.

But in 2026, two structural shifts have reversed the situation.

### First — GUI operations and settings are harder for AI

It might sound counterintuitive, but for AI like Claude, **teaching you how to operate or configure something through a GUI is much harder than teaching it through commands**.

GUIs are structurally difficult to describe in words. "Third item from the top of the left menu in Settings" changes between versions. "Click the gear icon" depends on where it sits on screen. Even with a screenshot, AI can only point at roughly the right area. The deeper the settings hierarchy, the higher the cost of handing the steps to a human. Windows's deep settings, in particular, are exactly the kind of place AI has trouble guiding you through in words.

Commands are different. They live entirely in text. Claude — the most widely used AI in enterprise — writes the command, you copy and paste, and it runs as-is. If an error comes up, you paste the error text back to Claude and it can locate the cause.

**Linux's "too many commands" weakness flipped into a strength once AI sits beside you**. And at the same time, **Windows's "everything completes in the GUI" strength flipped into a weakness in the AI era**.

### Second — Flathub

For everyday apps, you don't even need a command. Open [flathub.org](https://flathub.org) and the apps that run on Linux are gathered in one place.

| Category | Apps |
|---|---|
| Browsers | Firefox, Google Chrome, Chromium, Brave |
| Office | ONLYOFFICE Desktop Editors, LibreOffice |
| Communication | Zoom, Slack, Discord, Element, Signal |
| Media | Spotify, VLC, Audacity, OBS Studio |
| Creative | GIMP, Inkscape, Krita, Blender, darktable |
| Development | Zed, VSCodium, Visual Studio Code, PyCharm, IntelliJ IDEA, Android Studio |
| Utility | Bitwarden, Joplin, Obsidian, Thunderbird |

On the office side, [Learning Debian with Claude](/en/claude-debian/) puts **ONLYOFFICE at the center, with LibreOffice as a backup**. ONLYOFFICE has high visual fidelity to MS Office and can open and return `.docx` / `.xlsx` / `.pptx` files as-is — while your own work shifts to Markdown and Python. That is the book's stance.

In Windows terms, this is the equivalent of the Microsoft Store. But Flathub is, in several concrete ways, **better stocked**.

**Microsoft Store does not carry Google Chrome.** Microsoft favors its own Edge browser and effectively excludes competing browsers. A user who wants Chrome won't find it by searching the Store and has to look elsewhere. Flathub lists Chrome, Firefox, and Brave side by side. **The lineup is not bent by the vendor's preferences.**

**Microsoft Store shows ads.** While you're looking for an app, irrelevant paid apps push themselves in as "recommendations." Flathub has no ads.

**Microsoft Store frequently asks you to sign in with a Microsoft account.** Flathub requires no account. You sign up for nothing and install what you want.

So modern Linux is **two-layered**:

- **Everyday apps**: install via Flathub's GUI. No commands needed.
- **Configuration and development**: operate via commands. This is exactly where AI shines.

These two layers are what make Linux strong in the AI era. Windows is in the awkward middle on both — its GUI doesn't reach deep settings, and PowerShell commands are awkward even for AI to handle.

## Learning with Claude

This site has two textbooks for learning with Claude beside you.

[**Learning Debian with Claude**](/en/claude-debian/) is a prologue-plus-23-chapter textbook for migrating to Debian through dialogue with Claude. What to tell Claude, how to pull environment information, how to hand it logs, what to try when you're stuck — these are less about Linux knowledge per se and more about **the discipline of learning with AI**.

[**AI-Native Ways of Working**](/en/ai-native-ways/) covers what to do after you arrive in Debian. Excel VBA into Python, Word into Markdown, CSV into JSON / SQLite — the toolkit for an era when AI is your colleague, organized across 14 chapters.

Once you internalize this discipline, it becomes the foundation **not just for Debian, but for anything you'll learn or build alongside AI from here on**.

## Now is the Time

This is not "I'm stuck with Debian because Windows 10 died." It is "Debian + AI + Flathub all came together — and now is exactly when it's a good fit."

Three years ago this would have been different. Linux commands were hard, Flathub's catalog was thinner, and AI wasn't there. **The three came together in 2026 — now**.

You can dispose of a PC anytime. You can buy a new one anytime. But **the doorway to "use the PC you already have one stage longer" is open right now — at this very moment, when Windows 10 support has ended**. If everyone in the world replaces their machine at the same time, it becomes a mountain of e-waste, and producing new PCs consumes mineral resources and fossil fuels. Whether you join that wave is, also, a choice you make now.

In the AI era, Linux is the easier choice.
AI writes the commands. Flathub installs the apps. Even old PCs run lightly.
The tools came together on the Linux side, not the Windows side.

[Learning Debian with Claude →](/en/claude-debian/)

---

*Related: [Windows is Breaking Down — How Nadella has given up on Windows](/en/blog/windows-breaking-down/)*

*Related: [Are You Still Going to Keep Using Windows and Office? — Detailed structural analysis with primary sources](/en/blog/windows-office-facts/)*

*Related: [Japan's Windows Disaster Risk — Social impact of synchronized end of support](/en/blog/japan-windows-disaster-risk/)*

*Related: ["In the AI Era, Become a Specialized Engineer" Misreads the Structure — From software engineering to liberal arts](/en/blog/software-three-transitions/)*
