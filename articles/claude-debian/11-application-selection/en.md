---
slug: claude-debian-11-application-selection
lang: en
number: "11"
title: Chapter 11 — Choosing Applications
subtitle: What to replace your Windows apps with on Debian
description: Browser, mail, office, image / video, communication, file sync, password management — replace Windows apps with Debian apps category by category. Together with Claude, make the choices that fit your use.
date: 2026.04.23
label: Claude × Debian 11
prev_slug: claude-debian-10-japanese-input
prev_title: Chapter 10 — Setting Up Japanese Input
next_slug: claude-debian-12-config-management
next_title: Chapter 12 — Understanding and Managing Configuration
cta_label: Learn with Claude
cta_title: There is no single "the alternative."
cta_text: To "what replaces Office?" there are several answers depending on context. Talk it through with Claude and narrow down to the best fit for your use.
cta_btn1_text: Continue to Chapter 12
cta_btn1_link: /en/claude-debian/12-config-management/
cta_btn2_text: Back to Chapter 10
cta_btn2_link: /en/claude-debian/10-japanese-input/
---

## Replace by Category

With the dependency map from Chapter 4 open beside you, decide replacements in the following eight categories.

1. Browser
2. Mail and calendar
3. Office (documents, spreadsheets, presentations)
4. Communication (chat, video calls)
5. Image, video, audio
6. File sync and cloud storage
7. Password management and authentication
8. Utilities (PDF, screenshots, clipboard)

## Section 1 — Browser

### Candidates

- **Firefox** (`sudo apt install firefox-esr`): Debian standard, privacy-focused.
- **Chromium** (`sudo apt install chromium`): the open-source build of Chrome.
- **Brave**: built-in ad blocking, privacy-focused.
- **Vivaldi**: highly customizable.
- **Google Chrome**: Google's official build (install from a deb file).

### Axes for Choosing

- **Bookmark and password sync.** How easy is it to migrate from your current browser?
- **Privacy.** Stance toward ads and trackers.
- **Integration with Electron apps.** Some business tools assume a specific browser.

**The book's recommendation: Firefox primary, Chromium secondary.** If a particular workflow truly needs Chrome, install it.

### Ask Claude ①: Browser Migration

> I currently use [Edge / Chrome / Safari]. Tell me how to migrate bookmarks, passwords, extensions, and open tabs to [Firefox / Chromium] on Debian.
> Give me the approach that minimizes data loss, and list things I should verify right after the move.

## Section 2 — Mail and Calendar

### Candidates

- **Thunderbird** (`sudo apt install thunderbird`): a long-standing client; rich features; supports POP / IMAP / Exchange.
- **Evolution** (`sudo apt install evolution`): GNOME's standard; relatively strong Exchange integration.
- **Geary**: simple and snappy; fits GNOME well.
- **Webmail.** Continuing to use Gmail or Outlook in the browser is also valid.

### Migrating from Outlook (Work Use)

Microsoft 365's Exchange Online can be read from Thunderbird via IMAP, or via Microsoft's own EWS. If your company's IT department permits IMAP, it works without trouble.

### Migrating Past Mail

There is a tool to import Outlook's `.pst` files into Thunderbird.

```bash
# ImportExportTools NG (a Thunderbird extension)
```

### Ask Claude ②: Choosing a Mail Client

> My mail environment is:
> - Work: [company domain, Exchange Online / private server].
> - Personal: [Gmail / iCloud / etc.].
> - Past mail: [.pst, .mbox, etc.].
>
> Recommend the best mail client and give me the initial setup and the steps for migrating past mail.

## Section 3 — Office

### LibreOffice (`sudo apt install libreoffice libreoffice-l10n-ja`)

The face of Debian office: Writer (documents), Calc (spreadsheets), Impress (presentations), Draw (diagrams), Base (database), Math (formulas).

**The reality of Office-file compatibility:**
- Simple documents: no problem.
- Tables, forms, simple functions: mostly no problem.
- Complex Excel macros: can break.
- PowerPoint animations: subtly off.

### OnlyOffice (Distributed as deb)

Visual fidelity to Office files is higher than LibreOffice. A candidate if you exchange business documents with MS Office users frequently.

### Google Workspace / Microsoft 365 Online

A pragmatic split: "use the online version in the browser only when I need full Office-file fidelity."

### Ask Claude ③: Office Strategy

> My frequency of Office files is:
> - Word: __ per week, my own or received, complexity.
> - Excel: __, with / without macros, complexity.
> - PowerPoint: __, with / without animation, complexity.
>
> Of LibreOffice, OnlyOffice, Microsoft 365 Online, Google Workspace, which should I make primary and which secondary?
> Tell me the points where compatibility is most likely to fail, and how to avoid them.

## Section 4 — Communication

### Candidates

- **Slack.** Official deb available, or via Flatpak.
- **Microsoft Teams.** The official Linux client has been discontinued; use the browser version.
- **Zoom.** Official deb; works well.
- **Discord.** Official deb.
- **LINE.** No official Linux client. Use LINE Web, a virtual machine, or rely on your phone.
- **Signal / Element.** Official deb.

### The LINE Problem

There is no official LINE desktop client for Linux. Options:

1. LINE Web (log in by QR code from the phone).
2. Make the phone your primary.
3. Run LINE inside a Windows virtual machine.

### Ask Claude ④: The Residual Issues for Communication

> The communication tools I use are [list].
> Make a table of the best way to use each on Debian (official deb / Flatpak / Snap / Web / alternative).
> For tools without Linux support like LINE, propose realistic handling tied to how often I use them.

## Section 5 — Image, Video, Audio

### Image

- **GIMP.** A Photoshop alternative.
- **Krita.** Illustration and digital painting.
- **Inkscape.** Vector graphics (an Illustrator alternative).
- **darktable / RawTherapee.** RAW development (a Lightroom alternative).
- **Shotwell / digiKam.** Photo management.

### Video

- **DaVinci Resolve.** Pro-grade editing; the free version is sufficient. Linux version available.
- **Kdenlive.** Open-source editing.
- **OBS Studio.** Streaming and recording.
- **HandBrake.** Encoding.

### Audio

- **Audacity.** Waveform editing.
- **Ardour.** A DAW.
- **LMMS.** Composition.

### Ask Claude ⑤: Creative Tools

> I work with [photos / video / illustration / music] at [frequency]. My current app is [name].
> Evaluate the Debian alternatives in terms of feature parity and learning cost.
> In particular, make explicit what I lose and what I gain in return.

## Section 6 — File Sync and Cloud

### Candidates

- **Nextcloud.** Self-hostable; subscription services exist (a fork of OwnCloud).
- **Syncthing.** Peer-to-peer sync between multiple PCs. No server required.
- **Rclone.** A CLI tool to many cloud storage services.
- **OneDrive.** No official Linux client. The unofficial `onedrive` CLI.
- **Google Drive.** No official Linux client. `rclone` or GNOME Online Accounts.
- **Dropbox.** Official Linux version available.
- **MEGA.** Official Linux version available.

### What This Book Recommends

**A home NAS plus Syncthing, or a Nextcloud subscription.** Reduce dependency on third-party cloud providers.

Syncthing in particular doesn't depend on a cloud vendor: it syncs encrypted between PC, phone, and NAS. The opposite of vendor lock-in.

### Ask Claude ⑥: A Sync Strategy

> My sync targets are [documents, photos, code, music], and my devices are [Debian, phone, family PC].
> Of Syncthing, Nextcloud, and rclone+existing cloud, which should I make primary, considering capacity, privacy, and cost?

## Section 7 — Password Management and Authentication

### Candidates

- **Bitwarden.** A service; official Linux client; browser extensions.
- **KeePassXC** (`sudo apt install keepassxc`). Local storage; open source.
- **1Password.** Official Linux version; subscription.

### Working with Security Keys

Security keys like YubiKey work without trouble on Linux. The `yubico-authenticator` package handles OATH.

### Ask Claude ⑦: Password Management

> I currently use [Chrome's password manager / Apple Keychain / Bitwarden / other].
> Tell me the best choice for the Debian environment and the steps to safely import / export the current passwords.

## Section 8 — Utilities

### PDF

- **Evince / Okular.** Viewing.
- **Xournal++.** Annotation, handwriting.
- **pdftk-java**, **qpdf.** Command-line manipulation.
- **LibreOffice Draw.** Simple editing.

### Screenshots

- **Flameshot.** Feature-rich, annotation included.
- **GNOME Screenshot** / **Spectacle** (KDE). Standard.
- **Shutter.** Many features.

### Clipboard History

- **CopyQ.** Cross-DE.
- **KDE.** Klipper, by default.
- **GNOME.** The `Clipboard Indicator` extension.

## Section 9 — The Pace of Migration

Don't migrate everything at once. Move in this order.

**Day 1.** Browser, mail, messenger (the daily essentials).
**Week 1.** Office, cloud sync, password manager.
**Month 1.** Image / video, utilities, specialized use.

Set priorities and don't rush.

### Ask Claude ⑧: My App Migration Plan

> Based on the B and D categories of my dependency map (`dependency-map.md`) and how often I use each, draft an app migration schedule split into Day 1 / Week 1 / Month 1.
> Add a risk level to each item (impact if the migration fails).

## Summary

What you did in this chapter:

1. Replaced Windows apps with Debian apps in eight categories.
2. Handled honestly the things that don't fully replace (LINE, Teams, etc.).
3. Designed the migration pace (Day / Week / Month).

Where you are now:
- A set of Debian apps usable for daily life.
- A migration plan.

In Chapter 12, "Understanding and Managing Configuration," we cover where Debian's configuration files live, dotfiles management, backup, and tracking with Git. Get into the practice of **leaving your environment as documentation**.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
