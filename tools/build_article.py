#!/usr/bin/env python3
"""
Markdown → HTML article builder for aiseed.dev

Usage:
    python3 tools/build_article.py articles/09-healthcare-fiscal.md
    python3 tools/build_article.py --all          # Build all articles
    python3 tools/build_article.py --list         # List available articles

Dependencies: jinja2, markdown-it-py
Templates are in tools/templates/:
    article.html  — single article page (Jinja2)
    index.html    — insights index page (Jinja2)
"""

import sys
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt


SITE_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = SITE_ROOT / "articles"
OUTPUT_BASE = SITE_ROOT / "html" / "insights"
TEMPLATES_DIR = Path(__file__).parent / "templates"

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
            "With nature, we can live.", "自然とともにあれば、生きられる")),
        "cta_text": meta.get("cta_text", _text(is_en,
            "Every structural analysis converges on one conclusion.",
            "全ての構造分析は、一つの結論に向かう。")),
        "cta_btn1_text": meta.get("cta_btn1_text", _text(is_en, "Natural Farming", "自然農法とは")),
        "cta_btn1_link": meta.get("cta_btn1_link", "/about/"),
        "cta_btn2_text": meta.get("cta_btn2_text", "Light Farming"),
        "cta_btn2_link": meta.get("cta_btn2_link", "/light-farming/"),
        # Paths
        "css_path": "../../../css/style.css" if is_en else "../../css/style.css",
        "js_path": "../../../js/main.js" if is_en else "../../js/main.js",
        "img_path": "../../../images/IMG_3285.jpg" if is_en else "../../images/IMG_3285.jpg",
        "insights_base": insights_base,
        # Navigation labels
        "site_name": _text(is_en, "Living with Nature", "自然と対話する暮らし"),
        "site_tagline": "Natural Farming",
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
            "With nature, we can live. The path shown by Masanobu Fukuoka's natural farming "
            "and the science of Light Farming.",
            "自然とともにあれば、生きられる。福岡正信の自然農法とLight Farmingの科学が示す、生きるための道。"),
    }


def index_vars(lang, article_list_html):
    """Build template variables for index pages."""
    is_en = lang == "en"
    insights_base = "/en/insights" if is_en else "/insights"

    intro_text = _text(is_en,
        "Masanobu Fukuoka's philosophy asks: \"How do we survive?\"\n"
        "Light Farming provides the scientific answer.\n"
        "Every article here converges on one conclusion — the further we move\n"
        "from nature, the higher the cost of living becomes.\n"
        "Agriculture, energy, finance, AI, defense, healthcare.\n"
        "Follow the structure, and the answer is always the same.",

        "福岡正信の思想は「生きるためにどうするか」。\n"
        "Light Farmingはその科学的根拠。\n"
        "全ての記事は一つの結論に向かう——自然から離れるほど、生きるコストは上がる。\n"
        "農業、エネルギー、金融、AI、医療、年金。\n"
        "構造を追跡すれば、答えは同じ場所に収束する。"
    )

    method_text = _text(is_en,
        "Trace the production route. Observe the physical process. Cross field boundaries.\n"
        "Agriculture, energy, finance, AI, defense — the structure connects to one conclusion.",

        "生産ルートを追跡する。物理的プロセスを見る。分野の境界を越える。\n"
        "農業も、エネルギーも、金融も、AIも——構造は一つにつながっている。"
    )

    quote_text = _text(is_en,
        "With nature, we can live.<br>\n"
        "The further we move from nature, the higher the cost of living becomes.<br>\n"
        "Fukuoka and Okada knew this. Dr. Christine Jones proved it.",

        "自然とともにあれば、生きられる。<br>\n"
        "自然から離れるほど、生きるコストは上がる。<br>\n"
        "福岡正信はそれを知っていた。Light Farmingがそれを証明した。"
    )

    cta_text = _text(is_en,
        "The production route of fertilizer, the network of soil microbes —<br>\n"
        "understanding the structure changes how you see everything.",

        "肥料の生産ルートも、土壌微生物のネットワークも、<br>\n"
        "構造を理解すれば見え方が変わる。"
    )

    return {
        "lang": lang,
        "site_name": _text(is_en, "Living with Nature", "自然と対話する暮らし"),
        "home_label": _text(is_en, "Home", "ホーム"),
        "about_label": _text(is_en, "Natural Farming", "自然農法とは"),
        "gallery_label": _text(is_en, "Field Notes", "畑の記録"),
        "contact_label": _text(is_en, "Contact", "お問い合わせ"),
        "menu_label": _text(is_en, "Menu", "メニュー"),
        "pages_label": _text(is_en, "Pages", "ページ"),
        "links_label": _text(is_en, "Links", "関連リンク"),
        "insights_base": insights_base,
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
            "With nature, we can live. The path shown by Masanobu Fukuoka's natural farming "
            "and the science of Light Farming.",
            "自然とともにあれば、生きられる。福岡正信の自然農法とLight Farmingの科学が示す、生きるための道。"),
        "copyright_text": _text(is_en, "Living with Nature — aiseed.dev", "自然と対話する暮らし"),
    }


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
        print(f"\nBuilt {ok}/{len(files)} articles + 2 index pages.")
        return

    build_article(arg)


if __name__ == "__main__":
    main()
