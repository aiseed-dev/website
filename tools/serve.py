#!/usr/bin/env python3
"""Development server with auto-rebuild for aiseed.dev.

Watches articles/, blog/, tools/templates/ and html/{css,js} and re-runs
build_article.py --all on changes. Serves html/ over HTTP.

Usage:
    python3 tools/serve.py             # build once, watch, serve on :8000
    python3 tools/serve.py --port 8080
    python3 tools/serve.py --no-initial-build
"""

from __future__ import annotations

import argparse
import http.server
import socketserver
import subprocess
import sys
import threading
from pathlib import Path
from typing import Optional

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

SITE_ROOT = Path(__file__).resolve().parent.parent
BUILD_SCRIPT = SITE_ROOT / "tools" / "build_article.py"
HTML_DIR = SITE_ROOT / "html"
DEBOUNCE_SEC = 0.4

WATCH_DIRS = [
    SITE_ROOT / "articles",
    SITE_ROOT / "blog",
    SITE_ROOT / "tools" / "templates",
    HTML_DIR / "css",
    HTML_DIR / "js",
]


class RebuildHandler(FileSystemEventHandler):
    def __init__(self) -> None:
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
        result = subprocess.run([sys.executable, str(BUILD_SCRIPT), "--all"])
        if result.returncode != 0:
            print("[serve] build failed", flush=True)

    def cancel(self) -> None:
        with self._lock:
            self._stopped = True
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None


def initial_build() -> None:
    print("[serve] initial build…", flush=True)
    subprocess.run([sys.executable, str(BUILD_SCRIPT), "--all"], check=True)


def start_watcher() -> tuple[Observer, RebuildHandler]:
    handler = RebuildHandler()
    observer = Observer()
    for target in WATCH_DIRS:
        if target.exists():
            observer.schedule(handler, str(target), recursive=True)
    observer.daemon = True
    observer.start()
    return observer, handler


def serve(port: int) -> None:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(HTML_DIR), **kw)

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
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-initial-build", action="store_true")
    args = parser.parse_args()

    if not args.no_initial_build:
        initial_build()

    observer, handler = start_watcher()
    try:
        serve(args.port)
    finally:
        handler.cancel()
        observer.stop()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()
