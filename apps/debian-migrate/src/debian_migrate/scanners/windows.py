"""Windows installed-app scanner via the Uninstall registry keys."""

from __future__ import annotations

from debian_migrate.state import DetectedApp


UNINSTALL_KEYS = [
    (r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", "HKLM64"),
    (r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall", "HKLM32"),
    (r"HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", "HKCU"),
]


def scan() -> list[DetectedApp]:
    try:
        import winreg  # type: ignore[import-not-found]
    except ImportError:
        return []

    roots = {
        "HKLM64": (winreg.HKEY_LOCAL_MACHINE,
                   r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        "HKLM32": (winreg.HKEY_LOCAL_MACHINE,
                   r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        "HKCU":   (winreg.HKEY_CURRENT_USER,
                   r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    }

    seen: set[str] = set()
    out: list[DetectedApp] = []
    for source, (root, path) in roots.items():
        try:
            with winreg.OpenKey(root, path) as base:
                i = 0
                while True:
                    try:
                        sub_name = winreg.EnumKey(base, i)
                    except OSError:
                        break
                    i += 1
                    try:
                        with winreg.OpenKey(base, sub_name) as sub:
                            name = _try_value(sub, "DisplayName")
                            if not name:
                                continue
                            publisher = _try_value(sub, "Publisher") or ""
                            version = _try_value(sub, "DisplayVersion") or ""
                            system_component = _try_value(sub, "SystemComponent")
                            if system_component == 1:
                                continue
                            key = name.lower().strip()
                            if key in seen:
                                continue
                            seen.add(key)
                            out.append(
                                DetectedApp(
                                    name=name,
                                    publisher=publisher,
                                    version=version,
                                    source=f"registry:{source}",
                                )
                            )
                    except OSError:
                        continue
        except OSError:
            continue
    out.sort(key=lambda a: a.name.lower())
    return out


def _try_value(key, name: str):  # type: ignore[no-untyped-def]
    try:
        import winreg  # type: ignore[import-not-found]
        v, _ = winreg.QueryValueEx(key, name)
        return v
    except OSError:
        return None
    except Exception:
        return None
