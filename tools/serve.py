#!/usr/bin/env python3
"""Development server with auto-rebuild for aiseed.dev-compatible sites.

Watches <site>/{articles,tools/templates} and <site>/html/{css,js},
re-runs build_article.py --all on changes, and serves <site>/html/ over HTTP.

Usage:
    python3 tools/serve.py                            # use parent dir of script
    python3 tools/serve.py --site /path/to/site
    python3 tools/serve.py --site . --port 8080
    AISEED_SITE=/path/to/site python3 tools/serve.py
    python3 tools/serve.py --no-initial-build
"""

from __future__ import annotations

import argparse
import http.server
import os
import socketserver
import subprocess
import sys
import threading
from pathlib import Path
from typing import Optional

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

BUILD_SCRIPT = Path(__file__).resolve().parent / "build_article.py"
DEBOUNCE_SEC = 0.4


def resolve_site(cli_value: str | None) -> Path:
    candidate = cli_value or os.environ.get("AISEED_SITE")
    if candidate is None:
        candidate = str(Path(__file__).resolve().parent.parent)
    site = Path(candidate).resolve()
    if not (site / "articles").exists():
        raise SystemExit(
            f"[serve] {site} does not look like an aiseed-style site "
            "(no articles/). Pass --site <path> or set AISEED_SITE."
        )
    return site


def watch_dirs(site: Path) -> list[Path]:
    html_dir = site / "html"
    return [
        site / "articles",
        site / "tools" / "templates",
        html_dir / "css",
        html_dir / "js",
    ]


class RebuildHandler(FileSystemEventHandler):
    def __init__(self, site: Path) -> None:
        self._site = site
        self._lock = threading.Lock()
        self._timer: Optional[threading.Timer] = None
        self._stopped = False

    def on_any_event(self, event) -> None:
        if event.is_directory:
            return
        src = getattr(event, "src_path", "") or ""
        if src.endswith(("~", ".swp", ".swo")) or "/__pycache__/" in src:
            return
        with self._lock:
            if self._stopped:
                return
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(DEBOUNCE_SEC, self._run_build)
            self._timer.daemon = True
            self._timer.start()

    def _run_build(self) -> None:
        print("[serve] change detected — rebuilding…", flush=True)
        result = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT), "--site", str(self._site), "--all"]
        )
        if result.returncode != 0:
            print("[serve] build failed", flush=True)

    def cancel(self) -> None:
        with self._lock:
            self._stopped = True
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None


def initial_build(site: Path) -> None:
    print(f"[serve] initial build… (site: {site})", flush=True)
    subprocess.run(
        [sys.executable, str(BUILD_SCRIPT), "--site", str(site), "--all"],
        check=True,
    )


def start_watcher(site: Path) -> tuple[Observer, RebuildHandler]:
    handler = RebuildHandler(site)
    observer = Observer()
    for target in watch_dirs(site):
        if target.exists():
            observer.schedule(handler, str(target), recursive=True)
    observer.daemon = True
    observer.start()
    return observer, handler


def serve(html_dir: Path, port: int) -> None:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(html_dir), **kw)

        def log_message(self, format: str, *args) -> None:
            print(f"[http] {self.address_string()} — {format % args}", flush=True)

    with socketserver.ThreadingTCPServer(("", port), Handler) as httpd:
        print(f"[serve] http://localhost:{port} (Ctrl+C to stop)", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[serve] shutting down", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", help="Path to the site root (default: parent dir of this script, or $AISEED_SITE).")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-initial-build", action="store_true")
    args = parser.parse_args()

    site = resolve_site(args.site)
    if not args.no_initial_build:
        initial_build(site)

    observer, handler = start_watcher(site)
    try:
        serve(site / "html", args.port)
    finally:
        handler.cancel()
        observer.stop()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()
