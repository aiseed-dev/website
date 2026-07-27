#!/usr/bin/env python3
"""
creativeweb.jp を aiseed.dev 上の静的アーカイブ (/creativeweb/) に書き出す。

旧サイトは ASP.NET Core MVC + Razor だが、コンテンツは実質静的:
  - シェル(ナビ/フッター)は _BootstrapMaster.cshtml にハードコード
  - 本文は App_Data/html/**.html のフラグメント
  - メタ情報は App_Data/config/*.json
このスクリプトは .NET を動かさずにそれらを読み、

  * AdSense と旧 Google Analytics (UA-16580464-4) を一切含めず
  * aiseed の Google Analytics (G-9FLQ963JXM) を注入し
  * すべてのルート絶対パス(/css, /img, /umb, /archive ...)を /creativeweb/ に書き換え

て、website/html/creativeweb/ 配下に静的 HTML として出力する。

除外(ユーザー決定):
  * /learning/ オンライン教室セクション
  * ブログ検索 / お問い合わせフォーム / Disqus コメント (動的機能)

使い方:
    python3 tools/build_creativeweb_archive.py \
        --src /home/niji/dev/aiseed-dev/CreativeWeb/CreativeWeb \
        --out html/creativeweb
"""

import argparse
import html as htmllib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

GA_ID = "G-9FLQ963JXM"          # aiseed の GA4 計測 ID
PREFIX = "/creativeweb"          # アーカイブの配置パス
AISEED_ABOUT = "https://aiseed.dev/about/"

# learning は除外。ナビ/フッターから外し、本文中のリンクが残っても 404 で許容。
EXCLUDE_PARTS = {"learning"}

# ---------------------------------------------------------------------------
# 読み込み
# ---------------------------------------------------------------------------

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


# ---------------------------------------------------------------------------
# リンク / アセットのパス書き換え
# ---------------------------------------------------------------------------

# href="/..." src="/..." を /creativeweb/... に。// と /creativeweb は除外。
_ATTR_RE = re.compile(r'((?:href|src)\s*=\s*["\'])/(?!/|creativeweb)', re.IGNORECASE)
# CSS / インライン style の url(/...) 用
_URL_RE = re.compile(r'url\(\s*([\'"]?)/(?!/|creativeweb)')


def rewrite_paths(text: str) -> str:
    text = text.replace("~/", PREFIX + "/")          # Razor の ~/ アプリルート
    text = _ATTR_RE.sub(r"\1" + PREFIX + "/", text)
    text = _URL_RE.sub(r"url(\1" + PREFIX + "/", text)
    # 旧サイトはルーティングが大文字小文字を無視するが静的配信は区別するため正規化
    text = text.replace(PREFIX + "/Manga/", PREFIX + "/manga/")
    text = text.replace(PREFIX + "/Archive/", PREFIX + "/archive/")
    text = text.replace(PREFIX + "/Blog/", PREFIX + "/blog/")
    return text


# ---------------------------------------------------------------------------
# シェル (head / navbar / footer)
# ---------------------------------------------------------------------------

GA_SNIPPET = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>"""

ARCHIVE_BAR = (
    '<div style="background:#2d2d2d;color:#eee;font-size:13px;text-align:center;'
    'padding:6px 12px;line-height:1.5">\n'
    '  これは <strong>creativeweb.jp</strong> のアーカイブです（'
    '<a href="https://aiseed.dev/" style="color:#9cf">aiseed.dev</a> 上に保存）。'
    'サイトは更新を終了しています。\n'
    '</div>'
)

# ナビ (learning ドロップダウンを除いた Navbar.cshtml の静的版)
NAVBAR = """\
<ul class="nav navbar-nav">
  <li class="dropdown">
    <a href="/aspnet-oss/" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">C# <span class="caret"></span></a>
    <ul class="dropdown-menu">
      <li><a href="/code/aspdotnetcore-linux">ASP.NET Core アプリを Linux で公開</a></li>
      <li><a href="/code/csharp">C# を使おう</a></li>
      <li><a href="/aspnet-oss/excel-tools/">Excel Library</a></li>
    </ul>
  </li>
  <li class="dropdown">
    <a href="/umb/" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Umbraco <span class="caret"></span></a>
    <ul class="dropdown-menu">
      <li><a href="/umb/">Umbracoについて</a></li>
      <li><a href="/umb/umb7azurewebsite/">Azure Web サイトにインストール</a></li>
      <li><a href="/umb/webpi46/">5分間インストール</a></li>
      <li><a href="/umb/install/">インストール</a></li>
      <li><a href="/umb/getting-started/">Web サイトの制作</a></li>
      <li><a href="/umb/publish/">WebMtrix からの発行</a></li>
      <li><a href="/umb/razor/">Razor を使う</a></li>
    </ul>
  </li>
  <li class="dropdown">
    <a href="/fc/" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">SQL Server <span class="caret"></span></a>
    <ul class="dropdown-menu">
      <li><a href="/fc/">SQL Serverについて</a></li>
      <li><a href="/fc/2016-express/">2016 Express</a></li>
      <li><a href="/fc/2014-express/">2014 Express</a></li>
      <li><a href="/fc/2012-express/">2012 Express</a></li>
      <li><a href="/fc/2008-r2/">2008 Express</a></li>
      <li><a href="/fc/web-pi/">Web PI でインストール</a></li>
      <li><a href="/fc/remote/">リモート接続</a></li>
      <li><a href="/fc/apppool-identity/">Windows 認証</a></li>
    </ul>
  </li>
  <li class="dropdown">
    <a href="/personal-site/" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">サーバー <span class="caret"></span></a>
    <ul class="dropdown-menu">
      <li><a href="/server/">サーバ/インフラについて</a></li>
      <li role="separator" class="divider"></li>
      <li><a href="/personal-site/">Windows PC で自宅サーバー</a></li>
      <li><a href="/personal-site/iis/">IIS のインストール</a></li>
      <li><a href="/personal-site/php/">PHP のインストール</a></li>
      <li><a href="/personal-site/mysql/">MySQL のインストール</a></li>
      <li><a href="/personal-site/router/">ルーターの設定</a></li>
      <li role="separator" class="divider"></li>
      <li><a href="/hosting/">Windows レンタルサーバー</a></li>
      <li><a href="/hosting/windows-vps/">Windows VPS</a></li>
      <li><a href="/hosting/amazon-ec2/">Amazon EC2</a></li>
      <li><a href="/server/linux-vps/">低価格 Linux VPS を使う</a></li>
    </ul>
  </li>
  <li><a href="/blog/">ブログ</a></li>
</ul>"""

FOOTER = """\
<footer class="field dark">
  <div class="container">
    <div class="row">
      <div class="hidden-xs col-sm-3">
        <strong>サイトメニュー</strong>
        <ul>
          <li><a href="/manga/webdesigner/page1/">マンガでなれる？WEBデザイナー講座</a></li>
          <li><a href="/aspnet-oss/">プログラム</a></li>
          <li><a href="/umb/">Umbraco</a></li>
        </ul>
      </div>
      <div class="hidden-xs col-sm-3">
        <strong>　</strong>
        <ul>
          <li><a href="/fc/">SQL Server</a></li>
          <li><a href="/collaboration/">共同作業</a></li>
          <li><a href="/personal-site/">サーバー</a></li>
          <li><a href="/blog/">ブログ</a></li>
        </ul>
      </div>
      <div class="col-xs-6 col-sm-3">
        <strong class="hidden-xs">このサイトについて</strong>
        <ul>
          <li><a href="/about/">このサイトについて</a></li>
          <li><a href="/privacypolicy/">プライバシーポリシー</a></li>
        </ul>
      </div>
      <div class="col-xs-6 col-sm-3">
        <strong class="hidden-xs">お問い合わせ</strong>
        <ul>
          <li><a href="%s">お問い合わせ（aiseed.dev）</a></li>
        </ul>
      </div>
    </div>
    <p style="text-align:center;margin-top:10px">Copyright © 2008 - 2025 creativeweb.jp All Rights Reserved.（アーカイブ）</p>
  </div>
</footer>""" % AISEED_ABOUT

HEAD_CSS = """\
<link href="/css/bootstrap-custom-1.0.2.min.css" rel="stylesheet">
<link href="/css/WebStyle-1.0.0.min.css" rel="stylesheet">
<link href="/fonts/font-awesome-4.3.0/css/font-awesome.min.css" rel="stylesheet">
<link href="/css/myfont.css" rel="stylesheet">
<link href="/css/hilite.min.css" rel="stylesheet">"""

BLOG_CSS = """\
<link href="/css/bootstrap-custom-1.0.2.min.css" rel="stylesheet">
<link href="/lib/blog/1.0/css/style2.css" rel="stylesheet">
<link href="/fonts/font-awesome-4.3.0/css/font-awesome.min.css" rel="stylesheet">
<link href="/css/myfont.css" rel="stylesheet">
<link href="/css/hilite.min.css" rel="stylesheet">"""


def page(title: str, body: str, *, head_css: str = HEAD_CSS,
         description: str = "") -> str:
    """完成した 1 ページの HTML を返す（パス書き換え前）。"""
    desc = f'<meta name="description" content="{htmllib.escape(description)}">' if description else ""
    doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/favicon.ico">
<title>{htmllib.escape(title)}</title>
{desc}
{head_css}
{GA_SNIPPET}
</head>
<body>
{ARCHIVE_BAR}
<nav class="navbar navbar-default">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="/"><img src="/images/creativeweb.png" alt="クリエイティブWeb"></a>
    </div>
    <div id="navbar" class="collapse navbar-collapse">
      {NAVBAR}
    </div>
  </div>
</nav>
{body}
{FOOTER}
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script src="/js/bootstrap.min.js"></script>
</body>
</html>"""
    return rewrite_paths(doc)


def write_page(out: Path, rel: str, content: str) -> None:
    dest = out / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# 本文テンプレート断片
# ---------------------------------------------------------------------------

def text_section(title: str, inner_html: str) -> str:
    return f"""<section class="container">
  <h2>{htmllib.escape(title)}</h2>
  <div class="row">
    <div class="col-md-8">
{inner_html}
    </div>
  </div>
</section>"""


def fmt_date(s: str) -> str:
    if not s:
        return ""
    try:
        dt = datetime.fromisoformat(s)
        return f"{dt.year}年{dt.month}月{dt.day}日"
    except ValueError:
        return s


# ---------------------------------------------------------------------------
# 各種ページ生成
# ---------------------------------------------------------------------------

def textpage_rel(pname: str, name: str) -> str:
    if pname == "home" and name == "index":
        return "index.html"
    if name == "index":
        return f"{pname}/index.html"
    return f"{pname}/{name}/index.html"


def redirect_stub(target: str) -> str:
    """meta-refresh のリダイレクト stub（旧サイトの 301 を静的に再現）。
    target は旧サイトのルート絶対パス。/creativeweb/ 配下に正規化する。"""
    t = PREFIX + "/" if target == "/" else PREFIX + target
    doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={t}">
<link rel="canonical" href="{t}">
<title>移動しました</title>
</head>
<body>
<p>このページは <a href="{t}">{t}</a> に移動しました。</p>
</body>
</html>"""
    return doc


def derive_title(inner: str, fallback: str) -> str:
    m = re.search(r"<h[1-3][^>]*>(.*?)</h[1-3]>", inner, re.IGNORECASE | re.DOTALL)
    if m:
        t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if t:
            return t
    return fallback


def build_textpages(src: Path, out: Path, textdata, stats, covered: set):
    html_dir = src / "App_Data" / "html"
    for part in textdata:
        pname = part["Part"]
        if pname in EXCLUDE_PARTS:
            continue
        for tp in part.get("TextPages", []):
            name = tp["Name"]
            covered.add((pname, name))
            rel = textpage_rel(pname, name)
            redirect = tp.get("RedirectUrl")
            if redirect:                       # 旧→新の内部リダイレクトを stub 化
                write_page(out, rel, redirect_stub(redirect))
                stats["redirects"] += 1
                continue
            frag = html_dir / pname / f"{name}.html"
            if not frag.exists():
                continue
            inner = frag.read_text(encoding="utf-8", errors="ignore")
            title = tp.get("Title") or name
            body = text_section(title, inner)
            write_page(out, rel, page(f"{title} - クリエイティブWeb", body))
            stats["textpages"] += 1


# textpage.json に未登録だが実在するフラグメント（孤立ページ）も拾う
ORPHAN_SKIP_PARTS = {"home", "learning", "blog", "manga", "link"}
ORPHAN_SKIP_PAGES = {("about", "index"), ("privacypolicy", "index")}


def build_orphans(src: Path, out: Path, covered: set, stats):
    html_dir = src / "App_Data" / "html"
    for frag in sorted(html_dir.rglob("*.html")):
        parts = frag.relative_to(html_dir).parts
        pname, name = parts[0], frag.stem
        if pname in ORPHAN_SKIP_PARTS or (pname, name) in ORPHAN_SKIP_PAGES:
            continue
        if (pname, name) in covered:
            continue
        inner = frag.read_text(encoding="utf-8", errors="ignore")
        title = derive_title(inner, name)
        body = text_section(title, inner)
        write_page(out, textpage_rel(pname, name),
                   page(f"{title} - クリエイティブWeb", body))
        covered.add((pname, name))
        stats["orphans"] += 1


def extract_cshtml_body(path: Path):
    """About/PrivacyPolicy の .cshtml から本文 HTML と ViewBag.Header を取り出す。"""
    raw = path.read_text(encoding="utf-8-sig", errors="ignore")
    m = re.search(r'ViewBag\.Header\s*=\s*"([^"]+)"', raw)
    header = m.group(1) if m else ""
    body = re.sub(r"@\{[\s\S]*?\}", "", raw, count=1).strip()  # 先頭の @{...} を除去
    return header, body


def build_static_views(src_root: Path, out: Path, stats):
    views = src_root / "Views"
    for rel_view, out_rel in [("About/Index.cshtml", "about/index.html"),
                              ("PrivacyPolicy/Index.cshtml", "privacypolicy/index.html")]:
        p = views / rel_view
        if not p.exists():
            continue
        header, body = extract_cshtml_body(p)
        section = text_section(header, body)
        write_page(out, out_rel, page(f"{header} - クリエイティブWeb", section))
        stats["textpages"] += 1

    # お問い合わせ -> aiseed への案内に差し替え
    contact_body = text_section("お問い合わせ", f"""
<p>creativeweb.jp はアーカイブとして保存されており、フォームでのお問い合わせの受付は終了しました。</p>
<p>ご連絡は <a href="{AISEED_ABOUT}">aiseed.dev のお問い合わせ</a> からお願いします。</p>""")
    write_page(out, "contacts/index.html", page("お問い合わせ - クリエイティブWeb", contact_body))
    stats["textpages"] += 1


def blog_article_html(post, body_html: str) -> str:
    cats = post.get("Categories") or []
    cat_links = " | ".join(
        f"<a href='/blog/categories/{htmllib.escape(c)}/'>{htmllib.escape(c)}</a>" for c in cats)
    cat_block = f'<div class="postfooter box-inner"><span>Categories:</span> {cat_links}</div>' if cat_links else ""
    return f"""<article>
  <a class="title" href="/archive/{post['Name']}/"><h1 class="titulo-articulo">{htmllib.escape(post['Title'])}</h1></a>
  <small class="fecha">{fmt_date(post.get('PublishDate',''))}</small>
  <div class="texto">
{body_html}
  </div>
</article>
{cat_block}"""


def blog_sidebar(categories) -> str:
    cat_items = "".join(
        f'<li><a href="/blog/categories/{htmllib.escape(c)}/">{htmllib.escape(c)}</a></li>'
        for c in categories)
    return f"""<div class="col-md-4">
  <div class="sidenav box small">
    <div class="widgetzone">
      <ul><li><a href="/blog/categories/">ブログ一覧（カテゴリー）</a></li></ul>
      <div class="widget categorylist"><h4>カテゴリー</h4><div class="content"><ul>{cat_items}</ul></div></div>
    </div>
  </div>
</div>"""


def pager(page_no: int, page_max: int) -> str:
    if page_max <= 1:
        return ""
    prev_url = (f"/blog/" if page_no == 2 else f"/blog/page/{page_no-1}/")
    out = ['<div class="pagination" role="pagination">']
    if page_no > 1:
        out.append(f'<a class="newer-posts" href="{prev_url}"><i class="fa fa-chevron-circle-left"></i> 前ページ</a>')
    out.append(f'<span class="page-number"> Page {page_no} of {page_max} </span>')
    if page_no < page_max:
        out.append(f'<a class="older-posts" href="/blog/page/{page_no+1}/">次ページ <i class="fa fa-chevron-circle-right"></i></a>')
    out.append("</div>")
    return "".join(out)


def build_blog(src: Path, out: Path, blogdata, categories, stats):
    blog_dir = src / "App_Data" / "html" / "blog"

    def read_body(post):
        f = blog_dir / post["RedirectUrl"]
        return f.read_text(encoding="utf-8", errors="ignore") if f.exists() else ""

    # 個別記事 /archive/{id}/
    for post in blogdata:
        body = read_body(post)
        cats = post.get("Categories") or []
        cat_links = " | ".join(
            f"<a href='/blog/categories/{htmllib.escape(c)}/'>{htmllib.escape(c)}</a>" for c in cats)
        cat_block = f'<div class="postfooter box-inner"><span>Categories:</span> {cat_links}</div>' if cat_links else ""
        article = f"""<div class="main"><article>
  <h1 class="titulo-articulo">{htmllib.escape(post['Title'])}</h1>
  <small class="fecha">{fmt_date(post.get('PublishDate',''))}</small>
  <div class="texto">
{body}
  </div>
</article>{cat_block}
<p><a href="/blog/">&laquo; ブログ一覧へ戻る</a></p></div>"""
        section = f'<div class="container"><div class="row"><div class="col-md-8">{article}</div>{blog_sidebar(categories)}</div></div>'
        write_page(out, f"archive/{post['Name']}/index.html",
                   page(f"{post['Title']} - クリエイティブWeb", section, head_css=BLOG_CSS))
        stats["blog_posts"] += 1

    # 索引（5件/ページ・新着順）
    page_size = 5
    page_max = (len(blogdata) + page_size - 1) // page_size
    for pno in range(1, page_max + 1):
        chunk = blogdata[(pno-1)*page_size: pno*page_size]
        articles = "\n".join(blog_article_html(p, read_body(p)) for p in chunk)
        main = f'<div class="main"><h4>Webアプリを創る</h4>{articles}{pager(pno, page_max)}</div>'
        section = f'<div class="container"><div class="row"><div class="col-md-8">{main}</div>{blog_sidebar(categories)}</div></div>'
        full = page("Webアプリを創る - クリエイティブWeb", section, head_css=BLOG_CSS)
        rel = "blog/index.html" if pno == 1 else f"blog/page/{pno}/index.html"
        write_page(out, rel, full)
        stats["blog_index"] += 1

    # カテゴリー一覧
    cat_list = "".join(
        f'<li><a href="/blog/categories/{htmllib.escape(c)}/">{htmllib.escape(c)}</a> '
        f'({sum(1 for p in blogdata if c in (p.get("Categories") or []))})</li>'
        for c in categories)
    section = text_section("ブログ カテゴリー", f"<ul>{cat_list}</ul>")
    write_page(out, "blog/categories/index.html",
               page("ブログ カテゴリー - クリエイティブWeb", section, head_css=BLOG_CSS))

    # 各カテゴリー（タイトル一覧）
    for c in categories:
        posts = [p for p in blogdata if c in (p.get("Categories") or [])]
        items = "".join(
            f'<li><small>{fmt_date(p.get("PublishDate",""))}</small> '
            f'<a href="/archive/{p["Name"]}/">{htmllib.escape(p["Title"])}</a></li>'
            for p in posts)
        section = text_section(f"カテゴリー: {c}", f'<ul class="recentPosts">{items}</ul>')
        write_page(out, f"blog/categories/{c}/index.html",
                   page(f"{c} - ブログ - クリエイティブWeb", section, head_css=BLOG_CSS))
        stats["blog_cat"] += 1


def build_manga(src: Path, out: Path, mangadata, stats):
    manga_dir = src / "App_Data" / "html" / "manga"

    # 索引
    panels = []
    for part in mangadata:
        pages = part.get("MangaPages") or []
        if not pages:
            continue
        first = pages[0]
        plinks = "".join(
            f'<p><a href="/manga/{part["Name"]}/{pg["Name"]}/">{htmllib.escape(pg["Title"])}</a></p>'
            for pg in pages)
        panels.append(f"""<div class="panel panel-info">
  <div class="panel-heading"><h3 class="panel-title">{htmllib.escape(part['Title'])}</h3></div>
  <div class="panel-body"><div class="row">
    <div class="col-sm-5"><a href="/manga/{part['Name']}/{first['Name']}/"><img src="/img/manga/{first['ImageUrl']}" class="img-responsive"></a></div>
    <div class="col-sm-7">{plinks}</div>
  </div></div>
</div>""")
    idx_body = f"""<section class="container">
  <img src="/img/manga/manga-top.png" class="img-responsive">
  <div class="manga-header"><h1>マンガでなれる？WEBデザイナー講座</h1></div>
  <p>「マンガでなれる？WEBデザイナー講座」では、現場で求められるWebデザイン制作方法を初心者〜中級者向けに漫画で解説しています。</p>
  {''.join(panels)}
</section>"""
    write_page(out, "manga/index.html",
               page("マンガでなれる？WEBデザイナー講座 - クリエイティブWeb", idx_body))
    stats["manga"] += 1

    # シリーズ索引 /manga/{series}/ （内容リンクと「目次」ボタンの宛先）
    for part in mangadata:
        pages = part.get("MangaPages") or []
        if not pages:
            continue
        items = "".join(
            f'<p><a href="/manga/{part["Name"]}/{pg["Name"]}/">{htmllib.escape(pg["Title"])}</a></p>'
            for pg in pages)
        body = f"""<section class="container">
  <div class="row"><div class="col-md-10 col-md-offset-1">
    <div class="panel panel-info">
      <div class="panel-heading"><h3 class="panel-title">{htmllib.escape(part['Title'])}</h3></div>
      <div class="panel-body">{items}</div>
    </div>
    <p class="text-center"><a href="/manga/">マンガ一覧へ戻る</a></p>
  </div></div>
</section>"""
        write_page(out, f"manga/{part['Name']}/index.html",
                   page(f"{part['Title']} - マンガでなれる？WEBデザイナー講座", body))
        stats["manga"] += 1

    # 各ページ
    for part in mangadata:
        pages = part.get("MangaPages") or []
        for i, pg in enumerate(pages):
            frag = manga_dir / part["Name"] / f"{pg['Name']}.html"
            inner = frag.read_text(encoding="utf-8", errors="ignore") if frag.exists() else ""
            nav = []
            if i > 0:
                nav.append(f'<a class="btn btn-default" href="/manga/{part["Name"]}/{pages[i-1]["Name"]}/">&laquo; 前へ</a>')
            nav.append(f'<a class="btn btn-default" href="/manga/{part["Name"]}/">このシリーズの目次</a>')
            if i < len(pages) - 1:
                nav.append(f'<a class="btn btn-default" href="/manga/{part["Name"]}/{pages[i+1]["Name"]}/">次へ &raquo;</a>')
            body = f"""<section class="container">
  <div class="row"><div class="col-md-10 col-md-offset-1">
    <div class="panel panel-info">
      <div class="panel-heading"><h3 class="panel-title">{htmllib.escape(pg['Title'])}</h3></div>
      {inner}
    </div>
    <div class="text-center" style="margin:20px 0">{' '.join(nav)}</div>
    <p class="text-center"><a href="/manga/">マンガ一覧へ戻る</a></p>
  </div></div>
</section>"""
            write_page(out, f"manga/{part['Name']}/{pg['Name']}/index.html",
                       page(f"{pg['Title']} - マンガでなれる？WEBデザイナー講座", body))
            stats["manga"] += 1


# ---------------------------------------------------------------------------
# アセットコピー
# ---------------------------------------------------------------------------

# 丸ごとコピーする軽量ディレクトリ（合計 ~7MB）
SMALL_ASSET_DIRS = ["css", "js", "lib", "fonts", "images"]
ASSET_FILES = ["favicon.ico"]
# img/ (228MB) は丸ごとではなく参照されたファイルだけコピーする
_IMG_REF_RE = re.compile(re.escape(PREFIX) + r"/img/([^\"')\s?#>]+)")


def copy_assets(src: Path, out: Path, *, img_mode: str = "referenced"):
    www = src / "wwwroot"
    for d in SMALL_ASSET_DIRS:
        s = www / d
        if s.is_dir():
            shutil.copytree(s, out / d, dirs_exist_ok=True)
    for f in ASSET_FILES:
        s = www / f
        if s.is_file():
            shutil.copy2(s, out / f)
    # コピーした CSS 内の url(/...) を /creativeweb/ に書き換え
    for css in (out).rglob("*.css"):
        try:
            t = css.read_text(encoding="utf-8", errors="ignore")
            css.write_text(rewrite_paths(t), encoding="utf-8")
        except Exception:
            pass

    src_img = www / "img"
    if not src_img.is_dir():
        return
    if img_mode == "all":
        shutil.copytree(src_img, out / "img", dirs_exist_ok=True)
        print(f"  img          全コピー ({sum(1 for _ in src_img.rglob('*') if _.is_file())} files)")
        return

    # 生成済み HTML / CSS を走査して参照された img/ のパスを集める
    refs: set[str] = set()
    for f in out.rglob("*"):
        if f.suffix.lower() in (".html", ".css") and f.is_file():
            for m in _IMG_REF_RE.finditer(f.read_text(encoding="utf-8", errors="ignore")):
                refs.add(htmllib.unescape(m.group(1)))

    copied = missing = 0
    for rel in sorted(refs):
        s = src_img / rel
        if s.is_file():
            dest = out / "img" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, dest)
            copied += 1
        else:
            missing += 1
    total = sum(f.stat().st_size for f in (out / "img").rglob("*") if f.is_file()) if (out / "img").exists() else 0
    print(f"  img          参照のみ {copied} files ({total/1024/1024:.1f} MB), "
          f"参照ありソース無し {missing}")


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", required=True, help="CreativeWeb プロジェクトのルート(.csproj のある所)")
    ap.add_argument("--out", required=True, help="出力先 (例 html/creativeweb)")
    ap.add_argument("--no-assets", action="store_true", help="アセットコピーをスキップ")
    ap.add_argument("--img-mode", choices=["referenced", "all"], default="referenced",
                    help="img/ のコピー方針: referenced=参照された画像のみ(既定), all=全部")
    ap.add_argument("--clean", action="store_true", help="出力先を空にしてから生成")
    args = ap.parse_args()

    src = Path(args.src).resolve()
    out = Path(args.out).resolve()
    cfg = src / "App_Data" / "config"

    if args.clean and out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    textdata = load_json(cfg / "textpage.json")
    blog_raw = load_json(cfg / "blogindex.json")
    categories = load_json(cfg / "categorydata.json")
    mangadata = load_json(cfg / "manga.json")

    # ブログ: RedirectUrl が null -> {Name}.html, "md" -> {Name}.md が実記事。
    # それ以外は旧 URL への 301 用なのでアーカイブからは除外。新着順に並べる。
    blogdata = []
    for b in blog_raw:
        ru = b.get("RedirectUrl")
        if ru is None:
            b["RedirectUrl"] = f"{b['Name']}.html"
            blogdata.append(b)
        elif ru == "md":
            b["RedirectUrl"] = f"{b['Name']}.md"
            blogdata.append(b)
    blogdata.sort(key=lambda x: x.get("PublishDate") or "", reverse=True)

    stats = {"textpages": 0, "orphans": 0, "redirects": 0, "blog_posts": 0,
             "blog_index": 0, "blog_cat": 0, "manga": 0}

    covered: set = set()
    build_textpages(src, out, textdata, stats, covered)
    build_orphans(src, out, covered, stats)
    build_static_views(src, out, stats)
    build_blog(src, out, blogdata, categories, stats)
    build_manga(src, out, mangadata, stats)

    if not args.no_assets:
        copy_assets(src, out, img_mode=args.img_mode)

    total = sum(stats.values())
    print(f"完了: {total} ページを {out}/ に生成")
    for k, v in stats.items():
        print(f"  {k:12} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
