---
slug: claude-debian-17-updates-maintenance
lang: en
number: "17"
title: Chapter 17 — Updates and Maintenance
subtitle: Keep the system up to date without disrupting daily life
description: Debian's update philosophy, safe procedures, disk cleanup, reading logs. The monthly and yearly maintenance rhythm, and preparing for major upgrades (Debian 12 → 13). Together with Claude, keep your environment in long-term shape.
date: 2026.04.23
label: Claude × Debian 17
prev_slug: claude-debian-16-python-flutter-other
prev_title: Chapter 16 — Python, Flutter, and Other Environments
next_slug: claude-debian-18-when-things-break
next_title: Chapter 18 — When Things Break
cta_label: Learn with Claude
cta_title: To use it daily, look after it weekly.
cta_text: Debian runs even when you leave it alone, but routine care keeps it comfortable for the long term. Build a weekly / monthly / yearly rhythm and 90% of trouble is prevented.
cta_btn1_text: Continue to Chapter 18
cta_btn1_link: /en/claude-debian/18-when-things-break/
cta_btn2_text: Back to Chapter 16
cta_btn2_link: /en/claude-debian/16-python-flutter-other/
---

## Three Layers of Updates

Debian updates split into three layers.

1. **Minor package updates.** Security patches and bug fixes. Weekly to monthly.
2. **Point releases.** Debian 12.x → 12.x+1 (about every six months).
3. **Major upgrades.** Debian 12 → Debian 13 (about every two years).

Each is handled differently. Trying to do them all with the same command will break the system one day.

On top of that, since Chapter 11 introduced Flatpak, **running the apt and
Flatpak streams in parallel** is the new baseline for Debian operations.

| Source | What's installed | Update command | Frequency |
|---|---|---|---|
| **apt** | OS base, shells, dev tools, Firefox-ESR | `sudo apt upgrade` | weekly |
| **Flatpak** | Chromium-family browsers, Slack/Zoom, Bitwarden, Krita, etc. | `flatpak update` | weekly (or auto) |
| **uv tool** | Python CLIs (`pre-commit`, `httpie`, `ruff`, etc.) | `uv tool upgrade --all` | monthly |
| **miniforge / conda** | DS / ML envs (PyTorch + CUDA, GDAL, scipy, ...) | `conda update --all -n <env>` | monthly (per project) |

The classic pitfall: updating apt only and leaving Chromium stale.
**This book recommends running every stream on the same day** with a
single script.

## Section 1 — Minor Package Updates

### Basic Commands

```bash
# Update the package list
sudo apt update

# Apply updates
sudo apt upgrade

# Remove packages no longer needed
sudo apt autoremove

# Reclaim disk space
sudo apt clean
```

### Frequency

- Once a week is enough (decide on a rhythm — Monday morning, etc.).
- For urgent vulnerability patches (kernel, browser), apply mid-week.

### Automate with unattended-upgrades

Security updates alone can be applied automatically.

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

This applies security updates in the background. Note that kernel updates that require a reboot still need a manual reboot.

### Updating Flatpak

```bash
# Update all Flatpak apps and runtimes
flatpak update -y

# Garbage-collect unused runtimes (the main reason disks balloon)
flatpak uninstall --unused -y

# Review per-app permissions (or use Flatseal)
flatpak info --show-permissions com.google.Chrome
```

If you installed Chromium-family browsers via Flatpak, **this is the
security-critical path**. apt's `firefox-esr` is fine on a weekly cadence,
but Chromium-family browsers occasionally need same-day patching for
zero-days.

### Updating uv tool

```bash
uv tool list
uv tool upgrade --all
```

CLIs you installed via uv tool / pipx in Chapter 16 (ruff, httpie,
pre-commit, etc.) update on their own schedule — not under apt's control.

### Updating miniforge / conda

```bash
# Bring an env up to date
conda update --all -n ds
conda update --all -n dl    # GPU env

# Update conda itself
conda update -n base -c conda-forge conda

# Reclaim disk
conda clean --all -y
```

If you have several DS / ML projects, **stagger their update timing**.
Deep-learning environments are sensitive to numerical reproducibility —
freeze them while a paper or experiment is in flight, and run
`conda update` only at clear breakpoints.

### A Single Script for All Streams

```bash
#!/bin/bash
# ~/.local/bin/weekly-update
set -e
echo "=== apt ==="
sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y && sudo apt clean

echo "=== flatpak ==="
flatpak update -y
flatpak uninstall --unused -y

echo "=== uv tool ==="
uv tool upgrade --all 2>/dev/null || true

echo "=== conda (miniforge) ==="
if command -v conda >/dev/null 2>&1; then
    conda update -n base -c conda-forge conda -y
    # Add per-env updates here, monthly is fine:
    # conda update --all -n ds -y
    conda clean --all -y
fi

echo "=== disk ==="
df -h /
du -sh ~/.cache ~/.local/share/flatpak ~/.local/share/uv ~/miniforge3 2>/dev/null
```

Add to cron (`0 8 * * 1`) and the **four streams update together** every
Monday at 08:00 — apt, Flatpak, uv tool, and conda(base). Per-env conda
updates are best left as a monthly per-project task.

### Ask Claude ①: Automating Weekly Maintenance

> Bundle my weekly Debian maintenance into a single shell script with the following items:
> (1) apt update / upgrade / autoremove.
> (2) flatpak update + flatpak uninstall --unused.
> (3) uv tool upgrade --all.
> (4) conda (miniforge) base update and clean (per-env can be monthly).
> (5) Disk free-space check (warn if over 80% full).
> (6) Confirm there are no failed services.
> (7) Show candidate old kernels for removal.
> (8) Detect errors in the logs.
>
> I want to run it weekly via cron (Monday 08:00). The result should be visible via mail or notification.

## Section 2 — Point Releases

Once every few months, a point release like Debian 12.5 → 12.6 comes out.

```bash
# Don't change the codename in sources.list (keep "bookworm")
sudo apt update
sudo apt full-upgrade
sudo reboot
```

Use `apt full-upgrade`, not `apt upgrade`. It updates packages whose dependencies have changed.

### Read the Release Notes

Each point release publishes "what changed" on the Debian official site. **Major changes are announced here.** Five minutes is enough — give it a read.

## Section 3 — Major Upgrade (Debian 12 → 13)

Once every two years, a new version is released. **Treat this as a separate piece of work.**

### Preparation

1. **Full backup of important data** (rsync to external SSD).
2. **System-wide snapshot** (Timeshift).
3. **Reserve at least half a day.**
4. **Confirm the way back** (snapshot restore, worst case clean install).

### Skeleton of the Procedure

```bash
# 1. Bring the current state fully up to date
sudo apt update
sudo apt full-upgrade
sudo apt autoremove

# 2. Rewrite sources.list to the new version
# bookworm → trixie (example)
sudo sed -i 's/bookworm/trixie/g' /etc/apt/sources.list

# 3. Upgrade
sudo apt update
sudo apt upgrade --without-new-pkgs
sudo apt full-upgrade

# 4. Reboot
sudo reboot
```

**Have Claude verify the latest version of this procedure.** The Debian official upgrade guide is the authoritative current recommendation.

### Ask Claude ②: Planning the Major Upgrade

> I'm on Debian 12 and want to upgrade to Debian 13 about six months after its release.
>
> Build a checklist covering:
> (1) Files and settings to back up beforehand.
> (2) The procedure on the day of the upgrade (referencing the official guide).
> (3) Common failures and how to handle them.
> (4) Post-upgrade checks (Wi-Fi, Japanese input, the major apps).
> (5) The fallback procedure if reverting is the only option.

## Section 4 — Disk Cleanup

### What's Eating Capacity

```bash
# Under home
du -sh ~/*

# Where on the whole system the large items are
sudo du -sh /* 2>/dev/null | sort -h

# Logs
sudo du -sh /var/log/*

# Package cache
du -sh /var/cache/apt/archives/
```

### Standard Cleanup

```bash
# apt cache
sudo apt clean
sudo apt autoremove

# Old kernels (verify by hand)
sudo apt list --installed | grep linux-image
# remove the unused ones with sudo apt remove

# journald logs (older entries)
sudo journalctl --vacuum-time=30d     # delete older than 30 days

# Caches per language
# Python: ~/.cache/pip
# Node: ~/.npm
# Docker: docker system prune -af
```

### Ask Claude ③: A Disk Stock-Take

> My Debian disk is filling up. The current state:
> ```
> [output of df -h]
> [output of du -sh ~/*]
> ```
>
> Sort what is safe to delete, what must not be deleted, and what can be compressed.
> Within each group, order by impact (biggest savings first).

## Section 5 — Reading Logs

Debian logs are mainly under `/var/log/` and via `journalctl`.

### Basics of journalctl

```bash
# Recent errors
journalctl -b -p err

# A specific service
journalctl -u nginx -f        # -f for live tail

# Time ranges
journalctl --since "yesterday"
journalctl --since "2026-04-20" --until "2026-04-22"
```

### Files Worth Watching

- `/var/log/syslog`: general.
- `/var/log/auth.log`: authentication, sudo.
- `/var/log/dpkg.log`: package operations.
- `/var/log/apt/history.log`: apt history.

### Ask Claude ④: Detecting Anomalies in the Logs

> Pull out anything noteworthy from the following log:
> ```
> [output of journalctl -b -p warning]
> ```
> For each warning, classify it as (A) safe to ignore, (B) check later, or (C) act on now.

## Section 6 — Yearly Maintenance

Once a year (your birthday or another easy-to-remember day), do the following.

1. **Stock-take dotfiles.** Delete unused settings and old scripts.
2. **Stock-take packages.** Run `apt list --manual-installed` and remove what you don't use.
3. **Verify backups work.** Try a real restore on another PC.
4. **Review passwords.** Change passwords for ssh, GitHub, and major services.
5. **Hardware cleaning.** Physically — clean dust off the fans.

### Ask Claude ⑤: A Yearly Stock-Take Template

> Build a yearly maintenance checklist for a Debian user.
> Cover the following categories, with time and priority for each item:
> (1) Settings and dotfiles.
> (2) Packages and apps.
> (3) Data backup.
> (4) Security.
> (5) Hardware.
> (6) Documentation (refresh of your environment record).

## Section 7 — Prevent "Won't Run Anymore"

### Don't Make Changes in Bulk

Installing new packages, changing settings, updating drivers — doing them all at once makes the cause unidentifiable.

**One change at a time.** After a change, reboot and use it for a day. If there's no problem, move to the next.

### Take Backups Before Changes

Before big changes (kernel update, GPU driver change, DE switch), take a Timeshift snapshot.

### Experiment as a Different User or in a VM

Trying new settings on the live environment kills your daily flow. It's better to install Debian 12 in a virtual machine (virt-manager) and experiment there.

## Section 8 — Make Maintenance a Habit

### Put It on the Calendar

- Every Monday 08:00: minor updates.
- First of the month 09:00: disk cleanup, log review.
- Annual birthday: yearly stock-take.

GNOME Calendar, Thunderbird Lightning, KOrganizer — any of them. **Writing it on the calendar raises the probability you'll do it.**

### Keep a Record

Keep a maintenance history in `~/maintenance-log.md`.

```markdown
# 2026-04-28 weekly maintenance
- apt update/upgrade: 17 packages updated (mainly firefox, kernel)
- autoremove: 3 packages removed
- reboot needed: yes (kernel update)
- noteworthy: none
```

This becomes **the source material for the yearly stock-take.**

## Summary

What you did in this chapter:

1. Understood the three layers of updates (minor / point / major).
2. Designed automated weekly maintenance.
3. Planned the major upgrade.
4. Got the standard disk-cleanup moves down.
5. Learned to read the logs.
6. Built a yearly maintenance template.

What you hold now:
- A weekly maintenance script (set up in cron).
- A maintenance record `maintenance-log.md`.
- Calendar entries.

In Chapter 18, we cover **what to do when things actually break**. Won't boot, no screen, an app won't run — for each, develop the practice of responding with Claude.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
