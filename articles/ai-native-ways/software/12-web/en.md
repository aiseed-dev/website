---
slug: web
number: "12"
lang: en
title: "The Window to the Outside — A Static Site and Cloudflare Pages"
subtitle: "Bake the company site and blog static, hold no server, ship to Cloudflare Pages — build, verify, deploy as separate steps"
description: The web you show the outside can be mostly static. Bake it from Markdown into HTML with Astro, Hugo, or your own build, and put it on Cloudflare Pages — hold no server. Borrow the CDN, automatic HTTPS, and DDoS defense at the front; keep the source and build on your own side. The crux is to separate build, verify, and deploy — avoid auto-rebuild and one-shot deploys, and keep what you verified identical to what goes live. Internal tools stay behind the Chapter 7 gate — borrow the window, hold the vault.
date: 2026.07.14
label: Software 12
title_html: A <span class="accent">static</span> window outside,<br>published with <span class="accent">no server</span>.
prev_slug: meetings
prev_title: "Meetings and Booking on Your Own Side — Jitsi and Cal.com"
next_slug: ai
next_title: "Stand Up Your Own AI — LLM and RAG"
---

# The Window to the Outside — A Static Site and Cloudflare Pages

So far the tools have been internal. Last, we stand up the **window** that
faces outward — the web. Company site, product pages, documentation, blog —
most of it can be **static.**

And if it is static, **you don't even need your own server.** Put the baked
HTML on **Cloudflare Pages** and it is published.

## Why static

The contents of an external site rarely change. So there is no need to
assemble it on the server each time — **bake it to HTML ahead of time** and it
is faster, safer, and cheaper.

- **Fast** — just file serving. No waiting on a database
- **Safe** — nothing moving, so almost no attack surface
- **Good with AI** — write Markdown, and Claude assembles the HTML

> This very site (aiseed.dev) is the example. It bakes Markdown into static
> HTML and serves it — there is no dynamic server.

## Build a static site

Write prose in Markdown and assemble HTML with **Astro** or **Hugo** (or your
own build). The output is just a set of files.

```bash
npm run build        # e.g. Astro. Output bakes into dist/ (or html/)
```

Updating means "write, build, ship" — here too, what you write is prose, not
code.

## Put it on Cloudflare Pages — hold no server

The home for the baked HTML is **Cloudflare Pages.** **Not a single server is
needed.** Upload the files and they are served from a global CDN, with
**automatic HTTPS** and DDoS defense.

This is the same shape as the mail relay (Chapter 10) and the AI to come —
**borrow delivery and defense at the front; keep the source and build on your
own side.** The published HTML holds no secrets (just the baked output), so
this is a layer you can borrow with confidence.

## Separate build, verify, and deploy

This is the structural crux of the chapter. Publishing splits into **three
independent steps.**

```bash
# 1. Build — generate html/
npm run build
# 2. Verify locally — no rebuild, no watch (you see exactly what was baked)
python -m http.server --directory html 8000
# 3. To a preview URL — check it on the real platform
wrangler pages deploy html --branch preview
# 4. Once verified, to production
wrangler pages deploy html --branch main
```

**Don't use auto-rebuild or a "build + deploy" one-shot.** If it silently
rebuilds in the background, what you verified by eye and what goes live drift
apart. Freeze the `html/` from the moment you built, verify it, and deploy the
**same thing.** Upload with wrangler or the Pages direct-upload API — what
matters is the **verification** wedged in between.

> Keep what you verified identical to what goes live.
> "Check against the current as the oracle, then cut over" — do that for
> publishing too.

## Connect the domain

A custom domain is just **added to Pages.** If your DNS is on Cloudflare, the
**A record that used to point at your server is swapped to Pages
automatically,** and the certificate is issued automatically.

**Leave mail (MX, SPF) untouched** — you are only changing where the web is
served; the mail path is a separate thing. If the switch makes you nervous,
keep the old server running and **verify on the preview** before pointing the
production domain (the same parallel-run cutover as Chapters 8–11).

## Wire only what must be dynamic

Wire the backend only for the **moving parts** — a contact form. The target is
your own API placed behind the Chapter 7 gate (auth at the gate, records in the
Chapter 6 DB, notifications via the Chapter 10 mail). Add a minimum of dynamic
points to a static window — **mostly static, dynamic only where needed.**

## Internal tools have a separate entrance

The public site is **borrowed** on Pages. But the **internal tools** stood up
in Chapters 7–11 (auth, documents, code, meetings) are different. Carrying
secrets and raw data, they stay **inside the Chapter 7 gate — your own reverse
proxy.**

- **The public window** (static, no secrets) — borrowed on Cloudflare Pages
- **The internal vault** (auth, business data) — on your own side, inside the gate

**Borrow the window, hold the vault.** Decide separately which to borrow and
which to keep.

## Summary

A static window outside, with no server.

- **Static site (Astro / Hugo / your own)** — bake Markdown to HTML; fast, safe, cheap
- **Cloudflare Pages** — publish with no server; borrow CDN, automatic HTTPS, DDoS at the front
- **Separate build → verify → deploy** — avoid auto-rebuild; keep what you verified identical to what goes live
- **Domain swaps automatically** — a custom domain points the A record at Pages; leave mail untouched
- **Borrow the window, hold the vault** — internal tools stay inside the Chapter 7 gate

The internal tools and the outward window are in place. In the final chapter, we
lay **AI (a self-hosted LLM and RAG)** on top of all of this and cut the
dependency on Copilot.

---

## Related articles

- [Chapter 7: Stand Up the Gate — One Login with PocketBase](/en/ai-native-ways/software/auth/)
- [Chapter 10: Mail on Your Own Side — Stalwart and Thunderbird](/en/ai-native-ways/software/mail/)
- [Parent series, Chapter 14: Replacing Microsoft 365 Wholesale](/en/ai-native-ways/microsoft-365/)
