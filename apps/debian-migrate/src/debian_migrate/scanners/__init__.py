"""OS-specific installed-app scanners.

Use `scan()` from outside; it dispatches to the right backend based on
the host platform.
"""

from __future__ import annotations

import platform

from debian_migrate.state import DetectedApp


def scan() -> list[DetectedApp]:
    """Return a list of installed applications on the current host.

    Best effort — different OSes expose different metadata and the
    result may be incomplete. Errors during scanning are swallowed
    silently and surface as an empty list, because this is a
    beginner-facing wizard and the next page (replacements) still works
    if the user enters apps by hand.
    """
    system = platform.system()
    try:
        if system == "Windows":
            from debian_migrate.scanners import windows
            return windows.scan()
        if system == "Darwin":
            from debian_migrate.scanners import macos
            return macos.scan()
        if system == "Linux":
            from debian_migrate.scanners import linux
            return linux.scan()
    except Exception:
        return []
    return []
