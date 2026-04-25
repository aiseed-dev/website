---
slug: claude-debian-04-dependency-inventory
lang: en
number: "04"
title: Chapter 4 — Taking Stock of Dependencies
subtitle: Before wiping Windows, lay out every connection between data and services
description: Finish the inventory before you wipe. Browser, mail, authenticator apps, licenses, cloud storage, printers, family-shared things. Together with Claude, build a dependency map and prevent gaps in the migration.
date: 2026.04.23
label: Claude × Debian 04
prev_slug: claude-debian-03-telling-environment
prev_title: Chapter 3 — How to Tell Claude About Your Environment
next_slug: claude-debian-05-installation-overview
next_title: Chapter 5 — Understanding the Installation Picture with Claude
cta_label: Learn with Claude
cta_title: Oversights show up after you wipe.
cta_text: "Wait, where was that authenticator app?" — remembering it the moment you wipe Windows is too late. Do the stock-taking in this chapter carefully, and you won't have to panic once in the chapters that follow.
cta_btn1_text: Continue to Chapter 5
cta_btn1_link: /en/claude-debian/05-installation-overview/
cta_btn2_text: Back to Chapter 3
cta_btn2_link: /en/claude-debian/03-telling-environment/
---

## What This Chapter Is For

In Chapter 1 we sorted out "what you lose." In Chapter 3 we wrote down "my environment." Chapter 4 is the work that connects those two.

Concretely, this chapter does the stock-taking that ensures **you do not miss a single thing that would put you in trouble the moment you wipe Windows**. It is not just about whether software runs. Login credentials, authenticator apps, license keys, data that hasn't reached the cloud, things shared with family, printer drivers, your New Year's-card address book — everyday connections you don't normally pay attention to suddenly show their faces the moment you wipe.

What you build with Claude in this chapter is **a dependency map**. With it in hand, you won't panic in the installation chapters from Chapter 5 onward.

## Section 1 — Five Categories of Dependency

If you split dependencies into the following five categories, you miss less.

**A. Authentication and identity verification.**
Login IDs, passwords, two-factor authentication, passkeys, physical security keys, authenticator apps (Microsoft Authenticator, Google Authenticator, Authy), phone SMS, physical IC cards.

**B. Data.**
Files saved locally, files you assumed were syncing to the cloud but were not, mail bodies, contacts, calendar, browser bookmarks and passwords, chat history, photos, music, videos, game save data.

**C. Licenses and subscriptions.**
OS license keys, Office accounts, Adobe, Microsoft 365, cloud subscriptions, various SaaS, license files for offline business software.

**D. Hardware and drivers.**
Printers, scanners, pen tablets, specific USB devices (industrial measurement equipment, readers), Bluetooth devices, webcams, external audio interfaces.

**E. Connections with people.**
Folders shared with family, LINE message history, OneDrive shared with colleagues, shared albums with relatives, your New Year's-card address book, something you inherited from a predecessor.

### Ask Claude ①: First Pass at the Five Categories

> Based on my profile (`my-claude-profile.md` from Chapter 2) and my environment information (`my-system.md` from Chapter 3), please list — concretely — what I should check before wiping Windows and migrating to Debian, sorted into the following five categories:
>
> A. Authentication and identity verification
> B. Data
> C. Licenses and subscriptions
> D. Hardware and drivers
> E. Connections with people
>
> For each item, add "how to verify," "treatment after the Debian migration," and "severity (high / medium / low)."
>
> [paste `my-claude-profile.md` and `my-system.md` here]

Claude will return a list adapted to your situation. It won't be complete, but it will trigger you to notice oversights.

## Section 2 — A: Pitfalls of Authentication and Identity Verification

### Treat Authenticator Apps Like a Phone Change

The PC-app version of an authenticator app on Windows (Microsoft Authenticator for Windows, etc.) disappears once you migrate to Debian. If you cannot regenerate authentication codes, you get locked out of online services.

The standard plays:

**1. Make the phone version of the authenticator app the primary one.**
Microsoft Authenticator, Google Authenticator, Authy, and Bitwarden all run on a phone. Wiping the PC has no effect.

**2. Where a service supports passkeys, move to passkeys.**
Passkeys are tied to a FIDO2-capable phone or a security key, so they do not depend on the PC's OS.

**3. Generate backup codes for every service.**
Generate "backup codes" or "recovery codes" for Google, Microsoft, the major social networks, online accounts at financial institutions, and every service where you have 2FA configured. Print them on paper, or store them as encrypted files, **somewhere other than where you'll be moving things to Debian**.

**4. A single physical security key is worth having.**
A hardware key like YubiKey is an OS-independent identity verification mechanism. Having one for important accounts is reassuring.

### Ask Claude ②: Authentication Stock-Take

> The major online services I use are: [Gmail, iCloud, LINE, banks, social media, Microsoft 365 for work, others].
>
> For each service, please put together a table with: (1) whether authentication remains intact at the moment I wipe Windows, (2) what to do beforehand if it does not, (3) the recommended authentication method after the Debian migration (passkey, phone authenticator app, physical key, etc.).

Once you have filled this table, **before wiping, log in again to every service and confirm authentication works**. Skip this step and there is a high chance you'll be locked out after the wipe.

## Section 3 — B: Moving All Your Data Out Safely

### The Trap of "I Assumed It's in the Cloud"

OneDrive, iCloud, Google Drive, Dropbox — it is easy to think "it's all in the cloud, so I'm safe." But in cases like the following, data exists only locally.

- The Desktop or Downloads folder (when you excluded it from sync).
- A folder where you logged in once, but sync stopped because of a quota overage.
- Local mail clients (Outlook's `.pst` files, the Thunderbird profile).
- Game save data (titles that don't support Steam Cloud).
- Browser bookmarks, passwords, history (when sync is off).
- Project files of paint software or DAWs.
- Data in proprietary formats from New Year's-card software, household-budget software, and the like.

### Concrete Steps for Stock-Taking

1. **Scan everything under `C:\Users\[you]`.**
   Open `Desktop`, `Documents`, `Downloads`, `Pictures`, `Videos`, `Music`, and `AppData` one at a time and look at the contents.

2. **Verify the cloud-sync state in each service.**
   In OneDrive's settings, check "folders selected for sync." Same for iCloud.

3. **Export your browser profile.**
   In Chrome, export "Bookmarks," "Passwords," and "Autofill" as CSV / HTML. Same for Firefox.

4. **Verify mail saved locally.**
   Outlook's `.pst`, the Thunderbird profile folder, the Apple Mail mailbox. Copy to external storage as needed.

5. **Convert app-proprietary data into a format you can carry.**
   Export to a generic format like CSV or JSON if possible. Keep the original-format file as well (in case you need to open it in a virtual machine later).

### Split Storage into Three

Sort the data you've moved out into three buckets.

1. **To take to Debian.** Things you use day to day.
2. **Archive.** Things you rarely look at but want to keep.
3. **Candidates for disposal.** Things you'll throw away on this occasion.

(3) is the one that actually matters most. A migration is the perfect opportunity to clean house. If you carry ten-year-old work files, unused images, and old backups into the new environment, Debian becomes a trash can.

### Ask Claude ③: Data Evacuation Checklist

> The apps and services I use are [paste again]. Among these, please lay out the data that may exist only locally before I wipe Windows.
>
> For each item:
> (1) Which folder or app setting do I need to check?
> (2) What file format can it be exported to?
> (3) Can it be opened on Debian, or do I need a virtual machine?
>
> Also, if there are "hidden data" I tend to overlook (under AppData, registry-dependent things, etc.), please warn me about them.

Claude will point out data in unexpected places. It will be the trigger that makes you say "ah, that thing too."

## Section 4 — C: Licenses and Subscriptions

### What to Look For

Use this opportunity to take stock of subscriptions. Many people are paying tens of thousands of yen a year for services they don't use.

| Type | Example | Treatment after Debian migration |
| --- | --- | --- |
| OS license | Windows 11 Pro | Won't be used. If unwanted, give up on a refund |
| Office | Microsoft 365 | If LibreOffice is enough, cancel |
| Security | Norton, Virus Buster | Debian's defaults are enough. Cancel |
| Cloud | OneDrive paid tier | Move to another service or scale down |
| Image / video | Adobe Creative Cloud | Consider whether DaVinci Resolve, GIMP, Inkscape can substitute |
| Specialized | Accounting, business apps | Look for alternatives, or keep a dedicated machine |

### Recover License Keys Before You Wipe

For perpetual-license (paid-once) software, write down the license keys. Many programs embed the key in a file on the installed PC. Wipe and you cannot get it back.

A PowerShell example for retrieving an old Microsoft product key:

```powershell
(Get-WmiObject -query "select * from SoftwareLicensingService").OA3xOriginalProductKey
```

For other software, check whether the key can be retrieved from the program's "License information" menu, or from your account page on the maker's website. **Do this work at least a week before the wipe day, not on the day itself.**

### Ask Claude ④: Sorting Subscriptions

> The subscriptions and licenses I currently pay for are these: [list].
>
> On the assumption that I'm migrating to Debian, please sort them into three:
> (1) Can be cancelled — alternatives are fine.
> (2) Downgrade is enough (drop from the current plan).
> (3) Need to be kept for work (continue if it runs on Debian; otherwise consider a separate PC or alternative).
>
> Please add a rough estimate of the annual amount that could be saved.

When the savings come out as concrete numbers, motivation for the migration goes up.

## Section 5 — D and E: Hardware and Connections with People

### Checking Printers and Scanners

Printers from the major home-use makers (Canon, Epson, Brother, HP) almost all have Linux drivers available. **The important thing is to write down the model name precisely.**

### Shared Formats with Family

If everyone in the family is on Windows, you'll need to align on the format of shared folders, New Year's-card software, and household-budget software. If you alone move to Debian, there will be points where exchanges with family stop working.

In this chapter's stock-taking, list out "with whom, through which software, in which format." In Chapter 11, "Choosing Applications," we'll set the policy for keeping family compatibility.

### Ask Claude ⑤: Hardware-and-People Dependency Map

> Based on my hardware environment (`my-system.md`) and the way I share things with family and colleagues [describe], when I migrate to Debian please put together two tables:
> (1) Hardware that may run into driver problems.
> (2) Places where I'll need to align shared formats with family or colleagues.

## Section 6 — Consolidate into One Dependency Map

Roll up all of the above into a single Markdown file.

```markdown
# My Debian Migration — Dependency Map  (2026-04-23)

## A. Authentication and identity verification
| Item | Current state | Action beforehand | Severity |
| --- | --- | --- | --- |
| Microsoft Authenticator (PC version) | On Windows | Already consolidated to phone | Medium |
| Google 2FA | Phone | Print backup codes | High |
| Bank A passkey | Win + face recognition | Already added phone passkey | High |

## B. Data
| Item | Current location | Destination | Status |
| --- | --- | --- | --- |
| Work documents | OneDrive | Stays as-is (accessible from Debian) | OK |
| Photos (2015-2020) | C: drive | Move to external SSD, then to Debian | To do |
| Outlook mail (.pst) | C: drive | Migrate to Thunderbird | To do |

## C. Licenses / subscriptions
## D. Hardware
## E. Connections with people

## Migration Go/No-Go preconditions
- [ ] All "high-severity" items in A are cleared
- [ ] Data evacuation in B is complete
- [ ] External SSD has the backup
- [ ] An old PC, or a Windows clone, secures a "way back"
```

Only when every checkbox is filled in do you have the right to move on to Chapter 5, "The Installation Picture."

## Summary

What you did in this chapter:

1. Took stock of dependencies in five categories (authentication, data, licenses, hardware, people).
2. Worked through each category's pitfalls with concrete questions to Claude.
3. Made the actual yearly savings visible by sorting subscriptions.
4. Consolidated everything into a single `dependency-map.md` file.

What you hold now:
- `dependency-map.md` (the dependency map).
- A set of backup codes, exported bookmarks and passwords, and the evacuated data.

The next part (starting with Chapter 5) finally enters the installation picture. With the three documents you produced in this preparation phase (`my-claude-profile.md`, `my-system.md`, `dependency-map.md`) in hand, you step into the Debian world.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
