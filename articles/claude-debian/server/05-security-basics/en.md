---
slug: claude-debian-server-05-security-basics
lang: en
number: "05"
title: Chapter 5 — The Basics of Defense
subtitle: Shrink the attack surface, automate updates
description: The moment you expose a server to the internet, bots from all over the world start knocking on the door. The idea of an attack surface, minimal allow-listing with ufw, automated updates with unattended-upgrades, and a watchdog called fail2ban — build up the basics of defense one piece at a time, handing logs to Claude as you go.
date: 2026.06.10
label: Claude × Debian Server 05
prev_slug: claude-debian-server-04-ssh
prev_title: Chapter 4 — SSH, the Front Door
next_slug: claude-debian-server-06-systemd-services
next_title: Chapter 6 — The Service as a Unit
cta_label: Learn with Claude
cta_title: Finish your defenses before you go public.
cta_text: Running a service is fun. But the moment you expose it, bots from all over the world start knocking on the door. Shrink the attack surface, automate updates, post a watchdog — this chapter builds the foundation for running anything with peace of mind.
cta_btn1_text: Continue to Chapter 6
cta_btn1_link: /en/claude-debian/server/06-systemd-services/
cta_btn2_text: Back to Chapter 4
cta_btn2_link: /en/claude-debian/server/04-ssh/
---

## Why the Defense Chapter Comes Before the Run-a-Service Chapter

In a typical primer, this is about where a "let's run something" chapter shows up. Stand up a web server, start sharing files, publish your own app — that is where the fun begins.

This book puts the defense chapter first. The reason is simple: **the moment you expose a server to the world, bots from all over the world start knocking on the door in unison.** That is not a scare tactic. While you have not exposed anything yet, take a peek at the SSH login failures.

```bash
sudo journalctl -u ssh --since "1 hour ago" | grep -i failed
```

If your server lives only inside a home LAN, this should be nearly silent. The failure log will be, at most, the few lines where you mistyped your own password. There is value in seeing this "quiet" with your own eyes once. **Run the same command after you go public, and failure logs from unknown IPs pile up by the minute.** That contrast is what makes you understand, in your body, what this chapter is defending.

```bash
# On older systems the same record also lives in /var/log/auth.log
sudo tail -n 50 /var/log/auth.log 2>/dev/null
```

How heavy your defense needs to be depends on where your server sits. Sorted out, there are two levels.

- **LAN-only.** Inside your home or office router, not directly reachable from outside. The threat is limited; defense need only prevent "household accidents."
- **Public (directly reachable from the internet).** A VPS, a static IP, an opened port — at that moment the threat model jumps a level. Everything in this chapter becomes mandatory.

**If you are LAN-only now, learn your defenses while it is still quiet.** Scrambling to learn after you go public is like searching for how to fit a lock while the door stands wide open.

## Section 1 — The Idea of an Attack Surface

Security talk is full of jargon and makes people brace themselves, but the idea underneath is startlingly simple.

**Software you never installed cannot be attacked. A service that is not running is not a hole.** This is called "shrinking the attack surface." The first step of defense is not adding clever settings; it is subtracting what you do not need. The stance repeated in ["Design by Subtraction"](/en/insights/subtraction-design/) works here too.

First, look at every "ear" your server has open to the outside.

```bash
# Ports and processes currently listening (LISTEN)
ss -tlnp
```

The output looks like this.

```
State   Recv-Q  Send-Q  Local Address:Port   Peer Address:Port  Process
LISTEN  0       128     0.0.0.0:22           0.0.0.0:*          users:(("sshd",pid=701,fd=3))
LISTEN  0       4096    127.0.0.1:631        0.0.0.0:*          users:(("cupsd",pid=812,fd=7))
```

What matters here is to **read every single line and what it means**. `0.0.0.0:22` means "listening on port 22 on every network interface" — that is, reachable from outside. `127.0.0.1:631` means "listening on localhost only" — not reachable from outside. Once you see this difference, you can see which services are truly exposed.

### Ask Claude ①: Decipher the `ss -tlnp` Output

> I ran `ss -tlnp` on my Debian 13 server and got this output:
> ```
> [paste the ss -tlnp output as-is]
> ```
> For each line, explain what service it is and whether it is reachable from outside (the internet) or local only.
> Then, given my server's purpose [e.g., LAN-only file sharing], classify which ones are "safe to close" and which "must not be closed," with reasons.

Having Claude walk through the `ss` output line by line is the single most valuable use in this chapter. What looks to your eyes like a string of symbols turns, once handed to Claude, into a map of "this ear is needed, this ear can be sealed."

Services that turn out to be unnecessary: stop them, and disable auto-start too.

```bash
# Example: the print server cups was unneeded on a server box
sudo systemctl disable --now cups
# Confirm it is no longer listening
ss -tlnp
```

`disable --now` does both "stop it now" and "do not start it from now on" at once. One less item on the attack surface.

## Section 2 — Firewall: Start from Minimal Allow

Once you have subtracted the attack surface, the next step decides "of the ears that remain, who do we answer?" That is the firewall's job. On Debian, `ufw` (Uncomplicated Firewall) is easy to handle.

The idea is one thing. **Deny everything by default. Allow only what is needed, by name.** A whitelist approach.

```bash
sudo apt install ufw
```

**Never get the order wrong here.** If you enable "deny everything" before allowing SSH, you lock out the very SSH session you are connected with. **Always write `allow ssh` first, then `enable`.**

```bash
# 1. Policy first: deny incoming by default, allow outgoing
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 2. Allow SSH first so you do not lock yourself out (most important)
sudo ufw allow ssh

# 3. Only now, enable it
sudo ufw enable

# 4. Check the current rules
sudo ufw status verbose
```

Make it a habit to pause right before `enable` and look back to confirm `allow ssh` is in place. Get this wrong on a remote server, and you cannot get back in short of a physical console or recovery means.

For a service used only inside your LAN, you can write "allow only from a specific network." This narrows the attack surface further.

```bash
# Example: allow web access only from the home LAN (192.168.1.0/24)
sudo ufw allow from 192.168.1.0/24 to any port 80
# To allow SSH only from the home LAN (for a non-public server)
sudo ufw allow from 192.168.1.0/24 to any port 22
```

`from 192.168.1.0/24` means "only from devices within this subnet." It becomes a setting that the outside cannot reach in the first place.

### Ask Claude ②: Design a Full ufw Ruleset from Your Use Case

> I am setting up ufw on my Debian 13 server. My usage is as follows:
> - Location: [e.g., inside my home LAN / on a VPS exposed to the internet]
> - Services I plan to run: [e.g., SSH, file sharing (Samba), a web server later]
> - IP range of my management devices: [e.g., home LAN is 192.168.1.0/24]
>
> Keeping the order that avoids a lockout, give me the `ufw` commands to run from top to bottom.
> Add a one-line comment on what each command allows or denies.

Convey your use case accurately, and the full ruleset drops straight onto your desk. **Then you vet it line by line and run it.** With a firewall, a one-character mistake leads directly to a lockout, so you need the stance of reviewing it rather than swallowing it whole.

## Section 3 — Automating Updates

The defense that works the most yet is forgotten the most is **keeping updates applied**. Most attacks aim at known holes for which a patch has long since shipped. The hole is closed, but it stays open because you did not update — this is the most frequent accident.

A server is often not sitting in front of a screen. So instead of relying on manual updates, make it so that **security updates at least get applied automatically**. Debian has `unattended-upgrades`.

```bash
sudo apt install unattended-upgrades
```

It is configured by default to auto-apply security updates, but confirm and enable it interactively.

```bash
sudo dpkg-reconfigure -plow unattended-upgrades
```

Answer Yes to "Enable automatic updates?" and from then on security updates apply quietly. You can read what got applied later with `cat /var/log/unattended-upgrades/unattended-upgrades.log`.

That said, some updates "do not take effect until you reboot" — kernel and glibc updates among them. Whether a reboot is needed shows up as the presence of a file.

```bash
# If this file exists, a reboot is pending
ls -l /var/run/reboot-required 2>/dev/null && cat /var/run/reboot-required

# Tells you which services are still holding old libraries
sudo apt install needrestart
sudo needrestart
```

`needrestart` handles what can be done without a reboot by just restarting the service, and tells you only about what truly needs a reboot. When you would rather not reboot a server needlessly, this distinction pays off.

### Ask Claude ③: Decipher Suspicious Lines in auth.log

> On my Debian 13 server, the output of `sudo journalctl -u ssh --since "today"` had lines like these:
> ```
> [paste the failure logs / unfamiliar lines as-is]
> ```
> Is this ordinary brute-forcing by bots, or a sign of something targeted?
> Line by line, explain what each means (source, attempted username, reason for failure).
> If there is action I should take now, tell me in order of severity.

The "hand the log to Claude as-is" craft you picked up in the main series' [Chapter 8 troubleshooting](/en/claude-debian/08-first-troubleshooting/) moves here into a security context. **Do not fear lines you cannot read — paste them.** Claude sorts them into "just bot noise" versus "a sign worth caring about."

## Section 4 — fail2ban, the Watchdog

Finally, post a watchdog. `fail2ban` is a tool that watches logs and, **when login failures from the same IP keep coming over a short span, blocks that IP for a set time.** It physically slows brute-force attacks.

Let me make the priority clear here. **fail2ban is a supplement, not the lead.** The heart of SSH defense is what you did in Chapter 4: **key authentication plus disabling password authentication.** Once passwords are disabled, no amount of brute-forcing gets through. On top of that, fail2ban is posted to chase off bots that keep polluting the logs and to keep those logs readable. **The order is "key auth first, fail2ban after."**

```bash
sudo apt install fail2ban
```

The Debian way is not to edit `jail.conf` directly but to write only your overrides into `jail.local`. The minimal config for SSH is just this.

```bash
# Create /etc/fail2ban/jail.local (contents below)
sudo tee /etc/fail2ban/jail.local > /dev/null <<'EOF'
[DEFAULT]
# How long to ban (10 minutes)
bantime = 10m
# Within this window
findtime = 10m
# After this many failures
maxretry = 5

[sshd]
enabled = true
EOF

sudo systemctl restart fail2ban
```

Whether it is running, and whether it has banned anyone, you check with the dedicated client.

```bash
sudo fail2ban-client status sshd
```

The IPs listed under `Banned IP list:` are who is currently shut out. On a LAN-only server this will stay empty for days. On a public server, within a few hours a handful start lining up. Proof that the watchdog is barking properly.

### Ask Claude ④: Inspect Whether Your Server's Defenses Are Complete

> Here is the current state of my Debian 13 server's defenses:
> ```
> $ ss -tlnp
> [output]
> $ sudo ufw status verbose
> [output]
> $ sudo fail2ban-client status sshd
> [output]
> ```
> SSH key auth is [enabled / not yet], password auth is [disabled / not yet].
> Placement is [LAN-only / planning to go public].
> In this state, point out what is missing from my defenses, what is out of order, and what is excessive.
> Inspect whether there is a fatal hole if I go public right now.

Hand over several command outputs together, and Claude can inspect "attack surface, firewall, watchdog, and SSH itself" as a single picture. **Ask Claude for a final check before you press the publish button.** It catches the "ordering holes" you would miss on your own.

## Summary

What you did in this chapter:

1. Peeked at pre-publication SSH failure logs and recorded the "quiet" as a baseline.
2. Read every open ear with `ss -tlnp` and `disable --now`'d the services you did not need.
3. Started ufw from "deny by default, allow SSH only," and learned LAN-restricted allows too.
4. Automated security updates with unattended-upgrades and learned to tell when a reboot is needed.
5. Posted fail2ban as a watchdog and sorted out its priority relative to key authentication.

What you hold now:
- A server with a narrowed attack surface, guarded by ufw.
- A state where security updates keep applying automatically.
- The craft of reading logs and handing them to Claude for inspection (carried over from Chapter 8).
- A checklist-like dialogue that has Claude inspect "is it OK to go public?"

The foundation of defense is in place. In [Chapter 6, "The Service as a Unit,"](/en/claude-debian/server/06-systemd-services/) you finally **run something**. The insides of a server are, in the end, "a collection of processes that systemd looks after." You will learn to handle starting, stopping, auto-start, logs, and failure response all through the same shape — the unit called a "service." The very verb you typed with `systemctl disable --now` in this chapter is the doorway into the next.

---

The server sub-series can be navigated from [Learning Debian with Claude — Server Edition](/en/claude-debian/server/). The main desktop series is at [all chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
