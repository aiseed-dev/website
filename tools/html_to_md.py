#!/usr/bin/env python3
"""
Convert existing HTML insight articles to Markdown format.
Extracts content from HTML and outputs Markdown with front matter.

Usage:
    python3 tools/html_to_md.py html/insights/agriculture/index.html
    python3 tools/html_to_md.py --all
"""

import sys
import re
import html
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent
INSIGHTS_DIR = SITE_ROOT / "html" / "insights"
ARTICLES_DIR = SITE_ROOT / "articles"

# Mapping of slugs to article numbers
ARTICLE_ORDER = {
    "climate-mistake": "01",
    "fossil-materials": "02",
    "agriculture": "03",
    "drone-defense": "04",
    "fusion": "05",
    "agi": "06",
    "nvidia": "07",
    "enterprise-tax": "08",
    "healthcare-fiscal": "09",
    "subtraction-design": "10",
    "regulation-redesign": "11",
    "ai-and-individual": "12",
}


def extract_text(html_str, tag_start, tag_end):
    """Extract text between tags."""
    start = html_str.find(tag_start)
    if start == -1:
        return ""
    start += len(tag_start)
    end = html_str.find(tag_end, start)
    if end == -1:
        return ""
    return html_str[start:end].strip()


def clean_html(text):
    """Remove HTML tags and decode entities."""
    # Replace <br> with newlines
    text = re.sub(r'<br\s*/?>', '\n', text)
    # Replace <strong> with **
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    # Replace <a href="...">text</a> with [text](url)
    text = re.sub(r'<a\s+href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)
    # Remove remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html.unescape(text)
    # Clean up whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()


def convert_chain_diagram(content):
    """Convert chain-diagram div content to :::chain block."""
    text = clean_html(content)
    # Replace → arrow entity remnants
    text = text.replace('→', '→')
    return f":::chain\n{text}\n:::"


def convert_highlight_box(content):
    """Convert highlight-box div content to :::highlight block."""
    text = clean_html(content)
    return f":::highlight\n{text}\n:::"


def convert_quote_block(content):
    """Convert quote-block div content to :::quote block."""
    # Extract just the quote-text paragraph
    match = re.search(r'class="quote-text"[^>]*>(.*?)</p>', content, re.DOTALL)
    if match:
        text = clean_html(match.group(1))
    else:
        text = clean_html(content)
    return f":::quote\n{text}\n:::"


def convert_table(content):
    """Convert comparison-table to :::compare block."""
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', content, re.DOTALL)
    if not rows:
        return ""

    lines = []
    for i, row in enumerate(rows):
        # Extract th or td cells
        cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, re.DOTALL)
        cells = [clean_html(c).replace('|', '\\|') for c in cells]
        line = "| " + " | ".join(cells) + " |"
        lines.append(line)
        if i == 0:
            # Add separator after header
            lines.append("| " + " | ".join(["---"] * len(cells)) + " |")

    return ":::compare\n" + "\n".join(lines) + "\n:::"


def process_body(body_html):
    """Convert article body HTML to Markdown."""
    result = []
    pos = 0

    while pos < len(body_html):
        # Check for chain-diagram
        chain_start = body_html.find('<div class="chain-diagram">', pos)
        highlight_start = body_html.find('<div class="highlight-box">', pos)
        quote_start = body_html.find('<div class="quote-block">', pos)
        table_start = body_html.find('<table class="comparison-table', pos)

        # Find the nearest special block
        starts = []
        if chain_start >= 0:
            starts.append(('chain', chain_start))
        if highlight_start >= 0:
            starts.append(('highlight', highlight_start))
        if quote_start >= 0:
            starts.append(('quote', quote_start))
        if table_start >= 0:
            starts.append(('table', table_start))

        if not starts:
            # No more special blocks, process rest as regular HTML
            remainder = body_html[pos:]
            result.append(convert_regular_html(remainder))
            break

        # Get nearest block
        starts.sort(key=lambda x: x[1])
        block_type, block_start = starts[0]

        # Process text before the block
        before = body_html[pos:block_start]
        if before.strip():
            result.append(convert_regular_html(before))

        # Find the closing tag
        if block_type == 'table':
            end_tag = '</table>'
        else:
            end_tag = '</div>'

        # Find matching close (need to handle nested divs)
        if block_type == 'table':
            close_pos = body_html.find(end_tag, block_start)
            if close_pos >= 0:
                close_pos += len(end_tag)
        else:
            # For divs, find matching close
            open_tag_end = body_html.find('>', block_start)
            depth = 1
            search_pos = open_tag_end + 1
            while depth > 0 and search_pos < len(body_html):
                next_open = body_html.find('<div', search_pos)
                next_close = body_html.find('</div>', search_pos)

                if next_close < 0:
                    break
                if next_open >= 0 and next_open < next_close:
                    depth += 1
                    search_pos = next_open + 4
                else:
                    depth -= 1
                    if depth == 0:
                        close_pos = next_close + len('</div>')
                        break
                    search_pos = next_close + 6
            else:
                close_pos = len(body_html)

        block_content = body_html[block_start:close_pos]

        if block_type == 'chain':
            result.append(convert_chain_diagram(block_content))
        elif block_type == 'highlight':
            result.append(convert_highlight_box(block_content))
        elif block_type == 'quote':
            result.append(convert_quote_block(block_content))
        elif block_type == 'table':
            result.append(convert_table(block_content))

        pos = close_pos

    return "\n\n".join(result)


def convert_regular_html(text):
    """Convert regular HTML paragraphs and headings to Markdown."""
    lines = []

    # Process headings
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', lambda m: f"\n## {clean_html(m.group(1))}\n", text, flags=re.DOTALL)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', lambda m: f"\n### {clean_html(m.group(1))}\n", text, flags=re.DOTALL)

    # Process paragraphs
    text = re.sub(r'<p[^>]*>(.*?)</p>', lambda m: f"\n{clean_html(m.group(1))}\n", text, flags=re.DOTALL)

    # Clean up remaining tags
    text = clean_html(text)

    # Clean up excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def convert_article(html_path):
    """Convert a single HTML article to Markdown."""
    html_path = Path(html_path)
    if not html_path.exists():
        print(f"Error: {html_path} not found")
        return False

    content = html_path.read_text(encoding="utf-8")

    # Determine slug from path
    slug = html_path.parent.name
    number = ARTICLE_ORDER.get(slug, "00")

    # Extract metadata
    title_match = re.search(r'<h1 class="hero-title">(.*?)</h1>', content, re.DOTALL)
    title = clean_html(title_match.group(1)) if title_match else ""

    subtitle_match = re.search(r'<p class="hero-subtitle">\s*(.*?)\s*</p>', content, re.DOTALL)
    subtitle = clean_html(subtitle_match.group(1)) if subtitle_match else ""

    label_match = re.search(r'<p class="hero-label">(.*?)</p>', content, re.DOTALL)
    label = clean_html(label_match.group(1)) if label_match else ""

    date_match = re.search(r'<p class="date">(.*?)</p>', content, re.DOTALL)
    date = clean_html(date_match.group(1)) if date_match else ""

    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    description = html.unescape(desc_match.group(1)) if desc_match else ""

    # Extract prev/next from article-nav
    prev_match = re.search(r'<a href="/insights/([^/]+)/">&larr;.*?:\s*(.*?)</a>', content)
    prev_slug = prev_match.group(1) if prev_match else ""
    prev_title = clean_html(prev_match.group(2)) if prev_match else ""

    next_match = re.search(r'<a href="/insights/([^/]+)/">次:\s*(.*?)\s*&rarr;</a>', content)
    next_slug = next_match.group(1) if next_match else ""
    next_title = clean_html(next_match.group(2)) if next_match else ""

    # Extract body content
    body_start = content.find('<div class="prose fade-in">')
    body_end = content.find('<!-- Article Navigation -->')
    if body_end < 0:
        body_end = content.find('<div class="article-nav">')

    if body_start < 0 or body_end < 0:
        print(f"Error: cannot find body content in {html_path}")
        return False

    body_start = content.find('>', body_start) + 1
    body_html = content[body_start:body_end].strip()

    # Convert body to Markdown
    body_md = process_body(body_html)

    # Build front matter
    front_matter = f"""---
slug: {slug}
number: "{number}"
title: {title}
subtitle: {subtitle}
description: {description}
date: {date}
label: {label}
prev_slug: {prev_slug}
prev_title: {prev_title}
next_slug: {next_slug}
next_title: {next_title}
---"""

    # Write output
    out_file = ARTICLES_DIR / f"{number}-{slug}.md"
    out_file.write_text(f"{front_matter}\n\n{body_md}\n", encoding="utf-8")

    print(f"Converted: {html_path} → {out_file}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/html_to_md.py <article.html>")
        print("       python3 tools/html_to_md.py --all")
        sys.exit(1)

    if sys.argv[1] == "--all":
        # Find all article directories (exclude index.html at root)
        for slug in ARTICLE_ORDER:
            html_file = INSIGHTS_DIR / slug / "index.html"
            if html_file.exists():
                convert_article(html_file)
            else:
                print(f"Skipping: {html_file} not found")
        return

    convert_article(sys.argv[1])


if __name__ == "__main__":
    main()
