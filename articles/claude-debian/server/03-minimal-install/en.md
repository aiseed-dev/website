---
slug: claude-debian-server-03-minimal-install
lang: en
number: "03"
title: Chapter 3 — The Minimal Install
subtitle: Installing Debian without a desktop
description: A server does not need most of what the desktop edition installed. With the netinst image and a single tasksel screen, you build a Debian that carries only an SSH server and standard utilities. This chapter handles just the delta from the main edition's Chapter 7, and carries you through to a fixed IP address.
date: 2026.06.10
label: Claude × Debian Server 03
prev_slug: claude-debian-server-02-where-to-run
prev_title: Chapter 2 — Where to Put Your Server
next_slug: claude-debian-server-04-ssh
next_title: Chapter 4 — SSH, the Front Door
cta_label: Learn with Claude
cta_title: The less you carry, the stronger you are.
cta_text: A server is safer, easier to grasp, and harder to break the less it carries. This chapter is about choosing what NOT to install, not what to install. When a screen confuses you, paste its exact wording to Claude and check.
cta_btn1_text: Continue to Chapter 4
cta_btn1_link: /en/claude-debian/server/04-ssh/
cta_btn2_text: Back to Chapter 2
cta_btn2_link: /en/claude-debian/server/02-where-to-run/
---

## Why "Minimal"

In the desktop edition, you installed GNOME, Japanese input, and a set of applications to build an environment you touch every day. A server is the opposite. **The less it carries, the better.**

There are three reasons.

**One: the attack surface shrinks.** Every installed piece of software is a potential way in. A server with no screen needs no browser, no office suite, no image editor. What you do not install cannot be used to break in.

**Two: the volume of updates shrinks.** Fewer packages mean `apt upgrade` touches fewer things. The odds that an update breaks something, and the time an update takes, both go down. The machine stays stable even when you leave it alone.

**Three: the cost of grasping it shrinks.** Keep "what is on this server" small enough to hold in your head, and when trouble comes you can guess at the cause. The desktop state of "I forget when I installed what" is exactly what you want to avoid on a server.

This chapter does not repeat the desktop edition's [Chapter 7, "The Install Dialogue"](/en/claude-debian/07-installation-execution/) from scratch. **The shared parts — UEFI boot, disk selection, the encryption passphrase, creating a user, GRUB — apply as-is from Chapter 7.** What we cover here is only the server-specific delta: how to trim the software selection, how to log in to a desktop-less environment, and how to fix the IP address. Keep Chapter 7 open beside you as you read.

## Section 1 — The Fork in the Installer

### Use the netinst Image

For a server, the image is the same one as the desktop edition: the **netinst (network install) ISO**. It is small — a few hundred MB — and pulls the packages it needs from the network during installation. The Debian 13 (trixie) netinst bundles non-free firmware, so a common network chip connects with no extra work.

If you rented a VPS, you often do not need this procedure at all. Pick "Debian 13" in the provider's control panel and a minimal Debian comes up in a few minutes. In that case, skip Section 1 and start from the first login in Section 2. **Only those installing onto a home mini-PC or an old laptop actually work through this section by hand.**

### tasksel — the Heart of This Chapter

Follow Chapter 7's steps and, near the end, the "Software selection" (tasksel) screen appears. In the desktop edition you checked "Debian desktop environment" and "GNOME" here.

**On a server, this screen is everything.** Uncheck everything desktop-related, and check only the following two.

```
[ ] Debian desktop environment   <- uncheck
[ ]   ... GNOME                   <- uncheck
[ ]   ... KDE Plasma              <- uncheck
[ ]   ... any other DE            <- uncheck all
[ ] web server                    <- uncheck (add only what you need later)
[*] SSH server                    <- check
[*] standard system utilities     <- check
```

The space bar toggles a check, Tab moves to "Continue," Enter confirms. End up with **only "SSH server" and "standard system utilities"** lit. That gives you a minimal Debian with no desktop.

If you forget "SSH server," you can add it later with `apt install openssh-server`, but checking it here lets you move straight into next chapter's SSH setup after reboot. Do not forget it.

### The root Password and sudo

Your approach to creating a user is the same as Chapter 7. **This book recommends leaving the root password blank and giving your ordinary user `sudo`.** The reasons are the same as in the desktop edition — it funnels administrative actions through a single entrance — and the "you cannot log in directly as root" state pays off when you tighten SSH next chapter.

Make the username short and lowercase (`taro`, `admin-t`). This username is the name you will type on every SSH connection from the next chapter on.

### Prefer an English Locale

In the desktop edition you chose "Japanese" for the language. On a server, do the reverse: **set the locale to English (`C.UTF-8` or `en_US.UTF-8`).** The logs and error messages a server emits are better left in English — easier when you paste them to Claude, easier when you search, easier to match against the world's records of the same error. An error string translated into your language actually thins out its sources. On a server with no human watching the screen, prioritize ease of investigation over friendliness of display.

### Ask Claude ①: Paste the Confusing Options Verbatim

> The Debian installer's "Software selection" screen shows the following items:
> [copy out each item shown on the screen, one line each, verbatim]
>
> I want to build a server with no desktop. Which should I check, and which should I uncheck? Add one line per item explaining what it installs.

The trick is to paste the screen's wording **as-is**. The items shift slightly with the Debian version and configuration. You get an answer aimed at the screen in front of you, not a generality.

## Section 2 — The First Login and the First Ten Minutes

### A Black Screen and a Prompt

After reboot, all the server shows is a black screen and a login prompt. There is no desktop. Type your username and password and a `$` prompt appears. **This is the server's bare face.** From here on, every task happens at this command line.

The first things to do are fixed. Work through them in order.

### Check Your Own IP Address

From the next chapter on, you connect to this server from another PC, so you need the server's IP address.

```bash
ip a
```

Look for a line like `inet 192.168.x.x`. The one that is *not* `127.0.0.1` (the loopback that points at itself) — usually a line beginning with `192.168.` or `10.` — is this server's address inside your home network. Note it down.

### Bring the System Up to Date

```bash
sudo apt update
sudo apt upgrade
```

With a minimal configuration, there is little to update. It finishes quickly.

### If sudo Is Missing

If you missed adding the user to the sudo group during install, `sudo` gets rejected. In that case log in once as root (`su -` if you set a root password, or from the physical console if you did not) and run:

```bash
apt install sudo
usermod -aG sudo your-username
```

Then log out and back in, and sudo will work. Group changes take effect on the next login.

### Check the Hostname

```bash
hostnamectl
```

This server's name appears. If you do not like it, change it with `sudo hostnamectl set-hostname server-name`. Avoid company or real names; a role-revealing name like `home-server` or `nas01` keeps you from getting lost once you have several machines.

### Ask Claude ②: Have It Read Your `ip a` Output

> I ran `ip a` on the server and got this:
> [paste the output as-is; you may mask the MAC address]
>
> Which is this server's IP address? What is the interface name (eth0 / enp3s0, etc.), and is it wired or wireless? Explain, for a beginner, how this server is connected inside my home LAN.

The output of `ip a` looks like a wall of symbols at first. Paste it to Claude and you get back, in terms of your own setup, what each line means. The "paste the output and have it read" craft you picked up in the main edition's [Chapter 3, "How to Tell Claude About Your Environment"](/en/claude-debian/03-telling-environment/) works here too.

## Section 3 — Fixing the IP Address

### Why It Has to Be Fixed

On a home network, the router hands out IP addresses automatically (DHCP). Convenient, but a problem for a server. **If the assignment changes on reboot or over time, the destination for SSH changes every time.** ".50 yesterday, .53 today" gives the front door you build next chapter no fixed address.

So fix the server's IP. There are two ways.

### Way One: Reserve It on the Router (Recommended)

**For most homes, this is the easiest and safest.** The router's settings screen has an item called "DHCP reservation," "static IP assignment," or "static DHCP." There you register "always hand this IP to the device with this MAC address." You touch nothing on the server side. The router keeps the promise.

But the location and the name of that settings screen differ wildly by router model. Here, telling Claude your model number and asking is fastest.

### Way Two: Fix It on the Server

If circumstances keep you from touching the router, fix it on the server. A minimal Debian is managed through `/etc/network/interfaces`. Below is a minimal example (replace the interface name `enp3s0` with the one from your own `ip a` output).

```bash
sudo nano /etc/network/interfaces
```

```text
auto enp3s0
iface enp3s0 inet static
    address 192.168.1.50/24
    gateway 192.168.1.1
```

Set `address` to an address free on your home network, and `gateway` to the router's address (usually `192.168.1.1` or `192.168.0.1`). Save, then apply.

```bash
sudo systemctl restart networking
```

**Fixing it on the server has a pitfall.** If you pick a number inside the range the router's DHCP hands out (say, .100–.200), it may collide with another device. Pick one outside the range (say, .50). If you are unsure how to tell, paste your setup to Claude and check.

### Ask Claude ③: Ask for the DHCP-Reservation Steps for Your Router

> My home router is a [maker and model, e.g. Buffalo WSR-3200AX4S].
> I want to assign a fixed IP to a Debian server. The server's MAC address is [the value from ip a], and the IP I want is [e.g. 192.168.1.50].
> Walk me through setting up a "DHCP reservation" in this router's admin screen, one step at a time, following the actual item names on the screen.

Router settings are the classic case of model dependence. A generality printed in a book is useless. **The steps specific to the model in front of you** are best gotten by telling Claude the model number. Open the router's screen with the returned steps beside you.

## Summary

What you did in this chapter:

1. With the netinst image, chose only "SSH server" and "standard system utilities" in tasksel.
2. Installed with root left blank and `sudo` given to your ordinary user.
3. Set the locale to English, prioritizing ease of investigation when trouble comes.
4. Checked the IP with `ip a` on first login and brought the system up to date with `apt update && upgrade`.
5. Fixed the IP address with a DHCP reservation on the router, or with server-side configuration.

What you hold now:

- A minimal Debian server with no desktop.
- An IP address fixed inside your home network (it becomes the destination for SSH next chapter).
- A note of this server's particulars (IP, interface name, hostname).

Up to here, you were still operating the server with a monitor and keyboard plugged in directly. In the next chapter, [Chapter 4, "SSH, the Front Door"](/en/claude-debian/server/04-ssh/), you build the mechanism to come and go safely from another PC. Once that is done, you can unplug the monitor and start running it as the screenless server it was always meant to be.

---

The server sub-series can be navigated from [Learning Debian with Claude — Server Edition](/en/claude-debian/server/). The main desktop series is at [all chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
