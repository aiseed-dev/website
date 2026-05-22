"""Tests for ch9 (desktop env) / ch10 (IME) / ch11 (install plan)."""

from __future__ import annotations

import pytest

from debian_migrate.data.install_commands import TABLE, find_install
from debian_migrate.pages.desktop_env import DESKTOP_ENVS, _recommend
from debian_migrate.pages.install_plan import (
    _build_batch_script,
    _build_install_lines,
)
from debian_migrate.prompts.templates import (
    desktop_env_prompt,
    ime_prompt,
    install_plan_prompt,
)
from debian_migrate.state import (
    STATE,
    HardwareInfo,
    Replacement,
)


# --- ch 9 -----------------------------------------------------------

def test_recommend_by_ram():
    assert _recommend(1.5) == "lxqt"
    assert _recommend(3.0) == "xfce"
    assert _recommend(5.0) == "cinnamon"
    assert _recommend(8.0) == "gnome"
    assert _recommend(16.0) == "gnome"


def test_desktop_env_list_complete():
    ids = {d["id"] for d in DESKTOP_ENVS}
    assert ids == {"gnome", "kde", "xfce", "cinnamon", "lxqt"}
    for d in DESKTOP_ENVS:
        assert d["tasksel"].startswith("task-")
        assert d["pros"] and d["cons"]


def test_desktop_env_prompt():
    hw = HardwareInfo(ram_gb=8.0, cpu_model="Intel", cpu_cores=4, gpu="Intel UHD")
    text = desktop_env_prompt(hw, "kde")
    assert "kde" in text
    assert "8.0" in text


# --- ch 10 ----------------------------------------------------------

def test_ime_prompt():
    hw = HardwareInfo(ram_gb=8.0)
    text = ime_prompt(hw, "gnome")
    assert "Fcitx5" in text
    assert "Mozc" in text
    assert "gnome" in text


# --- ch 11 ----------------------------------------------------------

def test_install_table_not_empty():
    assert len(TABLE) >= 50


def test_find_install_known():
    e = find_install("LibreOffice Writer")
    assert e is not None
    assert e["method"] == "apt"


def test_find_install_unknown_returns_none():
    assert find_install("TotallyMadeUpApp") is None


def test_find_install_strips_parens():
    e = find_install("Discord (Linux 公式)")
    assert e is not None
    assert e["method"] == "flatpak"


def test_install_plan_lines_built_from_replacements():
    # Seed state
    STATE.replacements = [
        Replacement(
            detected="Microsoft Word",
            alternatives=["LibreOffice Writer", "ONLYOFFICE Desktop"],
            confidence="ok",
            user_choice="ok",
        ),
        Replacement(
            detected="Slack",
            alternatives=["Slack (Linux 公式)"],
            confidence="ok",
            user_choice="ok",
        ),
        Replacement(
            detected="Notion",
            alternatives=["Joplin"],
            confidence="review",
            # Not yet decided — should be skipped
            user_choice=None,
        ),
    ]
    lines = _build_install_lines()
    detected_names = [l[0] for l in lines]
    assert any("Microsoft Word" in n for n in detected_names)
    assert any("Slack" in n for n in detected_names)
    assert not any("Notion" in n for n in detected_names)


def test_install_plan_batch_script_groups():
    STATE.replacements = [
        Replacement(
            detected="Microsoft Word",
            alternatives=["LibreOffice Writer"],
            confidence="ok",
            user_choice="ok",
        ),
        Replacement(
            detected="Slack",
            alternatives=["Slack (Linux 公式)"],
            confidence="ok",
            user_choice="ok",
        ),
    ]
    lines = _build_install_lines()
    script = _build_batch_script(lines)
    assert "apt パッケージ" in script
    assert "sudo apt install" in script and "libreoffice" in script
    assert "Flatpak" in script
    assert "com.slack.Slack" in script


def test_install_plan_prompt_empty():
    text = install_plan_prompt([])
    assert "まだ選んでいない" in text


def test_install_plan_prompt_with_lines():
    lines = [
        ("Microsoft Word → LibreOffice Writer", "LibreOffice Writer",
         "sudo apt install libreoffice", "Writer / Calc / Impress / Draw / Math が一括で入る"),
    ]
    text = install_plan_prompt(lines)
    assert "Microsoft Word" in text
    assert "sudo apt install libreoffice" in text


# --- ch 12 + 17 -------------------------------------------------------

def test_operations_prompt():
    from debian_migrate.prompts.templates import operations_prompt
    text = operations_prompt("kde")
    assert "dotfiles" in text
    assert "timeshift" in text or "snapshot" in text
    assert "kde" in text


@pytest.fixture(autouse=True)
def reset_state():
    snapshot = (
        STATE.detected_apps,
        STATE.replacements,
        STATE.hardware,
        STATE.usb_devices,
        STATE.selected_usb,
        STATE.chosen_desktop,
    )
    yield
    (
        STATE.detected_apps,
        STATE.replacements,
        STATE.hardware,
        STATE.usb_devices,
        STATE.selected_usb,
        STATE.chosen_desktop,
    ) = snapshot
