"""Markdown parsing: frontmatter, custom ::: blocks, CommonMark rendering."""

import html
import re
from pathlib import Path

from markdown_it import MarkdownIt


# CommonMark + tables (used for both article bodies and inline `:::highlight`)
md = MarkdownIt("commonmark", {"html": True}).enable("table")


# ---------------------------------------------------------------------------
# Mermaid: convert fenced ```mermaid blocks into <div class="mermaid"> so the
# Mermaid runtime can render them. Runs on the rendered HTML (after CommonMark)
# because doing it pre-render breaks on the blank lines that Mermaid DSL allows
# inside a single block.
# ---------------------------------------------------------------------------

_MERMAID_HTML_RE = re.compile(
    r'<pre><code class="language-mermaid">(.*?)</code></pre>',
    re.DOTALL,
)


def process_mermaid_blocks(html_text):
    """Replace markdown-rendered ```mermaid code blocks with <div class="mermaid">.

    markdown-it produces <pre><code class="language-mermaid">…</code></pre>
    with the diagram body HTML-escaped. Mermaid expects raw DSL text inside
    a div, so we unescape and re-wrap."""
    def _replace(match):
        diagram = html.unescape(match.group(1)).rstrip()
        return f'<div class="mermaid">\n{diagram}\n</div>'
    return _MERMAID_HTML_RE.sub(_replace, html_text)


def parse_frontmatter(text):
    """Parse YAML-like front matter between --- delimiters."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = {}
    for line in parts[1].strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, val = line.split(":", 1)
            val = val.strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            meta[key.strip()] = val
    body = parts[2].strip()
    return meta, body


def strip_leading_title(body):
    """Drop the leading `# Title` line if present.

    Blog posts (and some articles) duplicate their frontmatter `title:` as
    the first H1 of the body; the template already renders `{{ title }}` in
    the page hero, so leaving the H1 in the body produces two titles on the
    page. No-op when the body doesn't start with `# `.
    """
    if not body.startswith("# "):
        return body
    _, _, rest = body.partition("\n")
    return rest.lstrip("\n")


def translation_exists(md_path, lang):
    """Check whether the opposite-language sibling markdown file exists.

    Per-folder layout: each article lives in its own directory containing
    `ja.md` and `en.md` side by side.
    """
    md_path = Path(md_path)
    sibling_name = "en.md" if lang == "ja" else "ja.md"
    return (md_path.parent / sibling_name).exists()


# ---------------------------------------------------------------------------
# Custom Markdown blocks (:::chain, :::highlight, :::quote, :::compare)
# ---------------------------------------------------------------------------

def process_custom_blocks(body):
    """Convert custom ::: blocks to HTML."""
    lines = body.split("\n")
    result = []
    in_block = None
    block_content = []

    for line in lines:
        stripped = line.strip()

        # Block openers
        if stripped.startswith(":::chain"):
            if in_block:
                result.append(close_block(in_block, block_content))
                block_content = []
            in_block = "chain"
            continue
        elif stripped.startswith(":::highlight"):
            if in_block:
                result.append(close_block(in_block, block_content))
                block_content = []
            in_block = "highlight"
            continue
        elif stripped.startswith(":::quote"):
            if in_block:
                result.append(close_block(in_block, block_content))
                block_content = []
            in_block = "quote"
            continue
        elif stripped.startswith(":::compare"):
            if in_block:
                result.append(close_block(in_block, block_content))
                block_content = []
            in_block = "compare"
            continue
        elif stripped == ":::":
            if in_block:
                result.append(close_block(in_block, block_content))
                block_content = []
                in_block = None
            continue

        if in_block:
            block_content.append(line)
        else:
            result.append(line)

    if in_block:
        result.append(close_block(in_block, block_content))

    return "\n".join(result)


def close_block(block_type, lines):
    """Close a custom block and return HTML."""
    content = "\n".join(lines).strip()

    if block_type == "chain":
        content = content.replace("→", '<span class="arrow">&rarr;</span>')
        content = content.replace("\n\n", "<br><br>")
        content = content.replace("\n", "<br>\n")
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        return f'<div class="chain-diagram">\n{content}\n</div>'

    elif block_type == "highlight":
        html = md.render(content)
        return f'<div class="highlight-box">\n{html}\n</div>'

    elif block_type == "quote":
        content = content.replace("\n", "<br>\n")
        return f'<div class="quote-block">\n<p class="quote-text">\n{content}\n</p>\n</div>'

    elif block_type == "compare":
        return build_table(content)

    return content


def build_table(content):
    """Build comparison table from pipe-delimited text."""
    lines = [l.strip() for l in content.strip().split("\n") if l.strip()]
    if not lines:
        return ""

    html = '<table class="comparison-table fade-in">\n'
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if i == 0:
            html += "<tr>\n"
            for c in cells:
                html += f"  <th>{md.renderInline(c)}</th>\n"
            html += "</tr>\n"
        elif cells and all(set(c) <= {"-", ":"} for c in cells):
            # Skip Markdown table separator rows: `| --- | --- |`,
            # `|---|---|`, `| :--- | :---: | ---: |` etc.
            continue
        else:
            html += "<tr>\n"
            for c in cells:
                html += f"  <td>{md.renderInline(c)}</td>\n"
            html += "</tr>\n"
    html += "</table>"
    return html
