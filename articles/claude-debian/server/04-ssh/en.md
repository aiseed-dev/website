---
slug: claude-debian-server-04-ssh
lang: en
number: "04"
title: Chapter 4 — SSH, the Front Door
subtitle: Make keys, close passwords, come and go safely
description: You will never plug a monitor into the server again. You do everything from your own PC. The doorway for that is SSH. Make keys, close password authentication, narrow the door. This chapter locks down the front door together with Claude — including the craft of not locking yourself out and the settings that make daily access pleasant.
date: 2026.06.10
label: Claude × Debian Server 04
prev_slug: claude-debian-server-03-minimal-install
prev_title: Chapter 3 — The Minimal Install
next_slug: claude-debian-server-05-security-basics
next_title: Chapter 5 — The Basics of Defense
cta_label: Learn with Claude
cta_title: The door decides most of the defense.
cta_text: Eighty percent of a server's security is decided by where you can get in. Make a key, close the password. Just two tasks — but getting locked out here hurts. Have Claude review your settings, and proceed leaving yourself a way back.
cta_btn1_text: Continue to Chapter 5
cta_btn1_link: /en/claude-debian/server/05-security-basics/
cta_btn2_text: Back to Chapter 3
cta_btn2_link: /en/claude-debian/server/03-minimal-install/
---

## Why SSH Is the "Front Door"

In the previous chapter, you ended up with a desktop-less server. From here on, **you will never plug a monitor into this server again.** Unplug the keyboard too. Every operation happens from your own PC — the Debian machine you built in the main edition, or your work Windows, or your home Mac — across the network.

The doorway for that is SSH (Secure Shell). You log in to a server far away through an encrypted passage, type commands, and send files. Server administration runs almost entirely over this one passage.

So **the construction of the front door decides most of the server's security.** A server facing the internet even slightly is, from the moment it comes up, exposed to automated intrusion attempts from all over the world. Look at the logs and you will see strangers' IPs hammering away with "root / password," "admin / 123456." A weak door opens eventually. Conversely, a sturdy door is most of the foundation of defense.

There are only two things to do in this chapter. **Make a key. And close password access.** That alone renders brute-force attacks effectively powerless.

## Section 1 — Making Keys

### The Difference Between a Password and a Key

Against brute force, a password and a key differ utterly in strength.

A password is "memory." There is a limit to the length a person can remember, and a short one falls to brute force. As long as the server lets you try "is this the right string?" over and over, the danger remains that one day it gets guessed.

A key is "a possession." An SSH key is a pair of files — the **private key** you keep secret in your hands, and the **public key** you place on the server. The public key makes the lock; only the private key opens it. The private key is astronomically long, and brute force is practically impossible. **It asks "do you hold the right possession?", so guessing cannot get through.** That is the decisive difference between a password and a key.

### Make the Key

On your own PC (not the server — the side you operate from), run:

```bash
ssh-keygen -t ed25519 -C "taro@home-server"
```

`-t ed25519` is the key type — the short, strong type that current Debian recommends as standard. What follows `-C` is a comment, merely a note to tell later "which key this is" (many people put an email address or a purpose). 

When asked for a save location, press Enter for the default (`~/.ssh/id_ed25519`). You are asked for a passphrase. **Do not leave it blank here; always set a passphrase.** This is the lock that encrypts the private key itself, so that even if the private-key file is stolen, it is useless without the passphrase.

You end up with two files.

- `~/.ssh/id_ed25519` — **the private key. Never hand it to anyone.** Do not upload it to the server either.
- `~/.ssh/id_ed25519.pub` — the public key. This goes on the server. No harm in showing it to others.

### Place the Public Key on the Server

Register the public key on the server. There is a command that does it in one shot.

```bash
ssh-copy-id taro@192.168.1.50
```

`taro` is the username you made last chapter, `192.168.1.50` is the server IP you fixed last chapter. **Just this once, you are asked for a password.** Type it correctly and the public key is appended to the server's `~/.ssh/authorized_keys`. From now on you get in with the key.

### The First-Connection Fingerprint

The first time you connect, you are asked:

```text
The authenticity of host '192.168.1.50' can't be established.
ED25519 key fingerprint is SHA256:xxxxxxxx...
Are you sure you want to continue connecting (yes/no)?
```

This is the check of "**is this really the server I meant?**" Answer `yes` once and that fingerprint is recorded in your local `~/.ssh/known_hosts`, and next time it connects silently. For your own server on a home LAN, `yes` is fine — but if a "the fingerprint has changed" warning later appears, that means either tampering on the path or a rebuild of the server. You should not wave it through without knowing which.

### Ask Claude ①: Diagnose When You Cannot Connect

> I cannot connect to the server over SSH. Here is the output of running `ssh -v taro@192.168.1.50` on my own PC:
> [paste the verbose output from the -v flag, as-is]
>
> Where is it failing? Tell me, in the order to isolate it, whether the cause is the key, the network, or the server-side configuration.

For connection trouble, pasting the verbose output from the `-v` flag is the shortest path. Whether "the key was tried but refused" or "the connection never arrived at all," the output always says where it stopped. Claude reads that line and narrows the cause.

## Section 2 — Narrowing the Door

You can now get in with the key. But right now you can still get in with a password too. That is exactly what attackers go for. **Close password access, and forbid direct root login.** That makes the door key-only.

### The Way to Place a Config File

The server's SSH settings live in `/etc/ssh/sshd_config`. Rather than rewriting the main file directly, **current Debian recommends the way of dropping fragment files into `/etc/ssh/sshd_config.d/`.** Leave the main file alone and keep just your own changes in a separate file — easier to review later, and easy to remove.

On the server, create:

```bash
sudo nano /etc/ssh/sshd_config.d/99-hardening.conf
```

```text
PasswordAuthentication no
PermitRootLogin no
```

`PasswordAuthentication no` forbids password authentication, leaving only the key. `PermitRootLogin no` forbids direct root login (if you left root blank last chapter, this is a double insurance).

### The Craft of Not Locking Yourself Out

**This is the most important passage in this chapter.** Get the settings wrong and you lock yourself out. You meant to get in with the key, but a misconfiguration disables the key too, and the password is already closed — now you cannot get in over SSH at all. Always keep the following three.

**One: work with a second session held open.** Before you change the settings, open one more SSH window and leave it connected. If the new settings keep you out, you can revert the configuration from this still-open session. **This is the lifeline.**

**Two: check the syntax before applying.**

```bash
sudo sshd -t
```

If nothing prints, the syntax is correct. If an error prints, fix it before applying. A single typo can keep SSH from starting.

**Three: reload, do not restart.**

```bash
sudo systemctl reload ssh
```

`reload` re-reads only the settings without cutting existing connections. The session you have open stays alive while the new rules take effect. Once applied, **try a fresh key login from another window.** Confirm you can get in before you close the first session.

### Leave Yourself One Way Back

In case you still get locked out, keep exactly one way back. **For a home server, in a pinch you can plug in a monitor and keyboard and fix it from the physical console.** For a VPS, the provider's control panel always has a non-network entrance like a "web console" or "VNC console." Before you close SSH, confirm your server has this way back. Even if you lose the key, you can get in here and re-register.

### Ask Claude ②: Have It Review Your sshd_config

> To harden SSH, I am about to write the following into the server's `/etc/ssh/sshd_config.d/99-hardening.conf`:
> [paste the settings you wrote, as-is]
>
> With this content, is there a risk I lock myself out? Tell me what to check before applying, the safe procedure to apply, and how to roll back if I can no longer get in. I am on [a home server / a VPS].

Having Claude review the change **before applying** is the crux of this chapter. Ask specifically "is there a lockout risk?" Tell it whether you are on a home server or a VPS, and the answer reaches even to how to build your way back, fitted to your environment.

## Section 3 — Making Daily Access Pleasant

The door is sturdy now. Next, make the daily coming and going easy.

### Make an Alias with `~/.ssh/config`

Typing `ssh taro@192.168.1.50` every time is tedious. Write it into your local PC's `~/.ssh/config` and you connect by a short name.

```bash
nano ~/.ssh/config
```

```text
Host home
    HostName 192.168.1.50
    User taro
    IdentityFile ~/.ssh/id_ed25519
```

Now `ssh home` alone connects. `scp` and `rsync` can use this `home` name too. Even when you have several servers and several keys, list them here and you will not mix them up.

### Send and Receive Files

Two ways to move files between your hands and the server are enough to remember.

```bash
# One file from your hands to the server
scp ./backup.sql home:~/

# A whole directory, syncing only the differences, efficiently
rsync -av ./website/ home:~/website/
```

`scp` suits a one-off copy; `rsync -av` suits directory sync. `-a` means recursive while preserving attributes; `-v` means show what it is doing. From the second run on, `rsync` sends only the files that changed, so updating a large directory is fast.

### Paste Errors Straight to Claude

The connection drops, it is absurdly slow, you are rejected with `Permission denied` — do not try to interpret SSH-related error messages; **paste them to Claude as-is.** This is exactly the craft you picked up in the main edition's [Chapter 8, "Your First Troubleshooting"](/en/claude-debian/08-first-troubleshooting/). An error string always contains a clue to the cause. Setting the English locale last chapter was for this very moment.

### Ask Claude ③: Have It Write a Config for Your Setup

> Let me describe my environment. The servers I connect to over SSH are:
> - Home server: 192.168.1.50, user taro, key ~/.ssh/id_ed25519
> - A rented VPS: [IP], user [name], key [a different key file]
>
> Please write a `~/.ssh/config` that fits this setup. Give each a short alias and make explicit which key to use. The VPS uses port [number, if not 22].

Once you have several machines and several keys, hand-writing `config` is error-prone. Tell it your setup and Claude assembles a `config` with no mix-ups. Paste back what it returns and confirm one by one that `ssh alias` connects.

## Summary

What you did in this chapter:

1. Made an SSH key on your own PC with `ssh-keygen -t ed25519`.
2. Registered the public key on the server with `ssh-copy-id`, so you can log in with the key.
3. Placed a file in `sshd_config.d/` and forbade password authentication and direct root login.
4. Applied it without locking yourself out, via the three points of a second session, `sshd -t`, and `reload`.
5. Made an alias with `~/.ssh/config` and learned file transfer with `scp` / `rsync`.

What you hold now:

- A hardened SSH front door you enter with the key alone.
- A `~/.ssh/config` that connects by a short alias.
- Confirmation of a way back for emergencies (physical console or web console).

Now you can unplug the monitor from the server. A **screenless server, used across the network**, is complete here. In the next chapter, [Chapter 5, "The Basics of Defense"](/en/claude-debian/server/05-security-basics/), you lock down the layer beyond the door — the firewall, stopping unneeded services, automatic updates, and how to shut out the parties hammering you with brute force — together with Claude.

---

The server sub-series can be navigated from [Learning Debian with Claude — Server Edition](/en/claude-debian/server/). The main desktop series is at [all chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
