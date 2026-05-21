"""Shared mutable state across wizard pages.

The wizard is a single-user desktop app and the data flow is linear
(welcome → inventory → replacements → hardware → usb → export), so a
simple module-level singleton is enough. Each page reads / writes the
fields it owns.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DetectedApp:
    """One installed application detected on the host."""

    name: str
    publisher: str = ""
    version: str = ""
    source: str = ""  # "registry", "applications", "dpkg", ...


@dataclass
class Replacement:
    """A Debian-side alternative for a detected app."""

    detected: str
    alternatives: list[str]
    confidence: str = "ok"  # "ok" | "review" | "missing"
    note: str = ""
    user_choice: str | None = None  # which alternative the user picked


@dataclass
class HardwareInfo:
    """Best-effort hardware snapshot."""

    os_name: str = ""
    os_version: str = ""
    arch: str = ""
    cpu_model: str = ""
    cpu_cores: int = 0
    ram_gb: float = 0.0
    disks: list[dict[str, Any]] = field(default_factory=list)
    gpu: str = ""
    warnings: list[str] = field(default_factory=list)


@dataclass
class UsbDevice:
    """A removable storage device."""

    path: str
    label: str
    size_gb: float
    vendor: str = ""


@dataclass
class WizardState:
    detected_apps: list[DetectedApp] = field(default_factory=list)
    replacements: list[Replacement] = field(default_factory=list)
    hardware: HardwareInfo = field(default_factory=HardwareInfo)
    usb_devices: list[UsbDevice] = field(default_factory=list)
    selected_usb: str | None = None
    chosen_desktop: str | None = None  # ch 9: "gnome" / "kde" / ...


# Module-level singleton. Flet's declarative components read/write this
# directly; component re-renders are still driven by `use_state` for the
# UI-visible parts.
STATE = WizardState()
