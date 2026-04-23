"""Build Jinja2 template variable dicts for article/index/blog pages.

Each builder returns a flat dict consumed by tools/templates/{article,index}.html.
Localization uses _text() for hard-coded JA/EN strings and config.site_text()
for values overridable via site.json.
"""

from pathlib import Path

from . import config
from .images import resolve_og_image


def _text(is_en, en, ja):
    """Return English or Japanese text."""
    return en if is_en else ja


def _nl_to_br(text):
    """Convert newlines to <br> for HTML inline blocks."""
    return text.replace("\n", "<br>\n                    ")


# ---------------------------------------------------------------------------
# Article template variables
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
        "cta_btn1_link": meta.get("cta_btn1_link", "/en/natural-farming/" if is_en else "/natural-farming/"),
        "cta_btn2_text": meta.get("cta_btn2_text", "Light Farming"),
        "cta_btn2_link": meta.get("cta_btn2_link", "/en/light-farming/" if is_en else "/light-farming/"),
        # Paths
        "css_path": "../../../css/style.css" if is_en else "../../css/style.css",
        "js_path": "../../../js/main.js" if is_en else "../../js/main.js",
        # When hero_image is set, resolve_og_image() below generates og-image.jpg
        # in the same output directory; reuse it as the page-hero background
        # (1200x630 is already an appropriate wide aspect ratio).
        "img_path": "og-image.jpg" if meta.get("hero_image") else (
            "../../../images/IMG_3285.jpg" if is_en else "../../images/IMG_3285.jpg"
        ),
        "insights_base": insights_base,
        "blog_base": "/en/blog" if is_en else "/blog",
        # Navigation labels
        "site_name": config.site_text("site_name", lang, _text(is_en, "Living in the AI Era", "AI時代の暮らし")),
        "site_tagline": _text(is_en, "aiseed.dev", "aiseed.dev"),
        "home_label": _text(is_en, "Home", "ホーム"),
        "home_link": "/en/" if is_en else "/",
        "about_label": _text(is_en, "Natural Farming", "自然農法とは"),
        "lf_label": "Light Farming",
        "about_link": "/en/natural-farming/" if is_en else "/natural-farming/",
        "lf_link": "/en/light-farming/" if is_en else "/light-farming/",
        "our_approach_link": "/en/about/" if is_en else "/about/",
        "our_approach_label": _text(is_en, "Our Approach", "私たちのアプローチ"),
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
        "canonical_url": f"{config.SITE_URL}{insights_base}/{slug}/",
        "hreflang_ja": f"{config.SITE_URL}/insights/{slug}/",
        "hreflang_en": f"{config.SITE_URL}/en/insights/{slug}/",
        "og_locale": "en_US" if is_en else "ja_JP",
        "og_image": resolve_og_image(
            meta,
            Path(meta.get("_out_dir", ".")),
            f"{config.SITE_URL}{insights_base}/{slug}",
        ),
        # Language switch toggle
        "has_translation": bool(meta.get("_has_translation", False)),
        "lang_switch_link": f"/insights/{slug}/" if is_en else f"/en/insights/{slug}/",
        "lang_switch_label": "日本語" if is_en else "EN",
        "lang_switch_hreflang": "ja" if is_en else "en",
        "lang_switch_aria": "日本語版を表示" if is_en else "View in English",
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
        "site_name": config.site_text("site_name", lang, _text(is_en, "Living in the AI Era", "AI時代の暮らし")),
        "home_label": _text(is_en, "Home", "ホーム"),
        "home_link": "/en/" if is_en else "/",
        "about_label": _text(is_en, "Natural Farming", "自然農法とは"),
        "lf_label": "Light Farming",
        "about_link": "/en/natural-farming/" if is_en else "/natural-farming/",
        "lf_link": "/en/light-farming/" if is_en else "/light-farming/",
        "our_approach_link": "/en/about/" if is_en else "/about/",
        "our_approach_label": _text(is_en, "Our Approach", "私たちのアプローチ"),
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
        "lang_switch_label": "日本語" if is_en else "EN",
        "lang_switch_hreflang": "ja" if is_en else "en",
        "lang_switch_aria": "日本語版を表示" if is_en else "View in English",
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
        "copyright_text": config.site_text("copyright_text", lang, _text(is_en, "Living in the AI Era — aiseed.dev", "AI時代の暮らし")),
        # SEO
        "canonical_url": f"{config.SITE_URL}{insights_base}/",
        "hreflang_ja": f"{config.SITE_URL}/insights/",
        "hreflang_en": f"{config.SITE_URL}/en/insights/",
        "og_locale": "en_US" if is_en else "ja_JP",
        "og_image": config.DEFAULT_OG_IMAGE,
    }


# ---------------------------------------------------------------------------
# Blog template variables
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Book (long-form serial) template variables
#
# Content lives under articles/claude-debian/ and is published at
# /claude-debian/{stem}/ where stem = slug.removeprefix("claude-debian-").
# Only a Japanese edition exists, so no language switch is rendered.
# ---------------------------------------------------------------------------

_BOOK_SLUG_PREFIX = "claude-debian-"
_BOOK_BASE = "/claude-debian"
_BOOK_TITLE = "Claudeと一緒に学ぶDebian"


def _book_stem(slug):
    """Strip the book slug prefix so URLs read /claude-debian/{stem}/."""
    if slug.startswith(_BOOK_SLUG_PREFIX):
        return slug[len(_BOOK_SLUG_PREFIX):]
    return slug


def book_vars(meta, body_html):
    """Build template variables for a single book chapter."""
    slug = meta.get("slug", "")
    stem = _book_stem(slug)
    number = meta.get("number", "")

    prev_slug = meta.get("prev_slug", "")
    prev_title = meta.get("prev_title", "")
    next_slug = meta.get("next_slug", "")
    next_title = meta.get("next_title", "")

    # Navigation: prev/next frontmatter uses full slug; URLs use the stem.
    # At the tail of the book we fall back to the table of contents.
    book_top = f"{_BOOK_TITLE} 目次"
    nav_html = '<div class="article-nav">\n'
    if prev_slug:
        nav_html += f'  <a href="{_BOOK_BASE}/{_book_stem(prev_slug)}/">&larr; 前: {prev_title}</a>\n'
    else:
        nav_html += '  <span></span>\n'
    if next_slug:
        nav_html += f'  <a href="{_BOOK_BASE}/{_book_stem(next_slug)}/">次: {next_title} &rarr;</a>\n'
    else:
        nav_html += f'  <a href="{_BOOK_BASE}/">{book_top} &rarr;</a>\n'
    nav_html += '</div>'

    return {
        "lang": "ja",
        "title": meta.get("title", ""),
        "subtitle": meta.get("subtitle", ""),
        "description": meta.get("description", ""),
        "date": meta.get("date", ""),
        "number": number,
        "label": meta.get("label", f"{_BOOK_TITLE} {number}"),
        "body_html": body_html,
        "nav_html": nav_html,
        # CTA — fall back to generic "back to TOC" when chapter frontmatter
        # hasn't set its own CTA buttons.
        "cta_label": meta.get("cta_label", _BOOK_TITLE),
        "cta_title": meta.get("cta_title", "Claudeを横に置いて、次の章へ"),
        "cta_text": meta.get("cta_text",
            "読むだけでは身につかない。Claudeに自分の状況を打ち込みながら読むことで、"
            "教科書は自分専用の教材になる。"),
        "cta_btn1_text": meta.get("cta_btn1_text", "目次へ"),
        "cta_btn1_link": meta.get("cta_btn1_link", f"{_BOOK_BASE}/"),
        "cta_btn2_text": meta.get("cta_btn2_text", "Insights"),
        "cta_btn2_link": meta.get("cta_btn2_link", "/insights/"),
        # Reuse og-image.jpg (same dir) as page hero when hero_image is set
        "img_path": "og-image.jpg" if meta.get("hero_image") else "../../images/IMG_3285.jpg",
        # Navigation bar labels (shared site nav)
        "insights_base": "/insights",
        "blog_base": "/blog",
        "site_name": config.site_text("site_name", "ja", "AI時代の暮らし"),
        "site_tagline": "aiseed.dev",
        "home_label": "ホーム",
        "home_link": "/",
        "about_label": "自然農法とは",
        "lf_label": "Light Farming",
        "about_link": "/natural-farming/",
        "lf_link": "/light-farming/",
        "our_approach_link": "/about/",
        "our_approach_label": "私たちのアプローチ",
        "gallery_label": "畑の記録",
        "insights_label": "Insights",
        "contact_label": "お問い合わせ",
        "menu_label": "メニュー",
        "pages_label": "ページ",
        "links_label": "関連リンク",
        "series_label": f"{_BOOK_TITLE} {number}",
        "vegitage_label": "自然農法コミュニティ",
        "footer_about":
            "AIが仕事、農業、暮らしを変える。化石資源、食料、エネルギー、AI、医療、年金——全ての構造は一つに繋がっている。",
        # SEO — JA-only edition, so no hreflang=en alternate.
        "canonical_url": f"{config.SITE_URL}{_BOOK_BASE}/{stem}/",
        "hreflang_ja": f"{config.SITE_URL}{_BOOK_BASE}/{stem}/",
        "hreflang_en": "",
        "og_locale": "ja_JP",
        "og_image": resolve_og_image(
            meta,
            Path(meta.get("_out_dir", ".")),
            f"{config.SITE_URL}{_BOOK_BASE}/{stem}",
        ),
        # No English edition yet — hide the language switcher.
        "has_translation": False,
        "lang_switch_link": "",
        "lang_switch_label": "",
        "lang_switch_hreflang": "ja",
        "lang_switch_aria": "",
    }


def book_index_vars(chapter_list_html):
    """Build template variables for the book table-of-contents page."""
    return {
        "lang": "ja",
        "site_name": config.site_text("site_name", "ja", "AI時代の暮らし"),
        "home_label": "ホーム",
        "home_link": "/",
        "about_label": "自然農法とは",
        "lf_label": "Light Farming",
        "about_link": "/natural-farming/",
        "lf_link": "/light-farming/",
        "our_approach_link": "/about/",
        "our_approach_label": "私たちのアプローチ",
        "gallery_label": "畑の記録",
        "menu_label": "メニュー",
        "pages_label": "ページ",
        "links_label": "関連リンク",
        "insights_base": "/insights",
        "blog_base": "/blog",
        "css_path": "../css/style.css",
        "js_path": "../js/main.js",
        "img_path": "../images/IMG_3285.jpg",
        "meta_description":
            "Claudeを横に置いて読む新しい形の教科書。Debianへの移行を、対話を通じて自分の状況に合わせて学ぶ。",
        "structural_analysis_label": _BOOK_TITLE,
        "page_title": _BOOK_TITLE,
        "page_subtitle": "読むのではなく、対話する教科書",
        "other_lang_link": "",
        "other_lang_text": "",
        "lang_switch_label": "",
        "lang_switch_hreflang": "ja",
        "lang_switch_aria": "",
        "series_title": "全24章",
        "series_description":
            "序章から第23章まで。各章の末尾で、Claudeに自分の状況を打ち込んでから次に進む。",
        "article_list_html": chapter_list_html,
        "intro_html": (
            "教科書を読みながら、横でClaudeを開く。<br>\n                    "
            "あなたの状況を打ち込み、自分専用の答えを得る。<br>\n                    "
            "同じ本でも、人によって学びが変わる——それがこの本の前提だ。"
        ),
        "method_title": "読み方",
        "method_html": (
            "各章の末尾で、自分の状況を Claude に打ち込んでから次に進む。<br>\n                    "
            "抽象論を読むだけでは身につかない。自分の言葉に翻訳して初めて知識になる。"
        ),
        "quote_html":
            "答えを渡すのではなく、問いを立てる作法を渡す。<br>\n"
            "それがClaudeと一緒に学ぶ時代の、最も長く残るギフトになる。",
        "cta_title": "始める",
        "cta_html":
            "序章から、一緒に読み始めよう。<br>\n"
            "迷ったら、Claude に「ここまで読んで、自分はどうすべきか」と聞けばいい。",
        "footer_about":
            "AIが仕事、農業、暮らしを変える。化石資源、食料、エネルギー、AI、医療、年金——全ての構造は一つに繋がっている。",
        "copyright_text": config.site_text("copyright_text", "ja", "AI時代の暮らし"),
        # SEO — JA-only edition, so no hreflang=en alternate.
        "canonical_url": f"{config.SITE_URL}{_BOOK_BASE}/",
        "hreflang_ja": f"{config.SITE_URL}{_BOOK_BASE}/",
        "hreflang_en": "",
        "og_locale": "ja_JP",
        "og_image": config.DEFAULT_OG_IMAGE,
    }


def blog_vars(meta, body_html):
    """Build template variables for blog post pages."""
    lang = meta.get("lang", "ja")
    is_en = lang == "en"
    slug = meta.get("slug", "")
    blog_base = "/en/blog" if is_en else "/blog"

    # Blog navigation — prev/next derived from file-number order by
    # build_blog_post(); falls back to the blog index on either end.
    prev_post = meta.get("_prev_post")
    next_post = meta.get("_next_post")
    blog_top = "Blog Top" if is_en else "Blog トップ"
    prev_prefix = "Prev: " if is_en else "前: "
    next_prefix = "Next: " if is_en else "次: "

    nav_html = '<div class="article-nav">\n'
    if prev_post:
        nav_html += f'  <a href="{blog_base}/{prev_post.get("slug", "")}/">&larr; {prev_prefix}{prev_post.get("title", "")}</a>\n'
    else:
        nav_html += '  <span></span>\n'
    if next_post:
        nav_html += f'  <a href="{blog_base}/{next_post.get("slug", "")}/">{next_prefix}{next_post.get("title", "")} &rarr;</a>\n'
    else:
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
        # Reuse the generated og-image.jpg (same dir) as the page-hero background.
        "img_path": "og-image.jpg" if meta.get("hero_image") else (
            "../../../images/IMG_3285.jpg" if is_en else "../../images/IMG_3285.jpg"
        ),
        "insights_base": "/en/insights" if is_en else "/insights",
        "blog_base": "/en/blog" if is_en else "/blog",
        # Navigation labels
        "site_name": config.site_text("site_name", lang, _text(is_en, "Living in the AI Era", "AI時代の暮らし")),
        "site_tagline": _text(is_en, "aiseed.dev", "aiseed.dev"),
        "home_label": _text(is_en, "Home", "ホーム"),
        "home_link": "/en/" if is_en else "/",
        "about_label": _text(is_en, "Natural Farming", "自然農法とは"),
        "lf_label": "Light Farming",
        "about_link": "/en/natural-farming/" if is_en else "/natural-farming/",
        "lf_link": "/en/light-farming/" if is_en else "/light-farming/",
        "our_approach_link": "/en/about/" if is_en else "/about/",
        "our_approach_label": _text(is_en, "Our Approach", "私たちのアプローチ"),
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
        "canonical_url": f"{config.SITE_URL}{blog_base}/{slug}/",
        "hreflang_ja": f"{config.SITE_URL}/blog/{slug}/",
        "hreflang_en": f"{config.SITE_URL}/en/blog/{slug}/",
        "og_locale": "en_US" if is_en else "ja_JP",
        "og_image": resolve_og_image(
            meta,
            Path(meta.get("_out_dir", ".")),
            f"{config.SITE_URL}{blog_base}/{slug}",
        ),
        # Language switch toggle
        "has_translation": bool(meta.get("_has_translation", False)),
        "lang_switch_link": f"/blog/{slug}/" if is_en else f"/en/blog/{slug}/",
        "lang_switch_label": "日本語" if is_en else "EN",
        "lang_switch_hreflang": "ja" if is_en else "en",
        "lang_switch_aria": "日本語版を表示" if is_en else "View in English",
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
        "site_name": config.site_text("site_name", lang, _text(is_en, "Living in the AI Era", "AI時代の暮らし")),
        "home_label": _text(is_en, "Home", "ホーム"),
        "home_link": "/en/" if is_en else "/",
        "about_label": _text(is_en, "Natural Farming", "自然農法とは"),
        "lf_label": "Light Farming",
        "about_link": "/en/natural-farming/" if is_en else "/natural-farming/",
        "lf_link": "/en/light-farming/" if is_en else "/light-farming/",
        "our_approach_link": "/en/about/" if is_en else "/about/",
        "our_approach_label": _text(is_en, "Our Approach", "私たちのアプローチ"),
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
        "lang_switch_label": "日本語" if is_en else "EN",
        "lang_switch_hreflang": "ja" if is_en else "en",
        "lang_switch_aria": "日本語版を表示" if is_en else "View in English",
        # Blog index skips duplicate Intro/Series headers — page-hero already shows "Blog"
        "series_title": "",
        "series_description": "",
        "article_list_html": post_list_html,
        "intro_html": "",
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
        "copyright_text": config.site_text("copyright_text", lang, _text(is_en, "Living in the AI Era — aiseed.dev", "AI時代の暮らし")),
        # SEO
        "canonical_url": f"{config.SITE_URL}{blog_base}/",
        "hreflang_ja": f"{config.SITE_URL}/blog/",
        "hreflang_en": f"{config.SITE_URL}/en/blog/",
        "og_locale": "en_US" if is_en else "ja_JP",
        "og_image": config.DEFAULT_OG_IMAGE,
    }
