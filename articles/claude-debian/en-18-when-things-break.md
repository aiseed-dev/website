---
slug: claude-debian-18-when-things-break
lang: en
number: "18"
title: Chapter 18 — When Things Break
subtitle: Won't boot, no screen, an app won't run — recover step by step
description: When Debian won't boot, you can't log in, the screen is black, an app crashes — work through these crises with Claude in graduated stages. Practical use of recovery mode, a rescue USB, and chroot recovery.
date: 2026.04.23
label: Claude × Debian 18
prev_slug: claude-debian-17-updates-maintenance
prev_title: Chapter 17 — Updates and Maintenance
next_slug: claude-debian-19-growing-environment
next_title: Chapter 19 — Growing Your Own Environment
cta_label: Learn with Claude
cta_title: The day it breaks is the day to stay calm.
cta_text: The worst call is "panic-reinstall." Work through this chapter's stages step by step, and 90% of trouble can be recovered with your data intact.
cta_btn1_text: Continue to Chapter 19
cta_btn1_link: /en/claude-debian/19-growing-environment/
cta_btn2_text: Back to Chapter 17
cta_btn2_link: /en/claude-debian/17-updates-maintenance/
---

## Stages of a Crisis

Trouble worsens through these stages. Stop it at an earlier stage and recovery is easier.

1. **An app crashes.** A problem with one app.
2. **Part of the DE doesn't work.** The panel is gone, icons don't respond.
3. **Can't log in.** Black screen after the password.
4. **Won't boot.** Doesn't get past GRUB; kernel panic.
5. **Won't get past BIOS.** Hardware suspected.

The tools differ at each stage.

## Section 1 — An App Crashes

### Identify the Symptom First

```bash
# Launch from the command line and read the error message
appname

# Example: if VSCode crashes
code --verbose
```

### Common Causes

- Extension conflict → disable them one at a time.
- Corrupted config files → rename `~/.config/<appname>/` and start with defaults.
- Out of memory → check free memory with `htop`.
- GPU acceleration issues → flags like `--disable-gpu`.

### Ask Claude ①: Triaging an App Crash

> The following app crashes right after launch: [app name, version].
>
> Output from launching it on the command line:
> ```
> [the full error]
> ```
>
> Give me three likely causes in priority order.
> List the steps to try them one at a time, starting from the non-destructive.

## Section 2 — Part of the DE Doesn't Work

### Example Symptoms

- Panel / taskbar is missing.
- Icons don't respond when clicked.
- Animations stutter.
- The screen flickers.

### Handling It

```bash
# On GNOME, X11 keys can't be pressed under Wayland; switch to a TTY
# Ctrl + Alt + F3 to log in to TTY3

# Restart the DE
systemctl --user restart gnome-shell
# Or
sudo systemctl restart gdm     # GNOME's login manager
sudo systemctl restart sddm    # KDE's
sudo systemctl restart lightdm # Xfce's
```

### Discard the Session and Try Again

Delete the specific app's settings under `~/.config/`, and `~/.cache/`, then log back in. Settings are reset, but daily work returns.

## Section 3 — Can't Log In

### Symptom: Black Screen After Password Entry

When you can't enter a session from the login manager, it is usually a session-config or home-permission problem.

### Handling It

1. **Ctrl + Alt + F3** to a TTY (text console).
2. Log in via text.
3. Look at `~/.xsession-errors`.

```bash
# Check the error log
less ~/.xsession-errors

# Suspect the config directories under home
ls -la ~/ | grep -E "\.(config|cache|local)"

# Clear the cache
rm -rf ~/.cache/*
```

### Ask Claude ②: Triaging Login Failure

> I can't log in to the Debian GUI. After entering my password the screen goes black.
> I can get into a TTY.
>
> The tail of `~/.xsession-errors`:
> ```
> [last 50 lines]
> ```
>
> Identify the cause and propose the next five steps to try, in order of risk.

## Section 4 — Won't Boot

This is where things get serious. **Stay calm and go one step at a time.**

### GRUB Doesn't Appear, or GRUB Halts

Check the boot order from BIOS. Have you accidentally prioritized the wrong disk?

### Kernel Panic

The screen turns red, or stops with a wall of errors.

1. Reboot, and when the GRUB menu appears, press `e` to enter edit mode.
2. Find the line beginning with `linux`, and add `nomodeset` at the end (avoiding GPU-related issues).
3. Press Ctrl+X to boot.

If this boots, GPU driver problems are likely. Try `sudo apt install --reinstall <the relevant driver>`.

### Boot the Previous Kernel

Selecting "Advanced options for Debian" in the GRUB menu lists past kernels. Try the previous one.

- If the older kernel boots: the problem is in the latest kernel.
- If the older kernel also fails: the problem is elsewhere.

### Ask Claude ③: Step-by-Step Diagnosis of a Failed Boot

> Debian won't boot. The symptom:
> ```
> [if you can, transcribe a phone-photo of the screen]
> ```
>
> I want to triage in this order:
> (1) BIOS boot order.
> (2) Adding kernel options from GRUB (nomodeset, etc.).
> (3) Booting the previous kernel.
> (4) Rescue mode.
> (5) chroot from a live USB.
>
> Tell me the concrete operations at each stage and how to confirm success.

## Section 5 — chroot Recovery from a Live USB

The last resort when boot is completely impossible.

### Preparation

1. Plug in the Debian installer USB you used in Chapter 7 (you should still have it).
2. Boot from USB via UEFI.
3. From the installer choices, "Rescue mode," or a Debian Live USB built on another PC.

### Steps

```bash
# Once you've booted the rescue mode or live USB
# Confirm the disks
lsblk

# Unlock if encrypted
sudo cryptsetup open /dev/nvme0n1p3 root_dm
# enter the passphrase

# Activate the logical volumes (if LVM)
sudo vgchange -ay

# Mount root
sudo mount /dev/mapper/<root_LV> /mnt
sudo mount /dev/nvme0n1p2 /mnt/boot      # if /boot is a separate partition
sudo mount /dev/nvme0n1p1 /mnt/boot/efi

# Bind-mount the necessary virtual filesystems
for d in dev proc sys run; do
  sudo mount --bind /$d /mnt/$d
done

# Enter the real environment via chroot
sudo chroot /mnt
```

From inside, run `apt`, `dpkg`, `update-initramfs`, `update-grub`, and so on, to recover.

### Ask Claude ④: Recovery Commands After chroot

> I've entered the existing system via chroot from a Debian Live USB.
> The problem: [won't boot after a kernel update / GRUB is broken / /etc/fstab is broken].
>
> Show me the recovery commands to run inside chroot, in order.
> Include what each command does and what to try next if it fails.

## Section 6 — Rescuing the Data

Even in the worst case where you give up on the system and reinstall, **rescue the data**.

### Mounting from a Live USB

```bash
# Boot the live USB
sudo mkdir /mnt/rescue
sudo mount /dev/mapper/<root_LV> /mnt/rescue
cd /mnt/rescue/home/<you>

# Mount the external SSD
sudo mkdir /mnt/backup
sudo mount /dev/sdc1 /mnt/backup

# Copy
sudo rsync -av . /mnt/backup/rescued-home/
```

Even if you reinstall the OS, the data is safe.

**This work is unnecessary if Chapter 4's "full backup" is in place ahead of time.** Preparation in advance is the peace of mind for the day it happens.

## Section 7 — Reinstalling as a Choice

When recovery truly isn't possible, **reinstalling is not failure**.

If, in Chapter 12, you put dotfiles and `apt-manual.txt` under Git, after reinstalling:

```bash
# On the new Debian
git clone https://github.com/[you]/dotfiles.git
cd dotfiles
./install.sh
./apt-restore.sh
```

In a few hours, your environment is back. **The very ability to "reinstall" is one of Debian's strengths.**

## Section 8 — Mindset for Handling Trouble

### Stay Calm

Panic breaks more things. Brew coffee, take a deep breath, write the symptoms on paper — even a few minutes' break and the picture changes when you come back.

### Change One Thing at a Time

If, while recovering, you also try this and that, you don't know what worked. **Try one thing, observe the result, then move to the next.**

### Capture Logs

Photograph the screen, save command output, note the error messages. Material to hand to Claude is also material for your future self.

### Set a Time Limit

If you decided "I'll fix this tonight," and you can't, sleep on it. After sleep, the answer often becomes visible.

### Ask Claude ⑤: A Template for Trouble Time

> I am facing the following trouble: [symptoms]
>
> What I have tried: [bullet list]
> The current state: [bullet list]
> The tools I have: [live USB, separate PC, phone, etc.]
>
> Give me three next steps in order of risk. For each, the expected time and the next move if it fails.
> If I get tired, also tell me how to safely pause for now.

## Summary

What you did in this chapter:

1. Classified trouble into five stages.
2. Sorted out responses for app / DE / login / boot / BIOS stages.
3. Learned chroot recovery from a live USB.
4. Prepared the data-rescue procedure.
5. Positioned reinstalling as the final choice.
6. Confirmed the trouble-time mindset (calm, one at a time, log, time limit).

What you hold now:
- A live USB and an external SSD (kept on hand).
- A template prompt for trouble time.
- The peace of mind that "even if reinstalling is needed, dotfiles + apt-manual.txt brings me back."

In Chapter 19, we move to the **growing** view. Beyond just running daily life, the methods to evolve your Debian environment over the long term, in your own colors.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
