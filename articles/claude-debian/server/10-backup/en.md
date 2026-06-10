---
slug: claude-debian-server-10-backup
lang: en
number: "10"
title: Chapter 10 — Protecting Your Data
subtitle: Automate backups, rehearse restores
description: The server itself is disposable; only the data is the real thing. The OS and your services can be rebuilt in tens of minutes, but the data cannot. Decide what to protect, take encrypted backups with restic, automate them with a systemd timer, and then actually rehearse a restore — proving, with your own hands and alongside Claude, the principle that a backup you have never restored is the same as no backup at all.
date: 2026.06.10
label: Claude × Debian Server 10
prev_slug: claude-debian-server-09-publishing
prev_title: Chapter 9 — Opening Up to the Outside World
next_slug: claude-debian-server-11-operations
next_title: Chapter 11 — Growing Your Server
cta_label: Learn with Claude
cta_title: You protect the data, not the machine.
cta_text: A server can be rebuilt any number of times. The only thing that cannot be rebuilt is the data. Take backups automatically, and then actually try restoring — rehearse the "what if" once, and the day your server breaks you will not panic. Get that preparation in place together with Claude.
cta_btn1_text: Continue to Chapter 11
cta_btn1_link: /en/claude-debian/server/11-operations/
cta_btn2_text: Back to Chapter 9
cta_btn2_link: /en/claude-debian/server/09-publishing/
---

## Why Backup Gets Its Own Chapter

By now you have assembled a server, run services on it, and gone as far as publishing it to the outside world. Stop here for a moment and consider one thing. **If the disk in this server were to physically fail right now, what would be lost?**

The OS would be lost. But that is no great loss. The minimal install you did in Chapter 3 can be redone in tens of minutes as long as you kept the steps. The services you built in Chapter 6 come back in minutes from their unit files, and the PostgreSQL you installed in Chapter 7 can be reinstalled with `apt`. **The server itself was, by design, disposable from the start.** Recommending a minimal install in Chapter 3 and gathering your data into a database in Chapter 7 were, in fact, foreshadowing for this chapter — from the start, we kept "what can be rebuilt" and "the data that cannot" apart.

There is exactly one thing that cannot be rebuilt. **The data.** Family photos, work files, notes, the records your home-grown apps have accumulated. There is only one of each in the world. If it vanishes with the disk, it is gone for good.

That is why this chapter stands alone. You could fairly call it **the single most important chapter in the Server Edition**. Decide what to protect, take it automatically, and — this is the crux — **actually rehearse the restore**.

## Section 1 — Deciding What to Protect

### Taking Stock of What to Protect

Blindly "backing up everything" is actually the clumsy approach. Take the whole OS, system files and all, and your backup bloats and your restore slows down. First, sort out "what can be rebuilt and what cannot."

What a server needs to protect falls roughly into three kinds.

1. **Application data.** The contents of the PostgreSQL and SQLite databases from Chapter 7, the files under `/srv/photos` and `~/data`. This is the heart of the heart.
2. **Configuration.** The `Caddyfile` you wrote in Chapter 9, the home-grown systemd units you made in Chapter 6, the PostgreSQL settings you touched in Chapter 7, the changes you made by hand under `/etc`.
3. **The notes you have built up through this book.** `my-server.md`, your collected "Ask Claude" answers, your troubleshooting logs.

The OS itself (`/usr`, `/bin`, files installed by packages) you can, as a rule, leave unprotected. Those can be rebuilt with `apt`.

### Config to Git, Data to a Backup Tool — A Two-Track Setup

Here, split the craft in two.

**Configuration (text files) goes under git.** This is simply the server version of what you did for the desktop in [Chapter 12, "The Craft of Config Management"](/en/claude-debian/12-config-management/) of the main series. The `Caddyfile`, your home-grown units — all of it is text. Text is exactly what git is best at. The history of changes stays, and "when and why did I set it this way" can be traced afterward.

**Data (photos, documents, databases) is taken with a backup tool.** This is not text; it is large in volume and changes often. It is unsuited to git. It is the job of a dedicated backup tool — restic, which we use next.

The reason for the two tracks is this: with the configuration in git, recovery becomes two steps — "git clone, then write the data back." With configuration and data kept separate, you can deal calmly with whatever breaks.

### The 3-2-1 Rule

The backup world has a long-standing rule of thumb: **the 3-2-1 rule.** Keep **3** copies of your data (1 live plus 2 backups), on **2** different kinds of media (say, internal SSD and an external disk), with **1** of them in another location (off-site). If one place is wiped out by fire, flood, or theft, a copy elsewhere survives. A personal server need not follow it strictly, but do keep the instinct: "one copy is not enough; ideally one more in a separate place."

### Ask Claude ①: Build the List of What to Protect

> I am running the following on my Debian server:
> [list of what you are running as of Chapter 8. e.g. photo server (data at /srv/photos), file share (~/share), home-grown note app (DB: notesdb in PostgreSQL)…]
>
> Please sort these into three categories — "data (cannot be rebuilt, backup essential)", "config (text, managed in git)", and "OS / re-creatable (no need to protect)" — and put them in a table.
> For anything you classify as data, also add candidate concrete paths on the server, and the places easy to miss in a backup (warnings such as: copying a database's files directly while it is running can corrupt them).

When you hand over your own setup, points you would easily overlook line up in the table — "copying that database while it is live will corrupt the backup — dump it first," "that config can move to the git side." The list of what to protect is the starting point of this chapter.

## Section 2 — Taking Backups with restic

### Why restic

There are many backup tools, but in this Server Edition we use **restic**. There are four reasons.

- **It runs as a single binary.** No tangled dependencies. It installs with one `apt`.
- **Encryption is the default.** Backups are encrypted from the start. Even if your external disk is stolen, the contents are unreadable without the key.
- **It deduplicates.** Identical data is stored only once. Take it daily, and the disk grows less than you would expect.
- **It supports many destinations.** Local disk, another machine, S3-compatible storage, cloud via rclone — the same operation takes backups to a variety of places.

Installation is one line.

```bash
sudo apt update
sudo apt install restic
```

### Try It Against a Local USB Disk

First get a feel for it with the most straightforward case: a backup to an external USB disk. We proceed assuming the USB disk is mounted at `/mnt/backup`.

Once, and only once at the start, **initialize the repository (the backup store)**.

```bash
# Initialize the repository (only the very first time)
restic init -r /mnt/backup/repo
# You will be asked to set a password (the repository key). As covered below, this must never be lost.
```

Once initialized, take an actual backup. Specify the "things to protect" you sorted in Section 1.

```bash
# Back up data and config by specifying them
restic backup -r /mnt/backup/repo /srv/photos /srv/notes ~/share /etc

# Do not forget the git working directory holding the Caddyfile and your units
restic backup -r /mnt/backup/repo ~/server-config
```

Check whether it worked with the list of snapshots.

```bash
# The list of backups (snapshots) taken so far
restic snapshots -r /mnt/backup/repo
```

If a list of dates and IDs appears, it worked. From the second time on, only what changed gets added (thanks to deduplication it is fast and small).

### Databases Get Dumped First

One thing needs special handling: **a live database.** If you copy the data files of the PostgreSQL you installed in Chapter 7 while it is running, you can capture a half-finished write — and produce a backup **that will not restore**.

The correct pattern is: **dump first (write it out as text), then back up the dump.**

```bash
mkdir -p ~/backup-staging

# PostgreSQL: write the database out as SQL text
sudo -u postgres pg_dump myappdb > ~/backup-staging/myappdb.sql

# SQLite: make a safe copy even while in use
sqlite3 ~/data/notes.db ".backup $HOME/backup-staging/notes-backup.db"

# back up the staging directory with restic
restic backup -r /mnt/backup/repo ~/backup-staging
```

The output of `pg_dump` is plain SQL text, so you can inspect it with your own eyes or with Claude. Restoring is just feeding it back: `psql myappdb < myappdb.sql`. The "entrance to protecting your data" previewed at the end of Chapter 7 joins the main current here.

### Remote Destinations

Recall the 3-2-1 rule. A backup to an external disk satisfies "a different medium," but not yet "a different location." restic takes backups to distant places simply by changing the destination.

- **Another machine (via SFTP):** `-r sftp:user@otherhost:/path/to/repo`
- **S3-compatible storage:** pass the keys via environment variables and specify `-r s3:...`
- **Via rclone:** to any of the many clouds rclone supports, `-r rclone:remote:path`

The exact commands vary in detail depending on the destination you choose. The fastest way to get a command tuned to your own destination is to have Claude write it (box ② below).

### A Backup Whose Key Is Lost Is Just Random Noise

Here is the single most important caution. A restic backup is encrypted. Which means **if you lose the password (the repository key) you set at initialization, the backup can never be restored.** All that remains is a heap of encrypted random noise.

So keep the key safely, outside the server. Put it in a password manager, write it on paper in a safe, keep a copy in another trusted place — any method will do, but put it **somewhere that survives even if the entire server vanishes.** If the key lived only inside the server, the moment the server breaks the key is gone with it. That would defeat the whole purpose.

### Ask Claude ②: Have It Write the Backup Command for Your Destination

> I want to take backups with restic on my Debian server.
> What to protect (paths): [paste the data part of the table you made in Section 1 ①]
> Backup destination: [e.g. home NAS over SFTP / Backblaze B2 / Google Drive via rclone, as far as decided]
>
> For this destination, please write (1) the repository init command, (2) the command to take a backup, and (3) the command to check snapshots.
> Also tell me where and how to safely keep the password (repository key) and the destination's credentials. Add a one-line explanation of what each command does.

The fine differences per destination (environment variable names, URL formats) are not something you need to memorize. Hand Claude your own setup, and use the commands it produces while understanding them one line at a time. That is the way of this book.

## Section 3 — Automating It

### Reuse the systemd Timer from Chapter 6

"Take it by hand when the mood strikes" will not last for backups. You will always forget. So automate it. The tool here is the **systemd timer** you learned in Chapter 6. You need to learn nothing new — just apply the mechanism you picked up then to backups.

First, write the service that runs the backup.

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=restic backup of server data
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
# Keep the key and destination separate in an environment file (see the next note for its contents)
EnvironmentFile=/etc/restic/backup.env
# Dump the database first, then back it up (Section 2)
ExecStartPre=/bin/sh -c 'runuser -u postgres -- pg_dump myappdb > /srv/backup-staging/myappdb.sql'
ExecStart=/usr/bin/restic backup /srv/photos /srv/notes /srv/backup-staging /home/youruser/share /etc
# Tidy up old snapshots (keep the last 7 daily + 4 weekly + 6 monthly)
ExecStartPost=/usr/bin/restic forget --prune --keep-daily 7 --keep-weekly 4 --keep-monthly 6
```

Do not write the key and destination into the service itself; split them into an environment file.

```bash
# /etc/restic/backup.env (set permissions so only root can read it)
RESTIC_REPOSITORY=/mnt/backup/repo
RESTIC_PASSWORD=(repository key)
```

```bash
# Tighten permissions so nobody but root can read the environment file
sudo chmod 600 /etc/restic/backup.env
```

Next, write the timer that "runs it at a fixed time every day."

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Run restic backup daily

[Timer]
# Run at 04:00 every day (pick a low-load time of day)
OnCalendar=daily
# If the server was off and missed a run, catch up after it boots
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start the timer.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
```

### Confirm It Is Running

Once the timer is in place, confirm it is properly scheduled.

```bash
# The list of registered timers and the next scheduled run time
systemctl list-timers

# See the result of the backup run (whether it succeeded or failed)
journalctl -u backup.service
```

If `backup.timer` appears in `list-timers` with a next-run time shown, the automation is complete.

### A Mechanism for Noticing Failure

Automation has one trap. **"Believing it is being taken automatically" is the most dangerous state.** One day the disk fills up, or the external drive comes unplugged, and backups have been failing for weeks — and when you finally try to restore, there is nothing there. That accident really does happen often.

Leave elaborate monitoring for Chapter 11; start with a plain habit. **Once a week, look at `restic snapshots` with your own eyes.** Check that the date at the top of the list is properly "yesterday" or "this morning." That alone prevents "it stopped without my noticing."

```bash
# Make it a habit to look at this with your own eyes once a week
restic snapshots -r /mnt/backup/repo | tail
```

## Section 4 — Rehearsing the Restore

### A Backup You Have Never Restored Is the Same as No Backup

Here is the thing this chapter most wants to convey. **A backup you have never restored is the same as no backup at all.**

A backup that is merely "being taken" is only half of it. What truly matters is that you can "bring it back when it counts." But a backup you have only ever taken and never tried to restore — nobody knows whether it can really be brought back. You had the wrong key, you forgot to specify the crucial directory, the files were corrupt — these "tried to restore and it would not come back" cases happen precisely because the restore was never rehearsed.

So once you can take it, **always restore it once.**

### Actually Restore It

Do the restore rehearsal by writing out to a separate location (such as `/tmp/restore-test`), so as not to overwrite the live data. This way you can try it without breaking anything.

```bash
# Try restoring the latest snapshot to a test location
restic restore latest -r /mnt/backup/repo --target /tmp/restore-test

# Check the contents. Are the files you wanted to protect properly there?
ls -R /tmp/restore-test
```

If the photos, the documents, and the config files all line up inside `/tmp/restore-test` in a form you recognize, it worked. **At this moment, your backup changes from "something that might exist" into "something you can certainly bring back."** Once you have confirmed it, you may delete the test directory.

### Advanced Rehearsal: Rebuilding the Server

Let me propose one step further. **Recreate the server from scratch on another machine (or a VM or VPS at hand).**

The steps go like this. Start from the minimal install of Chapter 3, clone the config you put in git (the `Caddyfile`, home-grown units, setup notes), write the data back with restic, and feed the database back in from the `pg_dump` dump with `psql`. A server nearly identical to your live one should come up on the new machine.

See this rehearsal through and you gain two things. One is the conviction that "I really can rebuild from the start." The other is the **"things missing from the steps"** you are sure to find partway through — a setting you forgot to note, a file you forgot to put in git. Find and fill those, and you will not panic during a real "what if." The "encoding the configuration as code" covered in Chapter 11 connects directly here.

### Ask Claude ③: Build the Restore-Rehearsal Runbook

> I take backups with restic of the following setup:
> Data I protect: [list of paths]
> Config management: [e.g. I keep the Caddyfile / home-grown units / setup notes in a git repository]
> Backup destination: [local USB / SFTP / cloud, etc.]
>
> Please build a "server rebuild rehearsal" runbook for recreating this setup from scratch on a new machine (VPS or VM).
> In this order, concretely tailored to my setup: (1) what to do after the minimal OS install, (2) the steps to restore config from git, (3) the steps to restore data from restic, (4) how to confirm each service is running correctly.
> Also add a checklist for noticing "there was a gap in the steps" partway through the rehearsal.

This runbook is not just for the rehearsal. When a real disaster strikes, it becomes your recovery manual as-is. Make it once and put it in git, and it will save the future you (the you of a year from now, with the knowledge faded).

## Summary

What you did in this chapter:

1. Confirmed the philosophy that "the server itself is disposable; only the data is the real thing," and took stock of what to protect.
2. Set the two-track policy: config to git, data to restic.
3. Took an actual backup to a local disk with restic and checked the snapshots.
4. Automated a daily backup with a systemd timer, and confirmed it works with `list-timers` and `journalctl`.
5. **Actually rehearsed a restore**, confirming the backup is "something you can certainly bring back."
6. Through the advanced server-rebuild rehearsal, gained the conviction that "I can rebuild from the start."

What you hold now:
- An encrypted backup repository, and a repository key kept in a safe place.
- `backup.service` and `backup.timer` (the mechanism that takes a backup automatically every day).
- A "list of what to protect" and a "restore-rehearsal runbook" (these go in git).
- The reassurance — which gives operational slack — that "if it comes to it, I can rebuild."

With this, even if the server physically breaks, you will not panic. The OS and the services can be rebuilt, and the data can be brought back. In the final Chapter 11, on that foundation of reassurance, we talk about **growing the server over the long run** — a design that runs on fifteen minutes of watching a week, a rhythm of maintenance, a pattern for when things break, and "the next move." The craft of tending and growing a single server like a living thing.

---

The server sub-series can be navigated from [Learning Debian with Claude — Server Edition](/en/claude-debian/server/). The main desktop series is at [all chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
