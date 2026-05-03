---
slug: web
number: "07"
lang: en
title: "Building for the Web — Back to HTML+CSS+JavaScript"
subtitle: "You don't need React. Escape the framework trap"
description: 90% of websites are fine with HTML, CSS, and minimal JavaScript. No React, no Next.js, no Vite required. What AI writes is plain HTML/CSS/JS. Drop the framework, and the build disappears, dependencies vanish, and the site still works in ten years.
date: 2026.05.02
label: AI Native 07
title_html: The web is <span class="accent">HTML+CSS+JavaScript</span>.<br>Return to the origin.
prev_slug: business-systems
prev_title: "Working with Business Systems — Augment Legacy Assets with AI"
next_slug: apps
next_title: "Building Apps — CLI Tools, Flet Apps, Flutter Apps"
---

# Building for the Web — Back to HTML+CSS+JavaScript

Bring web-building tools back to HTML, CSS, and minimal JavaScript.

That single change makes the build disappear, dependencies vanish, and deploys go light. You write in a language AI is comfortable with, in the amount AI is comfortable producing. **For 90% of websites, this is enough.**

## React fatigue

For the past ten years, web development has been an "arms race of frameworks."

jQuery, Backbone, Angular, React, Vue, Svelte. Build tools: Grunt, Gulp, Webpack, Rollup, Vite, Turbopack. CSS: Sass, Less, PostCSS, Tailwind, CSS-in-JS. SSR: Next.js, Nuxt, Remix, SvelteKit, Astro.

Each solved some problem. But comparing the problems they solved against the problems they created, **it stopped being worth it** more often than not.

- It takes weeks to learn build configurations
- Dependencies pass 1000 packages
- Security updates arrive every week
- Builds stop working after a year
- A simple website needs 100 MB of folders

This is not technology. It is self-imposed complexity.

## Static HTML covers 90%

90% of websites are, honestly, just document delivery.

Company about pages, product pages, blogs, technical docs, portfolios, menus, price lists, contact pages — none of this needs React. HTML and CSS are enough. If a dynamic element is needed, write minimal JavaScript directly.

This site — aiseed.dev — runs on static HTML / CSS / JavaScript. Markdown converted to HTML by Python, served from Cloudflare. No React, no Next.js. **And nothing is missing.**

> 90% of websites are document delivery. Document delivery doesn't need React.

## Languages AI handles well

HTML, CSS, JavaScript. These three are the languages AI writes most easily.

The reason: little code, no transformation layer. Writing a React component requires JSX, state management, hooks, TypeScript types — all together. Even when AI writes it, the output requires a build environment.

With raw HTML, you can hand Claude's output straight to the browser and it works. The verification loop is fast. **There is no extra layer between AI and human.**

## What to drop

If you build a new website, drop these:

- **JavaScript frameworks** (React, Vue, Angular, Svelte)
- **Build tools** (Webpack, Vite, Turbopack, Parcel)
- **TypeScript** (JS is enough)
- **CSS frameworks** (Tailwind, Bootstrap)
- **Package managers** (npm, yarn, pnpm)
- **node_modules** (`rm -rf node_modules` makes it disappear)

And keep:

- **HTML** (structure)
- **CSS** (presentation)
- **JavaScript** (dynamic elements only, bare minimum)
- **Markdown** (content source)
- **Python** (build script, when needed)

The build disappears. Run `python build.py`, HTML comes out. Put HTML on a web server, the site runs.

## Dynamic? Do it server-side

"You can't make dynamic sites that way," you might think. Wrong.

Write dynamic processing on the server. Python (Flask, FastAPI, Django), Go, Rust, Ruby — anything works. The server returns HTML. The client receives HTML. **No need to ship piles of JavaScript to the browser.**

If you need real-time updates, return them from the server via WebSocket or HTMX. That, too, works without a JavaScript framework.

To build a complex single-page app (Google Docs, Figma, web Photoshop), React or Vue make sense. But that is the 1% of websites. The other 90% don't need it.

## The build is a Python script

The build for this site runs as a single Python script (`tools/build_article.py`). It reads Markdown, fills HTML templates, writes output. That's it.

Dependencies are three: `Jinja2`, `markdown-it-py`, `Pillow`. `pip install -r requirements.txt` and you are done. There is no `node_modules`.

The script itself was mostly written by Claude. You don't need to write it; have it written. **It is the era when you can own your build tool.**

## Deploys are light

Deploying static HTML is just copying files.

- Cloudflare Pages, GitHub Pages, Netlify, Vercel — all free or near-free
- Your own server: just `scp`
- On a CDN, fast worldwide

The CI/CD pipeline becomes simple. "When Markdown changes, Python builds, HTML uploads to CDN" — a few lines.

## Still works in ten years

A React v15 component may not build under v18. Webpack configurations need rewriting yearly.

HTML, CSS, and JavaScript core specs have maintained backward compatibility for 25+ years. An HTML file from 1999 still works in today's browser. **Raw web standards are time-tested.**

> Frameworks depend on the era. Web standards cross eras.

## In summary

Bring web tools back to the origin.

HTML, CSS, minimal JavaScript. Write in a language AI handles well, in an amount AI handles well. Drop the framework, kill the build, kill the dependencies.

This site is the proof. 30,000 lines of code, 42 pages, assembled in 24 hours. No React. Nothing is missing.

The next chapter moves to building apps. CLI tools, Flet apps, Flutter apps — scaling up in stages.

---

## Related

- [Chapter 06: Working with Business Systems — Augment Legacy Assets with AI](/en/ai-native-ways/business-systems/)
- [Chapter 04: Writing Logic — Have AI Write Python For You](/en/ai-native-ways/python/)
- [Structural Analysis 15: Security Design for the Mythos Era](/en/insights/security-design/)
- [Structural Analysis 08: Removing the Enterprise IT Tax](/en/insights/enterprise-tax/)
