---
slug: claude-debian-03-telling-environment
lang: en
number: "03"
title: Chapter 3 — How to Tell Claude About Your Environment
subtitle: Pulling hardware and software information and handing it to Claude in a structured form
description: To get sharp answers from Claude, you need to convey your own environment accurately. This chapter covers how to extract environment information on Windows / macOS / Linux, how to pick what to send out of that output, and how to shape it into a form Claude can read easily.
date: 2026.04.23
label: Claude × Debian 03
prev_slug: claude-debian-02-starting-conversation
prev_title: Chapter 2 — How to Begin a Dialogue with Claude
next_slug: claude-debian-04-dependency-inventory
next_title: Chapter 4 — Taking Stock of Dependencies
cta_label: Learn with Claude
cta_title: Claude is not a mind-reader.
cta_text: You need a way to "show" Claude what is running on your PC. This chapter is where you pick up that craft. Once you have it, every piece of troubleshooting from here on moves faster.
cta_btn1_text: Continue to Chapter 4
cta_btn1_link: /en/claude-debian/04-dependency-inventory/
cta_btn2_text: Back to Chapter 2
cta_btn2_link: /en/claude-debian/02-starting-conversation/
---

## Why a Whole Chapter on "Telling Your Environment"

Chapter 2 laid out how important it is to "hand over context." Chapter 3 zeroes in on the most concrete part of that context — hardware and software information — and covers how to pull it out, how to shape it, and how to hand it to Claude.

Before you get into installing Debian, you need to grasp the particulars of the PC you are using now. Is the CPU 64-bit? How much memory? What storage? What wireless chip? What is installed? If these are unknown, Claude can only answer in generalities.

By the end of this chapter, a single file called `my-system.md` will sit on your desk. That file becomes the foundation for every discussion from Chapter 4 onward.

## Section 1 — Pulling Information from Your Current OS

### Pulling It on Windows

If you are on Windows, open PowerShell (press Start and type "PowerShell") and run the following commands one by one.

```powershell
# System information
Get-ComputerInfo | Select-Object CsName, CsManufacturer, CsModel, OsName, OsVersion, CsProcessors

# Total memory
(Get-CimInstance Win32_PhysicalMemory | Measure-Object Capacity -Sum).Sum / 1GB

# Storage
Get-CimInstance Win32_DiskDrive | Select-Object Model, Size, InterfaceType

# Network adapters
Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, LinkSpeed

# Graphics
Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion

# Installed software (excerpt)
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |
  Select-Object DisplayName, DisplayVersion, Publisher |
  Where-Object { $_.DisplayName -ne $null } |
  Sort-Object DisplayName
```

### Pulling It on macOS

If you are on macOS, open Terminal (Spotlight → "terminal") and run these.

```bash
# Hardware overview
system_profiler SPHardwareDataType

# Storage
diskutil list

# Network
networksetup -listallhardwareports

# Applications
ls /Applications

# Homebrew-installed items (if you use it)
brew list
```

### Pulling It on Linux (If You Are Already on Linux)

If you are already using Linux, run the following. These are the same commands you will use on Debian after you migrate.

```bash
# CPU
lscpu

# Memory
free -h

# Storage
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE

# PCI devices (GPU, wireless LAN, etc.)
lspci -nnk

# USB devices
lsusb

# Installed packages (Debian / Ubuntu family)
dpkg -l | awk '{print $2, $3}' | head -50

# Kernel and distribution
uname -a
cat /etc/os-release
```

### Ask Claude ①: Tune the Command Set to Your OS

> I am currently on [Windows 11 / macOS Sonoma / Ubuntu 22.04, etc.].
> Please take this chapter's "commands for pulling environment information" and bundle them into a form I can run in one pass, tuned to my OS.
> Add a comment for each command explaining what it pulls. For ease when I hand the output to Claude, return the result wrapped in a Markdown code block.

The idea of having Claude shape the commands for you is itself the approach of this book. You do not need to memorize them yourself.

## Section 2 — Picking "What to Hand to Claude" Out of the Output

### Handing It All Over Is Noise

The output of `Get-ComputerInfo` or `lspci -v`, if pasted whole, runs hundreds of lines. Handing it all over makes Claude lose the thread. **What you hand over should be a focused summary.**

Pick out the following items and shape them into a single Markdown file.

### The Skeleton of `my-system.md`

```markdown
# My System Information (as of 2026-04-23)

## Machine
- Maker / Model / Year:
- CPU (model name, cores, frequency):
- Memory: ___ GB
- Storage: ___ GB (SSD / HDD, NVMe / SATA)
- GPU:
- Display: resolution, internal / external
- Wireless chip (Intel AX210, Realtek RTL8821CE, etc.):
- Bluetooth: yes / no
- Fingerprint / face recognition: yes / no, maker / model
- USB port layout: Type-A ×__, Type-C ×__, Thunderbolt yes / no

## Current OS
- OS name / version:
- BitLocker / FileVault enabled / disabled:
- Secure Boot enabled / disabled:
- TPM: present, version

## Software I Use Daily
- Browser:
- Mail:
- Office:
- Image editing:
- Music / video:
- Essential for work:

## Peripherals
- Printer (maker, model):
- Scanner:
- Pen tablet:
- External monitor:

## Network Environment
- Home Wi-Fi (2.4 / 5 / 6 GHz, encryption):
- Workplace VPN type (if any):
- Current Japanese input method:
```

Fill in each item with the corresponding information from the commands you ran in Section 1. You do not need to fill every item. For anything unknown, write "unknown."

### The Wireless Chip and the GPU Matter Most

These are the two things a Debian install trips on first.

- **Wireless chip.** Laptops vary by model. Intel chips mostly work out of the box. Broadcom and some Realtek chips need firmware separately.
- **GPU.** Integrated graphics (Intel, AMD) work without trouble. NVIDIA discrete GPUs take a little extra work on the driver side.

Always write these two into `my-system.md`. Later, when you ask Claude "will Debian run stably on my chip?", a concrete answer comes back.

### Ask Claude ②: Ask It to Shape the Information You Gathered

> I pulled the following information from my PC. [paste the output from Section 1's commands]
>
> Please shape it into my `my-system.md` skeleton:
> [paste the template above]
>
> For items you cannot determine, write "needs checking" and add the command I should run to find out.

In one round trip, you end up with a summary file of your system information on your desk.

## Section 3 — A Form That Is Easy for Claude to Read

### Forms Claude Is Good At

Claude reads the following forms especially well.

- **Markdown headings and bulleted lists.** The hierarchy is clear; there is no guessing about where things sit.
- **Tables.** The mapping between field and value is explicit.
- **Code blocks.** Always wrap command output and config files in ``` fences.
- **Short paragraphs.** No more than three or four lines each.

Conversely, avoid the following.

- Screenshots (OCR adds overhead).
- Pasted PDFs (layout breaks, hard to read).
- Heavy decorative use of emoji (processing cost rises).
- Massive text over 3,000 lines (attention thins out partway through).

### A Trick for Handing Over a Whole File

For config files or logs like `my-system.md`, hand them to Claude with **the filename stated explicitly**.

```
my-system.md:
[paste the file content as-is]
```

With this form, Claude recognizes that "this is a file," and in later exchanges you can reference it by name — for instance, "rewrite the GPU field in `my-system.md`."

### Ask Claude ③: Check the Form Itself

> Of the following two ways of writing, which is easier for Claude to handle? Please include the reason.
>
> A: "My PC is a Dell Latitude 7420, with 16 GB of memory, an i7 CPU, 512 GB SSD storage, and some kind of Intel wireless."
>
> B:
> ```
> - Maker / Model: Dell Latitude 7420 (2021)
> - CPU: Intel Core i7-1165G7 (4 cores 8 threads, up to 4.7 GHz)
> - Memory: 16 GB DDR4-3200
> - Storage: Samsung PM981a 512 GB (NVMe SSD)
> - Wireless LAN: Intel Wi-Fi 6 AX201
> ```

Claude will push for the latter. From here on, write that way yourself too.

## Section 4 — Handing It Over While Protecting Privacy

### Information Leaks That Are Easy to Overlook

Mixed into environment information are things you should not hand to Claude as-is.

- **Serial numbers.** A PC's serial is information useful for warranty or theft response. You do not need to hand it over.
- **MAC addresses / BSSIDs.** Your home Wi-Fi's MAC address or BSSID can lead to location identification.
- **Paths that include your user name.** The `John_Smith` in `C:\Users\John_Smith\Documents\` is part of your real name.
- **Mail folder names.** They often contain the names of clients or individuals.
- **Host names.** They may contain your company name.

### Re-read Once Before You Send

Once you have copied command output, **read it through once with your own eyes before pasting**. If a string worries you, replace it with something like `[REDACTED]`.

```
# Replacement examples
Host name:    YAMADA-LATITUDE-7420  →  [hostname]
User path:    C:\Users\yamada\       →  C:\Users\[user]\
MAC:          A1:B2:C3:D4:E5:F6      →  [mac]
```

This does not change the quality of Claude's answer. Your privacy is preserved.

### Ask Claude ④: Check for Sensitive Information

> Before I hand the following text to Claude, please point out places I should replace from a privacy standpoint:
>
> [paste the information you gathered]
>
> Add recommended replacement notation for each.

Having Claude judge what is sensitive is a bit paradoxical, but it works in practice. Do this once, and next time you will catch these things yourself.

## Summary

What you did in this chapter:

1. Ran commands to pull environment information from your current OS.
2. Selected "the key points to hand to Claude" from the output.
3. Consolidated them into a single `my-system.md` file.
4. Adjusted the form (Markdown, tables, code blocks).
5. Replaced anything with privacy concerns.

What you hold now:
- `my-system.md` (a summary of your system information).
- Placed alongside the `my-claude-profile.md` you made in Chapter 2, this completes your "set to hand to Claude."

In Chapter 4, using this environment information as the base, we take stock of **dependencies**. Together with Claude, we sort out "what does this software depend on?" and "what is this data tied to?", and lay out everything you should confirm before wiping Windows.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
