---
slug: hello
number: "01"
title: はじめての記事
subtitle: Insights 連載の始め方
description: このサンプル記事は tools/build_article.py で HTML に変換されます。フロントマターと Markdown の書き方を確認してください。
date: 2026.04.21
label: Sample 01
---

## これはサンプル記事です

`articles/NN-slug.md` に Markdown を置き、`python3 tools/build_article.py --all`
を実行すると `html/insights/<slug>/index.html` に HTML が生成されます。

### フロントマター

`---` で囲んだ先頭ブロックに、記事のメタ情報を `key: value` 形式で書きます。
フィールドの詳細は [tools/README.md](../tools/README.md) を参照してください。

### カスタムブロック

:::highlight
**ポイント：**
articles/ は連載記事（Insights）、blog/ は単発ノート（Blog）という使い分けです。
:::

### 次のステップ

- この記事を書き換える、または新しい `articles/02-*.md` を追加する
- `html/index.html` をサイトのトップページに仕立てる
- `html/css/style.css` で好みのデザインにする
