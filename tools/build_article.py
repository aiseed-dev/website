#!/usr/bin/env python3
"""
Markdown → HTML article/blog builder for aiseed.dev

Usage:
    python3 tools/build_article.py articles/09-healthcare-fiscal.md
    python3 tools/build_article.py blog/001-grid-attack-naphtha.md
    python3 tools/build_article.py --all          # Build all articles + blog
    python3 tools/build_article.py --list         # List available articles

Dependencies: jinja2, markdown-it-py
Templates are in tools/templates/:
    article.html  — single article/blog page (Jinja2)
    index.html    — insights/blog index page (Jinja2)
"""

import sys
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt


SITE_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = SITE_ROOT / "articles"
BLOG_DIR = SITE_ROOT / "blog"
OUTPUT_BASE = SITE_ROOT / "html" / "insights"
BLOG_OUTPUT_BASE = SITE_ROOT / "html" / "blog"
TEMPLATES_DIR = Path(__file__).parent / "templates"
SITE_URL = "https://aiseed.dev"

# Jinja2 environment
_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=False,
    keep_trailing_newline=True,
)

# markdown-it renderer (CommonMark + tables)
_md = MarkdownIt("commonmark", {"html": True}).enable("table")


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

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
        html = _md.render(content)
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
                html += f"  <th>{c}</th>\n"
            html += "</tr>\n"
        elif line.startswith("--") or line.startswith("|-"):
            continue
        else:
            html += "<tr>\n"
            for c in cells:
                html += f"  <td>{c}</td>\n"
            html += "</tr>\n"
    html += "</table>"
    return html


# ---------------------------------------------------------------------------
# Localization helpers
# ---------------------------------------------------------------------------

def _text(is_en, en, ja):
    """Return English or Japanese text."""
    return en if is_en else ja


def _nl_to_br(text):
    """Convert newlines to <br> for HTML inline blocks."""
    return text.replace("\n", "<br>\n                    ")


# ---------------------------------------------------------------------------
# Template variable builders
# ---------------------------------------------------------------------------

def article_vars(meta, body_html):
    """Build template variables for article pages."""
    lang = meta.get("lang", "ja")
    is_en = lang == "en"
    number = meta.get("number", "")
    prev_slug = meta.get("prev_slug", "")
    prev_title = meta.get("prev_title", "")
    next_slug = meta.get("next_slug", "")
    next_title = meta.get("next_title", "")

    slug = meta.get("slug", "")
    insights_base = "/en/insights" if is_en else "/insights"
    prev_prefix = "Prev: " if is_en else "前: "
    next_prefix = "Next: " if is_en else "次: "
    insights_top = "Insights Top" if is_en else "Insights トップ"

    # Article navigation HTML
    nav_html = '<div class="article-nav">\n'
    if prev_slug:
        nav_html += f'  <a href="{insights_base}/{prev_slug}/">&larr; {prev_prefix}{prev_title}</a>\n'
    else:
        nav_html += '  <span></span>\n'
    if next_slug:
        nav_html += f'  <a href="{insights_base}/{next_slug}/">{next_prefix}{next_title} &rarr;</a>\n'
    else:
        nav_html += f'  <a href="{insights_base}/">{insights_top} &rarr;</a>\n'
    nav_html += '</div>'

    return {
        "lang": lang,
        "title": meta.get("title", ""),
        "subtitle": meta.get("subtitle", ""),
        "description": meta.get("description", ""),
        "date": meta.get("date", ""),
        "number": number,
        "label": meta.get("label", f"Structural Analysis {number}"),
        "body_html": body_html,
        "nav_html": nav_html,
        # CTA
        "cta_label": meta.get("cta_label", "Back to Soil"),
        "cta_title": meta.get("cta_title", _text(is_en,
            "See the Structure", "構造を見る")),
        "cta_text": meta.get("cta_text", _text(is_en,
            "From AI to agriculture — every structural analysis converges on one conclusion.",
            "AIから農業まで——全ての構造分析は、一つの結論に向かう。")),
        "cta_btn1_text": meta.get("cta_btn1_text", _text(is_en, "Natural Farming", "自然農法とは")),
        "cta_btn1_link": meta.get("cta_btn1_link", "/about/"),
        "cta_btn2_text": meta.get("cta_btn2_text", "Light Farming"),
        "cta_btn2_link": meta.get("cta_btn2_link", "/light-farming/"),
        # Paths
        "css_path": "../../../css/style.css" if is_en else "../../css/style.css",
        "js_path": "../../../js/main.js" if is_en else "../../js/main.js",
        "img_path": "../../../images/IMG_3285.jpg" if is_en else "../../images/IMG_3285.jpg",
        "insights_base": insights_base,
        "blog_base": "/en/blog" if is_en else "/blog",
        # Navigation labels
        "site_name": _text(is_en, "Living in the AI Era", "AI時代の暮らし"),
        "site_tagline": _text(is_en, "aiseed.dev", "aiseed.dev"),
        "home_label": _text(is_en, "Home", "ホーム"),
        "about_label": _text(is_en, "Natural Farming", "自然農法とは"),
        "lf_label": "Light Farming",
        "gallery_label": _text(is_en, "Field Notes", "畑の記録"),
        "insights_label": "Insights",
        "contact_label": _text(is_en, "Contact", "お問い合わせ"),
        "menu_label": _text(is_en, "Menu", "メニュー"),
        "pages_label": _text(is_en, "Pages", "ページ"),
        "links_label": _text(is_en, "Links", "関連リンク"),
        "series_label": _text(is_en,
            f"Structural Analysis Series {number}",
            f"構造分析シリーズ {number}"),
        "vegitage_label": _text(is_en, "Natural Farming Community", "自然農法コミュニティ"),
        "footer_about": _text(is_en,
            "AI changes how we work, farm, and live. Structural analysis of fossil resources, "
            "food, energy, AI, healthcare, and pensions — every structure connects.",
            "AIが仕事、農業、暮らしを変える。化石資源、食料、エネルギー、AI、医療、年金——全ての構造は一つに繋がっている。"),
        # SEO
        "canonical_url": f"{SITE_URL}{insights_base}/{slug}/",
        "hreflang_ja": f"{SITE_URL}/insights/{slug}/",
        "hreflang_en": f"{SITE_URL}/en/insights/{slug}/",
        "og_locale": "en_US" if is_en else "ja_JP",
    }


def index_vars(lang, article_list_html):
    """Build template variables for index pages."""
    is_en = lang == "en"
    insights_base = "/en/insights" if is_en else "/insights"

    intro_text = _text(is_en,
        "AI is changing everything — how we work, how we farm, how we live.\n"
        "But the real question is: what structures remain when the hype fades?\n"
        "Fossil resources, food, energy, AI, healthcare, pensions.\n"
        "Follow the structure, and the answer is always the same.",

        "AIが全てを変える——仕事、農業、暮らし。\n"
        "しかし本当の問いは、バブルが消えた後に何が残るか。\n"
        "化石資源、食料、エネルギー、AI、医療、年金。\n"
        "構造を追跡すれば、答えは同じ場所に収束する。"
    )

    method_text = _text(is_en,
        "Trace the production route. Observe the physical process. Cross field boundaries.\n"
        "Agriculture, energy, finance, AI, defense — the structure connects to one conclusion.",

        "生産ルートを追跡する。物理的プロセスを見る。分野の境界を越える。\n"
        "農業も、エネルギーも、金融も、AIも——構造は一つにつながっている。"
    )

    quote_text = _text(is_en,
        "AI replaces desk work. Natural farming replaces chemical agriculture.<br>\n"
        "The further we move from nature, the higher the cost of living becomes.<br>\n"
        "Structure doesn't lie.",

        "AIがデスクワークを代替する。自然農法が化学農業を代替する。<br>\n"
        "自然から離れるほど、生きるコストは上がる。<br>\n"
        "構造は嘘をつかない。"
    )

    cta_text = _text(is_en,
        "From AI to agriculture, from energy to pensions —<br>\n"
        "understanding the structure changes how you see everything.",

        "AIから農業まで、エネルギーから年金まで——<br>\n"
        "構造を理解すれば見え方が変わる。"
    )

    return {
        "lang": lang,
        "site_name": _text(is_en, "Living in the AI Era", "AI時代の暮らし"),
        "home_label": _text(is_en, "Home", "ホーム"),
        "about_label": _text(is_en, "Natural Farming", "自然農法とは"),
        "gallery_label": _text(is_en, "Field Notes", "畑の記録"),
        "contact_label": _text(is_en, "Contact", "お問い合わせ"),
        "menu_label": _text(is_en, "Menu", "メニュー"),
        "pages_label": _text(is_en, "Pages", "ページ"),
        "links_label": _text(is_en, "Links", "関連リンク"),
        "insights_base": insights_base,
        "blog_base": "/en/blog" if is_en else "/blog",
        "css_path": "../../css/style.css" if is_en else "../css/style.css",
        "js_path": "../../js/main.js" if is_en else "../js/main.js",
        "img_path": "../../images/IMG_3285.jpg" if is_en else "../images/IMG_3285.jpg",
        "meta_description": intro_text.split("\n")[0],
        "structural_analysis_label": _text(is_en, "Structural Analysis", "構造分析"),
        "page_title": _text(is_en, "Insights", "Insights — 構造分析"),
        "page_subtitle": _text(is_en,
            "With nature, we can live — the structural evidence",
            "自然とともにあれば、生きられる——その構造的根拠"),
        "other_lang_link": "/insights/" if is_en else "/en/insights/",
        "other_lang_text": _text(is_en, "日本語版はこちら →", "English version available →"),
        "series_title": _text(is_en, "Structural Analysis Series", "構造分析シリーズ"),
        "series_description": _text(is_en,
            "All using the same methodology: trace the production route, observe the physical process, cross field boundaries.",
            "全て同じ方法論。生産ルートを追跡する。物理的プロセスを見る。分野の境界を越える。"),
        "article_list_html": article_list_html,
        "intro_html": _nl_to_br(intro_text),
        "method_title": _text(is_en, "Methodology:", "方法論："),
        "method_html": _nl_to_br(method_text),
        "quote_html": quote_text,
        "cta_title": _text(is_en, "See the Structure", "構造を見る"),
        "cta_html": cta_text,
        "footer_about": _text(is_en,
            "AI changes how we work, farm, and live. Structural analysis of fossil resources, "
            "food, energy, AI, healthcare, and pensions — every structure connects.",
            "AIが仕事、農業、暮らしを変える。化石資源、食料、エネルギー、AI、医療、年金——全ての構造は一つに繋がっている。"),
        "copyright_text": _text(is_en, "Living in the AI Era — aiseed.dev", "AI時代の暮らし"),
        # SEO
        "canonical_url": f"{SITE_URL}{insights_base}/",
        "hreflang_ja": f"{SITE_URL}/insights/",
        "hreflang_en": f"{SITE_URL}/en/insights/",
        "og_locale": "en_US" if is_en else "ja_JP",
    }


# ---------------------------------------------------------------------------
# Blog template variable builders
# ---------------------------------------------------------------------------

def blog_vars(meta, body_html):
    """Build template variables for blog post pages."""
    lang = meta.get("lang", "ja")
    is_en = lang == "en"
    slug = meta.get("slug", "")
    blog_base = "/en/blog" if is_en else "/blog"

    # Blog navigation — just link back to blog index
    blog_top = "Blog Top" if is_en else "Blog トップ"
    nav_html = '<div class="article-nav">\n'
    nav_html += '  <span></span>\n'
    nav_html += f'  <a href="{blog_base}/">{blog_top} &rarr;</a>\n'
    nav_html += '</div>'

    category = meta.get("category", _text(is_en, "Blog", "ブログ"))

    return {
        "lang": lang,
        "title": meta.get("title", ""),
        "subtitle": meta.get("subtitle", ""),
        "description": meta.get("description", ""),
        "date": meta.get("date", ""),
        "number": "",
        "label": meta.get("label", "Blog"),
        "body_html": body_html,
        "nav_html": nav_html,
        # CTA
        "cta_label": "Blog",
        "cta_title": _text(is_en, "See the Structure", "構造を見る"),
        "cta_text": _text(is_en,
            "From AI to agriculture — every structural analysis converges on one conclusion.",
            "AIから農業まで——全ての構造分析は、一つの結論に向かう。"),
        "cta_btn1_text": _text(is_en, "Insights", "構造分析シリーズ"),
        "cta_btn1_link": "/en/insights/" if is_en else "/insights/",
        "cta_btn2_text": "Blog",
        "cta_btn2_link": blog_base + "/",
        # Paths
        "css_path": "../../../css/style.css" if is_en else "../../css/style.css",
        "js_path": "../../../js/main.js" if is_en else "../../js/main.js",
        "img_path": "../../../images/IMG_3285.jpg" if is_en else "../../images/IMG_3285.jpg",
        "insights_base": "/en/insights" if is_en else "/insights",
        "blog_base": "/en/blog" if is_en else "/blog",
        # Navigation labels
        "site_name": _text(is_en, "Living in the AI Era", "AI時代の暮らし"),
        "site_tagline": _text(is_en, "aiseed.dev", "aiseed.dev"),
        "home_label": _text(is_en, "Home", "ホーム"),
        "about_label": _text(is_en, "Natural Farming", "自然農法とは"),
        "lf_label": "Light Farming",
        "gallery_label": _text(is_en, "Field Notes", "畑の記録"),
        "insights_label": "Insights",
        "contact_label": _text(is_en, "Contact", "お問い合わせ"),
        "menu_label": _text(is_en, "Menu", "メニュー"),
        "pages_label": _text(is_en, "Pages", "ページ"),
        "links_label": _text(is_en, "Links", "関連リンク"),
        "series_label": category,
        "vegitage_label": _text(is_en, "Natural Farming Community", "自然農法コミュニティ"),
        "footer_about": _text(is_en,
            "AI changes how we work, farm, and live. Structural analysis of fossil resources, "
            "food, energy, AI, healthcare, and pensions — every structure connects.",
            "AIが仕事、農業、暮らしを変える。化石資源、食料、エネルギー、AI、医療、年金——全ての構造は一つに繋がっている。"),
        # SEO
        "canonical_url": f"{SITE_URL}{blog_base}/{slug}/",
        "hreflang_ja": f"{SITE_URL}/blog/{slug}/",
        "hreflang_en": f"{SITE_URL}/en/blog/{slug}/",
        "og_locale": "en_US" if is_en else "ja_JP",
    }


def blog_index_vars(lang, post_list_html):
    """Build template variables for blog index pages."""
    is_en = lang == "en"
    blog_base = "/en/blog" if is_en else "/blog"

    intro_text = _text(is_en,
        "Quick analysis notes on current events — connecting the dots with structural analysis.",
        "時事ニュースを構造分析の視点で読む。速報ノート。")

    return {
        "lang": lang,
        "site_name": _text(is_en, "Living in the AI Era", "AI時代の暮らし"),
        "home_label": _text(is_en, "Home", "ホーム"),
        "about_label": _text(is_en, "Natural Farming", "自然農法とは"),
        "gallery_label": _text(is_en, "Field Notes", "畑の記録"),
        "menu_label": _text(is_en, "Menu", "メニュー"),
        "pages_label": _text(is_en, "Pages", "ページ"),
        "links_label": _text(is_en, "Links", "関連リンク"),
        "insights_base": "/en/insights" if is_en else "/insights",
        "blog_base": "/en/blog" if is_en else "/blog",
        "css_path": "../../css/style.css" if is_en else "../css/style.css",
        "js_path": "../../js/main.js" if is_en else "../js/main.js",
        "img_path": "../../images/IMG_3285.jpg" if is_en else "../images/IMG_3285.jpg",
        "meta_description": intro_text,
        "structural_analysis_label": "Blog",
        "page_title": "Blog",
        "page_subtitle": _text(is_en,
            "Current events through the lens of structural analysis",
            "構造分析の視点で読む時事ノート"),
        "other_lang_link": "/blog/" if is_en else "/en/blog/",
        "other_lang_text": _text(is_en, "日本語版はこちら →", "English version available →"),
        "series_title": "Blog",
        "series_description": _text(is_en,
            "Quick analysis notes connecting current events to structural reality.",
            "時事ニュースと構造分析をつなぐ速報ノート。"),
        "article_list_html": post_list_html,
        "intro_html": intro_text,
        "method_title": "",
        "method_html": "",
        "quote_html": _text(is_en,
            "Structure doesn't lie.<br>\nCurrent events prove it, every time.",
            "構造は嘘をつかない。<br>\n時事ニュースが、毎回それを証明する。"),
        "cta_title": _text(is_en, "See the Full Analysis", "構造分析シリーズ"),
        "cta_html": _text(is_en,
            "For the complete structural analysis, see the Insights series.",
            "完全な構造分析は、構造分析シリーズで。"),
        "footer_about": _text(is_en,
            "AI changes how we work, farm, and live. Structural analysis of fossil resources, "
            "food, energy, AI, healthcare, and pensions — every structure connects.",
            "AIが仕事、農業、暮らしを変える。化石資源、食料、エネルギー、AI、医療、年金——全ての構造は一つに繋がっている。"),
        "copyright_text": _text(is_en, "Living in the AI Era — aiseed.dev", "AI時代の暮らし"),
        # SEO
        "canonical_url": f"{SITE_URL}{blog_base}/",
        "hreflang_ja": f"{SITE_URL}/blog/",
        "hreflang_en": f"{SITE_URL}/en/blog/",
        "og_locale": "en_US" if is_en else "ja_JP",
    }


# ---------------------------------------------------------------------------
# Sitemap & robots.txt
# ---------------------------------------------------------------------------

def build_sitemap():
    """Generate sitemap.xml from all articles."""
    from datetime import date
    today = date.today().isoformat()

    urls = []
    # Homepages
    urls.append(("https://aiseed.dev/", today, "1.0"))
    urls.append(("https://aiseed.dev/en/", today, "0.8"))

    # Index pages
    urls.append((f"{SITE_URL}/insights/", today, "0.9"))
    urls.append((f"{SITE_URL}/en/insights/", today, "0.8"))

    # JP articles
    for meta in collect_articles("ja"):
        slug = meta.get("slug", "")
        urls.append((f"{SITE_URL}/insights/{slug}/", today, "0.7"))

    # EN articles
    for meta in collect_articles("en"):
        slug = meta.get("slug", "")
        urls.append((f"{SITE_URL}/en/insights/{slug}/", today, "0.6"))

    # Blog index pages
    urls.append((f"{SITE_URL}/blog/", today, "0.8"))
    urls.append((f"{SITE_URL}/en/blog/", today, "0.7"))

    # JP blog posts
    for meta in collect_blog_posts("ja"):
        slug = meta.get("slug", "")
        urls.append((f"{SITE_URL}/blog/{slug}/", today, "0.7"))

    # EN blog posts
    for meta in collect_blog_posts("en"):
        slug = meta.get("slug", "")
        urls.append((f"{SITE_URL}/en/blog/{slug}/", today, "0.6"))

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for loc, lastmod, priority in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{loc}</loc>")
        xml_lines.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_lines.append(f"    <priority>{priority}</priority>")
        xml_lines.append("  </url>")
    xml_lines.append("</urlset>")

    out = SITE_ROOT / "html" / "sitemap.xml"
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
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )
    out = SITE_ROOT / "html" / "robots.txt"
    out.write_text(content, encoding="utf-8")
    print(f"Built: {out}")


# ---------------------------------------------------------------------------
# Template rendering (Jinja2)
# ---------------------------------------------------------------------------

def render(template_name, variables):
    """Load a Jinja2 template and render with variables."""
    tpl = _env.get_template(template_name)
    return tpl.render(**variables)


# ---------------------------------------------------------------------------
# Build functions
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

    # Process custom blocks first
    body = process_custom_blocks(body)

    # Convert remaining Markdown to HTML (markdown-it-py, CommonMark)
    body_html = _md.render(body)

    # Indent body HTML for template
    indented = "\n".join(
        f"                {line}" if line.strip() else ""
        for line in body_html.split("\n")
    )

    # Build full HTML
    variables = article_vars(meta, indented)
    html = render("article.html", variables)

    # Write output — English articles go to html/en/insights/slug/
    lang = meta.get("lang", "ja")
    if lang == "en":
        out_dir = SITE_ROOT / "html" / "en" / "insights" / meta["slug"]
    else:
        out_dir = OUTPUT_BASE / meta["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")

    print(f"Built: {out_file}")
    return True


def collect_articles(lang="ja"):
    """Collect and sort article metadata for a given language."""
    prefix = "en-" if lang == "en" else ""
    pattern = f"{prefix}[0-9]*.md"
    articles = []
    for f in sorted(ARTICLES_DIR.glob(pattern)):
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
        out_file = SITE_ROOT / "html" / "en" / "insights" / "index.html"
    else:
        out_file = SITE_ROOT / "html" / "insights" / "index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"Built index: {out_file}")
    return True


# ---------------------------------------------------------------------------
# Blog build functions
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

    body = process_custom_blocks(body)
    body_html = _md.render(body)

    indented = "\n".join(
        f"                {line}" if line.strip() else ""
        for line in body_html.split("\n")
    )

    variables = blog_vars(meta, indented)
    html = render("article.html", variables)

    lang = meta.get("lang", "ja")
    if lang == "en":
        out_dir = SITE_ROOT / "html" / "en" / "blog" / meta["slug"]
    else:
        out_dir = BLOG_OUTPUT_BASE / meta["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")

    print(f"Built blog: {out_file}")
    return True


def collect_blog_posts(lang="ja"):
    """Collect and sort blog post metadata for a given language."""
    if not BLOG_DIR.exists():
        return []
    prefix = "en-" if lang == "en" else ""
    pattern = f"{prefix}[0-9]*.md"
    posts = []
    for f in sorted(BLOG_DIR.glob(pattern)):
        text = f.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        if meta.get("lang", "ja") == lang or (lang == "ja" and "lang" not in meta):
            posts.append(meta)
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
        out_file = SITE_ROOT / "html" / "en" / "blog" / "index.html"
    else:
        out_file = BLOG_OUTPUT_BASE / "index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"Built blog index: {out_file}")
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/build_article.py <article.md>")
        print("       python3 tools/build_article.py --all")
        print("       python3 tools/build_article.py --list")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--list":
        for f in sorted(ARTICLES_DIR.glob("*.md")):
            meta, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
            num = meta.get("number", "??")
            title = meta.get("title", "untitled")
            print(f"  [{num}] {f.name} → {title}")
        return

    if arg == "--all":
        files = sorted(ARTICLES_DIR.glob("*.md"))
        if not files:
            print("No .md files found in articles/")
            return
        ok = 0
        for f in files:
            if build_article(f):
                ok += 1
        build_index("ja")
        build_index("en")

        # Build blog posts
        blog_ok = 0
        blog_files = sorted(BLOG_DIR.glob("*.md")) if BLOG_DIR.exists() else []
        for f in blog_files:
            if build_blog_post(f):
                blog_ok += 1
        if blog_files:
            build_blog_index("ja")
            build_blog_index("en")

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
