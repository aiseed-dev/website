#!/usr/bin/env python3
"""
Markdown → HTML article/blog builder for aiseed.dev

Per-folder layout (single article = single folder):
    articles/insights/01-climate-mistake/{ja,en}.md
    articles/blog/015-japan-windows-disaster-risk/{ja,en}.md + assets
    articles/claude-debian/00-prologue/{ja,en}.md

Usage:
    python3 tools/build_article.py articles/insights/09-healthcare-fiscal/ja.md
    python3 tools/build_article.py articles/blog/001-grid-attack-naphtha/ja.md
    python3 tools/build_article.py --all          # Build all articles + blog
    python3 tools/build_article.py --list         # List available articles

    # Operate on a different site directory (layout: articles/, html/):
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
    aiways_index_vars,
    article_vars,
    blog_index_vars,
    blog_vars,
    book_index_vars,
    book_vars,
    index_vars,
)

BOOK_SLUG_PREFIX = "claude-debian-"


def _iter_article_files(series_dir, lang):
    """Yield `<lang>.md` files from each `NN-slug/` subfolder of `series_dir`,
    sorted by folder name (which leads with the chapter number).

    Returns an empty iterator if the series directory does not exist.
    """
    if not series_dir.exists():
        return
    fname = "ja.md" if lang == "ja" else "en.md"
    for sub in sorted(series_dir.iterdir()):
        if not sub.is_dir():
            continue
        if not sub.name[:1].isdigit():
            continue
        f = sub / fname
        if f.exists():
            yield f


def _detect_lang(md_path):
    """ja.md → 'ja',  en.md → 'en'."""
    return "en" if md_path.name == "en.md" else "ja"


def _book_stem(slug):
    """URL stem for a book chapter: slug without the `claude-debian-` prefix."""
    if slug.startswith(BOOK_SLUG_PREFIX):
        return slug[len(BOOK_SLUG_PREFIX):]
    return slug


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

    # Resolve output directory up front so OGP generation can target it.
    lang = meta.get("lang") or _detect_lang(md_path)
    meta["lang"] = lang
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

    # Copy assets from the article folder (lang-aware: JA build skips
    # `en-`-prefixed assets so EN-only PDFs don't leak in).
    copy_images(md_path.parent, out_dir, lang=lang)

    print(f"Built: {out_file}")
    return True


def collect_articles(lang="ja"):
    """Collect and sort article metadata for a given language."""
    articles = []
    for f in _iter_article_files(config.INSIGHTS_DIR, lang):
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

    lang = meta.get("lang") or _detect_lang(md_path)
    meta["lang"] = lang
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

    # Copy assets from the article folder (lang-aware).
    copy_images(md_path.parent, out_dir, lang=lang)

    print(f"Built blog: {out_file}")
    return True


def collect_blog_posts(lang="ja"):
    """Collect and sort blog post metadata for a given language."""
    posts = []
    for f in _iter_article_files(config.BLOG_DIR, lang):
        text = f.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        if meta.get("lang", "ja") == lang or (lang == "ja" and "lang" not in meta):
            # Folder name leads with the post number, e.g. "015-japan-…".
            num_match = re.match(r"(\d+)", f.parent.name)
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
# Build functions — book (long-form serial)
#
# Source:  articles/claude-debian/NN-slug.md
# Output:  html/claude-debian/{stem}/index.html   (stem = slug sans prefix)
# ---------------------------------------------------------------------------

def build_book_chapter(md_path):
    """Build a single book chapter from a Markdown file.

    JA source: articles/claude-debian/NN-slug.md    → html/claude-debian/{stem}/
    EN source: articles/claude-debian/en-NN-slug.md → html/en/claude-debian/{stem}/
    """
    md_path = Path(md_path)
    if not md_path.exists():
        print(f"Error: {md_path} not found")
        return False

    text = md_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    if "slug" not in meta:
        print(f"Error: {md_path} missing 'slug' in front matter")
        return False

    lang = meta.get("lang") or _detect_lang(md_path)
    meta["lang"] = lang

    stem = _book_stem(meta["slug"])
    if lang == "en":
        out_dir = config.SITE_ROOT / "html" / "en" / "claude-debian" / stem
    else:
        out_dir = config.BOOK_OUTPUT_BASE / stem
    out_dir.mkdir(parents=True, exist_ok=True)

    meta["_source_dir"] = str(md_path.parent)
    meta["_out_dir"] = str(out_dir)
    meta["_has_translation"] = translation_exists(md_path, lang)

    body = strip_leading_title(body)
    body = process_custom_blocks(body)
    body_html = md.render(body)

    indented = "\n".join(
        f"                {line}" if line.strip() else ""
        for line in body_html.split("\n")
    )

    variables = book_vars(meta, indented)
    html = render("article.html", variables)

    out_file = out_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")

    # Copy chapter assets into out_dir (lang-aware: JA build skips
    # `en-`-prefixed assets).
    copy_images(md_path.parent, out_dir, lang=lang)

    print(f"Built book: {out_file}")
    return True


def collect_book_chapters(lang="ja"):
    """Collect book chapter metadata for a language, in folder-name order."""
    chapters = []
    for f in _iter_article_files(config.BOOK_DIR, lang):
        text = f.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        if meta.get("lang", "ja") != lang and not (lang == "ja" and "lang" not in meta):
            continue
        num_match = re.match(r"(\d+)", f.parent.name)
        meta["_file_number"] = int(num_match.group(1)) if num_match else 0
        chapters.append(meta)
    chapters.sort(key=lambda m: m.get("_file_number", 0))
    return chapters


def build_book_index(lang="ja"):
    """Build the book table-of-contents page for a language."""
    chapters = collect_book_chapters(lang)
    if not chapters:
        return False

    is_en = lang == "en"
    book_base = "/en/claude-debian" if is_en else "/claude-debian"
    # "Translation exists" if the opposite language has any chapters built.
    has_translation = bool(collect_book_chapters("en" if not is_en else "ja"))

    chapter_list = ""
    for c in chapters:
        slug = c.get("slug", "")
        stem = _book_stem(slug)
        number = c.get("number", "").strip('"')
        title = c.get("title", "")
        subtitle = c.get("subtitle", "")
        description = c.get("description", "")
        chapter_list += f'''
                <a href="{book_base}/{stem}/" style="text-decoration: none; color: inherit;">
                    <div class="activity-item fade-in">
                        <div class="activity-number">{number}</div>
                        <div class="activity-content">
                            <h3>{title}{(" — " + subtitle) if subtitle else ""}</h3>
                            <p>{description}</p>
                        </div>
                    </div>
                </a>
'''

    variables = book_index_vars(lang, chapter_list, has_translation=has_translation)
    html = render("index.html", variables)

    if is_en:
        out_file = config.SITE_ROOT / "html" / "en" / "claude-debian" / "index.html"
    else:
        out_file = config.BOOK_OUTPUT_BASE / "index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"Built book index: {out_file}")
    return True


# ---------------------------------------------------------------------------
# Build functions — ai-native-ways (independent template)
#
# Source:  articles/ai-native-ways/NN-slug/{ja,en}.md
# Output:  html/ai-native-ways/{slug}/index.html  (JA)
#          html/en/ai-native-ways/{slug}/index.html  (EN)
#
# Unlike the other series, ai-native-ways ships its own self-contained
# template (articles/ai-native-ways/template.html, template.en.html) — fonts,
# CSS and layout are declared there. The build pipeline just feeds the
# rendered body and metadata into that template.
# ---------------------------------------------------------------------------

AIWAYS_SERIES_NAME_JA = "AIネイティブな仕事の作法"
AIWAYS_SERIES_NAME_EN = "AI-Native Ways of Working"


def _aiways_chapter_label(number: str, lang: str) -> str:
    """'00' → '序章' / 'Prologue'. Otherwise '第N章' / 'Chapter N'."""
    n = number.lstrip("0") or "0"
    if n == "0":
        return "序章" if lang == "ja" else "Prologue"
    return f"第{n}章" if lang == "ja" else f"Chapter {n}"


def _aiways_template_path(lang: str) -> Path:
    return config.AIWAYS_DIR / ("template.html" if lang == "ja" else "template.en.html")


def _aiways_chapter_examples_html(chapter_dir, chapter_slug: str, lang: str) -> str:
    """Render a callout at the end of a chapter listing its example-N/ pages.

    For EN chapters, if an example only ships JA content, link to the JA URL
    so the source / outputs are still reachable.
    """
    examples = sorted(
        sub for sub in Path(chapter_dir).iterdir()
        if sub.is_dir() and re.match(r"example-\d+$", sub.name)
    )
    if not examples:
        return ""

    is_en = lang == "en"
    heading = "実例" if not is_en else "Examples"
    intro = (
        "再現可能なソース・コマンド・実測結果を、別ページにまとめてある。"
        if not is_en
        else "Runnable source, commands, and measured results — see the dedicated example page(s)."
    )

    items = []
    for ex in examples:
        en_readme = ex / "README.en.md"
        # If EN README exists, link to /en/.../example-N/. Otherwise (or for JA)
        # link to the JA URL.
        if is_en and not en_readme.exists():
            href = f"/ai-native-ways/{chapter_slug}/{ex.name}/"
            ja_only_marker = ' <small>(JA)</small>'
        else:
            base = "/en/ai-native-ways" if is_en else "/ai-native-ways"
            href = f"{base}/{chapter_slug}/{ex.name}/"
            ja_only_marker = ''

        readme = en_readme if (is_en and en_readme.exists()) else (ex / "README.md")
        title = ""
        if readme.exists():
            text = readme.read_text(encoding="utf-8")
            m = re.search(r"^# (.+)$", text, re.MULTILINE)
            if m:
                title = m.group(1).strip()
        if not title:
            title = _example_label(ex.name, lang)
        items.append(f'<li><a href="{href}">{title}</a>{ja_only_marker}</li>')

    return (
        f'\n<h2>{heading}</h2>\n'
        f'<p>{intro}</p>\n'
        f'<ul>\n' + "\n".join(items) + "\n</ul>\n"
    )


def build_aiways_chapter(md_path):
    """Build a single ai-native-ways chapter using the series-local template."""
    from jinja2 import Template

    md_path = Path(md_path)
    if not md_path.exists():
        print(f"Error: {md_path} not found")
        return False

    text = md_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    if "slug" not in meta:
        print(f"Error: {md_path} missing 'slug' in front matter")
        return False

    lang = meta.get("lang") or _detect_lang(md_path)
    meta["lang"] = lang

    slug = meta["slug"]
    if lang == "en":
        out_dir = config.SITE_ROOT / "html" / "en" / "ai-native-ways" / slug
    else:
        out_dir = config.AIWAYS_OUTPUT_BASE / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    meta["_source_dir"] = str(md_path.parent)
    meta["_out_dir"] = str(out_dir)

    body = strip_leading_title(body)
    body = process_custom_blocks(body)
    body_html = md.render(body)

    # Append a "実例 / Examples" callout listing example-N/ folders for this chapter.
    examples_html = _aiways_chapter_examples_html(md_path.parent, meta["slug"], lang)
    if examples_html:
        body_html = body_html + examples_html

    series_name = AIWAYS_SERIES_NAME_EN if lang == "en" else AIWAYS_SERIES_NAME_JA
    series_index_path_ja = "/ai-native-ways/"
    series_index_path_en = "/en/ai-native-ways/"
    series_index_url = series_index_path_en if lang == "en" else series_index_path_ja

    canonical_url = f"{config.SITE_URL}/{'en/' if lang == 'en' else ''}ai-native-ways/{slug}/"
    hreflang_ja = f"{config.SITE_URL}/ai-native-ways/{slug}/"
    hreflang_en = f"{config.SITE_URL}/en/ai-native-ways/{slug}/"

    other_lang_url = (hreflang_ja if lang == "en" else hreflang_en)
    other_lang_label = "日本語" if lang == "en" else "EN"

    has_other = (md_path.parent / ("ja.md" if lang == "en" else "en.md")).exists()

    # Resolve OG image: prefer an article-folder hero_image, else default
    from build.images import resolve_og_image, OGP_FILENAME, generate_ogp_image
    og_image = resolve_og_image(meta, out_dir, public_base_url=canonical_url.rstrip("/"))

    date_str = meta.get("date", "")
    year = date_str.split(".")[0] if "." in date_str else (date_str[:4] if date_str else "")

    variables = {
        "title": meta.get("title", ""),
        "title_html": meta.get("title_html", ""),
        "subtitle": meta.get("subtitle", ""),
        "description": meta.get("description", ""),
        "date": date_str,
        "year": year,
        "number": meta.get("number", "").strip('"'),
        "label": meta.get("label", ""),
        "series": series_name,
        "series_index_url": series_index_url,
        "chapter_label": _aiways_chapter_label(meta.get("number", "").strip('"'), lang),
        "content_html": body_html,
        "canonical_url": canonical_url,
        "hreflang_ja": hreflang_ja if (md_path.parent / "ja.md").exists() else "",
        "hreflang_en": hreflang_en if (md_path.parent / "en.md").exists() else "",
        "og_image": og_image,
        "other_lang_url": other_lang_url if has_other else "",
        "other_lang_label": other_lang_label,
    }

    template_text = _aiways_template_path(lang).read_text(encoding="utf-8")
    html = Template(template_text).render(**variables)

    out_file = out_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")

    # Copy assets from the article folder (lang-aware).
    copy_images(md_path.parent, out_dir, lang=lang)

    print(f"Built ai-native-ways: {out_file}")
    return True


# ---------------------------------------------------------------------------
# Build functions — phosphorus-and-farming (independent template, like ai-native-ways)
#
# Source:  articles/phosphorus-and-farming/NN-slug/{ja,en}.md
# Output:  html/phosphorus-and-farming/{slug}/index.html       (JA)
#          html/en/phosphorus-and-farming/{slug}/index.html    (EN)
#
# Like ai-native-ways, the series ships its own self-contained template
# (articles/phosphorus-and-farming/template.html, template.en.html). The
# existing static /natural-farming/ landing page is independent and untouched
# (different URL prefix entirely).
# ---------------------------------------------------------------------------

FARMING_SERIES_NAME_JA = "リン資源枯渇と自然農法シリーズ"
FARMING_SERIES_NAME_EN = "Phosphorus Depletion and Natural Farming Series"


def _farming_chapter_label(number: str, lang: str) -> str:
    """'00' → '序章' / 'Prologue'. Otherwise '第N章' / 'Chapter N'."""
    n = number.lstrip("0") or "0"
    if n == "0":
        return "序章" if lang == "ja" else "Prologue"
    return f"第{n}章" if lang == "ja" else f"Chapter {n}"


def _farming_template_path(lang: str) -> Path:
    return config.FARMING_DIR / ("template.html" if lang == "ja" else "template.en.html")


def build_farming_chapter(md_path):
    """Build a single phosphorus-and-farming chapter using the series-local template."""
    from jinja2 import Template

    md_path = Path(md_path)
    if not md_path.exists():
        print(f"Error: {md_path} not found")
        return False

    text = md_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    if "slug" not in meta:
        print(f"Error: {md_path} missing 'slug' in front matter")
        return False

    lang = meta.get("lang") or _detect_lang(md_path)
    meta["lang"] = lang

    slug = meta["slug"]
    if lang == "en":
        out_dir = config.SITE_ROOT / "html" / "en" / "phosphorus-and-farming" / slug
    else:
        out_dir = config.FARMING_OUTPUT_BASE / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    meta["_source_dir"] = str(md_path.parent)
    meta["_out_dir"] = str(out_dir)

    body = strip_leading_title(body)
    body = process_custom_blocks(body)
    body_html = md.render(body)

    series_name = FARMING_SERIES_NAME_EN if lang == "en" else FARMING_SERIES_NAME_JA
    series_index_url = "/en/phosphorus-and-farming/" if lang == "en" else "/phosphorus-and-farming/"

    canonical_url = f"{config.SITE_URL}/{'en/' if lang == 'en' else ''}phosphorus-and-farming/{slug}/"
    hreflang_ja = f"{config.SITE_URL}/phosphorus-and-farming/{slug}/"
    hreflang_en = f"{config.SITE_URL}/en/phosphorus-and-farming/{slug}/"

    other_lang_url = (hreflang_ja if lang == "en" else hreflang_en)
    other_lang_label = "日本語" if lang == "en" else "EN"
    has_other = (md_path.parent / ("ja.md" if lang == "en" else "en.md")).exists()

    from build.images import resolve_og_image
    og_image = resolve_og_image(meta, out_dir, public_base_url=canonical_url.rstrip("/"))

    date_str = meta.get("date", "")
    year = date_str.split(".")[0] if "." in date_str else (date_str[:4] if date_str else "")

    variables = {
        "title": meta.get("title", ""),
        "title_html": meta.get("title_html", ""),
        "subtitle": meta.get("subtitle", ""),
        "description": meta.get("description", ""),
        "date": date_str,
        "year": year,
        "number": meta.get("number", "").strip('"'),
        "label": meta.get("label", ""),
        "series": series_name,
        "series_index_url": series_index_url,
        "chapter_label": _farming_chapter_label(meta.get("number", "").strip('"'), lang),
        "content_html": body_html,
        "canonical_url": canonical_url,
        "hreflang_ja": hreflang_ja if (md_path.parent / "ja.md").exists() else "",
        "hreflang_en": hreflang_en if (md_path.parent / "en.md").exists() else "",
        "og_image": og_image,
        "other_lang_url": other_lang_url if has_other else "",
        "other_lang_label": other_lang_label,
    }

    template_text = _farming_template_path(lang).read_text(encoding="utf-8")
    html = Template(template_text).render(**variables)

    out_file = out_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")

    copy_images(md_path.parent, out_dir, lang=lang)

    print(f"Built phosphorus-and-farming: {out_file}")
    return True


def collect_farming_chapters(lang="ja"):
    """Collect phosphorus-and-farming chapter metadata for a language."""
    chapters = []
    for f in _iter_article_files(config.FARMING_DIR, lang):
        text = f.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        if meta.get("lang", "ja") != lang and not (lang == "ja" and "lang" not in meta):
            continue
        num_match = re.match(r"(\d+)", f.parent.name)
        meta["_file_number"] = int(num_match.group(1)) if num_match else 0
        chapters.append(meta)
    chapters.sort(key=lambda m: m.get("_file_number", 0))
    return chapters


def build_farming_index(lang="ja"):
    """Build the phosphorus-and-farming TOC page using the shared index.html template."""
    from build.template_vars import farming_index_vars

    chapters = collect_farming_chapters(lang)
    if not chapters:
        return False

    is_en = lang == "en"
    farming_base = "/en/phosphorus-and-farming" if is_en else "/phosphorus-and-farming"
    has_translation = bool(collect_farming_chapters("en" if not is_en else "ja"))

    chapter_list = ""
    for c in chapters:
        slug = c.get("slug", "")
        number = c.get("number", "").strip('"')
        title = c.get("title", "")
        subtitle = c.get("subtitle", "")
        description = c.get("description", "")
        chapter_list += f'''
                <a href="{farming_base}/{slug}/" style="text-decoration: none; color: inherit;">
                    <div class="activity-item fade-in">
                        <div class="activity-number">{number}</div>
                        <div class="activity-content">
                            <h3>{title}{(" — " + subtitle) if subtitle else ""}</h3>
                            <p>{description}</p>
                        </div>
                    </div>
                </a>
'''

    variables = farming_index_vars(lang, chapter_list, has_translation=has_translation)
    html = render("index.html", variables)

    if is_en:
        out_file = config.SITE_ROOT / "html" / "en" / "phosphorus-and-farming" / "index.html"
    else:
        out_file = config.FARMING_OUTPUT_BASE / "index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"Built phosphorus-and-farming index: {out_file}")
    return True


# ---------------------------------------------------------------------------
# Build functions — ai-native-ways examples (per-chapter "example-N" pages)
#
# Source:  articles/ai-native-ways/NN-slug/example-N/{README.md, results.md, ...}
# Output:  html/ai-native-ways/<slug>/example-N/index.html
#
# Each example folder is rendered as a stand-alone technical doc page using
# template-example.html. README.md and results.md (if present) are concatenated
# as the page body. Source files (Makefile, *.py, etc.) are copied alongside as
# downloadable raw assets, and a "files in this example" section lists them.
# ---------------------------------------------------------------------------

# Files to copy into the html output dir as downloadable assets.
_EXAMPLE_INCLUDE_EXT = {
    ".py", ".sh", ".mk", ".css", ".js", ".html", ".md", ".mmd",
    ".json", ".yaml", ".yml", ".csv", ".tsv", ".txt", ".toml",
    ".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp",
    ".pdf", ".epub", ".docx", ".xlsx", ".log",
}
_EXAMPLE_INCLUDE_NAMES = {"Makefile", "Dockerfile", "Procfile", "requirements.txt"}
_EXAMPLE_SKIP_NAMES = {".stamp", ".gitignore", ".DS_Store"}
_EXAMPLE_SKIP_DIRS = {"__pycache__", ".venv", "node_modules", ".git"}


def _iter_example_files(example_dir):
    """Yield (Path, rel_path) for every file in example_dir (recursive) that
    should be copied into the published html output."""
    base = Path(example_dir)
    for p in sorted(base.rglob("*")):
        if any(part in _EXAMPLE_SKIP_DIRS for part in p.parts):
            continue
        if not p.is_file():
            continue
        if p.name in _EXAMPLE_SKIP_NAMES:
            continue
        if p.name in _EXAMPLE_INCLUDE_NAMES:
            yield p, p.relative_to(base)
            continue
        if p.suffix.lower() in _EXAMPLE_INCLUDE_EXT:
            yield p, p.relative_to(base)


def _humanize_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n / 1024 / 1024:.2f} MB"


def _example_files_html(example_dir):
    """Render the 'files in this example' section. Groups by top-level folder
    so out/, src/, docx/ etc. read cleanly."""
    files = list(_iter_example_files(example_dir))
    if not files:
        return ""

    groups = {}
    for src, rel in files:
        parts = rel.parts
        head = "" if len(parts) == 1 else parts[0]
        groups.setdefault(head, []).append((src, rel))

    parts_html = []
    group_order = sorted(groups.keys(), key=lambda k: (k == "", k))
    for head in group_order:
        if head:
            parts_html.append(f'<h3>{head}/</h3>')
        items = []
        for src, rel in groups[head]:
            href = "/".join(rel.parts)
            display = "/".join(rel.parts)
            size = _humanize_size(src.stat().st_size)
            items.append(
                f'<li><span class="filename"><a href="{href}">{display}</a></span>'
                f'<span class="filesize">{size}</span></li>'
            )
        parts_html.append("<ul>" + "".join(items) + "</ul>")
    return "\n".join(parts_html)


def _example_label(folder_name: str, lang: str) -> str:
    """'example-1' → '実例 1' / 'Example 1'."""
    m = re.match(r"example-(\d+)", folder_name)
    n = m.group(1) if m else folder_name
    return f"実例 {n}" if lang == "ja" else f"Example {n}"


def _example_chapter_meta(example_dir):
    """Read frontmatter from the parent chapter's ja.md (and en.md if exists)."""
    chapter_dir = Path(example_dir).parent
    meta_by_lang = {}
    for lang in ("ja", "en"):
        f = chapter_dir / f"{lang}.md"
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        if "lang" not in meta and lang == "en":
            meta["lang"] = "en"
        meta_by_lang[lang] = meta
    return meta_by_lang


def build_aiways_example(example_dir, lang="ja"):
    """Build a single example page at /ai-native-ways/<chapter-slug>/<example-N>/."""
    from jinja2 import Template

    example_dir = Path(example_dir)
    if not example_dir.is_dir():
        return False

    chapter_meta = _example_chapter_meta(example_dir)
    meta = chapter_meta.get(lang)
    if meta is None:
        return False

    # Pick README/results: language-specific variants if present, otherwise
    # fall back to the JA originals (no EN translation yet for examples — the
    # EN page links back to the same source folder so the artifacts are still
    # accessible).
    readme_lang = example_dir / f"README.{lang}.md"
    results_lang = example_dir / f"results.{lang}.md"
    readme = readme_lang if readme_lang.exists() else (example_dir / "README.md")
    results = results_lang if results_lang.exists() else (example_dir / "results.md")

    # If we are building EN but only JA content exists, skip EN — the EN chapter
    # page will link to the JA example URL instead.
    if lang == "en" and not readme_lang.exists():
        return False

    if not readme.exists():
        return False

    body_md = readme.read_text(encoding="utf-8")
    if results.exists():
        body_md = body_md.rstrip() + "\n\n---\n\n" + results.read_text(encoding="utf-8")

    body_md = strip_leading_title(body_md)
    body_md = process_custom_blocks(body_md)
    content_html = md.render(body_md)

    chapter_slug = meta["slug"]
    example_name = example_dir.name  # 'example-1'
    is_en = lang == "en"
    series_index_url = "/en/ai-native-ways/" if is_en else "/ai-native-ways/"
    chapter_url = f"{series_index_url}{chapter_slug}/"

    if is_en:
        out_dir = config.SITE_ROOT / "html" / "en" / "ai-native-ways" / chapter_slug / example_name
    else:
        out_dir = config.AIWAYS_OUTPUT_BASE / chapter_slug / example_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Copy raw asset files alongside index.html.
    for src, rel in _iter_example_files(example_dir):
        dst = out_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            dst.write_bytes(src.read_bytes())

    # Title: pull the first H1 from README.md, else fall back to "実例 N".
    h1_match = re.search(r"^# (.+)$", readme.read_text(encoding="utf-8"), re.MULTILINE)
    example_label = _example_label(example_name, lang)
    if h1_match:
        example_title = h1_match.group(1).strip()
        # Strip leading "実例 N — " / "Example N — " if present, since the label is shown separately.
        example_title = re.sub(r"^(実例\s*\d+|Example\s*\d+)\s*[—\-:：]\s*", "", example_title)
    else:
        example_title = example_label

    chapter_title = meta.get("title", "")
    chapter_label = _aiways_chapter_label(meta.get("number", "").strip('"'), lang)
    series_name = AIWAYS_SERIES_NAME_EN if is_en else AIWAYS_SERIES_NAME_JA

    canonical_url = (
        f"{config.SITE_URL}/{'en/' if is_en else ''}"
        f"ai-native-ways/{chapter_slug}/{example_name}/"
    )

    files_html = _example_files_html(example_dir)
    files_heading = "ファイル一覧" if not is_en else "Files"
    back_label = (
        f"{chapter_label}「{chapter_title}」に戻る"
        if not is_en
        else f"Back to {chapter_label}: {chapter_title}"
    )

    variables = {
        "lang": lang,
        "example_title": example_title,
        "example_label": example_label,
        "subtitle": "",
        "description": (
            f"{chapter_title} の {example_label}: 実行可能なソースと実測結果。"
            if not is_en
            else f"{example_label} for {chapter_title}: runnable source and measured results."
        ),
        "canonical_url": canonical_url,
        "og_image": f"{config.SITE_URL}/aiseed-og-default.png",
        "series": series_name,
        "series_index_url": series_index_url,
        "chapter_label": chapter_label,
        "chapter_title": chapter_title,
        "chapter_url": chapter_url,
        "content_html": content_html,
        "files_html": files_html,
        "files_heading": files_heading,
        "back_label": back_label,
    }

    tpl_path = config.AIWAYS_DIR / "template-example.html"
    template_text = tpl_path.read_text(encoding="utf-8")
    html = Template(template_text).render(**variables)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"Built ai-native-ways example: {out_dir / 'index.html'}")
    return True


def collect_aiways_examples(chapter_dir):
    """Yield example-N/ subfolders of a chapter, sorted by N."""
    if not Path(chapter_dir).is_dir():
        return
    for sub in sorted(Path(chapter_dir).iterdir()):
        if sub.is_dir() and re.match(r"example-\d+$", sub.name):
            yield sub


def collect_aiways_chapters(lang="ja"):
    """Collect ai-native-ways chapter metadata for a language."""
    chapters = []
    for f in _iter_article_files(config.AIWAYS_DIR, lang):
        text = f.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        if meta.get("lang", "ja") != lang and not (lang == "ja" and "lang" not in meta):
            continue
        num_match = re.match(r"(\d+)", f.parent.name)
        meta["_file_number"] = int(num_match.group(1)) if num_match else 0
        chapters.append(meta)
    chapters.sort(key=lambda m: m.get("_file_number", 0))
    return chapters


def build_aiways_index(lang="ja"):
    """Build the ai-native-ways table-of-contents page using the shared
    index.html template (matches the look of the insights / claude-debian
    series indexes, while individual chapters keep their custom typography)."""
    chapters = collect_aiways_chapters(lang)
    if not chapters:
        return False

    is_en = lang == "en"
    aiways_base = "/en/ai-native-ways" if is_en else "/ai-native-ways"
    has_translation = bool(collect_aiways_chapters("en" if not is_en else "ja"))

    chapter_list = ""
    for c in chapters:
        slug = c.get("slug", "")
        number = c.get("number", "").strip('"')
        title = c.get("title", "")
        subtitle = c.get("subtitle", "")
        description = c.get("description", "")
        chapter_list += f'''
                <a href="{aiways_base}/{slug}/" style="text-decoration: none; color: inherit;">
                    <div class="activity-item fade-in">
                        <div class="activity-number">{number}</div>
                        <div class="activity-content">
                            <h3>{title}{(" — " + subtitle) if subtitle else ""}</h3>
                            <p>{description}</p>
                        </div>
                    </div>
                </a>
'''

    variables = aiways_index_vars(lang, chapter_list, has_translation=has_translation)
    html = render("index.html", variables)

    if is_en:
        out_file = config.SITE_ROOT / "html" / "en" / "ai-native-ways" / "index.html"
    else:
        out_file = config.AIWAYS_OUTPUT_BASE / "index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"Built ai-native-ways index: {out_file}")
    return True


# ---------------------------------------------------------------------------
# Static pages: cache-bust style.css / main.js references
# ---------------------------------------------------------------------------

STATIC_PAGES_FOR_ASSETS = [
    "index.html",
    "en/index.html",
    "about/index.html",
    "en/about/index.html",
    "natural-farming/index.html",
    "en/natural-farming/index.html",
    "light-farming/index.html",
    "en/light-farming/index.html",
    "privacy/index.html",
    "en/privacy/index.html",
]

_CSS_REF_RE = re.compile(r'(href="[^"]*style\.css)(?:\?v=[^"]*)?(")')
_JS_REF_RE = re.compile(r'(src="[^"]*main\.js)(?:\?v=[^"]*)?(")')


def update_static_page_asset_versions():
    """Stamp the current asset version onto style.css / main.js references
    in hand-edited top-level pages. Without this, browsers keep serving the
    cached CSS/JS after a deploy until the file expires."""
    version = config.asset_version()
    replacement_css = rf'\1?v={version}\2'
    replacement_js = rf'\1?v={version}\2'
    html_root = config.SITE_ROOT / "html"
    updated = 0
    for rel in STATIC_PAGES_FOR_ASSETS:
        f = html_root / rel
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        new_text = _CSS_REF_RE.sub(replacement_css, text)
        new_text = _JS_REF_RE.sub(replacement_js, new_text)
        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            updated += 1
    if updated:
        print(f"Stamped asset version {version} onto {updated} static pages")


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
    ja_chapters = collect_book_chapters("ja")
    en_chapters = collect_book_chapters("en")
    ja_aiways = collect_aiways_chapters("ja")
    en_aiways = collect_aiways_chapters("en")
    ja_farming = collect_farming_chapters("ja")
    en_farming = collect_farming_chapters("en")

    all_dates = [
        norm_date(m.get("date"))
        for m in (*ja_articles, *en_articles, *ja_posts, *en_posts,
                  *ja_chapters, *en_chapters, *ja_aiways, *en_aiways,
                  *ja_farming, *en_farming)
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

    # Book: Claudeと一緒に学ぶDebian / Learning Debian with Claude
    if ja_chapters:
        urls.append((f"{site_url}/claude-debian/", latest, "0.8"))
        for meta in ja_chapters:
            slug = meta.get("slug", "")
            if not slug:
                continue
            stem = _book_stem(slug)
            urls.append((f"{site_url}/claude-debian/{stem}/", norm_date(meta.get("date")), "0.6"))
    if en_chapters:
        urls.append((f"{site_url}/en/claude-debian/", latest, "0.7"))
        for meta in en_chapters:
            slug = meta.get("slug", "")
            if not slug:
                continue
            stem = _book_stem(slug)
            urls.append((f"{site_url}/en/claude-debian/{stem}/", norm_date(meta.get("date")), "0.5"))

    # AI-Native Ways of Working
    if ja_aiways:
        urls.append((f"{site_url}/ai-native-ways/", latest, "0.8"))
        for meta in ja_aiways:
            slug = meta.get("slug", "")
            if not slug:
                continue
            urls.append((f"{site_url}/ai-native-ways/{slug}/", norm_date(meta.get("date")), "0.6"))
    if en_aiways:
        urls.append((f"{site_url}/en/ai-native-ways/", latest, "0.7"))
        for meta in en_aiways:
            slug = meta.get("slug", "")
            if not slug:
                continue
            urls.append((f"{site_url}/en/ai-native-ways/{slug}/", norm_date(meta.get("date")), "0.5"))

    # Natural Farming landing page (static)
    urls.append((f"{site_url}/natural-farming/", latest, "0.8"))
    urls.append((f"{site_url}/en/natural-farming/", latest, "0.7"))
    # Phosphorus and Natural Farming series chapters
    if ja_farming:
        urls.append((f"{site_url}/phosphorus-and-farming/", latest, "0.8"))
    if en_farming:
        urls.append((f"{site_url}/en/phosphorus-and-farming/", latest, "0.7"))
    for meta in ja_farming:
        slug = meta.get("slug", "")
        if not slug:
            continue
        urls.append((f"{site_url}/phosphorus-and-farming/{slug}/", norm_date(meta.get("date")), "0.6"))
    for meta in en_farming:
        slug = meta.get("slug", "")
        if not slug:
            continue
        urls.append((f"{site_url}/en/phosphorus-and-farming/{slug}/", norm_date(meta.get("date")), "0.5"))
    urls.append((f"{site_url}/about/", latest, "0.6"))
    urls.append((f"{site_url}/en/about/", latest, "0.5"))
    urls.append((f"{site_url}/light-farming/", latest, "0.8"))
    urls.append((f"{site_url}/en/light-farming/", latest, "0.7"))
    urls.append((f"{site_url}/privacy/", latest, "0.3"))
    urls.append((f"{site_url}/en/privacy/", latest, "0.2"))

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

    is_blog = md_path.parent.parent.name == "blog"
    is_en = (meta.get("lang") or _detect_lang(md_path)) == "en"
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
        for f in list(_iter_article_files(config.INSIGHTS_DIR, "ja")):
            meta, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
            num = meta.get("number", "??")
            title = meta.get("title", "untitled")
            print(f"  [{num}] {f.parent.name}/ja.md → {title}")
        return

    if arg == "--all":
        files = list(_iter_article_files(config.INSIGHTS_DIR, "ja")) \
              + list(_iter_article_files(config.INSIGHTS_DIR, "en"))
        if not files:
            print(f"No articles found in {config.INSIGHTS_DIR}")
            return
        ok = 0
        for f in files:
            if build_article(f):
                ok += 1
        build_index("ja")
        build_index("en")

        # Build blog posts
        blog_ok = 0
        blog_files = list(_iter_article_files(config.BLOG_DIR, "ja")) \
                   + list(_iter_article_files(config.BLOG_DIR, "en"))
        for f in blog_files:
            if build_blog_post(f):
                blog_ok += 1
        if blog_files:
            build_blog_index("ja")
            build_blog_index("en")
            update_home_latest_posts("ja")
            update_home_latest_posts("en")

        # Build book chapters (claude-debian) — JA + EN
        book_ok = 0
        book_files = list(_iter_article_files(config.BOOK_DIR, "ja")) \
                   + list(_iter_article_files(config.BOOK_DIR, "en"))
        for f in book_files:
            if build_book_chapter(f):
                book_ok += 1
        if collect_book_chapters("ja"):
            build_book_index("ja")
        if collect_book_chapters("en"):
            build_book_index("en")

        # Build ai-native-ways essays — JA + EN
        aiways_ok = 0
        aiways_files = list(_iter_article_files(config.AIWAYS_DIR, "ja")) \
                     + list(_iter_article_files(config.AIWAYS_DIR, "en"))
        for f in aiways_files:
            if build_aiways_chapter(f):
                aiways_ok += 1
        if collect_aiways_chapters("ja"):
            build_aiways_index("ja")
        if collect_aiways_chapters("en"):
            build_aiways_index("en")

        # Build phosphorus-and-farming chapters — JA + EN
        farming_ok = 0
        farming_files = list(_iter_article_files(config.FARMING_DIR, "ja")) \
                      + list(_iter_article_files(config.FARMING_DIR, "en"))
        for f in farming_files:
            if build_farming_chapter(f):
                farming_ok += 1
        if collect_farming_chapters("ja"):
            build_farming_index("ja")
        if collect_farming_chapters("en"):
            build_farming_index("en")

        # Build ai-native-ways examples — every chapter's example-N/ folders.
        examples_ok = examples_total = 0
        for chapter_sub in sorted(config.AIWAYS_DIR.iterdir()):
            if not chapter_sub.is_dir() or not chapter_sub.name[:1].isdigit():
                continue
            for ex in collect_aiways_examples(chapter_sub):
                for ex_lang in ("ja", "en"):
                    if not (chapter_sub / f"{ex_lang}.md").exists():
                        continue
                    examples_total += 1
                    if build_aiways_example(ex, ex_lang):
                        examples_ok += 1

        update_static_page_asset_versions()
        build_sitemap()
        build_robots()
        print(
            f"\nBuilt {ok}/{len(files)} articles + {blog_ok}/{len(blog_files)} blog posts"
            f" + {book_ok}/{len(book_files)} book chapters"
            f" + {aiways_ok}/{len(aiways_files)} ai-native-ways"
            f" + {examples_ok}/{examples_total} ai-native-ways examples"
            f" + {farming_ok}/{len(farming_files)} phosphorus-and-farming chapters"
            f" + indexes + sitemap.xml + robots.txt."
        )
        return

    # Auto-detect book / blog / aiways / article from the path. Per-folder
    # layout means the series name is the grandparent dir of
    # `<series>/<NN-slug>/<lang>.md`.
    p = Path(arg).resolve()
    series = p.parent.parent.name if p.is_file() else ""
    if series == "claude-debian" or "claude-debian/" in arg:
        build_book_chapter(arg)
    elif series == "blog" or "/blog/" in arg or arg.startswith("blog/"):
        build_blog_post(arg)
    elif series == "ai-native-ways" or "ai-native-ways/" in arg:
        build_aiways_chapter(arg)
    elif series == "phosphorus-and-farming" or "phosphorus-and-farming/" in arg:
        build_farming_chapter(arg)
    else:
        build_article(arg)


if __name__ == "__main__":
    main()
