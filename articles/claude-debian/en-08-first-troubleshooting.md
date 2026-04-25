---
slug: claude-debian-08-first-troubleshooting
lang: en
number: "08"
title: Chapter 8 — The First Round of Troubleshooting
subtitle: Display, Wi-Fi, sound, Bluetooth, suspend — knock down the seven usual suspects with Claude
description: Resolve the seven categories of trouble most commonly hit right after install — display resolution / scaling, Wi-Fi, Bluetooth, sound, suspend, Japanese input, external monitor — step by step with Claude. Learn how to capture and hand over logs.
date: 2026.04.23
label: Claude × Debian 08
prev_slug: claude-debian-07-installation-execution
prev_title: Chapter 7 — The Dialogue of the Install
next_slug: claude-debian-09-desktop-environment
next_title: Chapter 9 — Tuning the Desktop Environment
cta_label: Learn with Claude
cta_title: Not "everything is broken." Fix one thing at a time.
cta_text: When everything feels off right after install, breaking it down calmly usually leaves only two or three actually broken. This chapter teaches the craft of breaking it down and handling each piece.
cta_btn1_text: Continue to Part 3 / Chapter 9
cta_btn1_link: /en/claude-debian/09-desktop-environment/
cta_btn2_text: Back to Chapter 7
cta_btn2_link: /en/claude-debian/07-installation-execution/
---

## Break Down "It's Not Working"

When you feel "something is not working" right after install, don't panic — break it down. Check, in each of the following seven categories, whether things work or not.

1. Display (resolution, scaling, external monitor)
2. Wi-Fi (connects, speed, stability)
3. Bluetooth (mouse, keyboard, earphones)
4. Sound (built-in speakers, headphones, microphone)
5. Suspend / resume (close the lid and open it, power saving)
6. Japanese input (Fcitx5 + Mozc)
7. Peripherals (printer, webcam, USB devices)

**It is rare for everything to work. Two or three things will be off. Knocking those down one at a time is what Chapter 8 is for.**

## Section 1 — Common Diagnostic Practice

### Capture Logs and Hand Them Over

A strength of Linux is that everything that happens leaves a trace in the logs. There are three kinds of information you'll want to hand to Claude in trouble.

**1. System logs.**
```bash
journalctl -b -p err          # errors since this boot
journalctl -b --since "10 min ago"   # the last 10 minutes
```

**2. Hardware recognition state.**
```bash
lspci -nnk                    # PCI devices and their drivers
lsusb                         # USB devices
dmesg | tail -50              # tail of kernel messages
```

**3. The state of a specific service.**
```bash
systemctl status <service-name>
systemctl --failed            # list of failed services
```

### Ask Claude (Template): A Common Troubleshooting Prompt

A template prompt that works for any kind of trouble.

> On my Debian 12 [DE name], [symptom] is happening.
>
> Machine: [maker / model]
> What I did just before: [the action]
>
> Below is information about my environment:
> ```
> $ uname -a
> [output]
> $ lspci -nnk | grep -A 2 -i [related keyword]
> [output]
> $ journalctl -b -p err
> [output]
> ```
>
> Please list the three most likely causes in descending order of likelihood, with steps to verify each.
> Add a warning note for any destructive command.

Having this template raises the quality of Claude's answer significantly.

## Section 2 — Display

### Symptom: low resolution, blurry text

This is mostly about the GPU driver. Try the following.

```bash
# Confirm the current driver
lspci -nnk | grep -A 2 VGA

# Intel / AMD work with the standard drivers in most cases.
# NVIDIA may need a separate package.
```

For a discrete NVIDIA GPU, install `nvidia-driver` from the non-free-firmware repository.

```bash
# Confirm contrib non-free non-free-firmware are in /etc/apt/sources.list
cat /etc/apt/sources.list

# Add them if needed (ask Claude for the exact format)
sudo apt update
sudo apt install nvidia-driver
sudo reboot
```

### Symptom: external monitor doesn't show

```bash
# Connected displays
xrandr                        # X11
gnome-randr                   # Wayland on GNOME (apt install if needed)

# Resolution settings
Settings → Display → Arrangement and resolution
```

### Symptom: HiDPI (high resolution) makes the UI too small

- GNOME: Settings → Display → Scale 125% or 150%
- KDE Plasma: System Settings → Display and Monitor → Global scale
- Xfce: takes a bit of effort. Ask Claude for the `xfconf-query` settings.

## Section 3 — Wi-Fi and Network

### Symptom: Wi-Fi doesn't connect at all

The wireless chip's firmware is most likely missing.

```bash
# Identify the chip
lspci -nnk | grep -A 2 -i net

# Recognition state
dmesg | grep -i firmware
```

Install the needed firmware package — `firmware-iwlwifi` (Intel), `firmware-realtek`, `firmware-atheros`, etc.

```bash
sudo apt install firmware-linux firmware-linux-nonfree
sudo reboot
```

### Symptom: connects but slow / drops

The 2.4 GHz band may be congested. If a 5 GHz SSID is available, switch to it. Power saving can also misbehave.

```bash
# Power-saving state
iw dev <interface-name> get power_save
```

## Section 4 — Sound

### Symptom: no sound

```bash
# Confirm sound devices
pactl list sinks short

# Mixer
pavucontrol             # GUI mixer; apt install pavucontrol if needed
```

Common causes:
- The default output is wrong (going to HDMI, or muted).
- Headphone-detection auto-switching is misbehaving.
- A Bluetooth device is being prioritized.

### Symptom: microphone doesn't pick up

In `pavucontrol`'s "Input Devices" tab, check the input level. Confirm it isn't muted and that gain isn't at 0.

## Section 5 — Bluetooth

### Symptom: Bluetooth devices aren't found

```bash
# Bluetooth service
systemctl status bluetooth

# If it isn't running
sudo systemctl enable --now bluetooth
```

Some chips need firmware. Check with `dmesg | grep -i bluetooth`.

## Section 6 — Suspend / Resume

### Symptom: closing and reopening the lid doesn't bring it back

This is the trickiest issue on a laptop. The cause is a combination of kernel, drivers, and UEFI settings.

**First things to try:**
- In BIOS / UEFI, switch between `S3 sleep` and `Modern Standby (S0ix)` (if the option exists).
- Add `mem_sleep_default=deep` to the GRUB kernel parameters.

**Ask Claude:**

> On my [model], resume from suspend fails.
> Symptom: after closing the lid and waiting more than 5 minutes, opening it leaves the screen black.
> Kernel: [output of uname -a]
>
> Tell me the five most effective things to try, in order of effectiveness. Include the side effects of each step and how to revert.

### Symptom: battery drains fast

```bash
# Power consumption state
sudo apt install powertop
sudo powertop
```

Try `powertop --auto-tune` for automatic optimization (note: some optimizations reduce usability, so be careful).

## Section 7 — Japanese Input

### Standard Configuration: Fcitx5 + Mozc

```bash
sudo apt install fcitx5 fcitx5-mozc fcitx5-config-qt
```

After install, run `im-config -n fcitx5`. Log out and back in.

Key bindings: the Hankaku/Zenkaku key, or Ctrl+Space (configurable in settings).

### Symptom: Japanese input doesn't work in a specific app

Electron-based apps and Snap packages sometimes use a different input-method mechanism than the standard.

Ask Claude:

> With Fcitx5 + Mozc, only [app name] won't accept Japanese input.
> Launch command and environment variables: [output of `env | grep -i xim` or `GTK_IM_MODULE`, etc.]
>
> Tell me the environment variables or settings that need to be set on the app side.

## Section 8 — Peripherals

### Printers

Debian supports many printers via CUPS.

```bash
sudo apt install cups
sudo systemctl enable --now cups
```

Open http://localhost:631 in a browser to add a printer. Canon, Epson, and Brother sometimes provide a separate driver for the Japanese market on the maker's site.

### Webcam

```bash
# Recognition check
v4l2-ctl --list-devices

# Test
sudo apt install cheese
cheese
```

## Section 9 — Priority Order for "Not Working"

When several issues show up at once, knock them down in this order.

1. **Wi-Fi** (without it you can't look anything up).
2. **Display** (you use it every day).
3. **Sound** (a problem in meetings).
4. **Japanese input** (affects most daily work).
5. **Suspend / battery** (gets in the way of constant use).
6. **Bluetooth** (alternatives are usually available).
7. **Printer, webcam** (handle when needed).

Don't try to solve everything at once. Once Wi-Fi works, you can knock down the rest in dialogue with Claude.

### Ask Claude ⑥: Prioritize My List of Trouble

> Right after install, the following issues are happening:
> - [symptom 1]
> - [symptom 2]
> - [symptom 3]
>
> Tell me the order in which to knock them down, the expected time for each, and the very first step I should try.

## Section 10 — Keep a Trouble-Resolution Log

For every issue you knock down, record it in a text file.

```markdown
# My Debian Trouble-Resolution Log

## 2026-04-24 Wi-Fi wouldn't connect
- Symptom: right after install, the Wi-Fi list was empty
- Cause: firmware-iwlwifi was not installed
- Fix: sudo apt install firmware-iwlwifi; sudo reboot
- Reference: dialogue with Claude (saved at: [location])

## 2026-04-25 Black screen after closing and reopening the lid
- Symptom: resume from suspend failed
- Cause: Modern Standby vs. Linux compatibility
- Fix: switched BIOS to "Linux" mode + added mem_sleep_default=deep to GRUB
```

This log will help you in the future. When the same issue comes back, when someone else asks you about a similar issue, when you reinstall.

## Summary

What you did in this chapter:

1. Got the common diagnostic commands (journalctl, lspci, dmesg) under your fingers.
2. Covered the typical issues for display, Wi-Fi, sound, Bluetooth, suspend, Japanese input, and peripherals.
3. Established the practice of knocking them down by priority.
4. Built `troubleshooting-log.md`.

Where you are now:
- A Debian environment usable day to day.
- A personal log for when things stumble.

This closes Part 2 (Installation). In Part 3 (Chapters 9–12), we move into **building the daily environment**. Going deeper into the desktop environment, finalizing Japanese input, choosing daily-use applications, and managing config files — together with Claude.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
