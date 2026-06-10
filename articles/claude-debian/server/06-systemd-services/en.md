---
slug: claude-debian-server-06-systemd-services
lang: en
number: "06"
title: Chapter 6 — The Service as a Unit
subtitle: Run things with systemd, read them with journalctl
description: The insides of a server are, in the end, "a collection of processes that systemd looks after." The basic verbs of systemctl, reading logs with journalctl, writing a unit file that turns your own script into a service, and scheduled runs with a systemd timer — learn to handle starting, stopping, logs, and failure response all through one unit called a "service."
date: 2026.06.10
label: Claude × Debian Server 06
prev_slug: claude-debian-server-05-security-basics
prev_title: Chapter 5 — The Basics of Defense
next_slug: claude-debian-server-07-database
next_title: Chapter 7 — The Database as a Foundation
cta_label: Learn with Claude
cta_title: A server is "a collection of services."
cta_text: Starting, stopping, auto-start, logs, failure response — operations that look scattered all reduce to one unit: the service. Once you hold this shape, you can handle unfamiliar software with the same touch.
cta_btn1_text: Continue to Chapter 7
cta_btn1_link: /en/claude-debian/server/07-database/
cta_btn2_text: Back to Chapter 5
cta_btn2_link: /en/claude-debian/server/05-security-basics/
---

## Why Learn the "Service" as a Unit

Once you start touching a server, it looks like there is too much to memorize. Starting SSH, the firewall's state, restarting a web server, auto-starting your own app, checking logs, responding to failures — each feels like a separate piece of craft.

But here is the reveal: **the insides of a server are, in the end, nothing but "a collection of processes that systemd looks after."** SSH, cron, the fail2ban you installed in Chapter 5, the app you are about to run — from systemd's view, all of them are the same "service (service unit)."

This is the crux of the chapter. **Once you can think in terms of the single unit called a "service," starting, stopping, auto-start, logs, and failure response can all be handled through the same shape.** Install new software, and you can guess "this is probably a service too" and operate it with the same verbs. Rather than more to memorize, everything converges into one shape. This chapter is where you put that shape into your body.

## Section 1 — The Basic Verbs of systemctl

The entry point for driving systemd is the `systemctl` command. The verbs are just a handful, and they apply uniformly to every service.

```bash
# See the state (the one you use most)
systemctl status ssh

# Run / stop
sudo systemctl start  ssh
sudo systemctl stop   ssh

# Restart / just re-read the config (without dropping connections)
sudo systemctl restart ssh
sudo systemctl reload  ssh

# Enable / disable auto-start (takes effect from the next boot)
sudo systemctl enable  ssh
sudo systemctl disable ssh

# List the services running now
systemctl list-units --type=service
```

`start`/`stop` operate on "this very moment." `enable`/`disable` operate on "what happens at the next boot." **These two are different things.** The `disable --now` you typed in Chapter 5 was a shorthand that does both at once (`stop` + `disable`).

The output of `status`, once you are used to it, gives you the whole picture in seconds. Read it with `ssh` as the example.

```bash
systemctl status ssh
```

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/usr/lib/systemd/system/ssh.service; enabled; preset: enabled)
     Active: active (running) since Wed 2026-06-10 09:12:01 JST; 3h ago
   Main PID: 701 (sshd)
      Tasks: 1 (limit: 4915)
     Memory: 5.2M
        CPU: 120ms
     CGroup: /system.slice/ssh.service
             └─701 "sshd: /usr/sbin/sshd -D ..."

Jun 10 11:30:14 myserver sshd[1820]: Accepted publickey for user from 192.168.1.5
```

There are four things to read. **`Active: active (running)`** is that it is running now. **`enabled`** is that it auto-starts at the next boot too. **`Main PID: 701`** is its process number. And at the bottom, **the most recent log lines hang off it.** Just looking at status tells you at a glance "running, auto-starts, and recently logged this."

cron can be peeked at through the same shape.

```bash
systemctl status cron
```

### Ask Claude ①: Have It Explain the `systemctl status` Output

> I ran `systemctl status [service name]` on my Debian 13 server and got this output:
> ```
> [paste the status output as-is]
> ```
> Explain what each line means — especially Active / Loaded (enabled or not) / Main PID / the trailing log lines, one by one.
> Is this state healthy? Point out any signs I should care about.

The status output is dense with information, so at first it is overwhelming. **Paste the whole thing and have it explained line by line.** Do it once, and from then on you can look at the same spots with your own eyes.

## Section 2 — Reading the Journal

systemd gathers the logs of every service in one place. Reading it is `journalctl`'s job. You can name a service and pull only its logs.

```bash
# All logs for a specific service
journalctl -u ssh

# Follow the logs as they stream (exit with Ctrl+C)
journalctl -u ssh -f

# Just the last 10 minutes
journalctl -u ssh --since "10 min ago"

# Only error level and above, since this boot
journalctl -p err -b
```

Narrow by service with `-u`, by time with `--since`, by severity and boot with `-p err -b`. Rather than reading a long log whole, **narrow it like this before you read or hand it over** — that is the trick.

And here is the most important single line of this chapter. **Pasting the log to Claude as-is becomes the basic operating motion of running a server.** This is the server-edition carryover of the "hand the log over as-is" craft you picked up in the main series' [Chapter 8 troubleshooting](/en/claude-debian/08-first-troubleshooting/). What was screen or Wi-Fi logs on the desktop becomes a service's journal on the server. The action is the same — **do not fear lines you cannot read; narrow, and paste.**

When the log is too long to hand to Claude easily, narrow it before handing it over.

```bash
# Pull only errors from this boot, made easy to copy
journalctl -u myapp -p err -b --no-pager | tail -n 50
```

Adding `--no-pager` dumps it all at once, which is easy to copy. `tail -n 50` narrows it to just the tail.

### Ask Claude ②: Have It Write a Unit File That Turns Your Script into a Service

> On my Debian 13 server, I want to auto-run the following script of mine at boot:
> - Start command: [e.g., /usr/bin/python3 /home/user/myapp/server.py]
> - Run as user: [e.g., the ordinary user "user"; I do not want it running as root]
> - Working directory: [e.g., /home/user/myapp]
> - I want it to restart automatically if it crashes
>
> Write a systemd unit file (/etc/systemd/system/myapp.service).
> Then explain, line by line, what each section and line of [Unit] [Service] [Install] does.
> Add the `systemctl` command steps from applying it to enabling auto-start.

**Have Claude write the unit file, and you review it** — this is the way of the AI era. But do not swallow it whole. **Have Claude explain the meaning of each line at least once**, so you can read it yourself. In the next section, you confirm it by actually moving your hands.

## Section 3 — Writing Your Own Service

You get the theory. With a small example, promote something of your own into a "service." The subject can be anything — a Python script on hand, or, for a trial, a simple web server that runs on the standard library alone.

```bash
# Subject: just a simple HTTP server on port 8000
#   python3 -m http.server 8000
# Make this a "service that comes up on reboot, and after a crash, automatically"
```

Create the unit file as `/etc/systemd/system/myapp.service`. The minimal form is three sections: [Unit] [Service] [Install].

```bash
sudo tee /etc/systemd/system/myapp.service > /dev/null <<'EOF'
[Unit]
Description=My sample HTTP server
After=network.target

[Service]
# Run as an ordinary user (not as root)
User=user
WorkingDirectory=/home/user/myapp
ExecStart=/usr/bin/python3 -m http.server 8000
# Restart automatically on abnormal exit
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
```

The three sections mean this. **[Unit]** is the service's description and start order (`After=network.target` runs it after the network comes up). **[Service]** is what to run, as whom, where, and what to do if it crashes (`Restart=on-failure`). **[Install]** is "when it starts" when you `enable` it — `multi-user.target` means "when the system reaches normal server-running state."

Once written, run it with the verbs from Section 1. The sequence is always the same.

```bash
# 1. After editing a unit file, first have systemd re-read it
sudo systemctl daemon-reload

# 2. Start it now and enable auto-start too
sudo systemctl enable --now myapp

# 3. Confirm it is running
systemctl status myapp

# 4. Read the logs
journalctl -u myapp
```

Forget `daemon-reload` and your edits do not take effect. This is an easy spot to get stuck on, so remember: **"edited a unit file, run daemon-reload."** Bring it up with `enable --now`, confirm with `status`, read logs with `journalctl -u myapp` — the verbs from Sections 1 and 2 link up into one line here.

### Ask Claude ③: From journalctl Error Lines, Ask for the Next Move

> My service myapp fails to start. `systemctl status myapp` shows failed.
> Here is the output of `journalctl -u myapp -p err -b --no-pager`:
> ```
> [paste the error lines as-is]
> ```
> Here is my unit file:
> ```
> [paste the contents of /etc/systemd/system/myapp.service]
> ```
> List up to three likely causes in order of probability, with a check procedure for each.
> Show me the order to narrow it down — whether file permissions, the path, or the user spec is the suspect.

The trick is to hand over **both** the unit file and the error log. Claude cross-checks the "config (unit file)" against the "result (log)" and shows you the narrowing-down — whether the `ExecStart` path is wrong, whether `User=` lacks permission, and so on. This is the same craft as the inspection dialogue in Chapter 5.

## Section 4 — Scheduled Runs: cron and systemd timer

Scheduled runs like "take a backup every night" or "tally logs every hour" were traditionally cron's job. cron is still alive and well, and you can write it concisely with `crontab -e`.

But systemd has a **timer** that can be handled in the same unit as a service. The advantages: the run results are readable with journalctl, the next run can be listed with `systemctl list-timers`, and you can write dependencies like "after the network is up."

A timer is made as a **pair** of `.timer` and `.service`. The `.service` is "what to do," the `.timer` is "when to run it."

```bash
# What to do: /etc/systemd/system/mybackup.service
sudo tee /etc/systemd/system/mybackup.service > /dev/null <<'EOF'
[Unit]
Description=Daily backup job

[Service]
Type=oneshot
ExecStart=/home/user/bin/backup.sh
EOF

# When to run it: /etc/systemd/system/mybackup.timer
sudo tee /etc/systemd/system/mybackup.timer > /dev/null <<'EOF'
[Unit]
Description=Run mybackup daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF
```

`OnCalendar=daily` means "midnight every day." `Persistent=true` means that if the server was down and missed the run time, it runs late the next time it boots. Enable the timer itself (the `.timer`) and it starts going.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now mybackup.timer

# List the registered timers and "when each runs next"
systemctl list-timers
```

The `NEXT` column of `list-timers` lines up the next run time. This is **foreshadowing for the backup automation in Chapter 10.** A backup — work you want done "regularly, reliably, leaving a record" — fits exactly into this timer + service shape.

## Summary

What you did in this chapter:

1. Got the basic verbs of `systemctl` (status/start/stop/restart/reload/enable/disable/list-units).
2. Became able to read the `status` output (Active, enabled, Main PID, trailing logs).
3. Established the craft of narrowing logs by service, time, and severity with `journalctl` and handing them to Claude (carried over from Chapter 8 of the main series).
4. Turned your own script into `/etc/systemd/system/myapp.service` and ran the daemon-reload → enable --now → status → journalctl sequence.
5. Built the minimal form of a scheduled run with a systemd timer (.timer + .service).

What you hold now:
- A service of your own that auto-starts and revives after a crash (myapp.service).
- A template for scheduled runs (a .timer + .service pair).
- A dialogue shape of "hand both the config (unit file) and the result (log) to Claude to narrow it down."
- The touch to handle unfamiliar software with the same verbs by guessing "this is probably a service too."

You have the "service" as a unit. But a running service is only half the story. Where, and in what form, does the **data** it reads and writes live? In [Chapter 7, "The Database as a Foundation,"](/en/claude-debian/server/07-database/) we sort out when to use SQLite and when PostgreSQL, install PostgreSQL for real, and lay the foundation of where your data lives.

---

The server sub-series can be navigated from [Learning Debian with Claude — Server Edition](/en/claude-debian/server/). The main desktop series is at [all chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
