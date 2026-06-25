#!/usr/bin/env python3
"""
Mirror an existing website into a static bundle (SiteSucker, in Python).

It opens each page in a real (headless) browser, saves the HTML — and, crucially,
**every file the page loads** (CSS, JS, images, fonts, …) — and rewrites
references to local relative paths. The result is a folder of static files you
can host on Cloudflare Pages, which lets you shut down the dynamic site
(e.g. WordPress) — attack surface and all.

Why a browser and not requests/wget: the browser discovers and fetches every
asset the page actually loads (including ones referenced from CSS), and — with
--js — can render JavaScript-built pages whose body isn't in the raw HTML.

By default JavaScript is NOT executed: the saved HTML is what the server
delivered — small, and free of the large iframe/DOM trees that client-side
widgets (ad networks like AdSense, analytics) inject at render time. Pass --js
for sites whose body is built by JavaScript (SPAs); the browser then renders the
page before saving (at the cost of heavier, widget-inflated HTML).

Usage:
    python3 tools/mirror_site.py https://example.com/ --out mirror
    python3 tools/mirror_site.py https://example.com/ --out mirror --max-pages 300
    python3 tools/mirror_site.py https://example.com/ --out mirror --js
    python3 tools/mirror_site.py https://example.com/ --out mirror --skip-existing

Options:
    URL                 start URL to crawl from
    --out DIR           output directory (default: mirror)
    --max-pages N       max HTML pages to crawl (default: 200)
    --same-host-only    only follow links on the start host (default: on)
    --wait MS           extra wait after networkidle, ms (default: 0)
    --js                execute JavaScript (render the page) before saving.
                        Needed for SPA / JS-rendered sites; off by default so the
                        saved HTML stays small and free of injected ad/analytics
                        markup.
    --skip-existing     don't re-fetch files already present in the output dir:
                        skip pages whose HTML already exists (their links are
                        still read from disk so the crawl continues) and don't
                        overwrite existing assets. Use to resume / incrementally
                        update a mirror.

Setup (one time):
    ./.venv/bin/pip install playwright
    ./.venv/bin/playwright install chromium

This is a starting point — finish the edge cases (srcset, JS-built URLs,
query-string assets) in dialogue with AI.
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag


def local_rel(url: str, start_host: str, *, is_page: bool) -> str:
    """Map a URL to a local relative path under the output dir."""
    p = urlparse(url)
    host = p.netloc
    path = p.path or "/"
    # cross-origin assets go under _ext/<host>/...
    base = path if host == start_host else f"/_ext/{host}{path}"
    if is_page:
        # treat every page route as a directory holding index.html
        if base.endswith("/"):
            base += "index.html"
        elif "." not in base.rsplit("/", 1)[-1]:
            base += "/index.html"
        else:  # page URL that ends in a file name
            base += "/index.html" if not base.endswith(".html") else ""
    else:
        if base.endswith("/"):
            base += "index.html"
    return base.lstrip("/")


def save_bytes(out: Path, rel: str, data: bytes) -> None:
    dest = out / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)


def rewrite_text(text: str, hosts: set[str], start_host: str) -> str:
    """Rewrite absolute references to local paths (start host → root-relative,
    other saved hosts → /_ext/<host>)."""
    for host in sorted(hosts, key=len, reverse=True):
        repl = "" if host == start_host else f"/_ext/{host}"
        for prefix in (f"https://{host}", f"http://{host}", f"//{host}"):
            text = text.replace(prefix, repl)
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description="Mirror a website into static files.")
    ap.add_argument("url", help="start URL, e.g. https://example.com/")
    ap.add_argument("--out", default="mirror", help="output directory (default: mirror)")
    ap.add_argument("--max-pages", type=int, default=200, help="max HTML pages (default: 200)")
    ap.add_argument("--same-host-only", action="store_true", default=True,
                    help="only follow links on the start host (default)")
    ap.add_argument("--wait", type=int, default=0, help="extra wait after load, ms")
    ap.add_argument("--js", action="store_true", default=False,
                    help="execute JavaScript before saving (for SPA / JS-rendered "
                         "sites); off by default to keep HTML small and ad-free")
    ap.add_argument("--skip-existing", action="store_true", default=False,
                    help="don't re-fetch files already in the output dir "
                         "(resume / incremental update)")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright is not installed. Run:\n"
                 "  ./.venv/bin/pip install playwright\n"
                 "  ./.venv/bin/playwright install chromium")

    out = Path(args.out)
    start = urldefrag(args.url)[0]
    start_host = urlparse(start).netloc
    if not start_host:
        sys.exit(f"not a valid URL: {args.url}")

    seen_pages: set[str] = set()
    queue: list[str] = [start]
    saved_hosts: set[str] = {start_host}
    html_pages: list[tuple[str, str]] = []  # (rel_path, html_text)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(java_script_enabled=args.js)
        page = context.new_page()

        def on_response(resp):
            try:
                req = resp.request
                if req.method != "GET" or not resp.ok:
                    return
                ctype = (resp.headers or {}).get("content-type", "")
                if "text/html" in ctype:
                    return  # pages are saved separately as rendered HTML
                rurl = urldefrag(resp.url)[0]
                host = urlparse(rurl).netloc
                rel = local_rel(rurl, start_host, is_page=False)
                saved_hosts.add(host)  # record host for rewriting even if not re-saved
                if args.skip_existing and (out / rel).exists():
                    return
                body = resp.body()
            except Exception:
                return
            save_bytes(out, rel, body)

        page.on("response", on_response)

        while queue and len(seen_pages) < args.max_pages:
            url = queue.pop(0)
            if url in seen_pages:
                continue
            seen_pages.add(url)
            rel = local_rel(url, start_host, is_page=True)

            if args.skip_existing and (out / rel).exists():
                # already mirrored: don't re-fetch, but mine its saved HTML for
                # <a href> links so the crawl still reaches the rest of the site
                try:
                    saved = (out / rel).read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    saved = ""
                links = re.findall(r'<a\b[^>]*?\bhref=["\']([^"\']+)["\']', saved,
                                   flags=re.IGNORECASE)
                print(f"[{len(seen_pages)}] {url} -> {rel} (skip: exists)")
            else:
                try:
                    page.goto(url, wait_until="networkidle", timeout=45000)
                    if args.wait:
                        page.wait_for_timeout(args.wait)
                    html = page.content()
                    links = page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
                except Exception as e:
                    print(f"  skip {url}: {e}", file=sys.stderr)
                    continue
                html_pages.append((rel, html))
                print(f"[{len(seen_pages)}] {url} -> {rel}")

            for link in links:
                link = urldefrag(urljoin(url, link))[0]
                if not link.startswith(("http://", "https://")):
                    continue
                if args.same_host_only and urlparse(link).netloc != start_host:
                    continue
                if link not in seen_pages and link not in queue:
                    queue.append(link)

        browser.close()

    # rewrite + write pages (now that we know every host we saved from)
    for rel, html in html_pages:
        save_bytes(out, rel, rewrite_text(html, saved_hosts, start_host).encode("utf-8"))

    # rewrite saved CSS in place (urls inside stylesheets)
    for css in out.rglob("*.css"):
        try:
            t = css.read_text(encoding="utf-8", errors="ignore")
            css.write_text(rewrite_text(t, saved_hosts, start_host), encoding="utf-8")
        except Exception:
            pass

    print(f"\nDone. {len(html_pages)} pages saved under {out}/")
    print("Serve it: ./.venv/bin/python -m http.server --directory "
          f"{out} 8000   (then deploy to Cloudflare Pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
