# Claude Code project guide

This directory was scaffolded by `tools/init_site.py` from the
[aiseed-dev/website](https://github.com/aiseed-dev/website) toolchain.
It is a self-contained static site: Markdown in, HTML out.

## Layout

```
articles/          Insights articles (serialized). Filenames: NN-slug.md, en-NN-slug.md
blog/              Blog posts (standalone notes). Filenames: NNN-slug.md, en-NNN-slug.md
html/              Output. Served as-is.
  index.html       Top page (hand-edited; markers LATEST_BLOG_POSTS_*)
  en/index.html    English top page
  css/style.css    Stylesheet
  images/          Static images, referenced by absolute path
  insights/        GENERATED — do not hand-edit
  en/insights/     GENERATED
  blog/            GENERATED
  en/blog/         GENERATED
tools/templates/   Jinja2 templates (article.html, index.html). Override bundled ones.
CLAUDE.md          This file
README.md          Human-readable project overview
```

## Build commands

The build toolchain lives in the `aiseed-dev/website` repo and is driven via
`--site`. Replace `PATH_TO_WEBSITE` with the checkout location.

```bash
# One-shot build of all articles + blog + indexes + sitemap
python3 PATH_TO_WEBSITE/tools/build_article.py --site . --all

# Build a single article
python3 PATH_TO_WEBSITE/tools/build_article.py --site . articles/01-hello.md

# Dev server: watch + rebuild + HTTP
python3 PATH_TO_WEBSITE/tools/serve.py --site . --port 8000

# Or set the default once:
export AISEED_SITE=$(pwd)
python3 PATH_TO_WEBSITE/tools/build_article.py --all
```

Install dependencies once (they match the website repo):

```bash
pip install jinja2 markdown-it-py Pillow watchdog
```

## Conventions

- **Filenames carry metadata**: `articles/NN-slug.md` → `/insights/slug/`,
  `articles/en-NN-slug.md` → `/en/insights/slug/`. Same pattern for `blog/`
  except the prefix is 3 digits (`001-`, `002-`...).
- **Images sharing the numeric prefix** (e.g. `blog/012-photo.jpg`) are copied
  into the generated article directory automatically.
- **OGP images** are generated from `hero_image` at 1200×630.
- **Frontmatter fields** (`slug`, `title`, `subtitle`, `description`, `date`,
  `label`, `hero_image`, `lang: en` for English). Detailed reference:
  `PATH_TO_WEBSITE/tools/README.md`.
- **Custom Markdown blocks**: `:::chain`, `:::highlight`, `:::quote`,
  `:::compare` — see the upstream docs.

## Editing guidelines for Claude

- Never hand-edit files under `html/insights/`, `html/en/insights/`,
  `html/blog/`, `html/en/blog/` — they are overwritten by the build.
- Hand-edit `html/index.html` and `html/en/index.html`; the build only
  rewrites the region between `<!-- LATEST_BLOG_POSTS_START -->` and
  `<!-- LATEST_BLOG_POSTS_END -->`.
- When adding a new Insights article, update `prev_slug/next_slug` on
  neighbouring articles so the pager keeps working.
- Run `--all` after edits and verify the generated files.
