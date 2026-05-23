---
slug: claude-debian-05-installation-overview
lang: en
number: "05"
title: Chapter 5 — Understanding the Installation Picture with Claude
subtitle: Before the steps, understand what is happening
description: Before launching the installer, work with Claude to grasp the overall picture of the Debian installation process. ISO download, USB creation, boot, partitioning, network, package selection, bootloader — sort out the role and the decisions of each stage in advance.
date: 2026.04.23
label: Claude × Debian 05
prev_slug: claude-debian-04-dependency-inventory
prev_title: Chapter 4 — Taking Stock of Dependencies
next_slug: claude-debian-06-hardware-choice
next_title: Chapter 6 — Choices That Fit Your Hardware
cta_label: Learn with Claude
cta_title: Hold the map before tracing the steps.
cta_text: If you proceed without understanding what "burn the ISO and boot" actually means, you get lost the moment an error appears. Grasp the whole picture, then enter the individual steps — that order pays off when trouble strikes.
cta_btn1_text: Continue to Chapter 6
cta_btn1_link: /en/claude-debian/06-hardware-choice/
cta_btn2_text: Back to Chapter 4
cta_btn2_link: /en/claude-debian/04-dependency-inventory/
---

## Why Start from "the Whole Picture"

Most installation articles start with a procedure: "download → create USB → boot → ..." That works fine when it works, but the moment it doesn't, you no longer know where you are. It is like climbing a mountain without a map.

In this chapter we break the Debian installation into eight stages. Together with Claude, we understand what each stage is for, what decisions it requires, and what can fail. The individual steps are covered in Chapters 6, 7, and 8. **You don't even need a USB stick yet. We're just building a map in your head.**

### Conclusion first — installing Debian 13 is easier than installing Windows

One mindset note before diving in.

**Installing Debian 13 (Trixie) is easier than a fresh Windows 11 setup.** This is the author's conclusion after doing it on real hardware.

- The netinst ISO **ships with non-free firmware included by default** (since Debian 12). Wireless and GPU firmware no longer derails the install.
- If you pick Japanese (or other locales with bundled IMs) for language, **the installer pulls Fcitx5 + Mozc automatically**. Most of what Chapter 10 used to walk through by hand is no longer necessary.
- Partitioning is **"use whole disk + encrypt" — one choice**. The installer handles LVM and volume layout for you.
- After reboot, **Wi-Fi, GPU, audio, and suspend tend to work out of the box** on a wider range of machines than they used to.

You can mentally skip every Windows 11 setup chore: the Microsoft account requirement, the wall of consent dialogs, the OneDrive push, the Copilot opt-in. The reason we still decompose the install into eight stages is **not because it's complicated** — it's so that, if something does break, you don't lose your place. In practice the steps run almost in a straight line.

### Two things to do on the Windows 11 side first

The "easier than Windows" line above comes with a caveat. **If your current PC ships with Windows 11, there are exactly two things you must do on the Windows side before booting the Debian installer.**

1. **Disable BitLocker (Device Encryption).**
   On recent Windows 11 machines, **BitLocker is enabled by default**. If you leave it on, the Debian installer can't read the disk cleanly, and in the worst case the Windows-side data becomes unrecoverable. Go to `Settings → Privacy & security → Device encryption` and turn it off, then wait for decryption to complete (this takes anywhere from tens of minutes to several hours). On Windows Pro, disable it from the "BitLocker Drive Encryption" control panel instead.
2. **Disable Fast Startup.**
   `Control Panel → Power Options → Choose what the power buttons do → Change settings that are currently unavailable → uncheck "Turn on fast startup"`. With Fast Startup on, Windows doesn't fully flush disk state on shutdown, which leads to the Debian installer either failing to see your USB or seeing the disk as corrupt.

Once those two are done and you reboot, the PC is in a "ready to install Debian" state. Put another way: **most "stuck during the Debian install" stories are not Linux-side problems — they're missed Windows-side prep**.

## Section 1 — The Eight Stages of Installation

### 1. Obtaining the ISO Image

Download a file with a `.iso` extension from the Debian official site. This is the "OS as a single package."

Decision points:
- **Edition.** Stable / Testing / Unstable. **For beginners, Stable, no question.** (At the time of writing, that means Debian 13 "Trixie.")
- **Type.** netinst (a small ISO that pulls additional packages from the network during install) / DVD (self-contained offline). **If your network is decent, netinst.**
- **Architecture.** amd64 (a normal Intel / AMD PC) / arm64 (Raspberry Pi, certain ARM devices). **For a normal PC, amd64.**
- **Firmware.** Since Debian 12, the official netinst ISO **already includes non-free firmware**. **You no longer need to hunt for a separate `-firmware` image** — older articles still say so, but just grab the standard netinst from debian.org.

### 2. Creating a USB Boot Medium

Write the downloaded ISO onto a USB stick. The USB stick becomes a "bootable Debian installer."

Decision points:
- **Writing tool.** On Windows: Rufus. On macOS: Balena Etcher or `dd`. On an existing Linux: `dd` or Etcher.
- **USB capacity.** 8 GB is plenty (the netinst ISO is around 500 MB).
- **Everything on the USB will be erased.** Use a stick that doesn't hold anything important.

### 3. Changing the PC's Boot Order (UEFI / BIOS)

Configure the PC to boot from the USB instead of the SSD when you turn it on. This is where people get stuck.

Decision points:
- **Entering UEFI.** The key differs by maker (Dell: F12, HP: F9 or Esc, Lenovo: F12, ThinkPad: Enter → F12, ASUS: F2 / Del, custom builds: Del / F2).
- **Secure Boot.** Debian 12 and later support it, but turning it off at first is safer.
- **Fast Boot / Fast Startup.** Always disable Windows' Fast Startup (it can cause USB to not be recognized).
- **TPM.** Leave it enabled.

### 4. Launching the Installer

Boot from the USB, and the Debian installer screen appears.

Decision points:
- **Graphical install.** A clear, mouse-friendly screen. **For beginners, this.**
- **Install.** Text-based. For advanced users.
- **Advanced options.** Expert mode and the like. Don't touch yet.

### 5. Basic Settings (Language, Region, Keyboard, Hostname)

In the first few screens of the installer, choose options for an English (or Japanese) environment.

Decision points:
- **Language.** Selecting English makes the menus and initial packages English-language.
- **Region.** Selecting your country sets the time zone and the default repository.
- **Keyboard.** "American English" for a US keyboard, "Japanese" for a Japanese keyboard.
- **Hostname.** A name for this PC. Something easy to recognize, like `debian-taro`. Avoid company name or your real name.
- **Domain name.** Leave blank.

### 6. Partitioning and Disk Encryption

Decide how to split the disk and where to put Debian. **The most important stage in this chapter.**

Decision points:
- **If Windows remains, wipe it.** Following the policy decided in earlier chapters: wipe and give the entire disk to Debian.
- **Use the entire disk vs. manual.** First time, "use the entire disk" is safe.
- **LVM or not.** Keep it simple the first time. This book recommends not using LVM.
- **Encrypt or not.** On a laptop, **enable LUKS full-disk encryption**. Your data is protected if the machine is stolen. You will need to enter a passphrase at boot (it is worth doing).
- **Swap.** A swap partition the same size as RAM. If you don't hibernate, less is fine.

### 7. Packages and Network Settings

Choose which apps to install first. The required packages are pulled over the network.

Decision points:
- **Mirror.** A nearby mirror is fast (e.g., `jp.debian.org` if you're in Japan). `deb.debian.org` auto-routes and works fine too.
- **Software selection.** Choose "Debian desktop environment," "GNOME," and "standard system utilities." That gets you a comfortable minimum (we revisit this in Chapter 9).
- **Input method.** If you chose Japanese (or another locale with a bundled IM) for the language, **Fcitx5 + Mozc gets installed automatically**. Chapter 10 is now about polishing and customizing it, not installing it from scratch.
- **SSH server.** Install if you want to log in from another PC. Beginners can leave it off for now.

### 8. Installing the Bootloader (GRUB)

Finally, write the bootloader so that Debian starts when you turn the PC on.

Decision points:
- **Which disk to write to.** **Choose the head of the disk Debian is being installed on (e.g., `/dev/sda`).**
- **If Windows isn't left, the GRUB question is simple.** Another reason to avoid dual-boot.

### Reboot and First Login

Pull out the USB and reboot. Encryption passphrase → login screen → desktop. Reaching here completes Stage One.

## Section 2 — Have Claude Organize the Whole Picture

### Ask Claude ①: A Process Plan for Your Own Environment

> Based on my `my-system.md`, please make a clean install of Debian 13 Stable concrete, following the eight stages above.
>
> For each stage:
> (1) Points I should pay extra attention to in my environment.
> (2) Common failure patterns and how to avoid them.
> (3) A rough estimate of how long the stage takes.
>
> [paste `my-system.md`]

The process plan that comes back is the deliverable of this chapter. Save it as a text file called `install-plan.md`.

### Ask Claude ②: UEFI Steps for My Specific Machine

> My PC is [maker / model]. Please tell me, with the specific keys for this machine, how to enter UEFI setup, how to set USB as the boot priority, and how to change Secure Boot and Fast Boot.
>
> If there are model-specific pitfalls (behavior differs by BIOS version, BitLocker enabled means you lose the encryption key, etc.), please warn me about them.

Claude returns the steps for your machine. Print this out and it becomes a help when USB boot gets stuck.

## Section 3 — Failure Patterns and the Way Back

### Five Typical Installation Failures

Most of these are largely resolved in Debian 13. Keep them in mind as the **residual landmines**.

**Failure 1: USB is not recognized.**
Causes: Fast Startup enabled, Secure Boot configuration, USB stick compatibility, USB 3.0 port compatibility.
Fix: Disable Fast Startup, turn off Secure Boot for now, try a different USB port and a different USB stick. **This still happens with Debian 13 — but the problem is on the Windows / UEFI side, not Linux.**

**Failure 2: The installer can't reach the network.**
Cause: the classic one used to be "missing wireless firmware," but **since Debian 12 the official netinst ISO ships firmware bundled**, so this is now rare. What remains is extremely new wireless chips or corporate proxies.
Fix: Just plug in over wired LAN, or USB tether from a phone.

**Failure 3: The partitioner can't see the existing Windows.**
Causes: BitLocker is encrypting the disk and it can't be read; an unusual RAID setup.
Fix: Decrypt BitLocker on the Windows side beforehand. **Windows 11 sometimes enables BitLocker silently by default**, so check before migrating.

**Failure 4: GRUB installation fails.**
Causes: wrong target disk, UEFI / BIOS mixing.
Fix: Redo it. Specify the GRUB target correctly. If you're doing a clean install with no Windows left, this is basically "pick the internal SSD" — one click.

**Failure 5: The screen is black after reboot.**
Causes: NVIDIA discrete GPU driver issues, certain integrated GPU compatibility issues.
Fix: Add `nomodeset` to the boot options (covered in Chapter 8). **For Intel / AMD integrated GPUs, this rarely happens.**

### Secure a "Way Back" in Advance

Before installing, prepare a path back in case things go wrong.

1. **A full backup to external storage.** Clone the Windows state (Macrium Reflect Free, Clonezilla, etc.). Worst case, you can return to the original Windows.
2. **Keep an old PC running.** You won't be able to use a search engine or Claude on the machine being installed, so keep a separate PC or your phone at hand.
3. **Have at least two USB sticks.** One is the Debian installer; the other is Windows recovery media (which you can build with Microsoft's official tool).

### Ask Claude ③: Confirm the Way Back

> I am planning a migration from [Dell Latitude 7420, Windows 11 Pro] to Debian.
> Please confirm the paths back to Windows in case the install fails, in three tiers:
>
> (1) Ideal: Windows can be restored without any trouble.
> (2) Insurance: Windows can be restored with one to several days of work.
> (3) Last resort: recovery is possible but requires a repair shop or repurchase.
>
> For each tier, list what I should prepare in advance.

## Section 4 — Build a Schedule

### A Recommended Time Allocation

The install itself takes **about 1–2 hours of real time on Debian 13**. With backups and a buffer for surprises, half a weekend day is a sensible reservation.

- **Preparation (morning of the day onward): 1–2 hours.**
  USB creation, confirming UEFI settings, the final backup check.
- **Installation proper: 30 min – 1 hour.**
  Including package downloads. Most of it is watching the bar move while you drink coffee.
- **Initial verification: 30 min – 1 hour.**
  Wireless LAN, display, sound. **On Debian 13 most of this just works**; you're confirming, not configuring.
- **First-round troubleshooting buffer: 1–2 hours.**
  Comfortable headroom in case one thing trips.

Total: 3–6 hours. **The install experience should feel shorter than a fresh Windows 11 setup.** But "fast" is not the same as "sloppy" — don't skip judgment calls to save time.

### Always Set Aside a Reserve Day

Don't start Friday night with work on Monday morning. Install on Saturday and keep Sunday as the reserve day. Even if something goes wrong, you can be back to a state where you can work by Monday.

### Ask Claude ④: My Schedule

> Considering my available time slots and deadlines [describe], I want to plan the install.
> Based on my situation (`my-system.md`), the process plan above, and the trouble patterns, please draft a realistic schedule. Include the reserve day and the day for securing the way back.

## Summary

What you did in this chapter:

1. Broke the installation into eight stages and grasped the whole picture.
2. Got hold of the decision points at each stage.
3. Built `install-plan.md`, a process plan for your own PC.
4. Confirmed failure patterns and the way back in advance.
5. Drew up a realistic schedule.

What you hold now:
- `install-plan.md` (a process plan customized to you).
- A note of the UEFI steps for your specific machine.
- A schedule.

In Chapter 6, we go deeper into "choices that fit your hardware." Concrete decisions about the desktop environment (GNOME / KDE / Xfce, etc.), filesystem, and encryption method get pinned down to your specific PC.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
