#!/usr/bin/env python3
"""
Markdown → HTML article/blog builder for aiseed.dev

Usage:
    python3 tools/build_article.py articles/09-healthcare-fiscal.md
    python3 tools/build_article.py blog/001-grid-attack-naphtha.md
    python3 tools/build_article.py --all          # Build all articles + blog
    python3 tools/build_article.py --list         # List available articles

    # Operate on a different site directory (layout: articles/, blog/, html/):
    python3 tools/build_article.py --site /path/to/other-site --all
    AISEED_SITE=/path/to/other-site python3 tools/build_article.py --all

Dependencies: jinja2, markdown-it-py, pillow

Implementation is split across tools/build/:
    config.py         — site paths, Jinja2 env, configure_site()
    markdown.py       — frontmatter + custom ::: blocks + CommonMark
    images.py         — image copying + OGP image generation
    template_vars.py  — *_vars() builders for article/index pages

Templates live in tools/templates/; a site may override them by placing its
own tools/templates/ under --site.
"""

import re
import sys
from pathlib import Path

from build import config
from build.config import render
from build.images import (
    OGP_FILENAME,
    OGP_SIZE,
    copy_images,
    generate_ogp_image,
)
from build.markdown import (
    md,
    parse_frontmatter,
    process_custom_blocks,
    strip_leading_title,
    translation_exists,
)
from build.template_vars import (
    article_vars,
    blog_index_vars,
    blog_vars,
    index_vars,
)


# ---------------------------------------------------------------------------
# Build functions — articles
# ---------------------------------------------------------------------------

def build_article(md_path):
    """Build a single article from Markdown file."""
    md_path = Path(md_path)
    if not md_path.exists():
        print(f"Error: {md_path} not found")
        return False

    text = md_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    if "slug" not in meta:
        print(f"Error: {md_path} missing 'slug' in front matter")
        return False

    # Resolve output directory up front so OGP generation can target it
    lang = meta.get("lang", "ja")
    if lang == "en":
        out_dir = config.SITE_ROOT / "html" / "en" / "insights" / meta["slug"]
    else:
        out_dir = config.OUTPUT_BASE / meta["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)

    # Context for OGP image resolution
    meta["_source_dir"] = str(md_path.parent)
    meta["_out_dir"] = str(out_dir)
    meta["_has_translation"] = translation_exists(md_path, lang)

    # Drop the leading `# Title` (duplicates frontmatter title rendered by template)
    body = strip_leading_title(body)

    # Process custom blocks first
    body = process_custom_blocks(body)

    # Convert remaining Markdown to HTML (markdown-it-py, CommonMark)
    body_html = md.render(body)

    # Indent body HTML for template
    indented = "\n".join(
        f"                {line}" if line.strip() else ""
        for line in body_html.split("\n")
    )

    # Build full HTML
    variables = article_vars(meta, indented)
    html = render("article.html", variables)

    out_file = out_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")

    # Copy images from source directory
    # e.g. articles/03-*.jpg → html/insights/slug/
    num_prefix = md_path.name.split("-", 1)[0]  # "03", "en"
    if num_prefix == "en":
        num_prefix = md_path.name.split("-", 2)[1]  # "en-03-..." → "03"
    copy_images(md_path.parent, out_dir, prefix=num_prefix)

    print(f"Built: {out_file}")
    return True


def collect_articles(lang="ja"):
    """Collect and sort article metadata for a given language."""
    prefix = "en-" if lang == "en" else ""
    pattern = f"{prefix}[0-9]*.md"
    articles = []
    for f in sorted(config.ARTICLES_DIR.glob(pattern)):
        text = f.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        if meta.get("lang", "ja") == lang or (lang == "ja" and "lang" not in meta):
            articles.append(meta)
    articles.sort(key=lambda m: m.get("number", "99"))
    return articles


def build_index(lang="ja"):
    """Build the insights index page from article metadata."""
    is_en = lang == "en"
    articles = collect_articles(lang)
    insights_base = "/en/insights" if is_en else "/insights"

    # Build article list HTML
    article_list = ""
    for a in articles:
        slug = a.get("slug", "")
        number = a.get("number", "").strip('"')
        title = a.get("title", "")
        subtitle = a.get("subtitle", "")
        description = a.get("description", "")
        article_list += f'''
                <a href="{insights_base}/{slug}/" style="text-decoration: none; color: inherit;">
                    <div class="activity-item fade-in">
                        <div class="activity-number">{number}</div>
                        <div class="activity-content">
                            <h3>{title} — {subtitle}</h3>
                            <p>{description}</p>
                        </div>
                    </div>
                </a>
'''

    variables = index_vars(lang, article_list)
    html = render("index.html", variables)

    # Write output
    if is_en:
        out_file = config.SITE_ROOT / "html" / "en" / "insights" / "index.html"
    else:
        out_file = config.SITE_ROOT / "html" / "insights" / "index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"Built index: {out_file}")
    return True


# ---------------------------------------------------------------------------
# Build functions — blog
# ---------------------------------------------------------------------------

def build_blog_post(md_path):
    """Build a single blog post from Markdown file."""
    md_path = Path(md_path)
    if not md_path.exists():
        print(f"Error: {md_path} not found")
        return False

    text = md_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    if "slug" not in meta:
        print(f"Error: {md_path} missing 'slug' in front matter")
        return False

    lang = meta.get("lang", "ja")
    if lang == "en":
        out_dir = config.SITE_ROOT / "html" / "en" / "blog" / meta["slug"]
    else:
        out_dir = config.BLOG_OUTPUT_BASE / meta["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)

    # Context for OGP image resolution
    meta["_source_dir"] = str(md_path.parent)
    meta["_out_dir"] = str(out_dir)
    meta["_has_translation"] = translation_exists(md_path, lang)

    # Prev/next navigation — posts are ordered by numeric filename prefix.
    # collect_blog_posts() returns them newest-first (descending file number),
    # so posts[i-1] is newer and posts[i+1] is older than posts[i]. We treat
    # "prev" as older (smaller number) and "next" as newer, matching how
    # articles frontmatter labels the series order.
    posts = collect_blog_posts(lang)
    idx = next(
        (i for i, p in enumerate(posts) if p.get("slug") == meta["slug"]),
        None,
    )
    if idx is not None:
        meta["_next_post"] = posts[idx - 1] if idx > 0 else None
        meta["_prev_post"] = posts[idx + 1] if idx < len(posts) - 1 else None
    else:
        meta["_prev_post"] = None
        meta["_next_post"] = None

    body = strip_leading_title(body)
    body = process_custom_blocks(body)
    body_html = md.render(body)

    indented = "\n".join(
        f"                {line}" if line.strip() else ""
        for line in body_html.split("\n")
    )

    variables = blog_vars(meta, indented)
    html = render("article.html", variables)

    out_file = out_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")

    # Copy images from source directory
    # e.g. blog/001-*.jpeg → html/blog/slug/
    num_prefix = md_path.name.split("-", 1)[0]  # "001", "en"
    if num_prefix == "en":
        num_prefix = md_path.name.split("-", 2)[1]  # "en-001-..." → "001"
        copy_images(md_path.parent, out_dir, prefix=f"en-{num_prefix}")
    copy_images(md_path.parent, out_dir, prefix=num_prefix)

    print(f"Built blog: {out_file}")
    return True


def collect_blog_posts(lang="ja"):
    """Collect and sort blog post metadata for a given language."""
    if not config.BLOG_DIR.exists():
        return []
    prefix = "en-" if lang == "en" else ""
    pattern = f"{prefix}[0-9]*.md"
    posts = []
    for f in sorted(config.BLOG_DIR.glob(pattern)):
        text = f.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        if meta.get("lang", "ja") == lang or (lang == "ja" and "lang" not in meta):
            # Extract numeric prefix from filename for ordering
            stem = f.stem
            if lang == "en" and stem.startswith("en-"):
                stem = stem[3:]
            num_match = re.match(r"(\d+)", stem)
            meta["_file_number"] = int(num_match.group(1)) if num_match else 0
            posts.append(meta)
    # Sort by file number descending (newest first; 006 before 005...)
    posts.sort(key=lambda p: p.get("_file_number", 0), reverse=True)
    return posts


def build_blog_index(lang="ja"):
    """Build the blog index page from post metadata."""
    is_en = lang == "en"
    posts = collect_blog_posts(lang)
    blog_base = "/en/blog" if is_en else "/blog"

    post_list = ""
    for p in posts:
        slug = p.get("slug", "")
        title = p.get("title", "")
        date = p.get("date", "")
        description = p.get("description", "")
        post_list += f'''
                <a href="{blog_base}/{slug}/" style="text-decoration: none; color: inherit;">
                    <div class="activity-item">
                        <div class="activity-number" style="font-size: 0.7rem;">{date}</div>
                        <div class="activity-content">
                            <h3>{title}</h3>
                            <p>{description}</p>
                        </div>
                    </div>
                </a>
'''

    variables = blog_index_vars(lang, post_list)
    html = render("index.html", variables)

    if is_en:
        out_file = config.SITE_ROOT / "html" / "en" / "blog" / "index.html"
    else:
        out_file = config.BLOG_OUTPUT_BASE / "index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"Built blog index: {out_file}")
    return True


# ---------------------------------------------------------------------------
# Home page: latest blog posts section
# ---------------------------------------------------------------------------

HOME_LATEST_COUNT = 5
HOME_MARKER_START = "<!-- LATEST_BLOG_POSTS_START -->"
HOME_MARKER_END = "<!-- LATEST_BLOG_POSTS_END -->"


def update_home_latest_posts(lang="ja", count=HOME_LATEST_COUNT):
    """Replace the 'Latest Blog Posts' block on the home page with the N
    newest posts, sourced from the blog markdown frontmatter."""
    is_en = lang == "en"
    posts = collect_blog_posts(lang)[:count]
    if not posts:
        return False

    blog_base = "/en/blog" if is_en else "/blog"
    cards = []
    for p in posts:
        slug = p.get("slug", "")
        title = p.get("title", "")
        date = p.get("date", "")
        description = p.get("description", "")
        cards.append(
            f'                <a href="{blog_base}/{slug}/" class="article-link">\n'
            f'                    <div class="activity-item">\n'
            f'                        <div class="activity-number" style="font-size: 0.7rem;">{date}</div>\n'
            f'                        <div class="activity-content">\n'
            f'                            <h3>{title}</h3>\n'
            f'                            <p>{description}</p>\n'
            f'                        </div>\n'
            f'                    </div>\n'
            f'                </a>'
        )

    home = config.SITE_ROOT / "html" / ("en/index.html" if is_en else "index.html")
    if not home.exists():
        print(f"Warning: home page not found: {home}")
        return False

    text = home.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(HOME_MARKER_START) + r".*?" + re.escape(HOME_MARKER_END),
        re.DOTALL,
    )
    if not pattern.search(text):
        print(f"Warning: markers not found in {home}")
        return False

    block = (
        HOME_MARKER_START
        + "\n\n"
        + "\n\n".join(cards)
        + "\n\n                "
        + HOME_MARKER_END
    )
    new_text = pattern.sub(block, text)
    home.write_text(new_text, encoding="utf-8")
    print(f"Updated home latest posts: {home}")
    return True


# ---------------------------------------------------------------------------
# Sitemap & robots.txt
# ---------------------------------------------------------------------------

def build_sitemap():
    """Generate sitemap.xml from all articles."""
    from datetime import date

    def norm_date(d):
        """Convert YYYY.MM.DD or YYYY-MM-DD to ISO YYYY-MM-DD."""
        if not d:
            return date.today().isoformat()
        return str(d).replace(".", "-")

    ja_articles = collect_articles("ja")
    en_articles = collect_articles("en")
    ja_posts = collect_blog_posts("ja")
    en_posts = collect_blog_posts("en")

    all_dates = [
        norm_date(m.get("date"))
        for m in (*ja_articles, *en_articles, *ja_posts, *en_posts)
        if m.get("date")
    ]
    latest = max(all_dates) if all_dates else date.today().isoformat()

    site_url = config.SITE_URL

    urls = []
    # Homepages
    urls.append((f"{site_url}/", latest, "1.0"))
    urls.append((f"{site_url}/en/", latest, "0.8"))

    # Index pages
    urls.append((f"{site_url}/insights/", latest, "0.9"))
    urls.append((f"{site_url}/en/insights/", latest, "0.8"))

    # JP articles
    for meta in ja_articles:
        slug = meta.get("slug", "")
        if not slug:
            continue
        urls.append((f"{site_url}/insights/{slug}/", norm_date(meta.get("date")), "0.7"))

    # EN articles
    for meta in en_articles:
        slug = meta.get("slug", "")
        if not slug:
            continue
        urls.append((f"{site_url}/en/insights/{slug}/", norm_date(meta.get("date")), "0.6"))

    # Blog index pages
    urls.append((f"{site_url}/blog/", latest, "0.8"))
    urls.append((f"{site_url}/en/blog/", latest, "0.7"))

    # JP blog posts
    for meta in ja_posts:
        slug = meta.get("slug", "")
        if not slug:
            continue
        urls.append((f"{site_url}/blog/{slug}/", norm_date(meta.get("date")), "0.7"))

    # EN blog posts
    for meta in en_posts:
        slug = meta.get("slug", "")
        if not slug:
            continue
        urls.append((f"{site_url}/en/blog/{slug}/", norm_date(meta.get("date")), "0.6"))

    # Natural Farming / About / Light Farming (both JP and EN)
    urls.append((f"{site_url}/natural-farming/", latest, "0.8"))
    urls.append((f"{site_url}/en/natural-farming/", latest, "0.7"))
    urls.append((f"{site_url}/about/", latest, "0.6"))
    urls.append((f"{site_url}/en/about/", latest, "0.5"))
    urls.append((f"{site_url}/light-farming/", latest, "0.8"))
    urls.append((f"{site_url}/en/light-farming/", latest, "0.7"))

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for loc, lastmod, priority in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{loc}</loc>")
        xml_lines.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_lines.append(f"    <priority>{priority}</priority>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>")

    out = config.SITE_ROOT / "html" / "sitemap.xml"
    out.write_text("\n".join(xml_lines) + "\n", encoding="utf-8")
    print(f"Built: {out}")


def build_robots():
    """Generate robots.txt."""
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /tools/\n"
        "Disallow: /articles/\n"
        "\n"
        f"Sitemap: {config.SITE_URL}/sitemap.xml\n"
    )
    out = config.SITE_ROOT / "html" / "robots.txt"
    out.write_text(content, encoding="utf-8")
    print(f"Built: {out}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def regenerate_ogp(md_path):
    """Regenerate only the og-image.jpg for a given article/blog markdown file."""
    md_path = Path(md_path)
    if not md_path.exists():
        print(f"Error: {md_path} not found")
        return False
    meta, _ = parse_frontmatter(md_path.read_text(encoding="utf-8"))
    if "slug" not in meta:
        print(f"Error: {md_path} missing 'slug'")
        return False
    hero = meta.get("hero_image", "").strip()
    if not hero:
        print(f"Skip: {md_path} has no hero_image")
        return False

    is_blog = md_path.parent.name == "blog"
    is_en = meta.get("lang", "ja") == "en"
    if is_blog:
        base = config.SITE_ROOT / "html" / "en" / "blog" if is_en else config.BLOG_OUTPUT_BASE
    else:
        base = config.SITE_ROOT / "html" / "en" / "insights" if is_en else config.OUTPUT_BASE
    out_dir = base / meta["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)

    src = md_path.parent / hero
    out = out_dir / OGP_FILENAME
    if generate_ogp_image(src, out):
        print(f"OGP: {out} ({OGP_SIZE[0]}x{OGP_SIZE[1]}) from {src.name}")
        return True
    print(f"Error: source image {src} not found")
    return False


def main():
    site, args = config.resolve_site(sys.argv[1:])
    config.configure_site(site)

    if not args:
        print("Usage: python3 tools/build_article.py [--site <dir>] <article.md>")
        print("       python3 tools/build_article.py [--site <dir>] --all")
        print("       python3 tools/build_article.py [--site <dir>] --list")
        print("       python3 tools/build_article.py [--site <dir>] --ogp <article.md>")
        sys.exit(1)

    arg = args[0]

    if arg == "--ogp":
        if len(args) < 2:
            print("Usage: python3 tools/build_article.py [--site <dir>] --ogp <article.md>")
            sys.exit(1)
        regenerate_ogp(args[1])
        return

    if arg == "--list":
        for f in sorted(config.ARTICLES_DIR.glob("*.md")):
            meta, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
            num = meta.get("number", "??")
            title = meta.get("title", "untitled")
            print(f"  [{num}] {f.name} → {title}")
        return

    if arg == "--all":
        files = sorted(config.ARTICLES_DIR.glob("*.md"))
        if not files:
            print(f"No .md files found in {config.ARTICLES_DIR}")
            return
        ok = 0
        for f in files:
            if build_article(f):
                ok += 1
        build_index("ja")
        build_index("en")

        # Build blog posts
        blog_ok = 0
        blog_files = sorted(config.BLOG_DIR.glob("*.md")) if config.BLOG_DIR.exists() else []
        for f in blog_files:
            if build_blog_post(f):
                blog_ok += 1
        if blog_files:
            build_blog_index("ja")
            build_blog_index("en")
            update_home_latest_posts("ja")
            update_home_latest_posts("en")

        build_sitemap()
        build_robots()
        print(f"\nBuilt {ok}/{len(files)} articles + {blog_ok}/{len(blog_files)} blog posts + indexes + sitemap.xml + robots.txt.")
        return

    # Auto-detect blog vs article
    if "blog/" in arg or "blog\\" in arg:
        build_blog_post(arg)
    else:
        build_article(arg)


if __name__ == "__main__":
    main()
