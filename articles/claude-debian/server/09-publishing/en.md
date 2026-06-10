---
slug: claude-debian-server-09-publishing
lang: en
number: "09"
title: Chapter 9 — Opening Up to the Outside World
subtitle: Domains, reverse proxies, TLS
description: Until now everything could be practiced safely on the LAN. Publishing is a near-irreversible decision — the attack surface changes all at once. We cover the three-piece set of domain, reverse proxy, and TLS certificate, all the way through the home-line obstacle (CGNAT), and design a publishing route that fits your situation together with Claude. "Not publishing" is a perfectly respectable choice.
date: 2026.06.10
label: Claude × Debian Server 09
prev_slug: claude-debian-server-08-fastapi
prev_title: Chapter 8 — Running Your Own App
next_slug: claude-debian-server-10-backup
next_title: Chapter 10 — Protecting Your Data
cta_label: Learn with Claude
cta_title: The decision to expose yourself to the world.
cta_text: Publishing is near-irreversible. The parties connecting to you become the whole world at once. That is exactly why you must design a route that fits your line and situation. Including the choice "not to publish," draw the map together with Claude.
cta_btn1_text: Continue to Chapter 10
cta_btn1_link: /en/claude-debian/server/10-backup/
cta_btn2_text: Back to Chapter 8
cta_btn2_link: /en/claude-debian/server/08-fastapi/
---

## Why Publishing Is a Chapter of Its Own

Every chapter up to here could be practiced safely inside your home LAN. The file share, note sync, the database in Chapter 7, the app you built in Chapter 8 — while they run only inside the house, the only party connecting to you is you. Even if you fail, no one is watching. So you could break things and rebuild them at ease.

Publishing is the decision to step one pace outside that safe zone. And **publishing is near-irreversible.** Once you expose a server to the internet, as Chapter 1 said, the parties connecting to you become the whole world. The world's automated scanners begin hammering your server 24 hours a day, starting the moment you publish. This is not a scare line — it is an observed fact that will appear in your logs on the day you publish. The attack surface changes all at once. So publishing rests entirely on the defenses you built in Chapter 5 (firewall, SSH key authentication, fail2ban).

Let me say this clearly first. **"Not publishing" is a perfectly respectable choice.** If all you want is to get into your own server from outside, you do not need to open a door toward the world. Using something like Tailscale, you can have "only you (and those you allow) get safely into your home LAN from outside." This is not publishing — it is, so to speak, an extension cord for yourself alone. The attack surface barely grows. For a family photo server or your own note sync, this is often enough.

Even so, there are scenes where you "want to publish something toward the world" — your own blog, a service you want to share with someone, an app you want others to use. This chapter sorts out, honestly, the parts you need then and the obstacles peculiar to a home line.

## Section 1 — The Three-Piece Set for Publishing

To make something "viewable by anyone on the internet," you need at least three parts. Grasp what each one is, a paragraph at a time.

**Domain.** A name a human can remember, like `example.com`. A server has only a numeric IP address, and memorizing that is not realistic. A domain is the "signboard" you hang on those numbers. You acquire it from a registrar (a domain registration business); the cost is around a thousand yen a year for a `.com` and the like. This becomes the address notation for your server.

**DNS.** The phone-book mechanism that converts a name (the domain) into the actual IP address. In the management screen of the domain you acquired, you register the mapping "this name points to this IP address." For IPv4 this is an **A record**; for IPv6, an **AAAA record**. Only once you set this can people worldwide reach your server by name.

**TLS certificate.** What encrypts the communication and makes the `https://` lock icon stand. Without it, traffic flows in plaintext and things like passwords can be eavesdropped. It used to be paid and laborious, but now you can get it for free and automatically through a mechanism called **Let's Encrypt**. The reverse proxy described below takes care of this almost entirely automatically.

Only when these three are in place does `https://your-domain` become visible from the world.

### Ask Claude ①: Have It Design a Publishing Route That Fits Your Line

> I run a home server on Debian 13, and I want to publish [what you want to publish; e.g., my own blog / a photo album shared with friends / a self-made app used from outside]. My line's situation is as follows:
> [the ISP you contract with, line type (fiber / mobile, etc.), whether you have a global IP, whether IPv6 is available, as far as you know]
>
> Please design several candidate routes to achieve that publishing on this line. For each candidate, add the parts needed, a cost estimate, how much the attack surface grows, and its suitability for my situation.

What moves are available for a publishing route changes with the nature of your line. The CGNAT problem described below is hard to notice on your own. The starting point is to tell Claude about your line first and narrow down the realistic options.

## Section 2 — The Reverse Proxy Pattern

Whether you publish one service or several, modern publishing uses a pattern called a **reverse proxy**.

A reverse proxy is **a mechanism where a single entrance (port 443, that is, `https://`) routes to several services behind it, by host name**. A connection to `blog.example.com` goes to the blog service; a connection to `photos.example.com` goes to the photo server — one machine directs traffic. The only entrance visible from outside is a single one, and this entrance handles the TLS work in bulk. If you run several services in the manner of Chapter 6, you can consolidate their exit into this one reverse proxy.

This chapter uses **Caddy** as the example. The reason is that its config file (the Caddyfile) takes only a few lines, and **it handles getting and renewing TLS certificates fully automatically**. Caddy does the back-and-forth with Let's Encrypt on its own, behind the scenes. A short config text also means a good fit with Claude.

```caddyfile
# /etc/caddy/Caddyfile
# Example routing two services by host name

blog.example.com {
    reverse_proxy localhost:8080
}

photos.example.com {
    reverse_proxy localhost:8081
}
```

That is all. It passes `https://` traffic arriving at `blog.example.com` to the blog running locally on port 8080 (such as a Chapter 6 service, or the FastAPI app you built in Chapter 8). `photos.example.com` goes to port 8081. The TLS certificate is obtained automatically from Let's Encrypt by Caddy at startup, and renewed automatically when it expires. You need not be aware the certificate exists.

```bash
# Install Caddy and apply the configuration
sudo apt install caddy
sudo nano /etc/caddy/Caddyfile   # write the contents above
sudo systemctl reload caddy      # re-read the configuration
systemctl status caddy           # check that it is running
```

The same thing can be done with **nginx**. nginx has a large volume of information and allows fine control, but automating TLS requires combining a separate tool called certbot, and the config text grows longer than Caddy's. **I recommend Caddy on the single point of "short text, automatic TLS finished"**, but if you are already used to nginx, there is no need to force a switch.

### Ask Claude ②: Have It Write a Caddyfile and Explain Each Line

> On my Debian 13 server, I want to publish the following services:
> [e.g., blog.example.com → localhost:8080 for a blog, photos.example.com → localhost:8081 for a photo server. List your domains and services.]
>
> Please write a Caddyfile that achieves this. Then **explain line by line what each line does**. Also explain how the TLS certificate is handled.

Here too, use the same craft as the unit files in Chapter 6. **Do not just have it write — have it explain the meaning of each line.** A reverse proxy is the very "entrance from outside to inside," so running it with lines you do not understand left in place is dangerous. Have it explain line by line, so you can read your own entrance yourself.

## Section 3 — The Obstacle of Publishing from Home

Even with the three-piece set in place, a home server has a peculiar wall. A home network was built, from the start, so that "no one gets in from outside."

The first wall is **port opening**. Your home router blocks all incoming connections from outside by default. To publish a server, you need to open a hole in the router's settings — "connections arriving at port 443 are passed to this server" (port forwarding). This is like adding one more keyhole to your front door. **The moment you open it, scanners worldwide start hammering that hole.** This is why Chapter 5's defenses are the premise.

The second, and more troublesome, wall is **CGNAT**. On many recent lines (especially mobile lines and some fiber lines), the subscriber is not assigned a unique global IP address. A scheme called **CGNAT (Carrier-Grade NAT)**, where several subscribers share one global IP, is used. In this case, **since you have no address pointable from outside in the first place, conventional port opening is impossible.** Whether your line falls under this is fastest to confirm with Claude in ① of Section 1.

There are several modern detours past the CGNAT wall. Each has its trade-offs.

- **Cloudflare Tunnel.** Open a tunnel outward from home and publish via Cloudflare. No port opening or global IP needed. Easy, but the traffic passes through Cloudflare (one more dependency added).
- **Tailscale Funnel.** The publishing feature of Tailscale, also touched on in Chapter 1. Likewise no port opening, with straightforward setup. Suited to small-scale publishing.
- **A cheap VPS as the entrance.** Rent a small VPS on the net as the publishing entrance and tunnel from there to your home server. High freedom, but it adds one more thing to manage — the VPS.

Let me state this honestly. Each of these detours means **adding one more dependency to "someone outside your own hands."** This sits in tension with the philosophy this book has held throughout — "reduce dependencies, widen the range you can fix with your own hands." Convenience and self-reliance collide here, once.

With that tension in mind, here is the way to sort it out that follows this book's premise — **the data does not leave your home.** **Keep the body (apps and data) on your home server, and borrow only the "entrance."** Cloudflare Tunnel and Tailscale Funnel are exactly this shape. If you use a VPS, let it serve strictly as the publishing entrance (the tunnel's far end) while the databases and files stay home. The thing taking on the attack surface is only the easily-disposable entrance, and your home machine and the important data on it are never directly exposed to the world. The entrance may be borrowed; the body is in your house — with this division of roles you keep the convenience without giving up the initiative.

### Ask Claude ③: Confirm Whether Your Line Is CGNAT and Decide the Route

> My home line's situation is as follows:
> [ISP, line type. The WAN-side IP address visible in the router's admin screen (e.g., 100.x.x.x or 10.x.x.x suggests a shared IP), whether IPv6 is present]
>
> Please tell me whether this line is CGNAT (a scheme sharing a global IP), together with how to judge it. Then, of the detours raised in Section 2 (Cloudflare Tunnel / Tailscale Funnel / VPS entrance), recommend the one that suits my situation, with reasons.

Whether it is CGNAT can be judged by whether the router's WAN-side IP matches your IP as seen from outside. Ask Claude for the judgment procedure as well, and what is possible on your line becomes clear in one pass.

## Section 4 — What to Do on the Day You Publish

There are things you must do on the very "day" you finish the setup and publish: confirming defenses, and observing from outside.

First, review the defenses you built in Chapter 5, once more, in the published state.

```bash
# Is the firewall opening only the intended ports?
sudo ufw status verbose

# Observe login attempts to SSH (they spike sharply after publishing)
sudo journalctl -u ssh --since "1 hour ago"

# Is fail2ban repelling attack sources?
sudo fail2ban-client status sshd
```

Next, confirm it is actually visible from outside. Better to run this not from the server itself but from outside the line if possible (such as a phone's mobile connection).

```bash
# From outside, fetch only your site's headers to confirm connectivity and TLS
curl -I https://your-domain
```

If you can confirm a response like `HTTP/2 200` and no certificate error, publishing has succeeded.

And there is an experience unique to the moment right after publishing. **Though you have done nothing, unfamiliar accesses begin flowing into the logs.** Persistent accesses to URLs that do not exist (`/wp-login.php`, `/.env`, and the like), SSH login attempts with common user names — these are all traces of the world's automated scanners mechanically hammering a freshly published server.

Do read this log to Claude as-is. Have it explain "what reconnaissance is this aimed at," and the map of the attack world becomes concrete all at once. The realization **so this is what "exposing yourself to the world" means** comes to you not as words in a textbook but as your own log. Chapter 5's threat model becomes, for the first time, the reality before your eyes.

### Ask Claude ④: Have It Read the Suspicious Lines in Your Post-Publish Access Log

> I published my home server. In the access log (or the SSH log) right after publishing, lines like the following are flowing:
> ```
> [from Caddy's access log or the output of journalctl -u ssh, paste the suspicious lines as-is]
> ```
>
> What reconnaissance or attack is each of these aimed at? Tell me what my server is already protected against and what likely still has a hole, on the premise of the firewall, key authentication, and fail2ban I set up in Chapter 5.

The craft of "pasting logs as text, as-is," picked up in Chapter 3, works directly in the most tense scene of all — publishing. Once you understand the meaning of the suspicious lines, you need neither to be excessively frightened nor to let your guard down. You become able to explain, in your own words, what is coming and what you are blocking.

## Summary

What you did in this chapter:

1. Confirmed that publishing is a near-irreversible decision, and that "not publishing (Tailscale, etc.)" is a perfectly respectable choice.
2. Grasped what the three-piece set for publishing (domain, DNS, TLS certificate) is.
3. Understood the reverse proxy pattern and wrote an example routing several services with a Caddyfile.
4. Sorted out the obstacles of home publishing (port opening, CGNAT) and the trade-offs of the modern detours.
5. Did, together with Claude, what to do on the day you publish (reconfirming defenses, confirming connectivity from outside, observing bots).

What you hold now:
- A publishing-route design that fits your line (or the conclusion "do not publish, enter via Tailscale").
- A working Caddyfile (or a note on the decision not to publish).
- The experience of reading the logs right after publishing — the realization of "exposing yourself to the world."

In Chapter 10, we consider finally **protecting** the services and data you have been running. The meaning of Chapter 7 — gathering your data into one database — pays off here. What to back up, to where, how often, and how to confirm you can "truly restore it" — together with Claude, we assemble the craft of preparing on the premise that things break.

---

The server sub-series can be navigated from [Learning Debian with Claude — Server Edition](/en/claude-debian/server/). The main desktop series is at [all chapters](/en/claude-debian/). Comments and discussion go to the Facebook group: [AISeed — Biodiversity, Food, AI and Life](https://www.facebook.com/groups/vegitage).
