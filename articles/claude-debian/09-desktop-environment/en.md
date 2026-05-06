---
slug: claude-debian-09-desktop-environment
lang: en
number: "09"
title: Chapter 9 — Tuning the Desktop Environment (a Claude Dialogue Example)
subtitle: Re-evaluate the DE you tentatively chose in Chapter 6 — after actually using it
description: After actually using Debian for a while, re-evaluate the desktop environment. Workflow, shortcuts, screen layout, theme — the steps for tuning it to fit you, and the craft of deciding to switch to another DE if it doesn't.
date: 2026.04.23
label: Claude × Debian 09
prev_slug: claude-debian-08-first-troubleshooting
prev_title: Chapter 8 — The First Round of Troubleshooting
next_slug: claude-debian-10-japanese-input
next_title: Chapter 10 — Setting Up Japanese Input
cta_label: Learn with Claude
cta_title: You have the right to choose again, after using it.
cta_text: The Chapter 6 choice was tentative. Use it for a week, and if it doesn't fit, switch to another DE. The strength of Debian lies in that flexibility.
cta_btn1_text: Continue to Chapter 10
cta_btn1_link: /en/claude-debian/10-japanese-input/
cta_btn2_text: Back to Chapter 8
cta_btn2_link: /en/claude-debian/08-first-troubleshooting/
---

## Re-evaluate the Chapter 6 Choice

In Chapter 6 you picked one of GNOME / KDE / Xfce / LXQt, and in Chapter 7 you installed it. After about a week of actually using it, answer the following.

1. **Are there things that bother you in daily operation?**
2. **Do the shortcuts you've picked up feel natural to your hands?**
3. **Are memory and CPU consumption within tolerance?**
4. **Do you want to try another DE?**

If it doesn't fit, switch. Debian even allows multiple DEs to coexist (not recommended, but possible).

### The AI-Native Lens

As Chapter 6 said, **the real battlefield is terminal + browser + editor.**
The DE only needs to do three things:

1. Lay out windows (tiling / floating).
2. Launch apps (launcher / menu).
3. Run the system tray (IME, network, volume, notifications).

That much is all you need — and a **thin DE like Xfce or LXQt covers it
completely.** People who insist on "I can't work without GNOME / KDE"
typically have **work whose substance has become DE-dependent** (the
visual chrome of the screen has bled into the job).

In this book's stance, **with Zed / Neovim at the center and browser +
terminal carrying the day, the DE can stay minimal.** Combined with the
three editors of Chapter 13 (Zed / Neovim / PyCharm), a thin DE is
fine.

### Ask Claude ①: Sort Through a Week of Usage

> I've used [DE name] for a week. The following are bothering me:
> - [bothering me 1]
> - [bothering me 2]
>
> Are these (A) things that go away with practice, (B) things that can be improved by configuration, or (C) properties of the DE itself, so I should consider another DE?
> If B, give me the concrete steps for the configuration changes. If C, give me alternative DE candidates and the cost of switching.

## Section 1 — Getting the Most out of GNOME

### Center on Activities Overview

GNOME's heart is "Activities" in the top-left of the screen, or the Overview that appears when you press `Super` (the Windows key).

- `Super`: Activities Overview (app search, workspace switching).
- `Super + A`: all applications.
- `Super + [number]`: the n-th workspace.
- `Super + Page Up / Down`: move between workspaces.
- `Ctrl + Alt + ↑/↓`: same (different binding).
- `Alt + Tab`: switch windows.

**Using workspaces sends productivity through the roof.** Just splitting them into work, personal, and research increases focus.

### Add What's Missing with Extensions

If GNOME feels lean out of the box, install `gnome-shell-extensions`.

```bash
sudo apt install gnome-shell-extension-manager gnome-tweaks
```

Standards:
- **Dash to Dock.** A persistent Mac-style dock.
- **AppIndicator Support.** System-tray icons.
- **Caffeine.** Suppress sleep temporarily.

Too many extensions makes things unstable. Keep it to five or six.

## Section 2 — Getting the Most out of KDE Plasma

### Closest to a Windows Feel

KDE's screen layout — taskbar, start menu, and system tray along the bottom — is close to Windows. People moving from Windows take to it easily.

### Travel Through the Forest of Settings

KDE's strength is "everything is configurable." Its weakness is the same: "too many settings to find your way."

**Settings to touch in the first week:**

1. System Settings → Appearance → Global Theme (changes the whole look at once).
2. System Settings → Input Devices → Keyboard (adjust shortcuts).
3. System Settings → Workspace Behavior → Virtual Desktops.
4. System Settings → Startup and Shutdown → Session (restoration on reboot).

### KWin Scripts and KRunner

`Alt + Space` brings up KRunner (a Spotlight-like launcher). Just remembering this makes KDE much easier to live with.

## Section 3 — Getting the Most out of Xfce

### The Philosophy of Lightness

Xfce is "only what you need, simply." A minimal feature set is not a weakness here; it's the design philosophy.

### Grow Your Panel

Customize the panel on screen (top by default) to fit your workflow.

- Right-click → "Panel" → "Panel Preferences."
- In the "Items" tab, add or remove launchers, the clock, workspace switchers, the notification tray, and so on.

### Shortcuts

- `Super + E`: file manager.
- `Super + T`: terminal.
- Add custom shortcuts under Settings → Keyboard → Application Shortcuts.

## Section 4 — Principles That Apply to Any DE

### Build Three Habits

Whichever DE you choose, the following three habits change how the system feels.

**Habit 1: Make everything doable from the keyboard.**
Touch the mouse less. Launch apps from a launcher, switch windows with keys, move workspaces with keys.

**Habit 2: Split workspaces by purpose.**
Workspace 1 for work, 2 for research, 3 for music, 4 for the Claude dialogue. That kind of split.

**Habit 3: Keep the taskbar / dock minimal.**
No more than five icons always shown. Launch the rest from a launcher.

### Ask Claude ②: Optimize My Workflow

> On [DE name], a typical day flows like this:
> - Morning: [activity]
> - Midday: []
> - Evening: []
>
> Please list five DE-specific shortcuts, extensions, or settings that would optimize this workflow.
> Prioritize features I'm not yet using that look like they would have high impact.

## Section 5 — Deciding to Switch DEs

### When Switching Is the Right Call

- Memory consumption is consistently tight → switch to a lighter DE.
- A Windows-style feel never goes away and the friction builds → KDE.
- GNOME didn't fit on a touch-screen machine → KDE, or a different GNOME setup.

### How to Switch

```bash
# Add a new DE (example: add Xfce)
sudo apt install task-xfce-desktop

# Whether to remove the old DE: decide after you've gotten used to the new one.
# Removing it cold causes settings confusion, so keep both around at first.
```

From the gear icon on the login screen, you can choose which DE to log in to. **The safe approach is to use both for a few days each and compare.**

### Ask Claude ③: A Switch Simulation

> I am currently using [DE A], but for [reason] I'm considering switching to [DE B].
> Please put together a table of what I'd lose and what I'd gain after switching.
> Also tell me the risks of switching (lost settings, relearning costs) and the steps to try it with minimum risk.

## Section 6 — Tune the Look

You will stare at this screen for hours every day. Making it something you like has a direct impact on productivity.

### Themes

- GNOME: `gnome-tweaks` → Appearance.
- KDE: System Settings → Appearance → Global Theme.
- Xfce: Settings → Appearance.

Dark themes are easier on the eyes. Day / night switching is supported on each DE.

### Fonts

The default Japanese font is Noto Sans CJK JP. By taste:

```bash
# Source Han Sans, Source Han Serif, IBM Plex Sans JP, BIZ UD Gothic, etc.
sudo apt install fonts-noto-cjk fonts-ibm-plex fonts-hack
```

For monospace, Hack, JetBrains Mono, or Source Han Code JP. Comfortable if you do development work.

### Wallpaper

For wallpapers, a calm, near-monochrome look suits work better than a dramatic photo.

## Summary

What you did in this chapter:

1. Used the Chapter 6 DE choice for a week and re-evaluated.
2. Sorted out the key practices for getting the most out of each DE.
3. Adopted the principles of keyboard-first, workspaces by purpose, and a minimal dock.
4. Set criteria for switching DE if needed.
5. Tuned themes, fonts, and wallpaper.

Where you are now:
- A DE that feels like yours (whether you switched or stayed).
- Three to five shortcuts you can use without thinking.
- A look you actually like.

In Chapter 10, "Setting Up Japanese Input," we pin down the detailed configuration of Fcitx5 + Mozc — user dictionaries, key bindings, app-specific behavior. Since you use it every day, build it without compromise.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
