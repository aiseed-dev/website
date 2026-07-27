---
slug: hello
number: "01"
title: First Article
subtitle: Starting the Insights series
description: This sample article is converted to HTML by tools/build_article.py. Use it to confirm the frontmatter and Markdown syntax.
date: 2026.04.21
lang: en
label: Sample 01
---

## This is a sample article

Place Markdown under `articles/NN-slug.md` and run
`python3 tools/build_article.py --all` — the HTML is written to
`html/insights/<slug>/index.html`.

### Frontmatter

The top block fenced by `---` carries per-article metadata as `key: value`.
See [tools/README.md](../tools/README.md) for the full field list.

### Custom blocks

:::highlight
**Note:**
`articles/` is for serialized Insights, `blog/` is for standalone notes.
:::

### Next steps

- Edit this article, or add a new `articles/02-*.md`
- Turn `html/index.html` into your real landing page
- Style the site in `html/css/style.css`
