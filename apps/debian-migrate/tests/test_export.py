"""Tests for the Markdown export and the export-side prompt rendering."""

from __future__ import annotations

import pytest

from debian_migrate.pages.export import _render_markdown
from debian_migrate.prompts.templates import summary_prompt
from debian_migrate.state import (
    STATE,
    DetectedApp,
    HardwareInfo,
    Replacement,
    UsbDevice,
)


@pytest.fixture
def seeded_state():
    """Populate STATE with realistic data; reset on teardown."""
    snapshot = (
        STATE.detected_apps,
        STATE.replacements,
        STATE.hardware,
        STATE.usb_devices,
        STATE.selected_usb,
    )
    STATE.detected_apps = [
        DetectedApp(name="Microsoft Word", version="2021", publisher="Microsoft"),
        DetectedApp(name="Slack", version="4.0"),
        DetectedApp(name="Adobe Photoshop 2024", version="25.0", publisher="Adobe"),
    ]
    STATE.replacements = [
        Replacement(
            detected="Microsoft Word",
            alternatives=["LibreOffice Writer"],
            confidence="ok",
            note="対外文書は PDF にして送る",
            user_choice="ok",
        ),
        Replacement(
            detected="Adobe Photoshop",
            alternatives=["GIMP", "Krita"],
            confidence="review",
            note="PSD は GIMP で開ける",
        ),
    ]
    STATE.hardware = HardwareInfo(
        os_name="Linux",
        os_version="6.18",
        arch="x86_64",
        cpu_model="Intel Xeon",
        cpu_cores=4,
        ram_gb=16.0,
        disks=[
            {
                "device": "/dev/sda1",
                "mountpoint": "/",
                "fstype": "ext4",
                "total_gb": 100.0,
                "free_gb": 50.0,
            }
        ],
        gpu="Intel UHD",
        warnings=[],
    )
    STATE.usb_devices = [
        UsbDevice(path="/dev/sdb", label="SanDisk Ultra", size_gb=16.0)
    ]
    STATE.selected_usb = "/dev/sdb"
    yield STATE
    (
        STATE.detected_apps,
        STATE.replacements,
        STATE.hardware,
        STATE.usb_devices,
        STATE.selected_usb,
    ) = snapshot


def test_markdown_export_renders_all_sections(seeded_state):
    md = _render_markdown()
    assert "# Debian 移行レポート" in md
    assert "## ハードウェア" in md
    assert "Intel Xeon" in md
    assert "## 代替検討" in md
    assert "| Microsoft Word | LibreOffice Writer | ok | ok | 対外文書は PDF にして送る |" in md
    assert "## 検出アプリ (3 件)" in md
    assert "Microsoft Word (2021, Microsoft)" in md
    assert "## インストール先 USB" in md
    assert "/dev/sdb" in md
    assert "## 次のステップ" in md


def test_markdown_export_handles_empty_state():
    """Run with the default empty state (no fixture)."""
    md = _render_markdown()
    assert "# Debian 移行レポート" in md
    # Should not crash, should still have the standard sections.
    assert "## ハードウェア" in md
    assert "## 検出アプリ" in md


def test_summary_prompt_includes_seeded_data(seeded_state):
    text = summary_prompt(
        STATE.detected_apps,
        STATE.replacements,
        STATE.hardware,
        STATE.selected_usb,
    )
    assert "検出アプリ数: 3" in text
    assert "代替検討メモ" in text  # the heading is "重要な代替検討メモ"
    # The review-confidence entry must show up
    assert "Adobe Photoshop" in text
    assert "/dev/sdb" in text
