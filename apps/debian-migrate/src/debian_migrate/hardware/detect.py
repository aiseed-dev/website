"""Best-effort cross-platform hardware detection.

The wizard uses this to advise on Debian compatibility: minimum RAM,
CPU architecture, disk free space, and a rough GPU note. Where the
host OS doesn't expose a clean API we accept fuzziness — this is a
guide, not an audit.
"""

from __future__ import annotations

import platform
import shutil
import subprocess

import psutil

from debian_migrate.state import HardwareInfo


def detect() -> HardwareInfo:
    info = HardwareInfo()
    info.os_name = platform.system()
    info.os_version = platform.release()
    info.arch = platform.machine()
    info.cpu_model = _cpu_model()
    info.cpu_cores = psutil.cpu_count(logical=False) or psutil.cpu_count() or 0
    try:
        info.ram_gb = round(psutil.virtual_memory().total / 1024**3, 1)
    except Exception:
        info.ram_gb = 0.0
    info.disks = _disks()
    info.gpu = _gpu()
    info.warnings = _evaluate(info)
    return info


def _cpu_model() -> str:
    system = platform.system()
    try:
        if system == "Linux":
            with open("/proc/cpuinfo", encoding="utf-8") as fh:
                for line in fh:
                    if line.startswith("model name"):
                        return line.split(":", 1)[1].strip()
        if system == "Darwin":
            r = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True, text=True, timeout=2,
            )
            return r.stdout.strip()
        if system == "Windows":
            r = subprocess.run(
                ["wmic", "cpu", "get", "Name"],
                capture_output=True, text=True, timeout=4,
            )
            for line in r.stdout.splitlines():
                line = line.strip()
                if line and not line.lower().startswith("name"):
                    return line
    except Exception:
        pass
    return platform.processor() or "Unknown"


def _disks() -> list[dict]:
    out: list[dict] = []
    try:
        for part in psutil.disk_partitions(all=False):
            if "loop" in part.device.lower():
                continue
            try:
                usage = psutil.disk_usage(part.mountpoint)
            except Exception:
                continue
            out.append(
                {
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "fstype": part.fstype,
                    "total_gb": round(usage.total / 1024**3, 1),
                    "free_gb": round(usage.free / 1024**3, 1),
                }
            )
    except Exception:
        pass
    return out


def _gpu() -> str:
    system = platform.system()
    try:
        if system == "Linux":
            if shutil.which("lspci"):
                r = subprocess.run(
                    ["lspci"], capture_output=True, text=True, timeout=3
                )
                for line in r.stdout.splitlines():
                    low = line.lower()
                    if "vga" in low or "3d" in low or "display" in low:
                        return line.split(":", 2)[-1].strip()
        if system == "Darwin":
            r = subprocess.run(
                ["system_profiler", "SPDisplaysDataType"],
                capture_output=True, text=True, timeout=4,
            )
            for line in r.stdout.splitlines():
                line = line.strip()
                if line.startswith("Chipset Model:"):
                    return line.split(":", 1)[1].strip()
        if system == "Windows":
            r = subprocess.run(
                ["wmic", "path", "win32_VideoController", "get", "Name"],
                capture_output=True, text=True, timeout=4,
            )
            for line in r.stdout.splitlines():
                line = line.strip()
                if line and not line.lower().startswith("name"):
                    return line
    except Exception:
        pass
    return "(検出できませんでした)"


def _evaluate(info: HardwareInfo) -> list[str]:
    """Return human-readable warnings about Debian compatibility."""
    warnings: list[str] = []
    if info.arch.lower() not in ("x86_64", "amd64", "arm64", "aarch64"):
        warnings.append(
            f"CPU アーキテクチャ {info.arch} は Debian の標準サポート外の可能性があります。"
        )
    if info.ram_gb and info.ram_gb < 4:
        warnings.append(
            f"メモリ {info.ram_gb}GB は最近のデスクトップ環境 (GNOME/KDE) には少なめ。"
            "XFCE / LXQt など軽量 DE の検討を (本書 第9章)。"
        )
    if info.disks:
        max_free = max((d["free_gb"] for d in info.disks), default=0)
        if max_free < 20:
            warnings.append(
                f"空き容量が最大 {max_free}GB しかありません。"
                "デュアルブートでも 30GB 以上は欲しいところ。"
            )
    gpu_low = info.gpu.lower()
    if "nvidia" in gpu_low:
        warnings.append(
            "NVIDIA GPU です。Debian 既定のオープンドライバ (nouveau) は性能が出にくいので、"
            "プロプライエタリドライバの導入を検討してください (本書 第8章)。"
        )
    if "apple m" in gpu_low or info.cpu_model.lower().startswith("apple m"):
        warnings.append(
            "Apple Silicon (M1/M2/M3 等) です。Debian は Asahi Linux 経由でしか動かないので、"
            "現状はインストール先として推奨できません。代わりに Linux 仮想マシン (UTM) の検討を。"
        )
    return warnings
