---
slug: claude-debian-06-hardware-choice
lang: en
number: "06"
title: Chapter 6 — Choices That Fit Your Hardware
subtitle: Desktop environment, filesystem, encryption — decide based on your PC
description: Choose the desktop environment (GNOME / KDE / Xfce / LXQt), filesystem (ext4 / btrfs / xfs), and encryption method (LUKS) for your specific hardware. Together with Claude, arrive at the best fit given the constraints of your machine and use case.
date: 2026.04.23
label: Claude × Debian 06
prev_slug: claude-debian-05-installation-overview
prev_title: Chapter 5 — Understanding the Installation Picture with Claude
next_slug: claude-debian-07-installation-execution
next_title: Chapter 7 — The Dialogue of the Install
cta_label: Learn with Claude
cta_title: The best choice differs from person to person.
cta_text: "GNOME is best," "ext4 is the safe pick" — generalities exist, but what is best for you is determined by your hardware and your use case. Make that call together with Claude.
cta_btn1_text: Continue to Chapter 7
cta_btn1_link: /en/claude-debian/07-installation-execution/
cta_btn2_text: Back to Chapter 5
cta_btn2_link: /en/claude-debian/05-installation-overview/
---

## What This Chapter Is For

In Chapter 5 we surveyed the eight stages of installation. Among them, the ones with **the most room for judgment** are the desktop environment, the filesystem, and the encryption method. Once decided, these three are hard to change later (not impossible, but expensive). Chapter 6 pins down these three for your specific PC.

## Section 1 — Choosing a Desktop Environment

### Features of the Major Candidates

There are four representative desktop environments to choose from on Debian.

**GNOME**
- Character: a modern, polished UI; good touch-screen support; tablet-like feel.
- Strengths: the official default, rich extensions, a large community.
- Weaknesses: relatively heavy on memory (2–3 GB); customization has its quirks.
- Suits: **a newer laptop (2019 or later), 16 GB or more RAM, a touch-capable machine.**

**KDE Plasma**
- Character: a Windows-style taskbar; abundant settings.
- Strengths: highly customizable; familiar to people coming from Windows.
- Weaknesses: too many settings can be confusing; occasionally feels heavy.
- Suits: **people moving from Windows, people who enjoy customization.**

**Xfce**
- Character: lightweight; a traditional UI.
- Strengths: comfortable on older PCs; stable; low memory footprint (runs in under 1 GB).
- Weaknesses: appearance is plain; distant from the latest UI trends.
- Suits: **PCs older than 2015, 8 GB or less RAM, when lightness is the priority.**

**LXQt**
- Character: ultra-lightweight; Qt-based.
- Strengths: the smallest memory footprint; brings old PCs back to life.
- Weaknesses: minimal feature set; integration of input methods (e.g., for Japanese) needs effort.
- Suits: **PCs more than ten years old, 4 GB or less RAM.**

### Define Your Decision Axes

There are three axes for choosing a desktop environment.

1. **Hardware performance:** memory, CPU, GPU generation.
2. **Closeness to Windows feel:** how much switching cost you can absorb.
3. **Aesthetic preference:** you'll use this every day, so liking the look matters more than people admit.

### Ask Claude ①: A Desktop Environment That Fits Me

> Based on the environment in `my-system.md` and how I use it from `my-claude-profile.md`, please compare the following four desktop environments: GNOME, KDE Plasma, Xfce, LXQt.
>
> Compare on:
> (1) Whether each runs comfortably on my hardware (expected memory usage, CPU load).
> (2) For me, coming from Windows, how close the feel is.
> (3) Initial learning cost (settings, shortcuts).
> (4) Long-term maintenance cost (stability of updates).
> (5) Ease of integrating Japanese input (Mozc, Fcitx5).
>
> Finally, recommend the single best option for me, with the reason.

This answer determines what to choose on the "Software selection" screen during the Chapter 7 install.

## Section 2 — Choosing a Filesystem

### Major Candidates

**ext4** (the default)
- The most widely used on Linux.
- Mature and stable; few problems.
- No snapshot feature.
- **For your first time, ext4 is the best choice.**

**btrfs**
- Snapshots (you can roll time back), compression, subvolumes.
- Configuration is somewhat complex; under heavy write loads, there have been past trouble reports.
- For advanced users, or for server use.

**xfs**
- Optimized for very large files.
- Few reasons to pick it for desktop use.

### What This Book Recommends

**Start with ext4. Reconsider only if you find a real reason to be unhappy.**

The snapshot feature of btrfs is appealing, but using it well takes learning. Rather than getting stuck starting on btrfs from day one, it's more practical to run your daily life on ext4 while taking backups to an external SSD via `rsync`.

### Ask Claude ②: Confirm the Filesystem Choice

> I plan to install Debian 12 on [SSD/HDD, capacity]. The use case is [daily work, development, media editing, etc.].
>
> I'm leaning toward ext4. Please judge whether this choice is reasonable for my use, and whether there is a scenario in which switching to btrfs would be worth it.

## Section 3 — The Encryption (LUKS) Decision

### Encrypt Laptops

A laptop carries a real risk of theft or loss. Without encryption, whoever takes the SSD can plug it into another machine and read everything — family photos, work documents, saved passwords, the lot.

**Always enable LUKS full-disk encryption on a laptop.**

### For Desktop PCs, It Is Optional

A desktop that doesn't leave home has low theft risk, so encryption is optional. That said, encryption gives you peace of mind when selling or disposing of the machine.

### The Cost of Encryption

- **Passphrase entry.** At boot, you enter a roughly 20-character passphrase once (separate from the login password).
- **Performance impact.** Modern CPUs accelerate encryption in hardware (AES-NI), so you're unlikely to feel a difference.
- **Forget it and it's over.** If you forget the passphrase, the data is gone. Always record it somewhere.

### Ask Claude ③: The Final Encryption Call

> My PC is [a laptop / a desktop], and the main place I use it is [home / I take it out / a café / I move around a lot].
>
> Please judge, with reasons, whether I should enable LUKS full-disk encryption.
>
> If I should, give me a guideline for passphrase strength, and the rescue plan if I forget (backup, emergency recovery key).

### Choosing a Passphrase

Choose your encryption passphrase under these conditions.

- **At least 20 characters**, made of words combined together (the `correct horse battery staple` pattern).
- **A combination not in any dictionary** (a context only you know).
- **Memorable enough that you can type it every morning.**
- **Written on paper and stored as a valuable** (do not save it digitally).

## Section 4 — What to Pick on the Software Selection Screen

Late in the install, a "Software selection" screen appears. The book's recommendation is below.

### Minimal Configuration (Recommended)

- [x] **Debian desktop environment**
- [x] **[the DE you chose in Section 1]** (e.g., GNOME, KDE Plasma, Xfce)
- [x] **standard system utilities**
- [ ] print server (only if you use a printer)
- [ ] SSH server (only if you want to access from outside)
- [ ] web server (not needed)

You can install everything else later via `apt`. Start minimal and add as needed — that is also easier to operate over time.

### "Debian Desktop Environment" vs. a Specific DE

Selecting "Debian desktop environment" installs the basic GUI packages. On top of that, selecting one specific DE (GNOME or KDE) also installs the packages dedicated to that DE. Checking both is the standard choice.

### Ask Claude ④: My Checkbox Configuration

> My choice of desktop environment is [the result from Section 1].
> Based on my use case [paste again], please pin down which items to check and which to uncheck on the "Software selection" screen during install.
>
> I want to keep it minimal at the start, on the assumption that I'll add things later with `apt install`.

## Section 5 — Consolidate the Decisions onto a Single Page

Compile the decisions so far into a checklist for install day.

```markdown
# My Debian Install Settings  (2026-04-23)

## Basic choices
- Debian edition: 12 Stable
- ISO: netinst, amd64, with firmware
- Installer: Graphical install
- Language: English (or Japanese)
- Region: [your country]
- Keyboard: [JP / US English]
- Hostname: [decide]
- Domain: (blank)

## Desktop
- Desktop environment: [GNOME / KDE / Xfce]
- Reason: [from the Section 1 dialogue with Claude]

## Disk
- Disk usage: entire disk, no LVM
- Filesystem: ext4
- Encryption: [enabled / disabled]
- Swap: [size]

## Passphrases
- Encryption passphrase: written on paper (in [the safe / etc.])
- Login password: [managed separately]

## Software selection screen
- [x] Debian desktop environment
- [x] [the DE chosen]
- [x] standard system utilities
- [ ] print server
- [ ] SSH server
- [ ] web server

## Mirror
- Nearby mirror (e.g., `jp.debian.org` or a local `deb.debian.org`)

## Bootloader
- Install GRUB
- Target: [/dev/sda or similar]
```

Print this checklist and have it on hand on install day. Confirm each item against what's on screen. **If you move to Chapter 7 with this not yet filled in, you'll lose time mid-install thinking it through.**

## Summary

What you did in this chapter:

1. Compared the four desktop-environment candidates against your hardware.
2. Locked in ext4 as the filesystem (consider btrfs later if you have reason to).
3. Sorted out the LUKS encryption call for laptop vs. desktop.
4. Decided what to pick during install for software selection.
5. Built a single-page checklist for install day.

What you hold now:
- `install-config.md` (the install-day checklist).
- A physical note of the passphrase.

In Chapter 7, "The Dialogue of the Install," we finally launch the Debian installer and walk through this checklist with hands on the keyboard. We cover concrete dialogue examples, checking with Claude at each screen.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
