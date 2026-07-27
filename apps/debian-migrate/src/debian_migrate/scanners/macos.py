"""macOS installed-app scanner via /Applications listing."""

from __future__ import annotations

import plistlib
from pathlib import Path

from debian_migrate.state import DetectedApp


APP_ROOTS = [
    Path("/Applications"),
    Path("/Applications/Utilities"),
    Path.home() / "Applications",
]


def scan() -> list[DetectedApp]:
    seen: set[str] = set()
    out: list[DetectedApp] = []
    for root in APP_ROOTS:
        if not root.exists():
            continue
        try:
            entries = list(root.iterdir())
        except OSError:
            continue
        for entry in entries:
            if not entry.name.endswith(".app"):
                continue
            display = entry.stem
            publisher = ""
            version = ""
            info_plist = entry / "Contents" / "Info.plist"
            if info_plist.exists():
                try:
                    with info_plist.open("rb") as fh:
                        info = plistlib.load(fh)
                    display = info.get("CFBundleDisplayName") or info.get(
                        "CFBundleName"
                    ) or display
                    version = info.get("CFBundleShortVersionString") or info.get(
                        "CFBundleVersion"
                    ) or ""
                    publisher = info.get("CFBundleIdentifier", "")
                except Exception:
                    pass
            key = display.lower().strip()
            if key in seen:
                continue
            seen.add(key)
            out.append(
                DetectedApp(
                    name=display,
                    publisher=publisher,
                    version=str(version),
                    source=f"applications:{root}",
                )
            )
    out.sort(key=lambda a: a.name.lower())
    return out
