---
slug: web
number: "12"
lang: en
title: "The Window to the Outside — A Static Site and Caddy"
subtitle: "Company site and docs as static files, with one Caddy as the single entrance"
description: The web you show the outside can be mostly static. Build it from Markdown with Astro or Hugo, and let Caddy serve it with automatic HTTPS. Caddy also binds the entrances of every app stood up so far into one reverse proxy. Only a few parts need to be dynamic — forms wire to the Chapter 6 DB and the Chapter 7 gate. Put Cloudflare in front to borrow delivery and defense.
date: 2026.07.14
label: Software 12
title_html: A <span class="accent">static</span> window outside,<br>a <span class="accent">single</span> entrance.
prev_slug: meetings
prev_title: "Meetings and Booking on Your Own Side — Jitsi and Cal.com"
next_slug: ai
next_title: "Stand Up Your Own AI — LLM and RAG"
---

# The Window to the Outside — A Static Site and Caddy

So far the tools have been internal. Last, we stand up the **window** that
faces outward — the web. Company site, product pages, documentation, blog —
most of it can be **static.**

And here we face, head-on, the **Caddy** that has appeared again and again
across the chapters: the gate that binds every app's entrance into one.

## Why static

The contents of an external site rarely change. So there is no need to
assemble it on the server each time — **bake it to HTML ahead of time** and it
is faster, safer, and cheaper.

- **Fast** — just file serving. No waiting on a database
- **Safe** — nothing moving, so almost no attack surface
- **Good with AI** — write Markdown, and Claude assembles the HTML

> This very site (aiseed.dev) is the example. It bakes Markdown into static
> HTML and serves it — there is no dynamic server.

## Stand up a static site

Write prose in Markdown and assemble HTML with **Astro** or **Hugo.** The
output is just a set of files.

```bash
npm create astro@latest site && cd site
npm run build        # HTML is baked into dist/
```

Hand `dist/` to Caddy and it is published. Updating means "write, build,
place" — here too, what you write is prose, not code.

## Caddy — automatic HTTPS and the single entrance

**Caddy** not only serves the static site; it binds **the entrances of every
app stood up so far** into one. Certificates are **obtained and renewed
automatically via Let's Encrypt,** and the config is a few lines.

```caddy
# Caddyfile — one file for the window and every app's entrance
example.com           { root * /srv/site/dist
                        file_server }            # static site
auth.example.com      { reverse_proxy auth:8090 }       # Ch.7 gate
docs.example.com      { reverse_proxy files:80 }        # Ch.8 documents
git.example.com       { reverse_proxy code:3000 }       # Ch.9 code
meet.example.com      { reverse_proxy jitsi-web:80 }    # Ch.11 meetings
book.example.com      { reverse_proxy booking:3000 }    # Ch.11 booking
```

The single lines written across the chapters **all gather into this one file.**
HTTPS is automatic for every domain. With one entrance, there is one place to
guard.

## Wire only what must be dynamic

Wire the backend only for the **moving parts** — a contact form, a sign-up. The
target is the **Chapter 6 PostgreSQL,** with the **Chapter 7 gate** where
identity is needed and the **Chapter 10 mail** for notifications.

Add a minimum of dynamic points to a static window — there is no need to make
the whole site dynamic. **Mostly static, dynamic only where needed.**

## Borrow the front with Cloudflare

To make delivery fast worldwide and to deflect attacks, the front can be
borrowed from **Cloudflare** — hiding your server behind a CDN and DDoS
defense. The same idea as the mail relay (Chapter 10): **keep control on your
side, borrow only scale and defense.**

## Summary

A static window outside, a single entrance.

- **Static site (Astro / Hugo)** — bake Markdown to HTML; fast, safe, cheap
- **Caddy** — automatic HTTPS, and the gate that binds every app's entrance into one
- **Dynamic minimal** — wire only forms to the Chapter 6 DB, Chapter 7 gate, Chapter 10 mail
- **Cloudflare** — borrow delivery and defense at the front, control stays yours

The internal tools and the outward window are in place. In the final chapter, we
lay **AI (a self-hosted LLM and RAG)** on top of all of this and cut the
dependency on Copilot.

---

## Related articles

- [Chapter 7: Stand Up the Gate — One Login with PocketBase](/en/ai-native-ways/software/auth/)
- [Chapter 9: Bring Code In-House — Forgejo and Zed](/en/ai-native-ways/software/code/)
- [Parent series, Chapter 14: Replacing Microsoft 365 Wholesale](/en/ai-native-ways/microsoft-365/)
