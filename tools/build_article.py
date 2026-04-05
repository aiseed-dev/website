#!/usr/bin/env python3
"""
Markdown → HTML article builder for aiseed.dev

Usage:
    python3 tools/build_article.py articles/09-healthcare-fiscal.md
    python3 tools/build_article.py --all          # Build all articles
    python3 tools/build_article.py --list         # List available articles

Markdown front matter (YAML-like, between --- lines):
    ---
    slug: healthcare-fiscal
    number: "09"
    title: 社会の設計ミス
    subtitle: 年金・医療・農業の構造的崩壊
    description: 透析医療の化石資源依存、社会保険料30%超...
    date: 2025.04.04
    label: Structural Analysis 09
    prev_slug: ai-solo-business
    prev_title: AIと個人事業
    next_slug:
    next_title:
    cta_label: Back to Soil
    cta_title: 自然とともにあれば、生きられる
    cta_text: 全ての構造分析は、一つの結論に向かう。
    cta_btn1_text: 自然農法とは
    cta_btn1_link: /about/
    cta_btn2_text: Light Farming
    cta_btn2_link: /light-farming/
    ---

Custom Markdown extensions:
    :::chain           → <div class="chain-diagram">
    :::highlight       → <div class="highlight-box">
    :::quote           → <div class="quote-block"><p class="quote-text">
    :::compare         → <table class="comparison-table fade-in">
    →                  → <span class="arrow">&rarr;</span>  (in chain blocks)
"""

import sys
import os
import re
import glob
import markdown
from pathlib import Path


SITE_ROOT = Path(__file__).parent.parent
ARTICLES_DIR = SITE_ROOT / "articles"
OUTPUT_BASE = SITE_ROOT / "html" / "insights"


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
            # Remove surrounding quotes
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            meta[key.strip()] = val
    body = parts[2].strip()
    return meta, body


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
        # Replace → with arrow spans
        content = content.replace("→", '<span class="arrow">&rarr;</span>')
        # Convert line breaks to <br>
        content = content.replace("\n\n", "<br><br>")
        content = content.replace("\n", "<br>\n")
        # Bold with **
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        return f'<div class="chain-diagram">\n{content}\n</div>'

    elif block_type == "highlight":
        # Process as mini-markdown
        html = markdown.markdown(content)
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


def build_html(meta, body_html):
    """Assemble full HTML page from template and content."""
    lang = meta.get("lang", "ja")
    is_en = lang == "en"
    slug = meta.get("slug", "article")
    number = meta.get("number", "")
    title = meta.get("title", "")
    subtitle = meta.get("subtitle", "")
    description = meta.get("description", "")
    date = meta.get("date", "")
    label = meta.get("label", f"Structural Analysis {number}")
    prev_slug = meta.get("prev_slug", "")
    prev_title = meta.get("prev_title", "")
    next_slug = meta.get("next_slug", "")
    next_title = meta.get("next_title", "")
    cta_label = meta.get("cta_label", "Back to Soil")
    cta_title = meta.get("cta_title",
                         "With nature, we can live." if is_en else "自然とともにあれば、生きられる")
    cta_text = meta.get("cta_text",
                        "Every structural analysis converges on one conclusion." if is_en
                        else "全ての構造分析は、一つの結論に向かう。")
    cta_btn1_text = meta.get("cta_btn1_text",
                             "Natural Farming" if is_en else "自然農法とは")
    cta_btn1_link = meta.get("cta_btn1_link", "/about/")
    cta_btn2_text = meta.get("cta_btn2_text", "Light Farming")
    cta_btn2_link = meta.get("cta_btn2_link", "/light-farming/")

    # Path prefix for English articles
    insights_base = "/en/insights" if is_en else "/insights"
    css_path = "../../../css/style.css" if is_en else "../../css/style.css"
    js_path = "../../../js/main.js" if is_en else "../../js/main.js"
    img_path = "../../../images/IMG_3285.jpg" if is_en else "../../images/IMG_3285.jpg"

    # Navigation labels
    home_label = "Home" if is_en else "ホーム"
    about_label = "Natural Farming" if is_en else "自然農法とは"
    lf_label = "Light Farming"
    gallery_label = "Field Notes" if is_en else "畑の記録"
    insights_label = "Insights"
    contact_label = "Contact" if is_en else "お問い合わせ"
    prev_prefix = "Prev: " if is_en else "前: "
    next_prefix = "Next: " if is_en else "次: "
    insights_top = "Insights Top" if is_en else "Insights トップ"
    series_label = f"Structural Analysis Series {number}" if is_en else f"構造分析シリーズ {number}"
    site_name = "Living with Nature" if is_en else "自然と対話する暮らし"
    site_tagline = "Natural Farming" if is_en else "Natural Farming"
    footer_about = ("With nature, we can live. The path shown by Masanobu Fukuoka's natural farming "
                    "and the science of Light Farming." if is_en
                    else "自然とともにあれば、生きられる。福岡正信の自然農法とLight Farmingの科学が示す、生きるための道。")

    # Article navigation
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

    return f'''<!DOCTYPE html>
<html lang="{lang}">

<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-9FLQ963JXM"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'G-9FLQ963JXM');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title} — {subtitle} | Insights | {site_name}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Zen+Old+Mincho:wght@400;700&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{css_path}">
    <style>
        .article-meta {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        .article-meta .date {{
            font-size: 0.8rem;
            color: var(--moss-green);
            letter-spacing: 0.15em;
        }}
        .article-meta .series {{
            font-size: 0.75rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--soil-rich);
            margin-top: 0.5rem;
        }}
        .chain-diagram {{
            background: var(--sand-light);
            border-left: 4px solid var(--moss-green);
            padding: 1.5rem 2rem;
            margin: 2rem 0;
            font-size: 0.95rem;
            line-height: 2.2;
            color: var(--earth-dark);
        }}
        .chain-diagram .arrow {{
            color: var(--moss-green);
            font-weight: 700;
            margin: 0 0.3rem;
        }}
        .highlight-box {{
            background: rgba(122, 154, 109, 0.08);
            border: 1px solid rgba(122, 154, 109, 0.2);
            padding: 1.5rem 2rem;
            margin: 2rem 0;
        }}
        .highlight-box p {{ margin-bottom: 0.5rem; }}
        .highlight-box p:last-child {{ margin-bottom: 0; }}
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.9rem;
        }}
        .comparison-table th {{
            background: var(--earth-dark);
            color: var(--cream);
            padding: 0.8rem 1rem;
            text-align: left;
            font-weight: 500;
        }}
        .comparison-table td {{
            padding: 0.8rem 1rem;
            border-bottom: 1px solid var(--root-tan);
            vertical-align: top;
        }}
        .comparison-table tr:nth-child(even) {{
            background: var(--sand-light);
        }}
        .article-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 2rem 0;
            border-top: 1px solid var(--root-tan);
            margin-top: 3rem;
            font-size: 0.9rem;
        }}
        .article-nav a {{
            color: var(--leaf-green);
        }}
        .quote-block {{
            border-left: 4px solid var(--moss-green);
            padding: 1.5rem 2rem;
            margin: 2rem 0;
            background: var(--sand-light);
        }}
        .quote-block .quote-text {{
            font-family: 'Zen Old Mincho', serif;
            font-size: 1.05rem;
            line-height: 2;
            color: var(--earth-dark);
        }}
    </style>
</head>

<body>
    <!-- Header -->
    <header class="header">
        <div class="header-inner">
            <a href="/" class="logo">
                {site_name}
                <span>{site_tagline}</span>
            </a>
            <nav class="nav">
                <a href="/">{home_label}</a>
                <a href="/about/">{about_label}</a>
                <a href="/light-farming/">{lf_label}</a>
                <a href="/gallery/">{gallery_label}</a>
                <a href="{insights_base}/" class="active">{insights_label}</a>
                <a href="/contact/">{contact_label}</a>
            </nav>
            <button class="nav-toggle" aria-label="メニュー">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </header>

    <!-- Article -->
    <section class="page-hero">
        <div class="page-hero-image" style="background-image: url('{img_path}');"></div>
        <div class="page-hero-content">
            <p class="hero-label">{label}</p>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
    </section>

    <section class="section">
        <div class="container-narrow">
            <div class="article-meta">
                <p class="date">{date}</p>
                <p class="series">{series_label}</p>
            </div>

            <div class="prose fade-in">
{body_html}

                <!-- Article Navigation -->
                {nav_html}
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="section section-green">
        <div class="container">
            <div class="section-header">
                <p class="section-label">{cta_label}</p>
                <h2 class="section-title">{cta_title}</h2>
            </div>
            <p class="cta-text">{cta_text}</p>
            <div class="text-center">
                <a href="{cta_btn1_link}" class="btn btn-light" style="margin-right: 1rem;">{cta_btn1_text}</a>
                <a href="{cta_btn2_link}" class="btn btn-outline">{cta_btn2_text}</a>
            </div>
            <p class="text-center" style="margin-top: 2rem;">
                <a href="https://www.facebook.com/groups/vegitage" target="_blank" rel="noopener noreferrer" style="color: rgba(255,255,255,0.85); text-decoration: underline;">Vegitage — {"Natural Farming Community" if is_en else "自然農法コミュニティ"}（Facebook）</a>
            </p>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-about">
                <h3>{site_name}</h3>
                <p>{footer_about}</p>
            </div>
            <div class="footer-nav">
                <h4>{"Pages" if is_en else "ページ"}</h4>
                <ul>
                    <li><a href="/">{home_label}</a></li>
                    <li><a href="/about/">{about_label}</a></li>
                    <li><a href="/light-farming/">{lf_label}</a></li>
                    <li><a href="/gallery/">{gallery_label}</a></li>
                    <li><a href="{insights_base}/">{insights_label}</a></li>
                    <li><a href="/contact/">{contact_label}</a></li>
                </ul>
            </div>
            <div class="footer-contact">
                <h4>関連リンク</h4>
                <ul>
                    <li><a href="https://www.amazingcarbon.com/">Amazing Carbon</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p class="footer-copyright">&copy; 2025 自然と対話する暮らし</p>
        </div>
    </footer>

    <script src="{js_path}"></script>
</body>

</html>
'''


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

    # Convert remaining Markdown to HTML
    body_html = markdown.markdown(
        body,
        extensions=["tables", "attr_list"],
        output_format="html5"
    )

    # Indent body HTML for template
    indented = "\n".join(
        f"                {line}" if line.strip() else ""
        for line in body_html.split("\n")
    )

    # Build full HTML
    html = build_html(meta, indented)

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
    css_path = "../../css/style.css" if is_en else "../css/style.css"
    js_path = "../../js/main.js" if is_en else "../js/main.js"
    img_path = "../../images/IMG_3285.jpg" if is_en else "../images/IMG_3285.jpg"
    other_lang_link = "/insights/" if is_en else "/en/insights/"
    other_lang_text = "日本語版はこちら →" if is_en else "English version available →"

    site_name = "Living with Nature" if is_en else "自然と対話する暮らし"
    home_label = "Home" if is_en else "ホーム"
    about_label = "Natural Farming" if is_en else "自然農法とは"
    gallery_label = "Field Notes" if is_en else "畑の記録"
    contact_label = "Contact" if is_en else "お問い合わせ"

    intro_text = (
        "Masanobu Fukuoka's philosophy asks: \"How do we survive?\"\n"
        "Light Farming provides the scientific answer.\n"
        "Every article here converges on one conclusion — the further we move\n"
        "from nature, the higher the cost of living becomes.\n"
        "Agriculture, energy, finance, AI, defense, healthcare.\n"
        "Follow the structure, and the answer is always the same."
    ) if is_en else (
        "福岡正信の思想は「生きるためにどうするか」。\n"
        "Light Farmingはその科学的根拠。\n"
        "全ての記事は一つの結論に向かう——自然から離れるほど、生きるコストは上がる。\n"
        "農業、エネルギー、金融、AI、医療、年金。\n"
        "構造を追跡すれば、答えは同じ場所に収束する。"
    )

    method_title = "Methodology:" if is_en else "方法論："
    method_text = (
        "Trace the production route. Observe the physical process. Cross field boundaries.\n"
        "Agriculture, energy, finance, AI, defense — the structure connects to one conclusion."
    ) if is_en else (
        "生産ルートを追跡する。物理的プロセスを見る。分野の境界を越える。\n"
        "農業も、エネルギーも、金融も、AIも——構造は一つにつながっている。"
    )

    quote_text = (
        "With nature, we can live.<br>\n"
        "The further we move from nature, the higher the cost of living becomes.<br>\n"
        "Fukuoka and Okada knew this. Dr. Christine Jones proved it."
    ) if is_en else (
        "自然とともにあれば、生きられる。<br>\n"
        "自然から離れるほど、生きるコストは上がる。<br>\n"
        "福岡正信はそれを知っていた。Light Farmingがそれを証明した。"
    )

    cta_title = "See the Structure" if is_en else "構造を見る"
    cta_text = (
        "The production route of fertilizer, the network of soil microbes —<br>\n"
        "understanding the structure changes how you see everything."
    ) if is_en else (
        "肥料の生産ルートも、土壌微生物のネットワークも、<br>\n"
        "構造を理解すれば見え方が変わる。"
    )

    footer_about = (
        "With nature, we can live. The path shown by Masanobu Fukuoka's natural farming "
        "and the science of Light Farming."
    ) if is_en else (
        "自然とともにあれば、生きられる。福岡正信の自然農法とLight Farmingの科学が示す、生きるための道。"
    )

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

    html = f'''<!DOCTYPE html>
<html lang="{lang}">

<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-9FLQ963JXM"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() {{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', 'G-9FLQ963JXM');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{intro_text.split(chr(10))[0]}">
    <title>Insights — {"Structural Analysis" if is_en else "構造分析"} | {site_name}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Zen+Old+Mincho:wght@400;700&family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{css_path}">
    <style>
        .highlight-box {{
            background: rgba(122, 154, 109, 0.08);
            border: 1px solid rgba(122, 154, 109, 0.2);
            padding: 1.5rem 2rem;
            margin: 1.5rem 0;
        }}
        .highlight-box p {{ margin-bottom: 0.5rem; }}
        .highlight-box p:last-child {{ margin-bottom: 0; }}
    </style>
</head>

<body>
    <!-- Header -->
    <header class="header">
        <div class="header-inner">
            <a href="/" class="logo">
                {site_name}
                <span>Natural Farming</span>
            </a>
            <nav class="nav">
                <a href="/">{home_label}</a>
                <a href="/about/">{about_label}</a>
                <a href="/light-farming/">Light Farming</a>
                <a href="/gallery/">{gallery_label}</a>
                <a href="{insights_base}/" class="active">Insights</a>
                <a href="/contact/">{contact_label}</a>
            </nav>
            <button class="nav-toggle" aria-label="{"Menu" if is_en else "メニュー"}">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </header>

    <!-- Page Hero -->
    <section class="page-hero">
        <div class="page-hero-image" style="background-image: url('{img_path}');"></div>
        <div class="page-hero-content">
            <p class="hero-label">Structural Analysis</p>
            <h1 class="hero-title">{"Insights" if is_en else "Insights — 構造分析"}</h1>
            <p class="hero-subtitle">
                {"With nature, we can live — the structural evidence" if is_en else "自然とともにあれば、生きられる——その構造的根拠"}
            </p>
        </div>
    </section>

    <!-- Intro -->
    <section class="section">
        <div class="container-narrow">
            <div class="prose fade-in text-center">
                <p>
                    {intro_text.replace(chr(10), '<br>' + chr(10) + '                    ')}
                </p>
                <p style="margin-top: 1rem; font-size: 0.9rem; color: var(--moss-green);">
                    <a href="{other_lang_link}" style="color: var(--moss-green);">{other_lang_text}</a>
                </p>
            </div>
        </div>
    </section>

    <!-- Structural Analysis Series -->
    <section class="section section-alt" id="series">
        <div class="container">
            <div class="section-header">
                <p class="section-label">Series</p>
                <h2 class="section-title">{"Structural Analysis Series" if is_en else "構造分析シリーズ"}</h2>
            </div>

            <div class="prose fade-in text-center" style="margin-bottom: 3rem;">
                <p>
                    {"All using the same methodology: trace the production route, observe the physical process, cross field boundaries." if is_en else "全て同じ方法論。生産ルートを追跡する。物理的プロセスを見る。分野の境界を越える。"}
                </p>
            </div>

            <div class="activity-list">
{article_list}
            </div>

            <div class="highlight-box fade-in" style="margin-top: 2rem;">
                <p><strong>{method_title}</strong></p>
                <p>
                    {method_text.replace(chr(10), '<br>' + chr(10) + '                    ')}
                </p>
            </div>
        </div>
    </section>

    <!-- Quote -->
    <section class="section">
        <div class="container-narrow">
            <div class="quote-block fade-in">
                <p class="quote-text">
                    {quote_text}
                </p>
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="section section-green">
        <div class="container">
            <div class="section-header">
                <p class="section-label">Explore</p>
                <h2 class="section-title">{cta_title}</h2>
            </div>
            <p class="cta-text">
                {cta_text}
            </p>
            <div class="text-center">
                <a href="/light-farming/" class="btn btn-light" style="margin-right: 1rem;">Light Farming</a>
                <a href="/about/" class="btn btn-outline">{"Natural Farming" if is_en else "自然農法とは"}</a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-about">
                <h3>{site_name}</h3>
                <p>{footer_about}</p>
            </div>
            <div class="footer-nav">
                <h4>{"Pages" if is_en else "ページ"}</h4>
                <ul>
                    <li><a href="/">{home_label}</a></li>
                    <li><a href="/about/">{about_label}</a></li>
                    <li><a href="/light-farming/">Light Farming</a></li>
                    <li><a href="/gallery/">{gallery_label}</a></li>
                    <li><a href="{insights_base}/">Insights</a></li>
                    <li><a href="/contact/">{contact_label}</a></li>
                </ul>
            </div>
            <div class="footer-contact">
                <h4>{"Links" if is_en else "関連リンク"}</h4>
                <ul>
                    <li><a href="https://www.amazingcarbon.com/">Amazing Carbon (Dr. Christine Jones)</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p class="footer-copyright">&copy; 2025 {"Living with Nature — aiseed.dev" if is_en else "自然と対話する暮らし"}</p>
        </div>
    </footer>

    <script src="{js_path}"></script>
</body>

</html>
'''

    # Write output
    if is_en:
        out_file = SITE_ROOT / "html" / "en" / "insights" / "index.html"
    else:
        out_file = SITE_ROOT / "html" / "insights" / "index.html"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    print(f"Built index: {out_file}")
    return True


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
        # Build index pages
        build_index("ja")
        build_index("en")
        print(f"\nBuilt {ok}/{len(files)} articles + 2 index pages.")
        return

    build_article(arg)


if __name__ == "__main__":
    main()
