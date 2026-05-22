"""Smoke tests for the platform-specific scanners.

These tests run on whichever OS the developer/CI uses, so they're
intentionally lenient — they assert that scanning **does not crash**
and that the dispatch picks the right backend. Detailed scanner
behavior is verified per-OS in CI matrix.
"""

from __future__ import annotations

import platform
import sys
import tempfile
from configparser import ConfigParser
from pathlib import Path

from debian_migrate import scanners
from debian_migrate.state import DetectedApp


def test_dispatch_does_not_crash():
    apps = scanners.scan()
    assert isinstance(apps, list)
    for a in apps:
        assert isinstance(a, DetectedApp)
        assert a.name  # non-empty


def test_linux_desktop_file_parsing(tmp_path: Path, monkeypatch):
    """Drop a fake .desktop file into a fresh dir and patch the
    DESKTOP_DIRS list to point at it. Confirm the scanner picks it up
    and ignores Hidden/NoDisplay entries."""
    if platform.system() != "Linux":
        # The linux scanner module imports cleanly on any platform,
        # but the test only makes sense on Linux runners.
        return

    from debian_migrate.scanners import linux as linux_scanner

    visible = tmp_path / "good.desktop"
    visible.write_text(
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=My Cool App\n"
        "Comment=Great tool\n"
        "Categories=Utility;\n",
        encoding="utf-8",
    )

    hidden = tmp_path / "hidden.desktop"
    hidden.write_text(
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=Hidden App\n"
        "NoDisplay=true\n",
        encoding="utf-8",
    )

    not_app = tmp_path / "link.desktop"
    not_app.write_text(
        "[Desktop Entry]\n"
        "Type=Link\n"
        "Name=Bookmark\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(linux_scanner, "DESKTOP_DIRS", [tmp_path])

    apps = linux_scanner.scan()
    names = {a.name for a in apps}
    assert "My Cool App" in names
    assert "Hidden App" not in names
    assert "Bookmark" not in names
