---
slug: website
number: "07"
part: "1"
lang: en
title: "Build a Website — In Dialogue with AI"
subtitle: "Company site or blog — build the machinery with Claude in dialogue, then just write Markdown"
description: One of Chapter 5's worked examples — a customer building a website with AI. The web you show the outside can be mostly static, and if it is static you don't need your own server. The machinery (the build and the template) can be made by talking with Claude — no need to learn Astro. Dialogue helps beginners most, and the web is easy to fix later. Build it light with plain CSS and minimal vanilla JS, then just write articles and posts in Markdown. Publishing is covered in the Independence part.
date: 2026.06.30
label: Introduction 7
title_html: Build a website<br>in <span class="accent">dialogue with Claude</span>.
prev_slug: vba-python
prev_title: "Move VBA to Python — Rewrite Excel Macros with AI"
next_slug: embedded
next_title: "Build Embedded — Think in Python, Have Claude Translate"
---

# Build a Website — In Dialogue with AI

As Chapter 5 showed, a customer can build with AI. One worked example is the
company site or blog — a website. Most of it can be **static,** and if it is
static, you don't even need your own server.

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
use a framework like Astro. But even a first-timer can just **tell Claude, and
it builds the website.**

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
the day-to-day operation. Write the content in Markdown. Add one article as a
file in a fixed place (e.g. `articles/`), and the build converts it to HTML.

```bash
# write Markdown in articles/, and build it into html/
python tools/build.py
```

Day to day, the operation is just **write Markdown, build, ship.** The output is
just a set of files (`html/`).

## Summary

- **Build the machinery once, with Claude in dialogue** — no need to learn Astro; dialogue even for first-timers
- **Plain CSS, minimal vanilla JS** — a static site needs no heavy base
- **Operation is just writing articles** — add Markdown and build; fix it later anytime

That covers "building" the site. **Publishing it (uploading to Cloudflare Pages,
the domain, verify-and-deploy)** is covered in the Independence part, alongside
your own-side tools. Next, another worked example — building **embedded software
(code that drives a device)** with AI.

---

## Related articles

- [Chapter 5: Customers Co-Develop with AI](/en/ai-native-ways/software/customer-codev/)
- [Independence — Publish the Web on Cloudflare Pages](/en/ai-native-ways/software/web/)
- [Parent series, Chapter 9: Building Apps — CLI Tools, Flet Apps, Flutter Apps](/en/ai-native-ways/apps/)
