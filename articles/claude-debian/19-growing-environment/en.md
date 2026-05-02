---
slug: claude-debian-19-growing-environment
lang: en
number: "19"
title: Chapter 19 — Growing Your Own Environment
subtitle: Three months, six months, a year — make it yours, a little at a time
description: As you keep using Debian, grow your environment. Small automations, optimized key bindings, your own scripts; observe and evolve your "shape of productivity."
date: 2026.04.23
label: Claude × Debian 19
prev_slug: claude-debian-18-when-things-break
prev_title: Chapter 18 — When Things Break
next_slug: claude-debian-20-community
next_title: Chapter 20 — Engaging with the Community
cta_label: Learn with Claude
cta_title: An environment is not a finished product.
cta_text: Windows was a box delivered to you. Debian is a garden you tend. Small daily care produces, six months later, an environment that fits you in surprising ways.
cta_btn1_text: Continue to Chapter 20
cta_btn1_link: /en/claude-debian/20-community/
cta_btn2_text: Back to Chapter 18
cta_btn2_link: /en/claude-debian/18-when-things-break/
---

## The View of "Growing"

Windows ships as a finished product, a box. The user uses the features given inside that box.

Debian is different. **The initial state is just the starting point.** As you use it daily, you fix the inconveniences you notice, one at a time. That is what "growing" means.

In this chapter, we work with Claude on how to grow your Debian environment over three-month, six-month, and one-year horizons.

## Section 1 — Observe

### Put Your Workflow into Words

Before growing it, observe what you are actually doing. For one week, write the following notes.

- The first five things you do every morning when you sit at the PC.
- Operations you do more than ten times a day.
- Operations you do once a month or so but always have to look up.
- The moments you thought "this could be faster."
- The things you thought "I could automate this."

### Ask Claude ①: Extract Improvements from the Observations

> Here are my one-week observation notes:
> [paste notes]
>
> From these, please extract "growing targets" in the following categories:
> (1) Things that get faster with a key binding.
> (2) Things that should become shell aliases.
> (3) Things that can be scripted.
> (4) Things that can be solved by application configuration.
> (5) Workflow itself that should be reconsidered.
>
> Estimate, for each item, the effect (time saved, mental comfort, mistake reduction) and the implementation cost.

## Section 2 — Three Months: Small Automations

### Build Up Shell Aliases

In `~/.bashrc` or `~/.zshrc`, define short forms for commands you use often.

```bash
# git operations
alias gs='git status -sb'
alias gd='git diff'
alias gl='git log --oneline -20'
alias gp='git pull --ff-only'

# directories you go to often
alias proj='cd ~/Projects'
alias dot='cd ~/dotfiles'

# long commands
alias update='sudo apt update && sudo apt upgrade && sudo apt autoremove'

# human-friendly units
alias df='df -h'
alias free='free -h'
alias ls='ls -h --color=auto'
```

### Custom Shortcuts

In the DE's key-binding settings, assign shortcuts to apps you use frequently.

- `Super + B`: browser.
- `Super + C`: Claude.
- `Super + F`: file manager.
- `Super + T`: terminal.
- `Super + Return`: terminal (Tmux session).

### Your Own Scripts in `~/bin`

Roll up actions you do many times a day into shell scripts.

```bash
# Example: ~/bin/daily-backup
#!/bin/sh
rsync -av --delete ~/Documents /mnt/backup/documents-$(hostname)/
rsync -av --delete ~/Projects /mnt/backup/projects-$(hostname)/
echo "Backup completed: $(date)"
```

If you put `~/bin/` on PATH in `.bashrc`, you call them by name.

### Ask Claude ②: The First Three Automations

> From my work observations [paste again], pick the three automations I should implement first, and write them as shell scripts.
> For each script:
> (1) The filename.
> (2) Usage (a command-line example).
> (3) A safety check (so an accidental run doesn't break things).
> (4) An example cron schedule (if relevant).

## Section 3 — Six Months: Redesigning the Workflow

### Adjust the Daily Rhythm

After three months, your work rhythm becomes visible. Mornings are documents, midday is meetings, evenings are coding — that kind of thing.

Redesign workspaces (virtual desktops) to match.

- Workspace 1 (morning): mail, calendar.
- Workspace 2 (focused work): just one app.
- Workspace 3 (communication): Slack, Discord.
- Workspace 4 (learning): Claude, browser.
- Workspace 5 (admin): terminal, monitoring.

### Tame Notifications

The DE manages notifications on Debian. Stop the ones that distract.

- Mail: badge only, no sound.
- Chat: mentions only, suppressed by time of day.
- System: only critical warnings.

### Build a Focus Mode

The method varies by DE, but you can build a single switch for "notifications off, other apps closed, terminal only."

### Ask Claude ③: Workflow Redesign

> I have used Debian for three months. My time allocation looks like this:
> [activities by time of day]
>
> Propose how to use workspaces, notification settings, and a focus mode that match this rhythm.
> Take into account whether I'm a morning or night person, the volume of meetings, and the peak time of my focus.

## Section 4 — One Year: Build Your Own Tools

### From Scripts to Small Apps

After a year, "the sequence of things I do every week" becomes visible. Make it into a single app.

Following the dashboard from Chapters 14–15, build a personal tool with Claude.

Examples:
- A household-budget tool (read CSV, summarize monthly).
- A reading log (add title, author, thoughts).
- A journal (Markdown diary, searchable).
- A work time tracker (per-project hours).

You could buy off-the-shelf alternatives, but **building it yourself fits you exactly**.

### Ask Claude ④: A Small Personal App

> "The weekly sequence" I noticed over a year is [content].
> Suppose I make this into a small app:
> (1) Minimum features (MVP).
> (2) Data storage (SQLite recommended).
> (3) UI (Flet or TUI).
> (4) Time estimate.
> (5) A staged expansion plan (1 month, 3 months, 6 months).

## Section 5 — Bring in New Hardware

### Give an Old PC a Second Role

Aside from the main machine you migrated, an older PC may be sleeping somewhere. Give it a new role with Debian.

- Home server: Nextcloud, Syncthing, media server (Jellyfin).
- Development server: Docker-running services, dedicated build machine.
- A PC for the kids: Debian Xfce with a restricted account.
- Lab machine: safely try the latest kernel or another DE.

Installing Debian on an old PC will be far easier than the first install. **Treat it as a review of Chapters 1–8.**

### Ask Claude ⑤: Putting an Old PC to Work

> An old PC I have: [specs].
> As a use, I'm thinking about [home server / lab / kids' PC].
>
> Tell me the optimal way to use it, the additional packages needed, and the initial setup steps.
> Include the angle of electricity cost, noise, and heat.

## Section 6 — Recording and Sharing

### Write Down the Trail of Growth

In `~/journal/`, record monthly changes to the environment.

```markdown
# Environment changes — July 2026

## Added
- script weekly-report.sh (automates Monday's report build)
- VSCode extension: errorLens

## Removed
- unused: LibreOffice Draw (never used it)

## Realizations
- After introducing Tmux, terminal work got dramatically faster
- Although I'm a night person, the habit of reading "yesterday's digest" in the morning is working

```

### Make It Shareable

The knowledge accumulated over six months or a year can become a blog post. "A year using Debian with Claude," "Reviving an old PC with Debian" — your experience becomes someone else's starting point.

### Ask Claude ⑥: Turning the Growth Record into an Article

> Over six months I have used Debian and accumulated [the knowledge gained].
> If I were to turn this into a single blog post, what structure would it take?
> Assuming readers who are considering migration, propose three title candidates and a chapter outline.
> To make it easier for me to write, list the elements to include in each chapter as bullet points.

## Section 7 — Don't Aim at "Done"

### There Is No End to Growing

The moment Debian fits you exactly, that isn't "done"; it is just "the shape of you now." Work changes, interests change, the environment changes again.

**Enjoy the change.** Try a new tool, touch a new language, try a new key binding — that flexibility is the meaning of having chosen Debian.

### Watch Out for Over-Customization

On the other hand, get absorbed in growing it and you stray from the actual work. **Keep customization within limits that don't get in the way of work.**

A guideline: 2–3 hours a month. If you start spending more than that on growing, ask yourself "do I really need this now?"

## Summary

What you did in this chapter:

1. Observed your own workflow and noted it down.
2. Three months: small automations (aliases, shortcuts, scripts).
3. Six months: shaped the rhythm with workspaces / notifications / focus mode.
4. One year: built a small personal tool.
5. Gave an old PC a new role.
6. Recorded and shared the trail of growth.

What you hold now:
- Grown-up dotfiles.
- Your own small app.
- A monthly environment journal.

In Chapter 20, we turn outward. **Engagement with the Debian community** — IRC and mailing lists, bug reports, translation — and the new shape of contribution to open source that Claude is bringing.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
