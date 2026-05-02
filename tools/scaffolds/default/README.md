# Sample Site

A minimal static site scaffolded by `tools/init_site.py` from the
[aiseed-dev/website](https://github.com/aiseed-dev/website) toolchain.

## Getting started

```bash
# 1. Install deps (once)
pip install jinja2 markdown-it-py Pillow watchdog

# 2. Build everything
python3 PATH_TO_WEBSITE/tools/build_article.py --site . --all

# 3. Dev server (auto-rebuild on file changes)
python3 PATH_TO_WEBSITE/tools/serve.py --site . --port 8000
```

Open `http://localhost:8000`.

## Layout

| Path | Purpose |
|---|---|
| `articles/insights/NN-slug/{ja,en}.md` | Insights articles (one folder per article) |
| `articles/blog/NNN-slug/{ja,en}.md` | Blog posts (one folder per post; assets co-located) |
| `html/` | Output (serve this directory) |
| `html/index.html`, `html/en/index.html` | Hand-edited top pages |
| `html/css/style.css` | Stylesheet |
| `html/images/` | Static images |
| `tools/templates/` | Jinja2 overrides for article/index pages |
| `CLAUDE.md` | Notes for AI agents |

Output paths `html/insights/`, `html/blog/`, `html/en/insights/`,
`html/en/blog/` are regenerated from Markdown — do not hand-edit.

## Next steps

- Replace the sample articles and blog posts under `articles/insights/` and `articles/blog/`.
- Customize the look in `html/css/style.css`.
- Customize page layout by editing `tools/templates/article.html` and
  `tools/templates/index.html`.
- Update `html/index.html` (the build only touches content between the
  `LATEST_BLOG_POSTS_*` markers).
