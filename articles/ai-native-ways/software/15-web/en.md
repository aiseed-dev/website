---
slug: web
number: "07"
part: "2"
lang: en
title: "Build the Website"
subtitle: "Make the company site and blog static, hold no server, ship to Cloudflare Pages — build, verify, deploy as separate steps"
description: The web you show the outside can be mostly static. Make HTML from Markdown with your own build or Hugo, and put it on Cloudflare Pages — hold no server. Leave the CDN and automatic HTTPS to Cloudflare; keep the source and build in your own hands. The crux is to separate build, verify, and deploy — avoid auto-rebuild and one-shot deploys, and keep the HTML you verified identical to the HTML that goes live. Internal tools stay behind the Chapter 7 gate.
date: 2026.07.14
label: Independence 7
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
- **Easy** — content is Markdown. Have Claude write it; the build turns it into HTML

This site (aiseed.dev) is static too. It makes HTML from Markdown and places it.
There is no dynamic server.

## Create the static site

The machinery — the build that turns Markdown into HTML, and the template for
the look — is made once, at the start. A professional front-end engineer may
build the site with a framework like Astro. But even a first-timer can just
**tell Claude, and it builds the website.**

The knack is not to settle it in one instruction but to **do it through
dialogue** — especially if you are new to this. You don't have to spell out a
full spec up front; what you want surfaces as you go back and forth. And **the
web is easy to fix later** — just rebuild and redeploy — so don't aim for
perfect; get a first version into shape. Start plainly — "Make a build that
turns Markdown articles into an HTML site" — then work it out with Claude, back
and forth. Worth bringing up:

- **What you write** — articles and posts in Markdown, each with a title, date, and summary (frontmatter) at the top
- **URL shape** — e.g. articles at `/<slug>/`, posts at `/blog/<slug>/`
- **Index pages** — a newest-first listing on the top page and per category
- **The look** — text-first and readable, in plain CSS; no fancy decoration and no CSS frameworks like Tailwind (to match an existing site, hand over its URL or images)
- **JavaScript** — minimal vanilla JS only, as a rule; no frameworks like React (a static site needs no heavy base)
- **Output and images** — write the result into `html/`, and carry images along
- **Languages** — to keep Japanese and English, split into `/` and `/en/`
- **Tools** — the build runs as a single command. No npm, no Node (Python or whatever you have)

From the exchange, Claude writes the conversion script and the templates. If
something is off, fix it while looking at the result — "two columns for the
list," "change the date format" — shaping it through dialogue (exactly the way
of building from Chapter 5). Once it exists, all that's left is writing articles.

## Write articles and posts

Once the machinery exists, all you do is **write articles and posts.** This is
the day-to-day operation.

You write the content in Markdown. Add one article as a file in a fixed place
(e.g. `articles/`), and the build converts it to HTML.

```bash
# write Markdown in articles/, and build it into html/
python tools/build.py
```

Day to day, the operation is just **write Markdown, build, ship.** The output is
just a set of files (`html/`).

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

- **Write articles and posts** — the operation is writing Markdown. The machinery is created once, by telling Claude (no Astro needed)
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
