---
slug: claude-debian-07-installation-execution
lang: en
number: "07"
title: Chapter 7 — The Dialogue of the Install
subtitle: Watching the screen, checking with Claude as you go
description: Actually launch the Debian installer and walk through the eight stages in order. What to choose on each screen, and what to ask Claude when you're unsure. The chapter where you put your hands on the keyboard. Read it with the Chapter 6 checklist beside you.
date: 2026.04.23
label: Claude × Debian 07
prev_slug: claude-debian-06-hardware-choice
prev_title: Chapter 6 — Choices That Fit Your Hardware
next_slug: claude-debian-08-first-troubleshooting
next_title: Chapter 8 — The First Round of Troubleshooting
cta_label: Learn with Claude
cta_title: One screen, one decision.
cta_text: Rushing through the installer screens leads to regret later. At each screen, stop once, cross-check against the checklist, and ask Claude when in doubt. This is the "stop-and-think" chapter.
cta_btn1_text: Continue to Chapter 8
cta_btn1_link: /en/claude-debian/08-first-troubleshooting/
cta_btn2_text: Back to Chapter 6
cta_btn2_link: /en/claude-debian/06-hardware-choice/
---

## Final Preparation Check

Before launching the installer, confirm all of the following are in place.

- [ ] `install-config.md` (the checklist from Chapter 6) is printed, or open on a separate device
- [ ] [claude.ai](https://claude.ai) is open on a separate PC or your phone (you can't ask from the Debian being installed)
- [ ] A full data backup is on external storage
- [ ] Windows license keys and authenticator backup codes are stored on paper
- [ ] The power adapter is plugged in (so the install isn't cut off mid-way by battery)
- [ ] Wired LAN is connected if possible. If not, you have the wireless SSID and password noted
- [ ] The Debian installer USB stick is plugged in
- [ ] You have a reserve day set aside

When everything is ticked, you can begin. If anything is missing, go back and fix it.

## Section 1 — Up to Launching the Installer

### Enter UEFI and Change the Boot Order

1. Shut the PC down completely (a full shutdown, not a restart).
2. Press the power button, and immediately tap the maker-specific key.
   - Dell: F12 / F2
   - HP: Esc → F9
   - Lenovo (ThinkPad): Enter → F12
   - ASUS / custom: F2 / Del
3. Open the Boot menu or Boot Order screen.
4. Move USB to the top, or pick USB from a one-time boot menu (the F12 menu).

Once it boots, the Debian installer screen appears. **Choose Graphical install, where you can use the mouse.**

### Ask Claude ①: A Quick-Response Dialogue When It Won't Boot

Have this template ready in Claude on the separate device.

> The Debian installer won't boot.
> Machine: [maker / model]
> What appears on screen at boot (or what the screen shows): [if you can't take a screenshot, describe in words]
> What I have done:
> - Disabled Fast Startup: [yes / no]
> - Disabled Secure Boot: [yes / no]
> - Tried a different USB port: [yes / no]
> - Tried a different USB stick: [yes / no]
>
> What should I try next?

Having this prepared makes the response fast when trouble hits.

## Section 2 — Language, Region, Keyboard

Once the installer is up, choose the following on the first three screens.

- **Language:** English (or Japanese)
- **Location:** your country
- **Keyboard:** the layout matching the keyboard print (US English for a US keyboard, Japanese for a JP keyboard)

If you pick the wrong layout, the symbol positions go off. Pick by looking at what is actually printed on your keyboard.

## Section 3 — Network Settings

### Wired Is Automatic

If a LAN cable is plugged in, it is detected automatically.

### For Wireless

For wireless LAN, you'll be asked for:

- SSID selection (from a list of nearby access points)
- Encryption type (WPA2 Personal is typical)
- Passphrase

**If the wireless chip's firmware is missing, the list comes up empty.** In that case:
1. Skip wireless and switch to wired.
2. If you have no wired option, USB tethering (sharing the network from your phone over USB).
3. If neither works, you may not have used the firmware-included ISO. Re-make the USB on another PC.

### Hostname and Domain

- **Hostname.** A name for this PC. Something easy to recognize, like `debian-desktop` or `taro-latitude`. Avoid company name, real name, or personally identifying information.
- **Domain name.** Leave blank.

## Section 4 — Creating Users

### What to Do with the Root Password

The "Set up the root password" screen has a choice.

- **Leave the root password blank.** Root login is disabled, and all admin actions go through `sudo`. **The book's recommendation.**
- **Set a root password.** The classic Unix way. Direct root login is enabled.

The blank-and-sudo style is safer, and closer to how Ubuntu works.

### Creating the Regular User

- **Full name.** Either Latin characters or Japanese is fine. It is shown on the login screen.
- **Username (short name).** **Always lowercase Latin letters, with minimal symbols and digits** (e.g., `taro`, `yamada-t`). It becomes the home directory name, so absolutely never use Japanese.
- **Password.** Used for both login and `sudo`. **Keep this distinct from the encryption passphrase.**

## Section 5 — Disk Partitioning

**This is the screen where you should be most careful.**

### What the Choices Mean

- **Guided — use entire disk.** Existing data (including Windows) is wiped, and Debian uses the whole disk. **Recommended by this book.**
- **Guided — use entire disk and set up encrypted LVM.** Comes with full-disk encryption (LUKS). For a laptop, choose this.
- **Manual.** Configure everything by hand. For advanced users.

For a laptop, **"use entire disk and set up encrypted LVM."** For a desktop without encryption, "use entire disk."

### Don't Pick the Wrong Disk

**If an external SSD or another HDD is plugged in, it will appear in the list.** If you accidentally pick the external one, your backup is wiped.

The disks shown can be told apart by capacity. The internal SSD on a laptop is often 512 GB or 1 TB. Externals tend to differ in capacity. If you're unsure, back out of the installer once, physically unplug the external, and resume.

### Ask Claude ②: Confirming the Partition Screen

Photograph the partition screen on your phone, or write down the disk names and capacities you see, and ask Claude.

> The partition screen shows the following disks:
> /dev/sda - 512 GB
> /dev/sdb - 2 TB
>
> My PC's internal SSD is 512 GB; the external is 2 TB. Is /dev/sda the right one to install Debian on? Tell me the risk if I pick the wrong one and how to confirm.

For operations you aren't sure about, **ask before you do**. This is the field application of "the three principles of verification" from Chapter 2.

### Entering the Encryption Passphrase

If you chose encryption, a passphrase entry screen appears. Type the passphrase you decided on in Chapter 6.

- 20+ characters.
- Exactly as written on paper.
- Slowly, to avoid typos.
- Type the same thing in the confirmation field.

**If you mistype here while convinced you got it right, you will not be able to boot after restart.** If you're not sure, type while looking at the paper.

## Section 6 — Installing the Base System and Configuring the Package Manager

From here on, much of it proceeds automatically. Wait several to a couple of dozen minutes.

### Choosing a Mirror Server

In "Configure the package manager," choose a nearby mirror.

- `deb.debian.org`: routes you to a good mirror automatically. A safe default.
- `ftp.jp.debian.org`, `ftp.riken.jp`: representative mirrors in Japan.

Proxy settings are only needed if your office LAN uses a proxy. Leave it blank at home.

## Section 7 — Software Selection

Apply the checkbox configuration you decided on in Chapter 6.

- [x] Debian desktop environment
- [x] [the DE you chose in Chapter 6] (e.g., GNOME)
- [x] standard system utilities

Uncheck the rest. Cross-reference against your printed checklist and be deliberate.

After this, ten to thirty minutes go to package download and install. Coffee time.

## Section 8 — GRUB Install and Completion

### Where to Put GRUB

"Install the GRUB bootloader to the master boot record" → "Yes," and the installation target candidates appear.

- Pick the head of the internal SSD (e.g., `/dev/sda`).
- Do not put it on external storage (unplug it and the system won't boot).

### When the Completion Screen Appears

- Pull out the USB stick.
- Press "Continue" to reboot.

After the reboot: encryption-passphrase screen → Debian login screen → desktop. If you reach this in order, success.

### Ask Claude ③: Quick Response If the Screen Doesn't Come Up After Reboot

> The Debian install completed and I rebooted. The USB stick is out.
> Symptom: [black screen / "No bootable device" message / no encryption-passphrase screen / etc.]
>
> Machine: []. What should I check? Tell me the steps one at a time.

## Section 9 — Three Things to Do Right After First Login

Once you're logged in, do these three things straight away.

### 1. Confirm This Is Your PC

- The desktop is showing.
- Wireless LAN connects (Wi-Fi from the settings menu).
- The display resolution is correct.

### 2. Bring the System Up to Date

Open a terminal (on GNOME: Activities → "terminal") and run:

```bash
sudo apt update
sudo apt upgrade
```

If packages were updated, reboot.

### 3. Take an Initial Screenshot

Take a phone photo of the state right after install. Later, when something doesn't work, this becomes a reference point for what was working initially.

## Summary

What you did in this chapter:

1. UEFI → USB boot → launching the installer.
2. Language, region, keyboard, network settings.
3. User creation (sudo style, Latin-letter username).
4. Disk partitioning (chosen carefully, confirmed with Claude).
5. The encryption passphrase.
6. Software selection (minimal configuration).
7. Installing GRUB.
8. Reboot, first login, system updates.

Where you are now:
- A PC that runs Debian.
- An environment protected by an encryption passphrase.
- The latest packages.

In Chapter 8, "The First Round of Troubleshooting," we go through the issues that tend to come up at this point — display resolution, Wi-Fi, sound, Bluetooth, suspend — and resolve them one by one with Claude.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
