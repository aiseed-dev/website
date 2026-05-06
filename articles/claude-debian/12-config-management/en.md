---
slug: claude-debian-12-config-management
lang: en
number: "12"
title: Chapter 12 — Understanding and Managing Configuration
subtitle: Track dotfiles and apt with Git
description: Debian's configuration files are all open text. Manage them with Git and your environment becomes a reproducible document. Together with Claude, design dotfiles, an apt package list, and an auto-restore script.
date: 2026.04.23
label: Claude × Debian 12
prev_slug: claude-debian-11-application-selection
prev_title: Chapter 11 — Choosing Applications
next_slug: claude-debian-13-dev-tools
next_title: Chapter 13 — Building the Development Tools
cta_label: Learn with Claude
cta_title: An environment can live as documentation.
cta_text: Reinstall, migrate to a new PC, replicate to another machine — all of it becomes a single command. This is one of Debian's biggest strengths.
cta_btn1_text: Continue to Part 4 / Chapter 13
cta_btn1_link: /en/claude-debian/13-dev-tools/
cta_btn2_text: Back to Chapter 11
cta_btn2_link: /en/claude-debian/11-application-selection/
---

## What It Means That Configuration Files Are Text

On Debian, most OS and app configuration is managed as **text files**. This is the decisive difference from Windows and macOS.

Not a registry, not opaque binaries. Because it is text:
- It can be read (you can grasp what is set, and how).
- It can be edited (you can change it with your own hands).
- It can be diffed (you can compare before and after).
- It can be Git-managed (you keep history; you share across multiple PCs).

This chapter establishes the practice of turning your environment into a Git-trackable document.

## Section 1 — Where Configuration Files Live

### Three Layers

**1. System-wide settings.** Under `/etc/`.
`/etc/ssh/sshd_config`, `/etc/apt/sources.list`, `/etc/fstab`, and so on. Editing requires `sudo`.

**2. User-specific settings.** Under `~/.config/` and `~/.[name]`.
`~/.config/fcitx5/`, `~/.config/Code/`, `~/.bashrc`, `~/.gitconfig`. In your home directory.

**3. App-specific settings.** Various places.
Like `~/.mozilla/firefox/`. Different per app.

### Frequently Touched Files (Examples)

```
~/.bashrc                       # bash settings
~/.profile                      # login shell settings
~/.gitconfig                    # git user info
~/.ssh/config                   # SSH connection definitions
~/.config/fcitx5/               # Japanese input
~/.config/zed/settings.json     # Zed editor settings
~/.config/nvim/                 # Neovim (init.lua / lazy-lock.json)
~/.config/JetBrains/PyCharmCE2026.1/  # PyCharm Community settings
~/.config/autostart/            # apps that auto-start
```

## Section 2 — Manage dotfiles with Git

### Create a dotfiles Repository

The "dot-prefixed" files in your home directory are collectively called dotfiles. Manage them with Git.

```bash
# Create the dotfiles directory
mkdir ~/dotfiles
cd ~/dotfiles
git init

# Create a personal repository on GitHub / GitLab and push
```

### The Symbolic Link Approach

Move the original files into `dotfiles/` and create symbolic links.

```bash
# Example: bring .bashrc under management
mv ~/.bashrc ~/dotfiles/bashrc
ln -s ~/dotfiles/bashrc ~/.bashrc

# Example: bring .gitconfig under management
mv ~/.gitconfig ~/dotfiles/gitconfig
ln -s ~/dotfiles/gitconfig ~/.gitconfig
```

### Separate Sensitive Information

API keys, access tokens, and passwords don't go in dotfiles.

- The main `.bashrc` is Git-managed.
- Put sensitive items in `.bashrc.local` and `source` it from `.bashrc`.
- Exclude `.bashrc.local` via `.gitignore`.

### Ask Claude ①: Designing the dotfiles

> I want to manage my Debian environment as Git-tracked dotfiles.
> The files I want under management now are [bashrc, gitconfig, ssh/config, fcitx5, Zed and Neovim configuration].
>
> Please give me:
> (1) A recommended directory structure.
> (2) An install script that creates the symbolic links automatically.
> (3) How to separate sensitive information.
> (4) The procedure for cloning and restoring on a new PC.
>
> The script should be POSIX sh.

Use what comes back as the base and adjust by hand.

## Section 3 — Make the apt Package List Reproducible

### Record What's Currently Installed

```bash
# List of manually installed packages
apt list --manual-installed > ~/dotfiles/apt-manual.txt

# Or, all packages via dpkg
dpkg --get-selections > ~/dotfiles/packages.txt
```

### Reproduce the Same Configuration on Another PC

```bash
# Restore from packages.txt
sudo dpkg --set-selections < packages.txt
sudo apt-get dselect-upgrade
```

### Build the Habit of Updating the List

Every time you install an app, update `apt-manual.txt` and commit to Git. If that's a hassle, batch it once a month.

```bash
# Skeleton of a monthly update script
apt list --manual-installed > ~/dotfiles/apt-manual.txt
cd ~/dotfiles
git add apt-manual.txt
git commit -m "apt: $(date +%Y-%m) $(wc -l < apt-manual.txt) packages"
```

### Ask Claude ②: A Restore Script

> Under my `dotfiles/` I have `apt-manual.txt` listing the packages I installed.
> Write a shell script that, on a fresh Debian 12, installs all of these packages from this list.
> Include error handling (continue when a package doesn't exist, permission checks, mirror reachability), in POSIX sh.

## Section 4 — Track Changes Under /etc

### Auto-Track with etckeeper

```bash
sudo apt install etckeeper
```

`etckeeper` automatically manages `/etc/` as a Git repository. When you install a package via apt, the state of `/etc/` at that moment is committed. Manual edits can also be committed.

```bash
# After editing /etc/ssh/sshd_config
sudo etckeeper commit "sshd: change PermitRootLogin to no"
```

This gives you a complete change history of system settings. You always know "when, what was changed."

## Section 5 — Backing Up the Home Directory

dotfiles is just configuration. Photos, documents, and project data need a separate backup.

### To an External SSD with rsync

```bash
# Mount the external SSD as /mnt/backup
rsync -av --delete --exclude='.cache' --exclude='node_modules' \
  ~/ /mnt/backup/home-$(hostname)/
```

- `--delete`: also delete files on the backup that you've deleted at the source.
- `--exclude`: leave caches and regenerable things out.

### System Snapshots with Timeshift

```bash
sudo apt install timeshift
```

Timeshift takes snapshots of the **system area**. `/home/` is generally excluded. Useful when an update breaks something.

A practical setup is two-tier: rsync or Syncthing for home, Timeshift for system snapshots.

### Ask Claude ③: A Backup Strategy

> My Debian PC layout:
> - Main data locations: ~/Documents, ~/Pictures, ~/Projects.
> - Storage candidates: external 2 TB SSD, NAS, cloud ([provider]).
>
> Build me a backup strategy that satisfies:
> - Daily automatic backup.
> - Weekly full copy.
> - Monthly off-site storage.
> - Recovery from accidental single-file deletion.
> - Recovery from total OS loss.
>
> Be concrete with the tools, cron settings, and steps.

## Section 6 — Simulate a Reinstall

### Try It Once

As the finishing touch of this chapter, **on another PC or a virtual machine, try restoring from the dotfiles**.

```bash
# After first login on the new Debian
cd ~
git clone https://github.com/[you]/dotfiles.git
cd dotfiles
./install.sh          # create the links
./apt-restore.sh      # install packages
./post-install.sh     # DE settings, fcitx5, etc.
```

**Only when this end-to-end works can you say your environment is documented.** Try it and fix what gets stuck.

### What "Success" Means

- A fresh PC, clone + run scripts, and you reach a state where you can do daily work.
- It doesn't have to be perfect. 90% restored is fine; the last 10% you can adjust by hand.
- Aim for total script time of 30–60 minutes.

## Section 7 — Make Claude Your Configuration-Management Partner

### Have Claude Summarize Changes

Periodically, have Claude summarize the dotfiles change history.

> Please summarize the following git log:
> ```
> [output of `git log --oneline -n 30`]
> ```
> Tell me how my Debian environment has changed over the past month and what trends you see.

You see directions of change you weren't conscious of.

### When Things Break, Hand Over the Whole Environment

When something goes wrong, hand the dotfiles set and the system info to Claude.

> My environment is as follows:
> - `my-system.md` [paste]
> - `~/.bashrc` [paste]
> - main files under `~/.config/fcitx5/` [paste]
>
> Please identify the cause of the following symptom: [symptom]

The more information you provide, the more concrete Claude's judgment becomes.

## Summary

What you did in this chapter:

1. Got the three layers of configuration files (system / user / app) under your fingers.
2. Put dotfiles under Git management and started running them via symbolic links.
3. Made the apt package list recordable and restorable as `apt-manual.txt`.
4. Set up automatic tracking of changes under `/etc/` with `etckeeper`.
5. Built a backup strategy combining rsync and Timeshift.
6. Tried (or planned) restoring from dotfiles in practice.

What you hold now:
- A `dotfiles/` repository (backed up on GitHub / GitLab / similar).
- Documentation of a reproducible environment.
- The habit of monthly updates.

This closes Part 3. **Your Debian environment has evolved from "made it and use it" to "a reproducible blueprint."** This was structurally hard on Windows.

In Part 4 (Chapters 13–16), we move into building the development environment. Terminal, editor, Git, language runtimes, and Claude Code — combined on Debian, you take a step into being a builder.

---

The full series can be navigated from [Learning Debian with Claude — All chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
