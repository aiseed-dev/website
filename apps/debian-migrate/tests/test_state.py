"""Smoke tests for state and prompt rendering."""

from __future__ import annotations

from debian_migrate.prompts.templates import (
    hardware_prompt,
    inventory_prompt,
    replacements_prompt,
    summary_prompt,
    usb_prompt,
)
from debian_migrate.state import (
    DetectedApp,
    HardwareInfo,
    Replacement,
    UsbDevice,
    WizardState,
)


def test_state_defaults():
    s = WizardState()
    assert s.detected_apps == []
    assert s.replacements == []
    assert s.hardware.os_name == ""
    assert s.selected_usb is None


def test_inventory_prompt_renders_without_apps():
    text = inventory_prompt([])
    assert "検出されたアプリ" in text
    assert "claude.ai" not in text  # we mention it in copy_prompt_button


def test_inventory_prompt_renders_with_apps():
    apps = [DetectedApp(name="Foo", version="1.0", publisher="Acme")]
    text = inventory_prompt(apps)
    assert "Foo" in text and "1.0" in text and "Acme" in text


def test_replacements_prompt_renders():
    reps = [
        Replacement(
            detected="X",
            alternatives=["A", "B"],
            confidence="review",
            note="hi",
        )
    ]
    text = replacements_prompt(reps)
    assert "X" in text and "A / B" in text and "review" in text


def test_hardware_prompt_renders():
    hw = HardwareInfo(
        os_name="Linux",
        os_version="6.18",
        arch="x86_64",
        cpu_model="Test CPU",
        cpu_cores=4,
        ram_gb=16.0,
        disks=[
            {"device": "/dev/sda1", "mountpoint": "/", "fstype": "ext4",
             "total_gb": 100.0, "free_gb": 50.0}
        ],
        gpu="Test GPU",
        warnings=["test warning"],
    )
    text = hardware_prompt(hw)
    assert "Linux 6.18" in text and "Test CPU" in text and "test warning" in text


def test_usb_prompt_renders():
    devices = [UsbDevice(path="/dev/sdb", label="My USB", size_gb=16.0)]
    text = usb_prompt(devices, "/dev/sdb")
    assert "/dev/sdb" in text and "My USB" in text


def test_summary_prompt_renders():
    text = summary_prompt([], [], HardwareInfo(), None)
    assert "全体まとめ" in text
