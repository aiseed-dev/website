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

        "asset_version": config.asset_version(),
        # When hero_image is set, resolve_og_image() below generates og-image.jpg
        # in the same output directory; reuse it as the page-hero background
        # (1200x630 is already an appropriate wide aspect ratio).
        "img_path": "og-image.jpg" if meta.get("hero_image") else (
            "../../../images/IMG_3285.jpg" if is_en else "../../images/IMG_3285.jpg"
        ),
        "insights_base": insights_base,
        "blog_base": "/en/blog" if is_en else "/blog",
        "book_base": "/en/claude-debian" if is_en else "/claude-debian",
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
        "privacy_link": "/en/privacy/" if is_en else "/privacy/",
        "privacy_label": _text(is_en, "Privacy", "プライバシー"),
        "insights_label": "Insights",
        "articles_parent_label": _text(is_en, "Articles", "記事"),
        "insights_child_label": _text(is_en, "Structural Analysis", "構造分析"),
        "book_label": _text(is_en, "Learning Debian with Claude", "Claudeと一緒に学ぶDebian"),
        "aiways_label": _text(is_en, "AI-Native Ways of Working", "AIネイティブな仕事の作法"),
        "farming_base": "/en/phosphorus-and-farming" if is_en else "/phosphorus-and-farming",
        "farming_label": _text(is_en, "Phosphorus Depletion and Natural Farming", "リン資源枯渇と自然農法"),
        "aiways_base": "/en/ai-native-ways" if is_en else "/ai-native-ways",
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
        "privacy_link": "/en/privacy/" if is_en else "/privacy/",
        "privacy_label": _text(is_en, "Privacy", "プライバシー"),
        "contact_label": _text(is_en, "Contact", "お問い合わせ"),
        "menu_label": _text(is_en, "Menu", "メニュー"),
        "pages_label": _text(is_en, "Pages", "ページ"),
        "links_label": _text(is_en, "Links", "関連リンク"),
        "articles_parent_label": _text(is_en, "Articles", "記事"),
        "insights_child_label": _text(is_en, "Structural Analysis", "構造分析"),
        "book_label": _text(is_en, "Learning Debian with Claude", "Claudeと一緒に学ぶDebian"),
        "aiways_label": _text(is_en, "AI-Native Ways of Working", "AIネイティブな仕事の作法"),
        "farming_base": "/en/phosphorus-and-farming" if is_en else "/phosphorus-and-farming",
        "farming_label": _text(is_en, "Phosphorus Depletion and Natural Farming", "リン資源枯渇と自然農法"),
        "aiways_base": "/en/ai-native-ways" if is_en else "/ai-native-ways",
        "insights_base": insights_base,
        "blog_base": "/en/blog" if is_en else "/blog",
        "book_base": "/en/claude-debian" if is_en else "/claude-debian",
        "css_path": "../../css/style.css" if is_en else "../css/style.css",
        "js_path": "../../js/main.js" if is_en else "../js/main.js",

        "asset_version": config.asset_version(),
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
_BOOK_BASE_JA = "/claude-debian"
_BOOK_BASE_EN = "/en/claude-debian"
_BOOK_TITLE_JA = "Claudeと一緒に学ぶDebian"
_BOOK_TITLE_EN = "Learning Debian with Claude"


def _book_stem(slug):
    """Strip the book slug prefix so URLs read /claude-debian/{stem}/."""
    if slug.startswith(_BOOK_SLUG_PREFIX):
        return slug[len(_BOOK_SLUG_PREFIX):]
    return slug


def book_vars(meta, body_html):
    """Build template variables for a single book chapter."""
    lang = meta.get("lang", "ja")
    is_en = lang == "en"
    book_base = _BOOK_BASE_EN if is_en else _BOOK_BASE_JA
    book_title = _BOOK_TITLE_EN if is_en else _BOOK_TITLE_JA

    slug = meta.get("slug", "")
    stem = _book_stem(slug)
    number = meta.get("number", "")

    prev_slug = meta.get("prev_slug", "")
    prev_title = meta.get("prev_title", "")
    next_slug = meta.get("next_slug", "")
    next_title = meta.get("next_title", "")

    # Navigation: prev/next frontmatter uses full slug; URLs use the stem.
    # At the tail of the book we fall back to the table of contents.
    book_top = _text(is_en, f"{book_title} TOC", f"{book_title} 目次")
    prev_prefix = "Prev: " if is_en else "前: "
    next_prefix = "Next: " if is_en else "次: "

    nav_html = '<div class="article-nav">\n'
    if prev_slug:
        nav_html += f'  <a href="{book_base}/{_book_stem(prev_slug)}/">&larr; {prev_prefix}{prev_title}</a>\n'
    else:
        nav_html += '  <span></span>\n'
    if next_slug:
        nav_html += f'  <a href="{book_base}/{_book_stem(next_slug)}/">{next_prefix}{next_title} &rarr;</a>\n'
    else:
        nav_html += f'  <a href="{book_base}/">{book_top} &rarr;</a>\n'
    nav_html += '</div>'

    return {
        "lang": lang,
        "title": meta.get("title", ""),
        "subtitle": meta.get("subtitle", ""),
        "description": meta.get("description", ""),
        "date": meta.get("date", ""),
        "number": number,
        "label": meta.get("label", f"{book_title} {number}"),
        "body_html": body_html,
        "nav_html": nav_html,
        # CTA — fall back to generic "back to TOC" when chapter frontmatter
        # hasn't set its own CTA buttons.
        "cta_label": meta.get("cta_label", book_title),
        "cta_title": meta.get("cta_title", _text(is_en,
            "Read with Claude beside you",
            "Claudeを横に置いて、次の章へ")),
        "cta_text": meta.get("cta_text", _text(is_en,
            "Reading alone isn't enough. Type your situation into Claude as you read,"
            " and the same textbook becomes tailored to you.",
            "読むだけでは身につかない。Claudeに自分の状況を打ち込みながら読むことで、"
            "教科書は自分専用の教材になる。")),
        "cta_btn1_text": meta.get("cta_btn1_text", _text(is_en, "Table of Contents", "目次へ")),
        "cta_btn1_link": meta.get("cta_btn1_link", f"{book_base}/"),
        "cta_btn2_text": meta.get("cta_btn2_text", "Insights"),
        "cta_btn2_link": meta.get("cta_btn2_link", "/en/insights/" if is_en else "/insights/"),
        # Paths
        "css_path": "../../../css/style.css" if is_en else "../../css/style.css",
        "js_path": "../../../js/main.js" if is_en else "../../js/main.js",
        "asset_version": config.asset_version(),
        # Reuse og-image.jpg (same dir) as page hero when hero_image is set
        "img_path": "og-image.jpg" if meta.get("hero_image") else (
            "../../../images/IMG_3285.jpg" if is_en else "../../images/IMG_3285.jpg"
        ),
        # Navigation bar labels (shared site nav)
        "insights_base": "/en/insights" if is_en else "/insights",
        "blog_base": "/en/blog" if is_en else "/blog",
        "book_base": book_base,
        "site_name": config.site_text("site_name", lang, _text(is_en, "Living in the AI Era", "AI時代の暮らし")),
        "site_tagline": "aiseed.dev",
        "home_label": _text(is_en, "Home", "ホーム"),
        "home_link": "/en/" if is_en else "/",
        "about_label": _text(is_en, "Natural Farming", "自然農法とは"),
        "lf_label": "Light Farming",
        "about_link": "/en/natural-farming/" if is_en else "/natural-farming/",
        "lf_link": "/en/light-farming/" if is_en else "/light-farming/",
        "our_approach_link": "/en/about/" if is_en else "/about/",
        "our_approach_label": _text(is_en, "Our Approach", "私たちのアプローチ"),
        "gallery_label": _text(is_en, "Field Notes", "畑の記録"),
        "privacy_link": "/en/privacy/" if is_en else "/privacy/",
        "privacy_label": _text(is_en, "Privacy", "プライバシー"),
        "insights_label": "Insights",
        "articles_parent_label": _text(is_en, "Articles", "記事"),
        "insights_child_label": _text(is_en, "Structural Analysis", "構造分析"),
        "book_label": _text(is_en, "Learning Debian with Claude", "Claudeと一緒に学ぶDebian"),
        "aiways_label": _text(is_en, "AI-Native Ways of Working", "AIネイティブな仕事の作法"),
        "farming_base": "/en/phosphorus-and-farming" if is_en else "/phosphorus-and-farming",
        "farming_label": _text(is_en, "Phosphorus Depletion and Natural Farming", "リン資源枯渇と自然農法"),
        "aiways_base": "/en/ai-native-ways" if is_en else "/ai-native-ways",
        "contact_label": _text(is_en, "Contact", "お問い合わせ"),
        "menu_label": _text(is_en, "Menu", "メニュー"),
        "pages_label": _text(is_en, "Pages", "ページ"),
        "links_label": _text(is_en, "Links", "関連リンク"),
        "series_label": f"{book_title} {number}",
        "vegitage_label": _text(is_en, "Natural Farming Community", "自然農法コミュニティ"),
        "footer_about": _text(is_en,
            "AI changes how we work, farm, and live. Structural analysis of fossil resources, "
            "food, energy, AI, healthcare, and pensions — every structure connects.",
            "AIが仕事、農業、暮らしを変える。化石資源、食料、エネルギー、AI、医療、年金——全ての構造は一つに繋がっている。"),
        # SEO
        "canonical_url": f"{config.SITE_URL}{book_base}/{stem}/",
        "hreflang_ja": f"{config.SITE_URL}{_BOOK_BASE_JA}/{stem}/",
        "hreflang_en": f"{config.SITE_URL}{_BOOK_BASE_EN}/{stem}/" if meta.get("_has_translation") else "",
        "og_locale": "en_US" if is_en else "ja_JP",
        "og_image": resolve_og_image(
            meta,
            Path(meta.get("_out_dir", ".")),
            f"{config.SITE_URL}{book_base}/{stem}",
        ),
        # Language switch — only shown when a sibling-language edition exists.
        "has_translation": bool(meta.get("_has_translation", False)),
        "lang_switch_link": (f"{_BOOK_BASE_JA}/{stem}/" if is_en else f"{_BOOK_BASE_EN}/{stem}/"),
        "lang_switch_label": "日本語" if is_en else "EN",
        "lang_switch_hreflang": "ja" if is_en else "en",
        "lang_switch_aria": "日本語版を表示" if is_en else "View in English",
    }


_AIWAYS_BASE_JA = "/ai-native-ways"
_AIWAYS_BASE_EN = "/en/ai-native-ways"
_AIWAYS_TITLE_JA = "AIネイティブな仕事の作法"
_AIWAYS_TITLE_EN = "AI-Native Ways of Working"


def aiways_index_vars(lang, chapter_list_html, has_translation=False):
    """Build template variables for the ai-native-ways table-of-contents page."""
    is_en = lang == "en"
    aiways_base = _AIWAYS_BASE_EN if is_en else _AIWAYS_BASE_JA
    aiways_title = _AIWAYS_TITLE_EN if is_en else _AIWAYS_TITLE_JA

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
        "privacy_link": "/en/privacy/" if is_en else "/privacy/",
        "privacy_label": _text(is_en, "Privacy", "プライバシー"),
        "menu_label": _text(is_en, "Menu", "メニュー"),
        "pages_label": _text(is_en, "Pages", "ページ"),
        "links_label": _text(is_en, "Links", "関連リンク"),
        "articles_parent_label": _text(is_en, "Articles", "記事"),
        "insights_child_label": _text(is_en, "Structural Analysis", "構造分析"),
        "book_label": _text(is_en, "Learning Debian with Claude", "Claudeと一緒に学ぶDebian"),
        "aiways_label": _text(is_en, "AI-Native Ways of Working", "AIネイティブな仕事の作法"),
        "farming_base": "/en/phosphorus-and-farming" if is_en else "/phosphorus-and-farming",
        "farming_label": _text(is_en, "Phosphorus Depletion and Natural Farming", "リン資源枯渇と自然農法"),
        "aiways_base": "/en/ai-native-ways" if is_en else "/ai-native-ways",
        "insights_base": "/en/insights" if is_en else "/insights",
        "blog_base": "/en/blog" if is_en else "/blog",
        "book_base": "/en/claude-debian" if is_en else "/claude-debian",
        "css_path": "../../css/style.css" if is_en else "../css/style.css",
        "js_path": "../../js/main.js" if is_en else "../js/main.js",

        "asset_version": config.asset_version(),
        "img_path": "../../images/IMG_3285.jpg" if is_en else "../images/IMG_3285.jpg",
        "meta_description": _text(is_en,
            "Tools for AI-native work. Office runs paperwork, Java/C# runs business systems — but AI runs on Python and text. A practical guide to working with AI as a colleague.",
            "AI ネイティブな仕事の道具立て。事務処理は Office、業務ソフトは Java/C#、しかし AI は Python とテキストでできている。AI を同僚として使うための実用的な作法。"),
        "structural_analysis_label": aiways_title,
        "page_title": aiways_title,
        "page_subtitle": _text(is_en,
            "Tools shape thinking. Change the tools, the thinking changes.",
            "道具を変えれば、思考が変わる。"),
        "other_lang_link": (_AIWAYS_BASE_JA + "/") if is_en else (_AIWAYS_BASE_EN + "/"),
        "other_lang_text": _text(is_en, "日本語版はこちら →", "English version available →") if has_translation else "",
        "lang_switch_label": "日本語" if is_en else "EN",
        "lang_switch_hreflang": "ja" if is_en else "en",
        "lang_switch_aria": "日本語版を表示" if is_en else "View in English",
        "series_title": _text(is_en, "Essays — series in progress", "連載エッセイ"),
        "series_description": _text(is_en,
            "Office, Java, and C# are tools from an era when humans handled information processing. Carrying these heavy tools to do work AI could do — that is what is happening in most workplaces today. The chapters that follow walk through, area by area, what to drop and what to pick up.",
            "Office、Java、C# は、人間が情報処理を担っていた時代の道具である。AI でもやれる仕事を、人間がわざわざ重い道具で抱え込む——これが、いま多くの職場で起きていることだ。次の章から、領域ごとに具体的な作法を見ていく。"),
        "article_list_html": chapter_list_html,
        "intro_html": _text(is_en,
            "OpenAI runs on Python. So does Anthropic. Data is Markdown, JSON, YAML.<br>\n                    "
            "Between AI-native tools and the standard tools of the enterprise, a decisive divide runs through.<br>\n                    "
            "What changes in the AI era — information processing becomes simple work that AI can do.",
            "OpenAI も Anthropic も Python で動いている。データは Markdown、JSON、YAML。<br>\n                    "
            "AI ネイティブな道具と、企業の標準的な道具のあいだに、決定的な断絶が走っている。<br>\n                    "
            "AI 時代に何が変わるか——情報の処理は、AI でもやれる簡単な仕事になる。"),
        "method_title": _text(is_en, "How to read", "読み方"),
        "method_html": _text(is_en,
            "Each chapter is a short essay. Read the prologue first; the rest can be read in any order based on what fits your work.<br>\n                    "
            "The page typography here is intentionally different — these are essays, not reference material.",
            "各章は短いエッセイ。まずは序章を読む。残りは仕事に合わせて好きな順で読める。<br>\n                    "
            "ページのタイポグラフィを敢えて他のシリーズと変えてある——これは資料ではなくエッセイだ。"),
        "quote_html": _text(is_en,
            "Change the tools, and your thinking changes. Change your thinking,<br>\n"
            "and you start spending time on work only humans can do.",
            "道具を変えれば、思考が変わる。思考が変われば、<br>\n"
            "人間にしかできない仕事に時間を使えるようになる。"),
        "cta_title": _text(is_en, "Start with the prologue", "序章から始める"),
        "cta_html": _text(is_en,
            "Begin from the prologue. The series is published as it is written.",
            "序章から読み始めよう。連載は書き上がり次第、順次公開していく。"),
        "footer_about": _text(is_en,
            "AI changes how we work, farm, and live. Structural analysis of fossil resources, "
            "food, energy, AI, healthcare, and pensions — every structure connects.",
            "AIが仕事、農業、暮らしを変える。化石資源、食料、エネルギー、AI、医療、年金——全ての構造は一つに繋がっている。"),
        "copyright_text": config.site_text("copyright_text", lang, _text(is_en, "Living in the AI Era — aiseed.dev", "AI時代の暮らし")),
        # SEO
        "canonical_url": f"{config.SITE_URL}{aiways_base}/",
        "hreflang_ja": f"{config.SITE_URL}{_AIWAYS_BASE_JA}/",
        "hreflang_en": f"{config.SITE_URL}{_AIWAYS_BASE_EN}/" if has_translation else "",
        "og_locale": "en_US" if is_en else "ja_JP",
        "og_image": config.DEFAULT_OG_IMAGE,
    }


_FARMING_BASE_JA = "/phosphorus-and-farming"
_FARMING_BASE_EN = "/en/phosphorus-and-farming"
_FARMING_TITLE_JA = "リン資源枯渇と自然農法"
_FARMING_TITLE_EN = "Phosphorus Depletion and Natural Farming"


def farming_index_vars(lang, chapter_list_html, has_translation=False):
    """Build template variables for the phosphorus-and-farming table-of-contents page."""
    is_en = lang == "en"
    farming_base = _FARMING_BASE_EN if is_en else _FARMING_BASE_JA
    farming_title = _FARMING_TITLE_EN if is_en else _FARMING_TITLE_JA

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
        "privacy_link": "/en/privacy/" if is_en else "/privacy/",
        "privacy_label": _text(is_en, "Privacy", "プライバシー"),
        "menu_label": _text(is_en, "Menu", "メニュー"),
        "pages_label": _text(is_en, "Pages", "ページ"),
        "links_label": _text(is_en, "Links", "関連リンク"),
        "articles_parent_label": _text(is_en, "Articles", "記事"),
        "insights_child_label": _text(is_en, "Structural Analysis", "構造分析"),
        "book_label": _text(is_en, "Learning Debian with Claude", "Claudeと一緒に学ぶDebian"),
        "aiways_label": _text(is_en, "AI-Native Ways of Working", "AIネイティブな仕事の作法"),
        "farming_base": "/en/phosphorus-and-farming" if is_en else "/phosphorus-and-farming",
        "farming_label": _text(is_en, "Phosphorus Depletion and Natural Farming", "リン資源枯渇と自然農法"),
        "aiways_base": "/en/ai-native-ways" if is_en else "/ai-native-ways",
        "insights_base": "/en/insights" if is_en else "/insights",
        "blog_base": "/en/blog" if is_en else "/blog",
        "book_base": "/en/claude-debian" if is_en else "/claude-debian",
        "css_path": "../../css/style.css" if is_en else "../css/style.css",
        "js_path": "../../js/main.js" if is_en else "../js/main.js",

        "asset_version": config.asset_version(),
        "img_path": "../../images/IMG_3285.jpg" if is_en else "../images/IMG_3285.jpg",
        "meta_description": _text(is_en,
            "Phosphorus depletion and the structural shift to microbial-driven natural farming. Why phosphate fertilizer prices won't return to cheap, why industrial farming fails, and why the surviving path is natural farming with imports as buffer.",
            "リン資源の枯渇と、微生物型自然農法への構造的転換。なぜリン酸肥料は安価に戻らないのか、なぜ工業型農業は成立しないのか、そしてなぜ残された道が自然農法+輸入補完なのか ── 経済と物理が決める唯一の現実解。"),
        "structural_analysis_label": farming_title,
        "page_title": farming_title,
        "page_subtitle": _text(is_en,
            "The economy decides the way of farming.",
            "経済が、農法を決める。"),
        "other_lang_link": (_FARMING_BASE_JA + "/") if is_en else (_FARMING_BASE_EN + "/"),
        "other_lang_text": _text(is_en, "日本語版はこちら →", "English version available →") if has_translation else "",
        "lang_switch_label": "日本語" if is_en else "EN",
        "lang_switch_hreflang": "ja" if is_en else "en",
        "lang_switch_aria": "日本語版を表示" if is_en else "View in English",
        "series_title": _text(is_en, "Series — phosphorus to natural farming", "全 9 章 — リン資源から自然農法へ"),
        "series_description": _text(is_en,
            "Phosphate fertilizer supply is collapsing on three independent fronts: China's export halt, sulfur supply via the Strait of Hormuz, and PFAS contamination in sewage sludge recovery. The structural conclusion is microbial natural farming, with imports as a transitional buffer.",
            "リン酸肥料の供給は三つの独立したルート ── 中国の輸出停止、ホルムズ海峡経由の硫黄供給、下水汚泥回収の PFAS 汚染 ── で同時に細っている。構造的に残るのは、微生物型自然農法+輸入補完という現実的な中間の道である。"),
        "article_list_html": chapter_list_html,
        "intro_html": _text(is_en,
            "The economy decides the way of farming.<br>\n                    "
            "Phosphate fertilizer supply tightens; industrial agriculture's books stop balancing;<br>\n                    "
            "the soil microbes step in to do what fertilizer used to do.<br>\n                    "
            "This is not philosophy. It is structural economics and biology.",
            "経済が、農法を決める。<br>\n                    "
            "リン酸肥料の供給が細り、工業型農業の収支が崩れ、<br>\n                    "
            "土壌微生物が肥料の代わりに働く ── これは思想ではない。<br>\n                    "
            "構造的な経済と生物学が、自ずと指し示す方向である。"),
        "method_title": _text(is_en, "How to read", "読み方"),
        "method_html": _text(is_en,
            "Read the prologue first to grasp the four-step logic. The chapters then walk through supply constraint (1), why prices won't drop (2), why industrial farming fails (3), the realistic position (4), soil microbes (5), CO2 as tailwind (6), implementation (7), and operating principles (8).<br>\n                    "
            "Each chapter cites primary sources — World Bank, USDA, MAFF, peer-reviewed literature.",
            "序章で 4 段階の論理を掴んでから、章ごとに ── 供給制約(1)、安価には戻らない(2)、工業型農業は成立しない(3)、現実的な立ち位置(4)、土壌微生物(5)、CO2 という追い風(6)、どう実装するか(7)、運用原則(8)── と読み進める。<br>\n                    "
            "各章は一次情報源(World Bank、USDA、農林水産省、査読論文等)を引用している。"),
        "quote_html": _text(is_en,
            "Phosphate fertilizer becomes expensive. That alone decides everything.<br>\n"
            "The era of cheap industrial agriculture is over.",
            "リン酸肥料が高くなる、それだけで全部が決まる。<br>\n"
            "安価な工業型農業の時代は終わった。"),
        "cta_title": _text(is_en, "Start with the prologue", "序章から始める"),
        "cta_html": _text(is_en,
            "Read the prologue, then chapter by chapter. The structural conclusion will become inescapable.",
            "序章から、章ごとに読み進めよう。構造的な結論は、避けようがないことが分かる。"),
        "footer_about": _text(is_en,
            "AI changes how we work, farm, and live. Structural analysis of fossil resources, "
            "food, energy, AI, healthcare, and pensions — every structure connects.",
            "AIが仕事、農業、暮らしを変える。化石資源、食料、エネルギー、AI、医療、年金——全ての構造は一つに繋がっている。"),
        "copyright_text": config.site_text("copyright_text", lang, _text(is_en, "Living in the AI Era — aiseed.dev", "AI時代の暮らし")),
        # SEO
        "canonical_url": f"{config.SITE_URL}{farming_base}/",
        "hreflang_ja": f"{config.SITE_URL}{_FARMING_BASE_JA}/",
        "hreflang_en": f"{config.SITE_URL}{_FARMING_BASE_EN}/" if has_translation else "",
        "og_locale": "en_US" if is_en else "ja_JP",
        "og_image": config.DEFAULT_OG_IMAGE,
    }


def book_index_vars(lang, chapter_list_html, has_translation=False):
    """Build template variables for the book table-of-contents page."""
    is_en = lang == "en"
    book_base = _BOOK_BASE_EN if is_en else _BOOK_BASE_JA
    book_title = _BOOK_TITLE_EN if is_en else _BOOK_TITLE_JA

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
        "privacy_link": "/en/privacy/" if is_en else "/privacy/",
        "privacy_label": _text(is_en, "Privacy", "プライバシー"),
        "menu_label": _text(is_en, "Menu", "メニュー"),
        "pages_label": _text(is_en, "Pages", "ページ"),
        "links_label": _text(is_en, "Links", "関連リンク"),
        "articles_parent_label": _text(is_en, "Articles", "記事"),
        "insights_child_label": _text(is_en, "Structural Analysis", "構造分析"),
        "book_label": _text(is_en, "Learning Debian with Claude", "Claudeと一緒に学ぶDebian"),
        "aiways_label": _text(is_en, "AI-Native Ways of Working", "AIネイティブな仕事の作法"),
        "farming_base": "/en/phosphorus-and-farming" if is_en else "/phosphorus-and-farming",
        "farming_label": _text(is_en, "Phosphorus Depletion and Natural Farming", "リン資源枯渇と自然農法"),
        "aiways_base": "/en/ai-native-ways" if is_en else "/ai-native-ways",
        "insights_base": "/en/insights" if is_en else "/insights",
        "blog_base": "/en/blog" if is_en else "/blog",
        "book_base": book_base,
        "css_path": "../../css/style.css" if is_en else "../css/style.css",
        "js_path": "../../js/main.js" if is_en else "../js/main.js",

        "asset_version": config.asset_version(),
        "img_path": "../../images/IMG_3285.jpg" if is_en else "../images/IMG_3285.jpg",
        "meta_description": _text(is_en,
            "A new kind of textbook you read with Claude beside you. Learn the migration to Debian through dialogue, tailored to your own situation.",
            "Claudeを横に置いて読む新しい形の教科書。Debianへの移行を、対話を通じて自分の状況に合わせて学ぶ。"),
        "structural_analysis_label": book_title,
        "page_title": book_title,
        "page_subtitle": _text(is_en,
            "A textbook you dialogue with, not just read",
            "読むのではなく、対話する教科書"),
        "other_lang_link": (_BOOK_BASE_JA + "/") if is_en else (_BOOK_BASE_EN + "/"),
        "other_lang_text": _text(is_en, "日本語版はこちら →", "English version available →") if has_translation else "",
        "lang_switch_label": "日本語" if is_en else "EN",
        "lang_switch_hreflang": "ja" if is_en else "en",
        "lang_switch_aria": "日本語版を表示" if is_en else "View in English",
        "series_title": _text(is_en, "All 24 chapters", "全24章"),
        "series_description": _text(is_en,
            "From the prologue through Chapter 23. At the end of each chapter, you type your own situation into Claude before moving on.",
            "序章から第23章まで。各章の末尾で、Claudeに自分の状況を打ち込んでから次に進む。"),
        "article_list_html": chapter_list_html,
        "intro_html": _text(is_en,
            "Open Claude beside the textbook as you read.<br>\n                    "
            "Type in your situation, get answers fitted to you.<br>\n                    "
            "The same book becomes different learning for every reader — that is the premise of this book.",
            "教科書を読みながら、横でClaudeを開く。<br>\n                    "
            "あなたの状況を打ち込み、自分専用の答えを得る。<br>\n                    "
            "同じ本でも、人によって学びが変わる——それがこの本の前提だ。"),
        "method_title": _text(is_en, "How to read", "読み方"),
        "method_html": _text(is_en,
            "At the end of each chapter, type your own situation into Claude before moving on.<br>\n                    "
            "Reading abstractions alone doesn't stick. Only once you translate them into your own words do they become knowledge.",
            "各章の末尾で、自分の状況を Claude に打ち込んでから次に進む。<br>\n                    "
            "抽象論を読むだけでは身につかない。自分の言葉に翻訳して初めて知識になる。"),
        "quote_html": _text(is_en,
            "Instead of handing over answers, hand over the craft of asking questions.<br>\n"
            "In the era of learning with Claude, that is the longest-lasting gift.",
            "答えを渡すのではなく、問いを立てる作法を渡す。<br>\n"
            "それがClaudeと一緒に学ぶ時代の、最も長く残るギフトになる。"),
        "cta_title": _text(is_en, "Start reading", "始める"),
        "cta_html": _text(is_en,
            "Start from the prologue and read together.<br>\n"
            'When you\'re stuck, just ask Claude: "Given what I\'ve read so far, what should I do?"',
            "序章から、一緒に読み始めよう。<br>\n"
            "迷ったら、Claude に「ここまで読んで、自分はどうすべきか」と聞けばいい。"),
        "footer_about": _text(is_en,
            "AI changes how we work, farm, and live. Structural analysis of fossil resources, "
            "food, energy, AI, healthcare, and pensions — every structure connects.",
            "AIが仕事、農業、暮らしを変える。化石資源、食料、エネルギー、AI、医療、年金——全ての構造は一つに繋がっている。"),
        "copyright_text": config.site_text("copyright_text", lang, _text(is_en, "Living in the AI Era — aiseed.dev", "AI時代の暮らし")),
        # SEO
        "canonical_url": f"{config.SITE_URL}{book_base}/",
        "hreflang_ja": f"{config.SITE_URL}{_BOOK_BASE_JA}/",
        "hreflang_en": f"{config.SITE_URL}{_BOOK_BASE_EN}/" if has_translation else "",
        "og_locale": "en_US" if is_en else "ja_JP",
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

        "asset_version": config.asset_version(),
        # Reuse the generated og-image.jpg (same dir) as the page-hero background.
        "img_path": "og-image.jpg" if meta.get("hero_image") else (
            "../../../images/IMG_3285.jpg" if is_en else "../../images/IMG_3285.jpg"
        ),
        "insights_base": "/en/insights" if is_en else "/insights",
        "blog_base": "/en/blog" if is_en else "/blog",
        "book_base": "/en/claude-debian" if is_en else "/claude-debian",
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
        "privacy_link": "/en/privacy/" if is_en else "/privacy/",
        "privacy_label": _text(is_en, "Privacy", "プライバシー"),
        "insights_label": "Insights",
        "articles_parent_label": _text(is_en, "Articles", "記事"),
        "insights_child_label": _text(is_en, "Structural Analysis", "構造分析"),
        "book_label": _text(is_en, "Learning Debian with Claude", "Claudeと一緒に学ぶDebian"),
        "aiways_label": _text(is_en, "AI-Native Ways of Working", "AIネイティブな仕事の作法"),
        "farming_base": "/en/phosphorus-and-farming" if is_en else "/phosphorus-and-farming",
        "farming_label": _text(is_en, "Phosphorus Depletion and Natural Farming", "リン資源枯渇と自然農法"),
        "aiways_base": "/en/ai-native-ways" if is_en else "/ai-native-ways",
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
        "privacy_link": "/en/privacy/" if is_en else "/privacy/",
        "privacy_label": _text(is_en, "Privacy", "プライバシー"),
        "menu_label": _text(is_en, "Menu", "メニュー"),
        "pages_label": _text(is_en, "Pages", "ページ"),
        "links_label": _text(is_en, "Links", "関連リンク"),
        "articles_parent_label": _text(is_en, "Articles", "記事"),
        "insights_child_label": _text(is_en, "Structural Analysis", "構造分析"),
        "book_label": _text(is_en, "Learning Debian with Claude", "Claudeと一緒に学ぶDebian"),
        "aiways_label": _text(is_en, "AI-Native Ways of Working", "AIネイティブな仕事の作法"),
        "farming_base": "/en/phosphorus-and-farming" if is_en else "/phosphorus-and-farming",
        "farming_label": _text(is_en, "Phosphorus Depletion and Natural Farming", "リン資源枯渇と自然農法"),
        "aiways_base": "/en/ai-native-ways" if is_en else "/ai-native-ways",
        "insights_base": "/en/insights" if is_en else "/insights",
        "blog_base": "/en/blog" if is_en else "/blog",
        "book_base": "/en/claude-debian" if is_en else "/claude-debian",
        "css_path": "../../css/style.css" if is_en else "../css/style.css",
        "js_path": "../../js/main.js" if is_en else "../js/main.js",

        "asset_version": config.asset_version(),
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
