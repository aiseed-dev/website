---
slug: website
number: "07"
part: "1"
lang: en
title: "Build a Website — In Dialogue with AI"
subtitle: "WordPress is vulnerable to cyberattacks — go static and the attack surface vanishes. Build the machinery with Claude in dialogue, then just write Markdown"
description: One of Chapter 5's worked examples — a customer building a website with AI. WordPress, with its running server, plugins, and admin login, is vulnerable to cyberattacks; online shops (e-shops), handling payments and personal data, should be fixed first. Going static makes almost all of that attack surface disappear. The machinery (the build and the template) can be made by talking with Claude — no need to learn Astro — and is easy to fix later. Build it light with plain CSS and minimal vanilla JS, then just write Markdown. Publishing is covered in the Independence part.
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

## WordPress is vulnerable to cyberattacks — fix this first

Much of the world's web runs on WordPress. Convenient — but also **the single
biggest target for cyberattacks.** The reason is in its structure.

- **There is a running server** — PHP executes code on every request and queries
  a database. The more moving parts, the wider the surface to attack.
- **Plugins and themes** — to add features you install many third-party plugins.
  An unmaintained or vulnerable plugin is the number-one entry point for a breach.
- **There is an admin login** — the admin password is brute-forced automatically,
  around the clock, from all over the world.
- **There are so many** — being the most-used CMS, attack tools constantly scan
  for WordPress; old, neglected sites get taken over one after another.

**The most dangerous case is the online shop (e-shop).** Because it handles
payments and customer personal data, it is a high-value target — card-skimming,
data leaks; the damage hits money and trust directly. **So WordPress sites, and
e-shops above all, should be fixed first.**

The fix is simple. **Go static and almost all of this attack surface
disappears** — no running PHP, no database, no admin login, no plugins. There is
nowhere left to attack. (For a shop, hand the payment to an external checkout
page like Stripe and never hold card data yourself — that shrinks the surface
too.)

> WordPress is attackable because of its **running server, plugins, and admin
> login.** Go static and that whole surface vanishes. E-shops first.

## Why static

The contents of an external site rarely change. So instead of assembling it on
a server every time, you make the HTML ahead of time and place it. That is
faster, safer, and cheaper.

- **Fast** — just file serving. No waiting on a database
- **Safe** — nothing moving, so almost no surface to attack (as above)
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

## For an existing site, suck it into static

If rebuilding an existing WordPress site from scratch is too much, there is a
faster move — **crawl the whole live site, save the HTML and images, and turn it
into a bundle of static files.** The running WordPress becomes a static fixture
that looks exactly the same.

On the Mac there is a well-known app, **SiteSucker** (paid). But the same thing
**can be done in Python** — for free, on any OS, in a form you can read.

One caveat. Fetching a page with `requests` and reading it with `BeautifulSoup`
is **not enough.** Today's WordPress and many sites **render their content with
JavaScript** — fetch the raw HTML and the body isn't there yet (`wget` doesn't
run JS either, so it misses the same way). So open the page in a **headless
browser**, let the JavaScript run, and **save the rendered HTML.** In Python,
**Playwright** does this.

And **the HTML alone won't work.** The **CSS, JavaScript, images, and fonts**
the page loads — all the related files — must be **downloaded too**, and the
references rewritten to local paths. With Playwright you can receive every
response the browser actually fetched (`page.on("response")`) — so you save all
the related files the page used, wholesale.

```python
# sketch: run JS, save the rendered HTML AND every file it loaded
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    page = p.chromium.launch().new_page()
    # save every resource the browser fetched (CSS / JS / images / fonts …)
    page.on("response", lambda r: save_to_disk(r.url, r.body()))
    page.goto("https://example.com/")
    page.wait_for_load_state("networkidle")  # wait for JS to render
    save_html("index.html", page.content())  # the rendered HTML
    # → rewrite references to local relative paths (finish it in dialogue with AI)
```

(This site's repository ships an implementation, `tools/mirror_site.py` — pass it
a URL and an output directory; it's runnable from a Zed task too.)

Upload the sucked-out static files to Cloudflare Pages and you can **shut down
the running WordPress — attack surface and all.** Dynamic features like contact
forms and checkout won't carry over, so move forms to an external service and
payment to an external page like Stripe.

> For an existing site, **crawl it and suck it into static.** Render the JS with
> Playwright and **save the HTML and every related file (CSS, JS, images, fonts)**,
> rewriting references to relative. What SiteSucker (Mac, paid) does, AI can build
> for you in Python, for free.

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

- **WordPress is vulnerable to cyberattacks** — running server, plugins, admin login are the targets; fix e-shops first of all
- **Go static and the attack surface vanishes** — no running PHP, no DB, no admin login
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
