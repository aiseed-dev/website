"""Linux installed-app scanner via .desktop files (XDG)."""

from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

from debian_migrate.state import DetectedApp


DESKTOP_DIRS = [
    Path("/usr/share/applications"),
    Path("/usr/local/share/applications"),
    Path("/var/lib/flatpak/exports/share/applications"),
    Path("/var/lib/snapd/desktop/applications"),
    Path.home() / ".local/share/applications",
]


def scan() -> list[DetectedApp]:
    seen: set[str] = set()
    out: list[DetectedApp] = []
    for root in DESKTOP_DIRS:
        if not root.exists():
            continue
        try:
            entries = list(root.glob("*.desktop"))
        except OSError:
            continue
        for entry in entries:
            cp = ConfigParser(interpolation=None, strict=False)
            try:
                cp.read(entry, encoding="utf-8")
            except Exception:
                continue
            if "Desktop Entry" not in cp:
                continue
            section = cp["Desktop Entry"]
            if section.get("NoDisplay", "false").lower() == "true":
                continue
            if section.get("Hidden", "false").lower() == "true":
                continue
            entry_type = section.get("Type", "Application")
            if entry_type != "Application":
                continue
            name = section.get("Name", entry.stem)
            comment = section.get("Comment", "")
            categories = section.get("Categories", "")
            out.append(
                DetectedApp(
                    name=name,
                    publisher=categories,
                    version="",
                    source=f"desktop:{root}",
                )
            )
            seen.add(name.lower())
    out.sort(key=lambda a: a.name.lower())
    return out
