#!/usr/bin/env python3
"""
Vegitage — 野菜辞典 静的サイトビルダー

作物ごとフォルダー構造を入力として静的 HTML を生成する。

入力:
  data/deep_research/<category>/
    ├── _categories.yaml  (任意 — 植物学的カテゴリ分類)
    └── <crop>/
        ├── history.md        (必須)
        ├── cultivation.md    (任意)
        ├── cuisine.md        (任意)
        ├── meta.yaml         (任意 — 学名・サブタイトル・hero 画像)
        ├── images/           (任意 — 画像ファイルを丸ごとコピー)
        └── resources/        (任意 — 原稿の素材。ビルドでは無視される)

出力:
  <OUT>/<category>/
    ├── index.html        (カテゴリ一覧)
    ├── style.css
    ├── <crop>/
    │   ├── index.html    (歴史)
    │   ├── cultivation.html
    │   ├── cuisine.html
    │   └── images/       (入力の images/ を丸ごとコピー)

Usage:
  python scripts/build.py                    # 出力先: ../html/vegitage/
  python scripts/build.py --out PATH         # 出力先を指定
  python scripts/build.py --category italian # カテゴリを指定
  python scripts/build.py --clean            # 出力先をクリーンアップしてからビルド
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

try:
    import markdown
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.toc import TocExtension
except ImportError:
    print("エラー: markdown パッケージが必要です。  pip install markdown")
    sys.exit(1)

try:
    import yaml  # type: ignore

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ── Paths ──────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent  # vegitage-data/
DEEP_RESEARCH_DIR = ROOT / "data" / "deep_research"
STATIC_DIR = ROOT / "static"
DEFAULT_OUT_DIR = ROOT.parent / "html" / "vegitage"


# ── Categories ────────────────────────────────────────
CATEGORIES = {
    "italian": {
        "title": "イタリア野菜図鑑",
        "subtitle": "Le Verdure Italiane — 地中海の恵みと食文化の物語",
        "description": "イタリア各地の風土と歴史が育んだ伝統野菜を紹介します。",
        "nav_label": "イタリア野菜一覧",
        "footer": "イタリア伝統野菜・料理データベース",
    },
}

# サブガイド定義: (source_filename, output_filename, guide_type_label)
SUBGUIDES = [
    ("cultivation.md", "cultivation.html", "栽培ガイド"),
    ("cuisine.md", "cuisine.html", "料理ガイド"),
]

# ガイドナビのボタン定義: (kind, label, filename)
# kind: "history" | "cultivation" | "cuisine"
GUIDE_NAV = [
    ("history", "歴史", "index.html"),
    ("cultivation", "栽培", "cultivation.html"),
    ("cuisine", "料理", "cuisine.html"),
]


# ── Markdown converter ─────────────────────────────────
def make_markdown() -> markdown.Markdown:
    return markdown.Markdown(
        extensions=[
            TableExtension(),
            TocExtension(
                toc_depth="2-3",
                slugify=lambda value, separator: re.sub(
                    r"\s+", separator, value.strip().lower()
                ),
            ),
            "markdown.extensions.fenced_code",
            "markdown.extensions.nl2br",
        ],
        output_format="html",
    )


# ── Deep Research MD のクレンジング ───────────────────
_CITATION_RE = re.compile(r"\s+\d+(?=[\s。、．，.,\)])")
_BOLD_HEADING_RE = re.compile(
    r"^(#{2,})\s*\*\*(?:\d+[\.\s]*)?(.+?)\*\*\s*$", re.MULTILINE
)
_ESCAPED_NUM_HEADING_RE = re.compile(r"^(#{2,})\s*(?:\d*)\\\.\s*", re.MULTILINE)
_NUMBERED_BOLD_RE = re.compile(r"\*\*(\d+[\.\d]*\s*)")


def clean_deep_research(md_text: str) -> str:
    """Deep Research 生 MD の軽いクレンジング（見出し正規化・citation 除去）。"""
    text = _BOLD_HEADING_RE.sub(
        lambda m: f"{m.group(1)} {m.group(2).strip()}", md_text
    )
    text = _ESCAPED_NUM_HEADING_RE.sub(r"\1 ", text)
    text = _NUMBERED_BOLD_RE.sub("", text)
    text = _CITATION_RE.sub("", text)
    return text


# ── メタデータ ─────────────────────────────────────────
def load_meta(crop_dir: Path, history_text: str) -> dict:
    """meta.yaml があれば読み、無ければ history.md から抽出する。

    返り値: {
      "title":      "イタリアのそば",       # h1 タイトル
      "short_name": "そば",                # カードに表示する名前
      "latin":      "Fagopyrum esculentum",
      "subtitle":   "アルプス山岳地域の「黒い穀物」",
      "hero_image": "images/hero.jpg" | None,
    }
    """
    crop_name = crop_dir.name
    meta: dict = {}

    # meta.yaml 優先
    meta_path = crop_dir / "meta.yaml"
    if meta_path.exists() and HAS_YAML:
        with open(meta_path, encoding="utf-8") as f:
            meta = yaml.safe_load(f) or {}

    # history.md の先頭からフォールバック抽出
    lines = history_text.strip().split("\n")
    h1_title = ""
    subtitle_line = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not h1_title:
            h1_title = stripped[2:].strip()
        elif (
            stripped
            and not stripped.startswith("#")
            and stripped != "---"
            and h1_title
            and not subtitle_line
        ):
            subtitle_line = stripped
            break

    latin_fallback = ""
    subtitle_fallback = ""
    if subtitle_line:
        m = re.search(r"\*([^*]+)\*", subtitle_line)
        if m:
            latin_fallback = m.group(1)
        m2 = re.search(r"—\s*(.+)", subtitle_line)
        if m2:
            subtitle_fallback = m2.group(1).strip()

    title = meta.get("title") or h1_title or f"イタリアの{crop_name}"
    short_name = meta.get("name_ja") or title.replace("イタリアの", "") or crop_name
    latin = meta.get("name_latin") or latin_fallback
    subtitle = meta.get("subtitle") or subtitle_fallback

    hero_image = meta.get("hero_image")
    if not hero_image:
        # images/hero.* が存在すれば自動検出
        for ext in ("jpg", "jpeg", "png", "webp"):
            candidate = crop_dir / "images" / f"hero.{ext}"
            if candidate.exists():
                hero_image = f"images/hero.{ext}"
                break

    return {
        "title": title,
        "short_name": short_name,
        "latin": latin,
        "subtitle": subtitle,
        "hero_image": hero_image,
    }


# ── HTML 変換ヘルパ ────────────────────────────────────
def convert_md_links(html: str) -> str:
    return re.sub(r'href="([^"]*?)\.md"', r'href="\1.html"', html)


def wrap_tables(html: str) -> str:
    return html.replace("<table>", '<div class="table-wrapper"><table>').replace(
        "</table>", "</table></div>"
    )


def build_article_body(
    md_converter: markdown.Markdown, md_text: str
) -> tuple[str, str]:
    md_converter.reset()
    html_body = md_converter.convert(md_text)
    html_body = convert_md_links(html_body)
    html_body = wrap_tables(html_body)
    return html_body, md_converter.toc


# ── ガイドナビ ─────────────────────────────────────────
def build_guide_nav(current: str, available: set[str]) -> str:
    """歴史・栽培・料理のボタン列（同一フォルダー内リンク）。"""
    buttons = []
    for kind, label, filename in GUIDE_NAV:
        if kind == current:
            buttons.append(f'<span class="guide-nav-current">{label}</span>')
        elif kind == "history" or kind in available:
            buttons.append(f'<a href="{filename}">{label}</a>')
    return '<nav class="guide-nav">' + "".join(buttons) + "</nav>"


# ── 2カラムレイアウト ────────────────────────────────
def wrap_two_column(
    article_html: str, toc_html: str, guide_nav: str, back_link: str
) -> str:
    sidebar = f"""<aside class="sidebar">
  <div class="sidebar-toc">
    <h2 class="sidebar-heading">目次</h2>
    {toc_html}
  </div>
  <div class="sidebar-ad">
    <!-- AdSense placeholder -->
  </div>
</aside>"""
    return f"""{guide_nav}
<div class="two-column">
  <div class="column-main">
    <article class="article-content">
{article_html}
    </article>
    {back_link}
  </div>
  {sidebar}
</div>"""


# ── ページテンプレート ─────────────────────────────────
def html_page(
    title: str,
    body: str,
    cat: dict,
    css_path: str,
    index_path: str,
) -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Vegitage</title>
<link rel="stylesheet" href="{css_path}">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-6V2KRRWHS8"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-6V2KRRWHS8');
</script>
</head>
<body>

<header class="site-header">
  <div class="site-header-inner">
    <a href="{index_path}" class="site-logo">Vegitage</a>
    <nav class="site-nav">
      <a href="{index_path}">{cat["nav_label"]}</a>
    </nav>
  </div>
</header>

<main class="container">
{body}
</main>

<footer class="site-footer">
  <p>Vegitage — {cat["footer"]}</p>
  <p>データは <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.ja">CC BY-SA 4.0</a> で提供されています。</p>
</footer>

</body>
</html>"""


# ── サブガイドの前処理 ───────────────────────────────
def preprocess_subguide(md_text: str, veg_name: str, guide_type_label: str) -> str:
    """サブガイド MD の見出し正規化: プリアンブル除去 + h1 統一。"""
    lines = md_text.split("\n")
    start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "---" or stripped.startswith("# "):
            start = i
            break
    if start < len(lines) and lines[start].strip() == "---":
        start += 1
    while start < len(lines) and not lines[start].strip():
        start += 1

    body_lines = lines[start:]
    new_title = f"# {veg_name}{guide_type_label}"
    for i, line in enumerate(body_lines):
        if line.strip().startswith("# "):
            body_lines[i] = new_title
            break
    return "\n".join(body_lines)


# ── 作物単位のビルド ────────────────────────────────
def build_crop(
    md_converter: markdown.Markdown,
    crop_dir: Path,
    out_dir: Path,
    cat: dict,
) -> dict | None:
    """1つの作物フォルダーをビルドしメタ情報を返す。"""
    crop_name = crop_dir.name
    history_path = crop_dir / "history.md"
    if not history_path.exists():
        print(f"  ✗ {crop_name}: history.md が見つかりません")
        return None

    # 出力ディレクトリ
    crop_out = out_dir / crop_name
    crop_out.mkdir(parents=True, exist_ok=True)

    # 画像コピー
    images_src = crop_dir / "images"
    if images_src.exists():
        images_dst = crop_out / "images"
        if images_dst.exists():
            shutil.rmtree(images_dst)
        shutil.copytree(images_src, images_dst)

    # メタ情報抽出（history.md 読み込み）
    history_raw = history_path.read_text(encoding="utf-8")
    meta = load_meta(crop_dir, history_raw)

    # どのサブガイドが存在するか
    available: set[str] = set()
    for src_name, _out_name, _label in SUBGUIDES:
        if (crop_dir / src_name).exists():
            available.add(src_name.replace(".md", ""))  # "cultivation" / "cuisine"

    # ── 歴史 (index.html) ────────────────────────────
    history_text = clean_deep_research(history_raw)
    history_html, history_toc = build_article_body(md_converter, history_text)
    guide_nav = build_guide_nav(current="history", available=available)
    back_link = (
        f'<a href="../index.html" class="back-link">← {cat["nav_label"]}に戻る</a>'
    )
    content = wrap_two_column(history_html, history_toc, guide_nav, back_link)
    (crop_out / "index.html").write_text(
        html_page(
            meta["title"],
            content,
            cat,
            css_path="../style.css",
            index_path="../index.html",
        ),
        encoding="utf-8",
    )

    # ── サブガイド ──────────────────────────────────
    for src_name, out_name, label in SUBGUIDES:
        src_path = crop_dir / src_name
        if not src_path.exists():
            continue
        kind = src_name.replace(".md", "")
        text = src_path.read_text(encoding="utf-8")
        text = clean_deep_research(text)
        text = preprocess_subguide(text, crop_name, label)

        html_body, toc_html = build_article_body(md_converter, text)
        sub_nav = build_guide_nav(current=kind, available=available)
        sub_content = wrap_two_column(html_body, toc_html, sub_nav, back_link)

        title = f"{crop_name}{label}"
        (crop_out / out_name).write_text(
            html_page(
                title,
                sub_content,
                cat,
                css_path="../style.css",
                index_path="../index.html",
            ),
            encoding="utf-8",
        )

    return {
        "crop_name": crop_name,
        "short_name": meta["short_name"],
        "latin": meta["latin"],
        "subtitle": meta["subtitle"],
        "hero_image": meta["hero_image"],
        "url": f"{crop_name}/",
    }


# ── カテゴリ分類の読み込み ────────────────────────
def load_category_groups(src_dir: Path) -> list[dict] | None:
    """_categories.yaml を読んで植物学的カテゴリ分類を返す。

    ファイルが無い・PyYAML 未インストールの場合は None を返し、
    呼び出し側は単一グループとしてフラット描画する。
    """
    path = src_dir / "_categories.yaml"
    if not path.exists() or not HAS_YAML:
        return None
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("categories") or None


# ── カード描画 ────────────────────────────────────
def render_card(c: dict) -> str:
    name = c["short_name"]
    latin = c["latin"]
    subtitle = c["subtitle"]
    url = c["url"]
    hero = c["hero_image"]
    if hero:
        img_html = (
            f'<div class="card-image">'
            f'<img src="{c["crop_name"]}/{hero}" alt="{name}" loading="lazy">'
            f"</div>\n"
        )
    else:
        img_html = ""
    return (
        f'<a href="{url}" class="vegetable-card">\n'
        f"  {img_html}"
        f'  <div class="card-name">{name}</div>\n'
        f'  <div class="card-latin">{latin}</div>\n'
        f'  <div class="card-desc">{subtitle}</div>\n'
        f"</a>"
    )


# ── カテゴリ一覧ページ ────────────────────────────
def build_index(
    crops: list[dict],
    out_dir: Path,
    cat: dict,
    category_groups: list[dict] | None,
) -> None:
    crops.sort(key=lambda c: c["short_name"])
    crop_by_name = {c["crop_name"]: c for c in crops}

    sections_html: list[str] = []
    toc_links: list[str] = []
    used: set[str] = set()

    if category_groups:
        for group in category_groups:
            key = group.get("key", "")
            label = group.get("label", "")
            description = group.get("description", "")
            names = group.get("crops", []) or []

            section_crops = [crop_by_name[n] for n in names if n in crop_by_name]
            if not section_crops:
                continue
            used.update(c["crop_name"] for c in section_crops)
            section_crops.sort(key=lambda c: c["short_name"])

            cards_html = "\n".join(render_card(c) for c in section_crops)
            desc_html = (
                f'  <p class="category-desc">{description}</p>\n' if description else ""
            )
            sections_html.append(
                f'<section class="category-section" id="cat-{key}">\n'
                f'  <h2 class="category-heading">{label} '
                f'<span class="category-count">({len(section_crops)})</span></h2>\n'
                f"{desc_html}"
                f'  <div class="vegetable-grid">\n{cards_html}\n  </div>\n'
                f"</section>"
            )
            toc_links.append(
                f'<a href="#cat-{key}" class="category-toc-link">'
                f'{label} <span>({len(section_crops)})</span></a>'
            )

    # カテゴリに分類されていない作物は「その他」に集約
    uncategorized = [c for c in crops if c["crop_name"] not in used]
    if uncategorized:
        uncategorized.sort(key=lambda c: c["short_name"])
        cards_html = "\n".join(render_card(c) for c in uncategorized)
        sections_html.append(
            f'<section class="category-section" id="cat-other">\n'
            f'  <h2 class="category-heading">その他 '
            f'<span class="category-count">({len(uncategorized)})</span></h2>\n'
            f'  <div class="vegetable-grid">\n{cards_html}\n  </div>\n'
            f"</section>"
        )
        toc_links.append(
            f'<a href="#cat-other" class="category-toc-link">'
            f'その他 <span>({len(uncategorized)})</span></a>'
        )
        print(
            f"  注意: カテゴリ未分類の作物が {len(uncategorized)} 件あります: "
            f"{', '.join(c['crop_name'] for c in uncategorized)}"
        )

    # カテゴリ分類が存在しない（_categories.yaml が無い）場合のフォールバック：
    # 従来通り単一グリッドでフラット表示する。
    if not category_groups and not sections_html:
        cards_html = "\n".join(render_card(c) for c in crops)
        sections_html.append(f'<div class="vegetable-grid">\n{cards_html}\n</div>')

    toc_html = ""
    if toc_links:
        toc_html = (
            '<nav class="category-toc">\n'
            + "\n".join(toc_links)
            + "\n</nav>\n"
        )

    group_count = sum(1 for s in sections_html)
    body = f"""<div class="index-hero">
  <h1>{cat["title"]}</h1>
  <p class="subtitle">{cat["subtitle"]}</p>
</div>

<p class="index-description">
  {cat["description"]}<br>
  DOP・IGP認定品種から地方の在来品種まで、{group_count}分類・{len(crops)}種の野菜の世界をお楽しみください。
</p>

{toc_html}
{"".join(sections_html)}
"""
    (out_dir / "index.html").write_text(
        html_page(
            cat["title"],
            body,
            cat,
            css_path="style.css",
            index_path="index.html",
        ),
        encoding="utf-8",
    )


# ── カテゴリ単位のビルド ────────────────────────────
def build_category(
    md_converter: markdown.Markdown,
    cat_key: str,
    cat: dict,
    src_dir: Path,
    out_dir: Path,
) -> int:
    if not src_dir.exists():
        print(f"[{cat_key}] ソースディレクトリが見つかりません: {src_dir}")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)

    # style.css をコピー
    style_src = STATIC_DIR / "style.css"
    if style_src.exists():
        shutil.copy2(style_src, out_dir / "style.css")

    # カテゴリ分類の読み込み
    category_groups = load_category_groups(src_dir)

    # 作物フォルダー一覧（name のアルファベット順ではなく発見順で処理し、最後にソート）
    crop_dirs = sorted(d for d in src_dir.iterdir() if d.is_dir())
    print(f"\n[{cat_key}] {cat['title']}: {len(crop_dirs)} 作物")
    if category_groups:
        print(f"  分類: {len(category_groups)} カテゴリ (_categories.yaml)")

    crops: list[dict] = []
    for crop_dir in crop_dirs:
        meta = build_crop(md_converter, crop_dir, out_dir, cat)
        if meta:
            crops.append(meta)
            subs = []
            if (crop_dir / "cultivation.md").exists():
                subs.append("cultivation")
            if (crop_dir / "cuisine.md").exists():
                subs.append("cuisine")
            suffix = f" (+{','.join(subs)})" if subs else ""
            print(f"  ✓ {crop_dir.name}/{suffix}")

    build_index(crops, out_dir, cat, category_groups)
    print(f"  ✓ {cat_key}/index.html (一覧ページ, {len(crops)} 作物)")

    # 作物数 * (1 history + サブガイド数) + 1 index
    total_pages = sum(
        1
        + sum(1 for src, _, _ in SUBGUIDES if (src_dir / c["crop_name"] / src).exists())
        for c in crops
    ) + 1
    return total_pages


# ── main ───────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Vegitage 静的サイトビルダー")
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help=f"出力先ディレクトリ（デフォルト: {DEFAULT_OUT_DIR}）",
    )
    parser.add_argument(
        "--category",
        action="append",
        choices=sorted(CATEGORIES.keys()),
        help="ビルドするカテゴリ（省略時は全て）",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="既存の出力先を削除してから生成する",
    )
    args = parser.parse_args()

    out_root: Path = args.out.resolve()
    categories = args.category or list(CATEGORIES.keys())

    print(f"入力: {DEEP_RESEARCH_DIR.relative_to(ROOT)}/")
    print(f"出力: {out_root}")
    print(f"対象カテゴリ: {', '.join(categories)}")
    if not HAS_YAML:
        print("注意: PyYAML がインストールされていないため meta.yaml はスキップされます")

    md_converter = make_markdown()
    total = 0

    for cat_key in categories:
        cat = CATEGORIES[cat_key]
        src_dir = DEEP_RESEARCH_DIR / cat_key
        out_dir = out_root / cat_key

        if args.clean and out_dir.exists():
            shutil.rmtree(out_dir)

        total += build_category(md_converter, cat_key, cat, src_dir, out_dir)

    print(f"\n完了: 約 {total} ファイル生成 → {out_root}")


if __name__ == "__main__":
    main()
