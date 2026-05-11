---
slug: web
number: "07"
lang: en
title: "Building for the Web — Back to HTML+CSS+JavaScript"
subtitle: "Content in Markdown and Mermaid. Frame only in HTML+CSS"
description: Split the web into two layers. Content in Markdown and Mermaid; frame in minimal HTML+CSS+JavaScript; Python connects the two. Keep content in Markdown and the same data is reusable beyond the web — for PDF, print, AI analysis, e-books.
date: 2026.05.02
label: AI Native 07
title_html: Content in <span class="accent">Markdown+Mermaid</span>.<br>Frame only in <span class="accent">HTML+CSS+JS</span>.
prev_slug: business-systems
prev_title: "Working with Business Systems — Rewrite via Parallel Operation"
next_slug: apps
next_title: "Building Apps — CLI Tools, Flet Apps, Flutter Apps"
---

# Building for the Web — Back to HTML+CSS+JavaScript

Split the web-building tools into **two layers**.

- **Content**: write in Markdown and Mermaid
- **Frame**: HTML, CSS, and minimal JavaScript

Python connects them. With this alone, the build disappears, dependencies vanish, and deploys go light. And — this is the big one — **the content is reusable outside the web**.

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

## The WordPress trap

"I'm not using React — I'm using WordPress." Many people are thinking exactly that, right now.

That is correct. About **43% of the world's websites** run on WordPress. In Japan too — corporate sites, personal blogs, news media, government sites — WordPress is everywhere.

But WordPress has its own trap. Different in nature from the React trap, **but at least as serious — often worse**.

**Problem 1: content locked into MySQL**

WordPress posts are not text files. They are records in a MySQL database, mixed with HTML. Want to convert the same post to PDF, move it to another site, hand it to AI for analysis? Every path begins with an export.

The export format is `.xml` (WordPress's own WXR), with HTML tags and proprietary shortcodes (like `[gallery]`) intermixed. **Content is locked into WordPress.** This has the same shape as Chapter 4's "data locked in Excel."

**Problem 2: plugins are a security minefield**

WordPress extensions rely on plugins built by volunteers worldwide. A typical site has 20–30 plugins. Each surfaces vulnerabilities periodically. **The whole site is a collection of attack surfaces.**

That 43% of the world's web runs on WordPress means, to an attacker, **43% of all targets are the same machine**. In an era when Mythos-class AI arrives, this becomes a fatal structure (see Structural Analysis 5: "Mythos Has Arrived").

**Problem 3: updates break things**

WordPress core, themes, plugins — all interdepend. Update one, and another stops working. "Applied an update; the site went down" is daily life in WordPress operations.

**Problem 4: PHP is not where AI shines**

WordPress themes and plugins are written in PHP. Claude can write PHP, but the output quality is less stable than Python. **For an AI-native toolset, PHP is not optimal.**

## Escaping WordPress

If you are on WordPress, the way out is clear. Use the same **parallel operation** pattern from Chapter 6.

1. Keep the existing WordPress running. **Export content to Markdown** (use plugins or CLI tools, or have Claude write a converter).
2. Build the new site with Markdown + minimal HTML/CSS + Python.
3. Preserve the URL structure (to retain SEO equity).
4. Verify behavior in a staging environment, prepare reindex requests.
5. Pick a DNS-cutover date.
6. After cutover, run WordPress read-only for one month.
7. If no issues, stop WordPress and cancel the hosting contract.

The cost effect is significant too. WordPress managed hosting (WP Engine, Kinsta, etc.) costs tens to hundreds of dollars per month. Put static HTML on Cloudflare Pages or GitHub Pages, and the cost is **zero per month**. Tens of thousands of yen per year disappear.

> WordPress, too, escapes via parallel operation. Export to Markdown, write the frame in HTML/CSS, generate with Python, serve as static. That is how you kill WordPress.

## Content in Markdown + Mermaid. Frame in HTML+CSS+JS

The essence of a website splits into "content" and "frame."

| Kind | What you write | Tool |
|---|---|---|
| **Content** | Prose, tables, quotes, code, diagrams | **Markdown** + **Mermaid** |
| **Frame** | Header, navigation, footer, layout, color | **HTML** + **CSS** + minimal JavaScript |
| **Connection** | Pour content into the frame, output HTML | **Python** |

Mixing these is the trap of past web development. A React component contains prose, formatting, and logic, all stirred together. A WordPress post mixes HTML tags with prose. Rewriting becomes hell.

The AI-native split is **complete separation of content from frame**. Content is Markdown and Mermaid only. No HTML tags. The frame is HTML and CSS, but it never touches the content of any individual article. Python connects them mechanically.

## Why hold content in Markdown + Mermaid

The biggest reason to write content in Markdown and Mermaid is **the data is also usable outside the web**.

From the same Markdown file:

- A web page (Python converts to HTML)
- A PDF (`pandoc`, or Claude does the conversion)
- A print-ready manuscript
- An e-book (EPUB)
- Input to AI for summary, translation, Q&A
- Pasting into other media
- Diff review and history in Git
- Co-editing with others

**Content is not locked into the web.** Content written in WordPress or Wix disappears when the service ends. Content in Notion is locked into Notion's format. Markdown is not locked into anything.

This is the web version of the "keep content in Markdown" principle from Chapter 2: **separate entrance, content, and exit**:

- **Entrance**: Claude converts various formats (image, PDF, audio, Word) to Markdown
- **Content**: held in Markdown and Mermaid (versioned in Git)
- **Exit**: web, PDF, print, AI analysis, e-book — Python converts as needed

> Keep content in Markdown. Convert at the exit. That is how you keep data usable for ten years.

## Write the frame minimally

The frame — header, navigation, footer, layout, color — is written **directly** in HTML and CSS. **Minimally.**

- HTML templates: 1–few files
- CSS: 1 file (a few hundred to a few thousand lines)
- JavaScript: only essentials (mobile menu toggle, etc.), tens of lines

You touch these only a few times a year. **Don't over-engineer the frame.** Skeleton stays as skeleton. Spend your time on content.

**What to drop**:

- JavaScript frameworks (React, Vue, Angular, Svelte)
- Build tools (Webpack, Vite, Turbopack, Parcel)
- TypeScript (JS is enough)
- CSS frameworks (Tailwind, Bootstrap)
- Package managers (npm, yarn, pnpm)
- `node_modules` (`rm -rf node_modules` makes it disappear)

**What to keep**:

- HTML (structure) — one template file
- CSS (presentation) — one file
- JavaScript (dynamic parts only, bare minimum) — tens of lines
- Markdown + Mermaid (content) — one file per article

Just raw web standards and Markdown. **The combination AI handles best.** HTML/CSS/JS has no transformation layer; Markdown is AI's native notation. Both can be used as Claude returns them.

## Python connects them

Converting Markdown to HTML, Mermaid diagrams to SVG or images, and pouring them into the frame template — that is the job of a Python script.

```
articles/foo/ja.md  ──→  Python  ──→  html/foo/index.html
                              ↑
                  tools/templates/article.html (frame)
```

You don't need to write the script yourself. **Have Claude write it.** Use `markdown-it-py` to convert Markdown to HTML; use `Jinja2` to fill the template. Together, that's 100–200 lines.

Three or four dependencies:

- `markdown-it-py` — CommonMark parser
- `Jinja2` — HTML template engine
- `Pillow` — image processing (OG image generation, if needed)
- (Mermaid diagrams render in the browser, or use `mermaid-cli` to produce SVG)

`uv add markdown-it-py jinja2 pillow`, then `git clone && uv sync` and
you are done. No `node_modules`, no `requirements.txt` either.

This site's build script (`tools/build_article.py`) was mostly written by Claude. **You can own your build tool.** Instead of obeying a framework's conventions, write under your own conventions.

## Dynamic processing: FastAPI, only

"You can't build dynamic sites that way," you might think. Wrong.

Write dynamic processing on the server. **Python's FastAPI, that one alone.**

Flask, Django, Go, Rust, Ruby — there are mountains of choices. But each added choice splits the organization. "We'll write in FastAPI" — once decided, all argument ends. **Pick, then forget you picked.** This is the AI-native way of choosing tools.

Why FastAPI:

- **It is Python**, matching the rest of the series stack
- Type hints and Pydantic work naturally
- async is standard
- OpenAPI docs auto-generate
- **Claude writes it best** (rich open-source training data)
- Minimal boilerplate

## And keep that minimal too

"Minimal" means concretely:

- **No ORM.** SQLAlchemy is not needed. Hit SQL directly with a PostgreSQL driver (asyncpg or psycopg).
- **No layers.** Repository layer, service layer, domain layer — none of it. Receive request, execute SQL, return HTML. That is all.
- **No extra dependencies.** FastAPI, PostgreSQL driver, Jinja2 (if templates are needed) — three are enough.
- **No multiplying config files.** Environment variables only.
- **No microservices.** One process.

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncpg

app = FastAPI()

@app.get("/items", response_class=HTMLResponse)
async def items():
    conn = await asyncpg.connect(...)
    rows = await conn.fetch("SELECT name, price FROM items")
    html = "".join(f"<li>{r['name']}: {r['price']}</li>" for r in rows)
    return f"<ul>{html}</ul>"
```

That alone is a server that "fetches items from a database and returns them as HTML." **Keep asking what more is actually needed.**

Spring Boot's tower of class hierarchies, Django's app/middleware/views/serializers, Express + Prisma + GraphQL stacks — these are legacy from past complexity. **In an era when Claude can write SQL directly, the ORM's abstraction is not needed.**

Client-side JavaScript stays minimal too. Link navigation uses `<a>`. Form submission uses `<form>`. Dynamic updates use HTMX (a few KB library, not a framework). Add WebSocket only when genuinely needed. **Don't start with an SPA.**

## This covers 90% of cases

For example, an internal inventory management web app:

```
Browser ─→ FastAPI (Python, one file, 200 lines) ─→ PostgreSQL
```

That works. Frontend, backend, database — one person can build it. Claude writes the code. **Hundreds of users and millions of records run normally.**

There is no need to design microservices for performance up front. When you hit a wall, design scale-out then. **90% of business web apps never get there.**

Narrowing choices is not abandoning freedom. It is **narrowing what you have to think about**. Don't burn time on technology debates. Write in FastAPI, SQL, and Jinja2. With AI.

> The dynamic layer: FastAPI, only, minimal.

## Concrete examples — what this stack actually builds

"Substance in Markdown, frame in HTML+CSS, Python in between" is
clearer in cases.

**Case 1: a sole proprietor's portfolio site**

- **Substance**: `portfolio/` with one `.md` per work, images,
  Mermaid diagrams.
- **Frame**: one `templates/article.html`, one `style.css`.
- **Python build**: 50 lines (`markdown-it-py` + `Jinja2`).
- **Delivery**: Cloudflare Pages (free), custom domain.
- **Updates**: write Markdown → `git push` → auto-build and
  publish.
- **Scale**: 30–100 pages, build in seconds, zero monthly fee.

**Case 2: a small business's corporate site**

- **Substance**: `pages/` with "about, services, contact, blog" as
  Markdown.
- **Frame**: same `templates/` + `style.css`.
- **Contact form**: 50 lines of FastAPI, sends SMTP email (can run
  on a LAN miniPC, Chapter 2).
- **Recruiting page's dynamic part** (job list): 30 lines of
  SQLite + FastAPI.
- **Delivery**: static parts on Cloudflare Pages, dynamic on a VPS
  or miniPC.
- **Scale**: 50–200 pages, thousands of monthly visits, under
  $10/month.

**Case 3: a non-profit's event-announcement site**

- **Substance**: `events/2026-04-foo.md` per event.
- **Past-event archive**: accumulates in `events/`; yearly index
  auto-generated by Python.
- **Event map**: `<iframe>` inline, or a Mermaid relationship
  diagram.
- **Sign-up form**: link to Google Forms (no dynamic backend
  needed), or 30 lines of FastAPI.
- **Delivery**: GitHub Pages or Codeberg Pages (free).

**Case 4: a teacher's class-newsletter site** (parent-restricted)

- **Substance**: `weekly/2026-04-week-1.md` per week, plus photos
  and Mermaid event calendars.
- **Frame**: one `style.css` in school colors.
- **Access control**: Basic auth (`htpasswd`) for parents-only, or
  a private Forgejo repo with parent accounts.
- **Delivery**: school miniPC over LAN, or external access via
  Cloudflare Tunnel.
- **Updates**: teacher edits `.md` in Zed → `git push` publishes.

**Case 5: a research group's paper-and-data site**

- **Substance**: paper Markdown (MyST embedding computation,
  Chapter 2); dataset metadata.
- **Data download**: direct download of Parquet files (Chapter 4).
- **Visualization**: D3 (Chapter 3) interactive figures.
- **Delivery**: a university server, or Codeberg.

What unites them: **3–4 dependency packages, build in seconds,
nearly zero monthly cost, AI writes most of the code**. Lighter to
build and to maintain than React + Next.js + a stack of SaaS — by
an order of magnitude. This site (aiseed.dev) itself runs on this
shape.

## Deploys are light

Deploying static HTML is just copying files.

- Cloudflare Pages, GitHub Pages, Netlify, Vercel — all free or near-free
- Your own server: just `scp`
- On a CDN, fast worldwide

The CI/CD pipeline becomes simple. "When Markdown changes, Python builds, HTML uploads to CDN" — a few lines.

## Still works in ten years

A React v15 component may not build under v18. Webpack configurations need rewriting yearly.

HTML, CSS, and JavaScript core specs have maintained backward compatibility for 25+ years. An HTML file from 1999 still works in today's browser. **Raw web standards are time-tested.**

Markdown too has barely changed since the original 2004 spec. The same files will still be readable in twenty years. **Both the frame and the content are held in formats that cross time.**

> Frameworks depend on the era. Web standards and Markdown cross eras.

## In numbers

Building a business web with React + Next.js + TypeScript + Tailwind: **3-month** development, **~1,200** dependencies, **3-minute** builds, **500 MB** `node_modules`. Same functionality with HTML+CSS+FastAPI+Markdown: **2-week** development, **4** dependencies, **5-second** builds, **10 MB** total.

WordPress managed hosting (WP Engine, Kinsta, etc.): **5,000–30,000 yen/month**. Static HTML on Cloudflare Pages: **zero/month**. Annual savings of **60K–360K yen**.

Page rendering speed: Next.js + Vercel dynamic rendering **~800 ms**. Static HTML + CDN **~50 ms**. **16x faster.**

The scale of this site (aiseed.dev): **150+ pages, 30,000 lines of code, assembled in 24 hours.** Zero React, Next.js, or TypeScript. Markdown, Mermaid, minimal HTML/CSS only.

## In summary

Split the web-building tools into two layers.

Content in **Markdown and Mermaid**. Frame in **HTML and CSS and minimal JavaScript**. Python connects the two.

The build disappears, dependencies vanish, deploys go light. **And the content is reusable outside the web.** The same Markdown becomes a PDF, a printed page, an input to AI, an e-book.

This site is the proof. 30,000 lines of code, 150+ pages, assembled in 24 hours. No React. Markdown and Mermaid and minimal HTML/CSS. Nothing is missing.

The next chapter moves to building apps. CLI tools, Flet apps, Flutter apps — scaling up in stages.

---

## Related

- [Chapter 01: Writing Logic — Have AI Write Python For You](/en/ai-native-ways/python/)
- [Chapter 02: Writing Documents — Markdown as the Minimal Choice](/en/ai-native-ways/markdown/)
- [Chapter 03: Designing — With Mermaid and Claude Design](/en/ai-native-ways/design/)
- [Chapter 06: Working with Business Systems — Rewrite via Parallel Operation](/en/ai-native-ways/business-systems/)
- [Structural Analysis 15: Security Design for the Mythos Era](/en/insights/security-design/)
