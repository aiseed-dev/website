#!/usr/bin/env python3
"""src/*.md をすべて HTML に焼く。これだけで Web サイト一式ができる。

第 7 章の主張: 「Web は HTML+CSS+最小 JS で十分。中身は Markdown と Mermaid」
を最小サイズで実演する。

依存: markdown-it-py だけ(pip install markdown-it-py)。
出力: out/*.html ── そのまま Cloudflare Pages や GitHub Pages にデプロイ可能。
"""
from __future__ import annotations

import re
import time
from pathlib import Path

from markdown_it import MarkdownIt

HERE = Path(__file__).parent
SRC = HERE / "src"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

md = MarkdownIt("commonmark", {"html": True, "linkify": True}).enable("table")


CSS = """
:root { --ink: #1a1a1a; --paper: #f4f1ea; --accent: #2f5f3f; --rule: #d4cdb8; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Hiragino Mincho ProN", "游明朝", "Noto Serif CJK JP", serif;
  background: var(--paper); color: var(--ink);
  line-height: 1.85; max-width: 720px; padding: 32px 24px; margin: 0 auto;
}
h1 { font-size: 32px; border-bottom: 3px double var(--ink); padding-bottom: 12px; margin-bottom: 24px; }
h2 { font-size: 22px; border-left: 4px solid var(--accent); padding-left: 12px; margin: 32px 0 16px; }
h3 { font-size: 17px; margin: 24px 0 10px; color: var(--accent); }
p, ul, ol, table { margin-bottom: 18px; }
ul, ol { padding-left: 1.5em; }
table { width: 100%; border-collapse: collapse; }
th, td { border: 1px solid var(--rule); padding: 8px 12px; text-align: left; }
th { background: #ebe6d8; }
code { font-family: ui-monospace, monospace; background: #ebe6d8; padding: 1px 5px; border-radius: 2px; font-size: 0.9em; }
a { color: var(--accent); }
nav { margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--rule); font-size: 13px; }
.mermaid { text-align: center; margin: 28px 0; }
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 山田農園</title>
<style>{css}</style>
</head>
<body>
{body}
<nav>© 2026 山田農園 / Markdown + Python ビルド</nav>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({{ startOnLoad: true, theme: "default" }});
</script>
</body>
</html>
"""


def render_markdown(text: str) -> tuple[str, str]:
    """Markdown → HTML。fenced code の `mermaid` ブロックは <div class=mermaid> に変換。"""
    # mermaid ブロックを抽出して特別扱い
    mermaid_re = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)
    placeholders = []

    def stash(m):
        placeholders.append(m.group(1))
        return f"§MERMAID{len(placeholders) - 1}§"

    text = mermaid_re.sub(stash, text)

    # タイトルを取り出す
    title_match = re.match(r"# (.+?)\n", text)
    title = title_match.group(1).strip() if title_match else "山田農園"

    html = md.render(text)
    for i, code in enumerate(placeholders):
        html = html.replace(
            f"§MERMAID{i}§",
            f'<div class="mermaid">{code}</div>',
        )
    return title, html


def main():
    t0 = time.perf_counter()
    files = sorted(SRC.glob("*.md"))
    for src in files:
        title, body = render_markdown(src.read_text())
        out = OUT / f"{src.stem}.html"
        out.write_text(PAGE_TEMPLATE.format(title=title, css=CSS, body=body))
        size = out.stat().st_size
        print(f"  → {out.name}  ({size:,} B)")
    elapsed = time.perf_counter() - t0
    total = sum((OUT / f"{p.stem}.html").stat().st_size for p in files)
    print(f"\n  {len(files)} ページを {elapsed*1000:.1f} ms で生成")
    print(f"  HTML 合計: {total:,} B ({total/1024:.1f} KB)")


if __name__ == "__main__":
    main()
