---
slug: web
number: "12"
lang: en
title: "Build the Website"
subtitle: "Make the company site and blog static, hold no server, ship to Cloudflare Pages — build, verify, deploy as separate steps"
description: The web you show the outside can be mostly static. Make HTML from Markdown with your own build or Hugo, and put it on Cloudflare Pages — hold no server. Leave the CDN and automatic HTTPS to Cloudflare; keep the source and build in your own hands. The crux is to separate build, verify, and deploy — avoid auto-rebuild and one-shot deploys, and keep the HTML you verified identical to the HTML that goes live. Internal tools stay behind the Chapter 7 gate.
date: 2026.07.14
label: Software 12
title_html: Make the site <span class="accent">static</span>,<br>publish it with <span class="accent">no server</span>.
prev_slug: meetings
prev_title: "Meetings and Booking on Your Own Side — Jitsi and Cal.com"
next_slug: ai
next_title: "Stand Up Your Own AI — LLM and RAG"
---

# Build the Website

The internal tools are in place. Last, build the website you show the outside.
Company site, product pages, documentation, blog — most of it can be **static.**

If it is static, you don't need your own server. Put the HTML you made on
**Cloudflare Pages** and it is published.

## Why static

The contents of an external site rarely change. So instead of assembling it on
a server every time, you make the HTML ahead of time and place it. That is
faster, safer, and cheaper.

- **Fast** — just file serving. No waiting on a database
- **Safe** — nothing moving, so almost no surface to attack
- **Easy** — write Markdown, and Claude turns it into HTML

This site (aiseed.dev) is static too. It makes HTML from Markdown and places it.
There is no dynamic server.

## Make a static site

Write prose in Markdown and convert it to HTML. Use one of these to convert:

- **Your own build** — a conversion script written in Python or the like (this site uses one)
- **Hugo** — a single-binary static site generator. No Node, no npm

```bash
# make html/ with your own build script
python tools/build.py
```

The output is just a set of files (`html/`). Updating means "write, make, ship."

## Put it on Cloudflare Pages

Put the HTML you made on **Cloudflare Pages.** No server needed. Upload the
files and they are served from a global CDN, with HTTPS added automatically.

Leave delivery and defense to Cloudflare, and **keep the source and build in
your own hands.** The published HTML holds no secrets, so this is safe to hand
off.

## Separate build, verify, and deploy

Publish in separate steps. Don't combine them.

```bash
# 1. Build — make html/
python tools/build.py
# 2. Verify — open the html/ you made and look at it
python -m http.server --directory html 8000
# 3. To a preview — check on the real platform before production
python tools/deploy_pages.py html --branch preview
# 4. Once verified, to production
python tools/deploy_pages.py html --branch main
```

Don't use auto-rebuild, or a command that combines "build and deploy." The point
is to **keep the HTML you verified identical to the HTML that goes live** (the
detailed procedure lives in an internal manual). Uploading needs no npm or Node
— one script hitting Cloudflare's API is enough.

## Connect the domain

Add the custom domain in **Cloudflare Pages.** If your DNS is on Cloudflare, the
**A record that used to point at your server switches to Pages automatically,**
and the certificate is added automatically.

**Leave mail (MX, SPF) untouched.** You are only changing where the web is
served. If unsure, keep the old server running and verify on the preview before
pointing the production domain.

## Wire only the moving parts

Wire the backend only for the **moving parts** — a contact form. The target is
your own API behind the Chapter 7 gate (auth at the gate, storage in the Chapter
6 DB, notifications via the Chapter 10 mail). **Mostly static, dynamic only where
needed.**

## Internal tools are separate

The public site goes on Cloudflare Pages. But the **internal tools** built in
Chapters 7–11 (auth, documents, code, meetings) are separate. Carrying secrets
and raw data, they stay behind the Chapter 7 gate — your own reverse proxy.

- **The public site** (static, no secrets) — Cloudflare Pages
- **The internal tools** (auth, business data) — on your own side, behind the gate

Decide separately what to borrow and what to hold yourself.

## Summary

- **Static site (your own build / Hugo)** — turn Markdown into HTML; fast, safe, cheap
- **Cloudflare Pages** — publish with no server; leave CDN and automatic HTTPS to it
- **Separate build → verify → deploy** — avoid auto-rebuild; ship what you verified
- **Domain switches automatically** — a custom domain points the A record at Pages; leave mail untouched
- **Internal tools are separate** — keep them behind the Chapter 7 gate

In the final chapter, we lay **AI (a self-hosted LLM and RAG)** on top of all of
this and cut the dependency on Copilot.

---

## Related articles

- [Chapter 7: Stand Up the Gate — One Login with PocketBase](/en/ai-native-ways/software/auth/)
- [Chapter 10: Mail on Your Own Side — Stalwart and Thunderbird](/en/ai-native-ways/software/mail/)
- [Parent series, Chapter 14: Replacing Microsoft 365 Wholesale](/en/ai-native-ways/microsoft-365/)
