#!/usr/bin/env python3
"""新旧サイトのビルド出力を突き合わせて移行の正しさを機械検証する。

    python3 tools/verify_migration.py <旧html> <新html> [--report verify.txt]

判定基準(HTMLのバイト一致ではない——レンダラが替わるので当然差が出る):
  1. URL一致(必須): index.html の相対パス集合が新旧で同一。sitemap.xml の
     URL集合も同一。
  2. メタデータ一致(必須): 各ページの <title>、meta description、canonical、
     hreflang、og:title/og:image/og:url、prev/next の rel リンク。
  3. 本文テキスト一致: <body> の可視テキストを空白正規化して比較。
     verify-allowlist.txt(1行 = <相対パス><TAB><理由>)にある差は許容。
  4. 資産一致(必須): 各出力ディレクトリの非HTMLファイル名が同一で、
     サイズ差が2%以内(og-image.jpg は Pillow の再エンコードで数%変わる
     ことがあるため 5% まで許容)。

終了コード 0=全一致(許容込み)、1=差分あり。詳細は --report ファイルへ。
"""

import argparse
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class _TextExtractor(HTMLParser):
    """<body> の可視テキスト抽出(script/style は除外)。"""

    def __init__(self):
        super().__init__()
        self.chunks = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag == "br":
            self.chunks.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.chunks.append(data)


def visible_text(html_text):
    m = re.search(r"<body[^>]*>(.*)</body>", html_text, re.DOTALL)
    body = m.group(1) if m else html_text
    p = _TextExtractor()
    p.feed(body)
    # 連結は空白を足さずに行う——インラインタグの境界(<code>や<strong>)に
    # 擬似的な空白を作ると、タグ構造の違いだけで本文差分に見えてしまう。
    # ブロック要素の境界はHTMLソース側の改行が空白として残る。
    text = "".join(p.chunks)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


_META_PATTERNS = {
    "title": re.compile(r"<title>(.*?)</title>", re.DOTALL),
    "description": re.compile(
        r'<meta\s+name="description"\s+content="([^"]*)"'
    ),
    "canonical": re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"'),
    "og:title": re.compile(r'<meta\s+property="og:title"\s+content="([^"]*)"'),
    "og:image": re.compile(r'<meta\s+property="og:image"\s+content="([^"]*)"'),
    "og:url": re.compile(r'<meta\s+property="og:url"\s+content="([^"]*)"'),
}
_HREFLANG_RE = re.compile(r'<link\s+rel="alternate"\s+hreflang="([^"]*)"\s+href="([^"]*)"')
_RELNAV_RE = re.compile(r'<link\s+rel="(prev|next)"\s+href="([^"]*)"')


def page_meta(html_text):
    meta = {}
    for key, pat in _META_PATTERNS.items():
        m = pat.search(html_text)
        meta[key] = m.group(1).strip() if m else ""
    meta["hreflang"] = sorted(_HREFLANG_RE.findall(html_text))
    meta["relnav"] = sorted(_RELNAV_RE.findall(html_text))
    return meta


def sitemap_urls(root):
    f = root / "sitemap.xml"
    if not f.exists():
        return set()
    return set(re.findall(r"<loc>(.*?)</loc>", f.read_text(encoding="utf-8")))


def load_allowlist(path):
    allow = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            rel, _, reason = line.partition("\t")
            allow[rel.strip()] = reason.strip() or "(理由未記入)"
    return allow


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("old_html")
    ap.add_argument("new_html")
    ap.add_argument("--report", default="verify.txt")
    args = ap.parse_args()

    old_root = Path(args.old_html).resolve()
    new_root = Path(args.new_html).resolve()
    allow = load_allowlist(Path(__file__).parent.parent / "verify-allowlist.txt")

    # 比較対象は記事系統の名前空間のみ(creativeweb/ 等のミラーアーカイブや
    # 手書き静的ページは移行対象外)。トップの index.html は
    # update_home_latest_posts が触るので含める。
    series = (
        "insights", "blog", "claude-debian", "ai-native-ways",
        "phosphorus-and-farming", "fable",
    )
    prefixes = tuple(f"{s}/" for s in series) + tuple(f"en/{s}/" for s in series)

    def in_scope(rel):
        return rel == "index.html" or rel.startswith(prefixes)

    hard = []      # 必須基準の違反
    text_diffs = []  # 本文テキスト差(allowlist対象外のもの)
    allowed_used = []
    notes = []

    old_pages = {r for p in old_root.rglob("index.html")
                 if in_scope(r := p.relative_to(old_root).as_posix())}
    new_pages = {r for p in new_root.rglob("index.html")
                 if in_scope(r := p.relative_to(new_root).as_posix())}
    for missing in sorted(old_pages - new_pages):
        hard.append(f"ページ欠落(新に無い): {missing}")
    for extra in sorted(new_pages - old_pages):
        hard.append(f"ページ過剰(旧に無い): {extra}")

    def sm_in_scope(url):
        path = re.sub(r"^https?://[^/]+/", "", url)
        return in_scope(path.rstrip("/") + "/index.html") if path else False

    old_sm = {u for u in sitemap_urls(old_root) if sm_in_scope(u)}
    new_sm = {u for u in sitemap_urls(new_root) if sm_in_scope(u)}
    for u in sorted(old_sm - new_sm):
        hard.append(f"sitemap欠落: {u}")
    for u in sorted(new_sm - old_sm):
        hard.append(f"sitemap過剰: {u}")

    n_meta_ok = n_text_ok = 0
    for rel in sorted(old_pages & new_pages):
        ot = (old_root / rel).read_text(encoding="utf-8", errors="replace")
        nt = (new_root / rel).read_text(encoding="utf-8", errors="replace")

        om, nm = page_meta(ot), page_meta(nt)
        page_meta_ok = True
        for key in om:
            if om[key] != nm[key]:
                hard.append(f"メタ不一致 {rel} [{key}]: 旧={om[key]!r} 新={nm[key]!r}")
                page_meta_ok = False
        if page_meta_ok:
            n_meta_ok += 1

        o_text, n_text = visible_text(ot), visible_text(nt)
        if o_text == n_text:
            n_text_ok += 1
        elif rel in allow:
            allowed_used.append(f"{rel}: {allow[rel]}")
        else:
            # 差の位置を出す(最初の不一致点の前後)
            k = next(
                (j for j, (a, b) in enumerate(zip(o_text, n_text)) if a != b),
                min(len(o_text), len(n_text)),
            )
            text_diffs.append(
                f"本文差分 {rel}:\n    旧: …{o_text[max(0, k-40):k+80]}…\n    新: …{n_text[max(0, k-40):k+80]}…"
            )

    # 資産(非HTML)の一致
    def asset_map(root):
        out = {}
        for p in root.rglob("*"):
            rel = p.relative_to(root).as_posix()
            if (p.is_file() and in_scope_asset(rel)
                    and p.suffix.lower() != ".html"):
                out[rel] = p.stat().st_size
        return out

    def in_scope_asset(rel):
        return rel.startswith(prefixes)

    old_assets, new_assets = asset_map(old_root), asset_map(new_root)
    for rel in sorted(old_assets.keys() - new_assets.keys()):
        hard.append(f"資産欠落: {rel}")
    for rel in sorted(new_assets.keys() - old_assets.keys()):
        notes.append(f"資産過剰(新のみ): {rel}")
    for rel in sorted(old_assets.keys() & new_assets.keys()):
        os_, ns_ = old_assets[rel], new_assets[rel]
        tol = 0.05 if rel.endswith("og-image.jpg") else 0.02
        if os_ and abs(ns_ - os_) / os_ > tol:
            hard.append(f"資産サイズ差 {rel}: 旧={os_} 新={ns_}")

    lines = []
    lines.append(f"共通ページ: {len(old_pages & new_pages)} / メタ一致: {n_meta_ok} / 本文一致: {n_text_ok}")
    if allowed_used:
        lines.append(f"\n許容済みの本文差 ({len(allowed_used)}):")
        lines += [f"  {a}" for a in allowed_used]
    if hard:
        lines.append(f"\n必須基準の違反 ({len(hard)}):")
        lines += [f"  {h}" for h in hard]
    if text_diffs:
        lines.append(f"\n本文テキスト差分 ({len(text_diffs)}):")
        lines += [f"  {t}" for t in text_diffs]
    if notes:
        lines.append(f"\n参考 ({len(notes)}):")
        lines += [f"  {n}" for n in notes]

    ok = not hard and not text_diffs
    lines.append("\n結果: " + ("合格" if ok else "不合格"))
    report = "\n".join(lines)
    Path(args.report).write_text(report + "\n", encoding="utf-8")
    print(report if len(report) < 8000 else "\n".join(lines[:60]) + f"\n…(全文は {args.report})")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
