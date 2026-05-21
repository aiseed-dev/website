"""USB-device enumeration — **read-only**.

v1 does not write to the USB device itself. Writing a bootable ISO is
destructive and the safe path is to hand the user the right command
(or a third-party GUI tool) for their OS. This module lists the
removable drives so the wizard can show what's plugged in and which
device the user means to use.
"""

from __future__ import annotations

import platform
import subprocess

import psutil

from debian_migrate.state import UsbDevice


DEBIAN_ISO_URL = "https://www.debian.org/distrib/"
DEBIAN_NETINST_URL = (
    "https://www.debian.org/CD/netinst/"
)


def list_usb_devices() -> list[UsbDevice]:
    """Best-effort enumeration of removable storage."""
    system = platform.system()
    try:
        if system == "Linux":
            return _linux()
        if system == "Darwin":
            return _macos()
        if system == "Windows":
            return _windows()
    except Exception:
        return []
    return []


def write_command(device_path: str, iso_path: str) -> dict[str, str]:
    """Return the platform-appropriate command **for the user to copy**.

    The wizard never runs these for the user — they're shown in the
    UI with a "コピー" button so the user can paste into a terminal
    and confirm before pressing Enter.
    """
    system = platform.system()
    if system == "Linux":
        return {
            "command": f"sudo dd if='{iso_path}' of={device_path} bs=4M status=progress conv=fsync",
            "tool": "dd (標準コマンド)",
            "gui": "Balena Etcher / GNOME ディスク",
        }
    if system == "Darwin":
        return {
            "command": f"sudo dd if='{iso_path}' of={device_path} bs=4m",
            "tool": "dd (標準コマンド)",
            "gui": "Balena Etcher",
        }
    if system == "Windows":
        return {
            "command": "(コマンドではなく GUI ツールの使用を推奨します)",
            "tool": "PowerShell / DiskPart",
            "gui": "Rufus / Balena Etcher",
        }
    return {"command": "", "tool": "", "gui": ""}


# ---------------------------------------------------------------------------

def _linux() -> list[UsbDevice]:
    try:
        r = subprocess.run(
            ["lsblk", "-d", "-J", "-o",
             "NAME,SIZE,TYPE,RM,MODEL,VENDOR,TRAN"],
            capture_output=True, text=True, timeout=3,
        )
    except FileNotFoundError:
        return []
    import json

    try:
        data = json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        return []
    out: list[UsbDevice] = []
    for blk in data.get("blockdevices", []):
        if blk.get("type") != "disk":
            continue
        # `rm` = removable. lsblk reports 1 (True) or "1".
        removable = str(blk.get("rm")) in ("1", "True")
        tran = (blk.get("tran") or "").lower()
        if not removable and tran != "usb":
            continue
        size_str = str(blk.get("size") or "0")
        size_gb = _parse_size_gb(size_str)
        out.append(
            UsbDevice(
                path=f"/dev/{blk.get('name')}",
                label=blk.get("model") or blk.get("name") or "",
                size_gb=size_gb,
                vendor=blk.get("vendor") or "",
            )
        )
    return out


def _macos() -> list[UsbDevice]:
    try:
        r = subprocess.run(
            ["diskutil", "list", "-plist", "external", "physical"],
            capture_output=True, text=True, timeout=4,
        )
    except FileNotFoundError:
        return []
    import plistlib

    try:
        data = plistlib.loads(r.stdout.encode("utf-8"))
    except Exception:
        return []
    out: list[UsbDevice] = []
    for d in data.get("AllDisksAndPartitions", []):
        ident = d.get("DeviceIdentifier", "")
        size_bytes = d.get("Size", 0)
        size_gb = round(size_bytes / 1024**3, 1) if size_bytes else 0.0
        out.append(
            UsbDevice(
                path=f"/dev/{ident}",
                label=d.get("VolumeName") or ident,
                size_gb=size_gb,
            )
        )
    return out


def _windows() -> list[UsbDevice]:
    """Use psutil for removable mountpoints; for full device path use
    a PowerShell call as fallback."""
    out: list[UsbDevice] = []
    seen: set[str] = set()
    try:
        for part in psutil.disk_partitions(all=False):
            if "removable" not in part.opts.lower():
                continue
            try:
                usage = psutil.disk_usage(part.mountpoint)
            except Exception:
                continue
            if part.device in seen:
                continue
            seen.add(part.device)
            out.append(
                UsbDevice(
                    path=part.device,
                    label=part.device,
                    size_gb=round(usage.total / 1024**3, 1),
                )
            )
    except Exception:
        return []
    return out


def _parse_size_gb(s: str) -> float:
    """lsblk emits human-readable sizes like '14.4G' / '512M'."""
    if not s:
        return 0.0
    try:
        unit = s[-1].upper()
        value = float(s[:-1])
        if unit == "G":
            return value
        if unit == "T":
            return value * 1024
        if unit == "M":
            return round(value / 1024, 2)
        if unit == "K":
            return round(value / 1024**2, 4)
        return float(s)
    except ValueError:
        return 0.0
