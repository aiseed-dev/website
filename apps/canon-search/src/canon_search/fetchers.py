"""正典の取得 — RFC(IETF)、日本の法令(e-Gov 法令API v2)、PDF、任意URL。

対象はすべて公開・権利クリアな一次資料に限る:
- RFC: IETF Trust のライセンスで複製可
- 法令: 著作権法13条により権利の目的とならない
- NIST 等の米国政府文書: 米国内パブリックドメイン
取得は単発の礼儀正しいリクエストのみ(連続クロールはしない)。
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

from .chunker import chunk_paragraphs

UA = "Mozilla/5.0 (compatible; canon-search/0.1; personal research tool)"


def _get(url: str, accept: str = "*/*", timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": accept, "Accept-Language": "ja,en"})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.read()


# ---------------------------------------------------------------- RFC

_PAGE_FOOTER = re.compile(r"^.*\[Page \d+\]\s*$")
_PAGE_HEADER = re.compile(r"^RFC \d+\s{2,}.*\s{2,}.*$")


def fetch_rfc(number: int) -> dict:
    meta = json.loads(_get(f"https://www.rfc-editor.org/rfc/rfc{number}.json"))
    raw = _get(f"https://www.rfc-editor.org/rfc/rfc{number}.txt").decode(
        "utf-8", errors="replace"
    )
    lines = []
    for line in raw.replace("\f", "\n").splitlines():
        if _PAGE_FOOTER.match(line) or _PAGE_HEADER.match(line):
            continue
        lines.append(line)
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    return {
        "source": "rfc",
        "doc_key": f"RFC {number}",
        "title": meta.get("title", f"RFC {number}"),
        "url": f"https://www.rfc-editor.org/rfc/rfc{number}",
        "license": "IETF Trust Legal Provisions",
        "chunks": chunk_paragraphs(text),
    }


# ---------------------------------------------------------------- 法令 (e-Gov API v2)

_EGOV = "https://laws.e-gov.go.jp/api/2"
_LAW_ID_RE = re.compile(r"^\d{3}[A-Z]{2}\d{10}$")


def resolve_law_id(name_or_id: str) -> tuple[str, str]:
    """法令名または法令IDから (law_id, law_title) を返す。"""
    if _LAW_ID_RE.match(name_or_id):
        return name_or_id, name_or_id
    q = urllib.parse.quote(name_or_id)
    data = json.loads(_get(f"{_EGOV}/laws?law_title={q}&limit=10",
                           accept="application/json"))
    laws = data.get("laws", [])
    if not laws:
        raise SystemExit(f"法令が見つかりません: {name_or_id}")
    # 完全一致を優先、なければ先頭
    best = next(
        (l for l in laws if l["revision_info"]["law_title"] == name_or_id), laws[0]
    )
    return best["law_info"]["law_id"], best["revision_info"]["law_title"]


def _article_text(article: ET.Element) -> str:
    parts = []
    for para in article.iter("Paragraph"):
        text = "".join(
            "".join(s.itertext()) for s in para.iter("Sentence")
        )
        num = para.findtext("ParagraphNum") or ""
        parts.append((num + " " if num else "") + text)
    return "\n".join(p for p in parts if p.strip())


def fetch_law(name_or_id: str) -> dict:
    law_id, _ = resolve_law_id(name_or_id)
    raw = _get(f"{_EGOV}/law_data/{law_id}", accept="application/xml")
    root = ET.fromstring(raw)
    title = root.findtext(".//revision_info/law_title") or law_id
    chunks: list[tuple[str, str]] = []
    for article in root.iter("Article"):
        caption = "".join(article.find("ArticleCaption").itertext()) \
            if article.find("ArticleCaption") is not None else ""
        art_title = article.findtext("ArticleTitle") or ""
        body = _article_text(article)
        if body.strip():
            chunks.append((f"{art_title} {caption}".strip(), body))
    if not chunks:  # 条建てでない法令(憲法前文など)への保険
        text = "".join(root.find(".//law_full_text").itertext())
        chunks = chunk_paragraphs(text)
    return {
        "source": "law",
        "doc_key": law_id,
        "title": title,
        "url": f"https://laws.e-gov.go.jp/law/{law_id}",
        "license": "著作権法13条(権利の目的とならない)",
        "chunks": chunks,
    }


# ---------------------------------------------------------------- HTML (任意URL)

class _TextExtractor(HTMLParser):
    _SKIP = {"script", "style", "noscript", "nav", "header", "footer", "aside"}
    _BLOCK = {"p", "div", "section", "article", "li", "tr", "table",
              "h1", "h2", "h3", "h4", "h5", "h6", "br", "dt", "dd"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title = ""
        self._skip_depth = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip_depth += 1
        elif tag == "title":
            self._in_title = True
        elif tag in self._BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1
        elif tag == "title":
            self._in_title = False
        elif tag in self._BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self._skip_depth:
            self.parts.append(data)


def robots_allows(url: str) -> bool:
    """RFC 9309 の解釈に従う: 4xx(未設置)=許可、5xx・通信不能=拒否。

    urllib.robotparser.read() は素の UA で取得して WAF に弾かれることがある
    ため、取得は自前の _get() で行い、パースだけ robotparser に任せる。
    """
    parts = urllib.parse.urlsplit(url)
    robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
    try:
        body = _get(robots_url, accept="text/plain", timeout=15)
    except urllib.error.HTTPError as e:
        return 400 <= e.code < 500
    except OSError:
        return False
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(body.decode("utf-8", errors="replace").splitlines())
    return rp.can_fetch(UA, url)


def fetch_url(url: str, title: str = "", doc_key: str = "",
              license: str = "") -> dict:
    if not robots_allows(url):
        raise SystemExit(f"robots.txt により拒否されています: {url}")
    charset_guess = "utf-8"
    raw = _get(url, accept="text/html")
    for enc in (charset_guess, "cp932", "euc-jp"):
        try:
            html = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        html = raw.decode("utf-8", errors="replace")
    ex = _TextExtractor()
    ex.feed(html)
    text = re.sub(r"[ \t]+", " ", "".join(ex.parts))
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(line.strip() for line in text.splitlines())
    text = re.sub(r"\n{3,}", "\n\n", text)
    return {
        "source": "url",
        "doc_key": doc_key or url,
        "title": title or " ".join(ex.title.split()) or url,
        "url": url,
        "license": license,
        "chunks": chunk_paragraphs(text),
    }


# ---------------------------------------------------------------- PDF / URL

def fetch_pdf(url: str, title: str, doc_key: str, license: str = "") -> dict:
    pdf = _get(url)
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(pdf)
        f.flush()
        text = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", f.name, "-"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8", errors="replace")
    text = re.sub(r"\n{3,}", "\n\n", text.replace("\f", "\n"))
    return {
        "source": "pdf",
        "doc_key": doc_key,
        "title": title,
        "url": url,
        "license": license,
        "chunks": chunk_paragraphs(text),
    }
