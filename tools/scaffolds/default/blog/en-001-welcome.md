---
slug: welcome
title: Welcome
subtitle: About this site's dev setup
description: This sample blog post walks through the tools/build_article.py and tools/serve.py workflow.
date: 2026.04.21
lang: en
label: Blog
category: Notes
---

## Dev workflow

```bash
# Dev server (watch + auto-rebuild + serve)
python3 /path/to/website/tools/serve.py --site .

# Static-only
cd html && python3 -m http.server 8000
```

## Layout

```
articles/    Insights (serialized)
blog/        Blog (standalone notes)
html/        Output (index.html, css/, images/)
tools/templates/  optional: template overrides
```

When you open this project in Claude Code, the top-level `CLAUDE.md`
explains the layout and the build commands.
