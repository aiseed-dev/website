---
slug: claude-debian-server-07-containers
lang: en
number: "07"
title: Chapter 7 — The Container Option
subtitle: Shipping in units you can break and rebuild
description: Installing directly with apt has limits — dependency clashes, leftover residue after removal, version mismatches. A container bundles an app and its dependencies into a unit you can break and rebuild. And its configuration becomes a single text file, compose.yaml. The moment it becomes text, it is Claude's home turf.
date: 2026.06.10
label: Claude × Debian Server 07
prev_slug: claude-debian-server-06-systemd-services
prev_title: Chapter 6 — The Service as a Unit
next_slug: claude-debian-server-08-publishing
next_title: Chapter 8 — Opening Up to the Outside World
cta_label: Learn with Claude
cta_title: Get a unit you are allowed to break.
cta_text: A container bundles "app plus dependencies" into a box you can rebuild any time. The blueprint for that box is a single text file, compose.yaml. Text is Claude's strong suit — hand over your situation and have it write a blueprint made for you.
cta_btn1_text: Continue to Chapter 8
cta_btn1_link: /en/claude-debian/server/08-publishing/
cta_btn2_text: Back to Chapter 6
cta_btn2_link: /en/claude-debian/server/06-systemd-services/
---

## Why Use Containers on a Server

Chapter 6 walked the path of installing software with apt and running it as a systemd service. To run one file share and one note-sync service, that approach is plenty. It is plain, transparent, and faithful to the Debian way.

But as the number of things you want to run grows, that approach starts to creak.

**First: dependency clashes.** App A wants an old library; app B wants a new one. Install both on the same machine with apt, and one of them can stop working. The moment you put several apps on a single server, this clash becomes real.

**Second: leftover residue.** Run `apt remove` on an app, and config files, logs, created users, and database fragments still linger here and there. Install-and-remove a few times, and the server slowly accumulates "dirt no one can explain."

**Third: version mismatches.** Debian packages prize stability, so they are often not the latest version. For an app where you want a new feature, this becomes a leash.

A container solves all three at once. **A container locks an app and its dependencies whole into a single box, cut off from the host environment.** What is inside the box stays inside the box and does not dirty the outside. If you do not like it, throw the whole box away and rebuild it.

And the decisive part is that the blueprint for that box becomes a single **text file** called `compose.yaml`. What runs and how, which ports open, where the data lives — all of it is written into one readable text file. **The moment it becomes text, it is Claude's home turf.** What this book has said all along — "anything that becomes text can be handled together with Claude" — finds its strongest expression on a server right here.

## Section 1 — Docker or Podman?

On Debian 13 (trixie), both tools for running containers install from standard apt: Docker and Podman. People hesitate over which to pick first, so here is the difference, stated honestly and briefly.

**Docker** is the de facto industry standard. The world's tutorials, the explanations for official images, the search results when something breaks — the sheer volume of information is overwhelming. Being able to reach an answer easily when stuck is a big advantage for a beginner. The flip side is a design weight: a resident daemon (a process that keeps running in the background) runs with root privileges.

**Podman** is designed without a daemon, and running containers as an ordinary user (rootless) is the natural path. Security-wise, this is the cleaner design. Its commands are almost compatible with Docker's — replace `docker` with `podman` and most things just work. That said, the volume of information lags Docker by a step.

This chapter proceeds with Docker. The reason is the volume of information. But **the content of this chapter holds just as well on Podman.** How you write compose.yaml, the idea of separating data from containers, the judgment criteria — none of it depends on the tool. If you later want to switch to Podman, nothing you learn here is wasted.

```bash
# Install Docker itself and the compose plugin
sudo apt update
sudo apt install docker.io docker-compose-v2

# Check that it is running
sudo systemctl status docker
docker --version
docker compose version
```

`docker.io` is Docker itself, and `docker-compose-v2` is the `docker compose` subcommand that handles several containers together. Older articles show `docker-compose` (with a hyphen, a standalone command), but the standard now is `docker compose` (space-separated, a plugin).

If you do not want to type `sudo` every time, add your user to the docker group.

```bash
# Add yourself to the docker group (use your own user name)
sudo usermod -aG docker $USER
# Logging back in (or rebooting the server) is needed to take effect
```

Let me state this honestly. **Joining the docker group means effectively gaining root privileges.** The Docker daemon runs as root, so anyone who can drive it can do whatever they like with host files through a container. On a solo experiment box you need not worry, but on a server several people log into, decide carefully who goes into the docker group. The meaning of this "effectively root" sits on the same line as the threat model covered in Chapter 5.

### Ask Claude ①: Which Suits Me, Docker or Podman?

> I run a home server on Debian 13. My situation is as follows:
> [paste my-server.md. In particular, state "is the only user me or several?", "LAN-only or planning to publish?", "the apps I want to run"]
>
> For this situation, which container runtime suits me better, Docker or Podman? From the angles of security, volume of information, and ease of switching, please explain with reasons grounded in my situation.

Tool choice tends to drift into ideology, but hand over your situation and Claude weighs it concretely. Even an obvious conclusion — Docker for a solo experiment box, consider Podman as people grow — clears away hesitation once you confirm it against your own situation.

## Section 2 — Your First Container and compose

### First, Run One and Confirm Connectivity

Before theory, run one. Docker has a small image made just for confirming connectivity.

```bash
# Minimal container for a sanity check. It auto-removes after running (--rm)
docker run --rm hello-world
```

If "Hello from Docker!" appears, then the whole path — downloading the image, starting and stopping the container — is working. Because we added `--rm`, the finished container disappears without leaving litter. This is the first step into the easygoing nature of containers.

### compose.yaml as a Blueprint

Instead of typing a long incantation as `docker run` every time, you write the configuration out into one text file and run that. That is `compose.yaml`. As an example, here is a complete configuration that brings up the nginx web server on port 8080 and slots in HTML you prepared yourself.

First, prepare a working directory and its contents.

```bash
mkdir -p ~/webtest/html
echo '<h1>My first container</h1>' > ~/webtest/html/index.html
```

Inside that `~/webtest/`, create `compose.yaml` with the following contents.

```yaml
services:
  web:
    image: nginx:stable          # the official image to use
    ports:
      - "8080:80"                # connect host 8080 to container 80
    volumes:
      - ./html:/usr/share/nginx/html:ro  # slot in local html read-only
    restart: unless-stopped       # restart automatically if it goes down
```

Run the following in this directory and the container comes up exactly as configured.

```bash
cd ~/webtest
docker compose up -d        # -d runs it in the background (detached)

docker compose ps           # list running containers
docker compose logs -f      # watch the logs streaming (Ctrl+C to leave)
```

Open `http://your-server-address:8080` from a browser or another machine, and the HTML you just wrote appears. Stopping and cleaning up is one line.

```bash
docker compose down         # stop and remove the container
```

`down` removes the container, but the files you placed in `./html` stay on your machine as they were. This is the crux.

### Data in Volumes, Containers Disposable

There is one principle in container design more important than any other, and I want you to remember it. **Put data you cannot lose outside the container (in a volume or a bind mount), and treat the container itself as disposable.**

- **Bind mount.** As with `./html:/usr/share/nginx/html` above, a way to wire a host directory directly into the container. Its contents are visible as local files, so it suits config files and small data.
- **Volume.** A way to slot a storage area managed by Docker into the container. It suits large, fast-changing data like a database.

Whichever you use, the principle is the same. **Separate data from the lifespan of the container.** With this in place, when you want to upgrade an app's version, all you do is "throw away the container and rebuild from a new image." The data remains outside, untouched. This separation — "the container is disposable, the data is outside" — becomes the major premise of the backups covered in Chapter 9. When the place where data-to-protect lives is clear, backups become dramatically simpler.

### Ask Claude ②: Have It Write a compose.yaml for the App You Want to Run

> On my Debian 13 server (Docker already installed), I want to run [app name; e.g., Nextcloud / Vaultwarden / Gitea / my own web app]. My server's situation is as follows:
> [paste my-server.md — memory, disk, whether LAN-only, etc.]
>
> Please write a compose.yaml for this app. Then **explain line by line what each line does**. To avoid losing data, also state clearly which directories should be a volume or a bind mount.

This is the heart of the chapter. Do not just "have it write" the compose.yaml — make it a set that includes **having it explain the meaning of each line**. Pasting a setting you do not understand and running it is the same as adding one more black box. Have it explain line by line, and next time you will be able to read a similar configuration yourself.

## Section 3 — Things You Are Better Off Not Containerizing

Read this far and you might think "I should containerize everything." But that is as extreme as "install everything with apt." Some things suit containers, and some do not.

The classic things that do not suit are **those at the core of the host, and those close to the hardware**.

- **sshd (the SSH listener).** The very door for getting into the server. Put it in a container, and you create the absurd situation of being locked out of the server when the container breaks. Run it directly on the host.
- **The firewall (ufw / nftables).** It protects the whole host, so running it on the host is the right shape. Use what you set up in Chapter 5 as-is.
- **Time sync, the kernel, drivers.** Things close to the foundation of the hardware or OS belong outside containers, as the host's responsibility.

Conversely, judge whether something suits a container by these three.

1. **Does it hold state?** Things with a "run it, rebuild it someday" nature, like web apps and services, suit containers. Conversely, things like host configuration itself, which are "decide once and do not move," sit more naturally on the host.
2. **Do you swap it often?** Things you try across versions, or install and remove, benefit from a container's disposability.
3. **The quality of the official image.** If the developer officially ships an image and it is maintained, you can use it with confidence. Avoid images of unknown provenance — they mean taking on a black box.

**Both "everything in containers" and "everything with apt" are extreme.** The host's core sits plainly on the host; apps that churn live easily in containers — this division of labor builds a server that breaks rarely and can be explained.

### Ask Claude ③: Have It Security-Review an Existing compose.yaml

> Here is a compose.yaml I am running, or about to use:
> ```
> [paste the compose.yaml contents as-is]
> ```
>
> Please review this configuration from a security standpoint. In particular, look at: ports needlessly open to the outside, dangerous passwords or keys written in plaintext, excessive privileges like `privileged`, and dangerous volume mounts. For each finding, add why it is dangerous and a recommended fix.

Before you run a compose.yaml grabbed off the web as-is, build the habit of inserting this one round trip. The handier the example, the more likely it is to be "all privileges, all ports open, for now." This habit pays off before you open up to the outside in Chapter 8.

## Section 4 — Containers, Operated with Claude

The daily life of running containers, distilled, is the repetition of three moves. **Have it write, have it explain, have it adjust to your situation.**

- **Have it write.** Tell it the app name you want to run and have it draft a compose.yaml (①).
- **Have it explain.** Have it explain the meaning of each line, one at a time. Leave no line you do not understand.
- **Have it adjust.** Have it rewrite the port numbers, volume locations, and environment variables (passwords, domain names, and so on) to match your own server's situation.

And the strongest single move when something will not run is to paste the logs as-is. A container that dies right after starting, a port that will not open, a database that will not connect — the cause is almost always written in the logs.

```bash
# See logs, including for a container that died
docker compose logs

# Follow just one service, recent lines
docker compose logs --tail=50 web
```

Paste this output to Claude as-is, and the meaning of the error and the fix come back. It is exactly the same craft as pasting `journalctl` logs in Chapter 6. **Everything that happens on a server becomes text, and text can be read together with Claude.** With containers, this principle does not change.

### Ask Claude ④: Have It Diagnose a compose Error Log

> Here is my compose.yaml:
> ```
> [paste the compose.yaml]
> ```
>
> After `docker compose up -d`, the container does not run properly. Here is the output of `docker compose logs`:
> ```
> [paste the log as-is]
> ```
>
> Please tell me what is happening, the cause, and the fix. Add the corrected compose.yaml and the commands I should run to confirm.

Being able to hand over an error log "in a readable form, as-is" is the strength of the server-and-Claude fit. Not a screenshot — paste it as text. Just reuse the craft you picked up in Chapter 3, on containers too.

## Summary

What you did in this chapter:

1. Confirmed the limits of installing directly with apt (dependency clashes, residue, version mismatches) and understood why containers solve them.
2. Grasped the difference between Docker and Podman, installed Docker, and confirmed connectivity (including the meaning of docker group = effectively root).
3. Wrote a minimal compose.yaml example (publishing nginx on 8080) and ran the full loop of start, check, and stop.
4. Sorted out the principle "data outside, container disposable" and the criteria for what does and does not suit a container.
5. Picked up the pattern of having Claude write, explain, and adjust a compose.yaml, and diagnose an error log.

What you hold now:
- One working compose.yaml (the minimal nginx) and a memory of the commands that run it.
- A draft compose.yaml for the app you want to run (made in ① and ②).
- A note on the criteria for "what does and does not suit a container."

In Chapter 8, we consider finally **opening up to the outside world** the server you have practiced with safely on the LAN until now. Domains, reverse proxies, TLS certificates — publishing is a near-irreversible decision. Including the perfectly respectable option of "not publishing," you will design, together with Claude, a publishing route that fits your own line and situation.

---

The server sub-series can be navigated from [Learning Debian with Claude — Server Edition](/en/claude-debian/server/). The main desktop series is at [all chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
