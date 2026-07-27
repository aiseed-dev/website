---
slug: welcome
title: ようこそ
subtitle: この Web サイトの開発環境について
description: このサンプルブログは tools/build_article.py と tools/serve.py による開発フローを紹介します。
date: 2026.04.21
label: Blog
category: ノート
---

## 開発フロー

```bash
# 開発サーバーを起動（監視 + 自動再ビルド + 配信）
python3 /path/to/website/tools/serve.py --site .

# 静的配信のみ
cd html && python3 -m http.server 8000
```

## 構造

```
articles/    Insights 記事（連載）
blog/        Blog 記事（単発ノート）
html/        出力先（index.html, css/, images/）
tools/templates/  任意：テンプレート上書き
```

Claude Code から開くときは、プロジェクトルート直下の `CLAUDE.md` を読めば
サイト構造とビルド方法が把握できます。
