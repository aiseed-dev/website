---
slug: web
number: "08"
part: "2"
lang: en
title: "Publish the Web — Cloudflare Pages (a WordPress Replacement)"
subtitle: "Drop dynamic WordPress and publish a static site with no server — build, verify, deploy as separate steps"
description: Publish, from your own side, the static site you built with AI in the Introduction part. Drop dynamic WordPress and put the baked HTML on Cloudflare Pages — hold no server. Leave the CDN and automatic HTTPS to Cloudflare; keep the source and build in your own hands. The crux is to separate build, verify, and deploy, keeping what you verified identical to what goes live. Internal tools stay behind the gate — borrow the window, hold the vault.
date: 2026.07.14
label: Independence 8
title_html: Drop WordPress;<br>publish with <span class="accent">no server</span>.
prev_slug: meetings
prev_title: "Meetings and Booking on Your Own Side — Jitsi and Cal.com"
next_slug: fastapi
next_title: "Build an API — Expose Core Logic with FastAPI"
---

# Publish the Web — Cloudflare Pages (a WordPress Replacement)

In the Introduction part, you built a static website with AI (1-07). Here, you **publish it from your own side.** Drop dynamic
**WordPress** and put the baked HTML on **Cloudflare Pages** — hold no server.

## Why drop WordPress

WordPress is a mass of dynamic server, database, and plugins. The burden of
updates, maintenance, and security never stops. Since a company site's contents
rarely change, **static is enough.** Static needs no server and no DB, and has
almost no surface to attack. Publish the `html/` you built in the Introduction
part, as-is.

## Put it on Cloudflare Pages — hold no server

Put the HTML on **Cloudflare Pages.** No server needed. Upload the files and
they are served from a global CDN, with HTTPS added automatically.

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
your own API behind the gate (2-03) — auth at the gate, storage in the
2-02 DB, notifications via the 2-06 mail. **Mostly static, dynamic
only where needed.**

## Internal tools are separate — borrow the window, hold the vault

The public site is **borrowed** on Cloudflare Pages. But the **internal tools**
stood up in this part (gate, documents, code, mail, meetings) are different.
Carrying secrets and raw data, they stay behind the gate — your own reverse
proxy.

- **The public site** (static, no secrets) — borrowed on Cloudflare Pages
- **The internal tools** (auth, business data) — on your own side, behind the gate

**Borrow the window, hold the vault.** Decide separately what to borrow and what
to keep.

## Summary

- **Drop WordPress** — shed the maintenance burden of a dynamic server, DB, and plugins
- **Cloudflare Pages** — publish with no server; borrow CDN and automatic HTTPS
- **Separate build → verify → deploy** — ship exactly what you verified
- **Domain switches automatically** — a custom domain points the A record at Pages; leave mail untouched
- **Borrow the window, hold the vault** — internal tools stay behind the gate

Next, we expose the core systems' logic as an **API (FastAPI)** so every app can
use it.

---

## Related articles

- [1-07: Build a Website — In Dialogue with AI](/en/ai-native-ways/software/website/)
- [2-03: Stand Up the Gate — One Login with PocketBase](/en/ai-native-ways/software/auth/)
- [2-01: Becoming Independent from Microsoft and Google — The Whole Map](/en/ai-native-ways/software/independence/)
