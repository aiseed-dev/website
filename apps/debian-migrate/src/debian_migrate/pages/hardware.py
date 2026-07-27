"""第 6 章: ハードウェアの確認."""

from __future__ import annotations

import flet as ft

from debian_migrate.hardware.detect import detect as detect_hardware
from debian_migrate.pages._common import (
    copy_prompt_button,
    navigate,
    page_intro,
    primary_button,
    secondary_button,
    section_title,
)
from debian_migrate.prompts.templates import hardware_prompt
from debian_migrate.state import STATE


@ft.component
def HardwarePage() -> ft.Control:
    detected, set_detected = ft.use_state(bool(STATE.hardware.os_name))
    detecting, set_detecting = ft.use_state(False)

    def run_detect(_=None):
        set_detecting(True)
        try:
            STATE.hardware = detect_hardware()
        except Exception:
            pass
        set_detecting(False)
        set_detected(True)

    if not detected and not detecting:
        # Auto-detect on first visit
        run_detect()

    return ft.Column(
        [
            section_title("3. ハードウェアの確認"),
            page_intro(
                "Debian がこの PC で動きそうか、CPU・メモリ・ディスク・GPU を"
                "見て判定します。"
            ),
            ft.Container(height=8),
            _body(detecting),
            ft.Container(height=16),
            ft.Row(
                [
                    secondary_button(
                        "戻る",
                        on_click=lambda _: navigate("/replacements"),
                        icon=ft.Icons.ARROW_BACK,
                    ),
                    ft.Container(expand=True),
                    copy_prompt_button(lambda: hardware_prompt(STATE.hardware)),
                    secondary_button(
                        "再検出", on_click=run_detect, icon=ft.Icons.REFRESH
                    ),
                    primary_button(
                        "USB 作成へ", on_click=lambda _: navigate("/usb")
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        spacing=6,
    )


def _body(detecting: bool) -> ft.Control:
    if detecting:
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [ft.ProgressRing(width=24, height=24), ft.Text("検出中...")],
                    spacing=12,
                ),
                padding=24,
            )
        )

    hw = STATE.hardware
    return ft.Column(
        [
            _summary_card(hw),
            ft.Container(height=8),
            _disks_card(hw),
            ft.Container(height=8),
            _warnings_card(hw),
        ],
        spacing=0,
    )


def _summary_card(hw) -> ft.Control:
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("基本構成", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(height=4),
                    _kv("OS", f"{hw.os_name} {hw.os_version}"),
                    _kv("アーキ", hw.arch),
                    _kv("CPU", f"{hw.cpu_model} ({hw.cpu_cores} コア)"),
                    _kv("メモリ", f"{hw.ram_gb} GB"),
                    _kv("GPU", hw.gpu),
                ],
            ),
            padding=14,
        ),
    )


def _disks_card(hw) -> ft.Control:
    if not hw.disks:
        return ft.Container()
    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(d["device"], size=12)),
                ft.DataCell(ft.Text(d["mountpoint"], size=12)),
                ft.DataCell(ft.Text(d["fstype"], size=12)),
                ft.DataCell(ft.Text(f"{d['total_gb']} GB", size=12)),
                ft.DataCell(ft.Text(f"{d['free_gb']} GB", size=12)),
            ]
        )
        for d in hw.disks
    ]
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("ディスク", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(height=4),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("デバイス")),
                            ft.DataColumn(ft.Text("マウント")),
                            ft.DataColumn(ft.Text("FS")),
                            ft.DataColumn(ft.Text("全体")),
                            ft.DataColumn(ft.Text("空き")),
                        ],
                        rows=rows,
                    ),
                ],
            ),
            padding=14,
        ),
    )


def _warnings_card(hw) -> ft.Control:
    if not hw.warnings:
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE,
                            color=ft.Colors.GREEN,
                            size=20,
                        ),
                        ft.Text(
                            "特に注意点はなさそうです。Debian の標準的な"
                            "インストールで進められます。",
                            size=13,
                        ),
                    ],
                    spacing=8,
                ),
                padding=14,
            )
        )
    items = [
        ft.Row(
            [
                ft.Icon(
                    ft.Icons.WARNING_AMBER,
                    color=ft.Colors.ORANGE,
                    size=20,
                ),
                ft.Text(w, size=13, expand=True),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        for w in hw.warnings
    ]
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "注意点", size=16, weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(height=4),
                    *items,
                ],
                spacing=6,
            ),
            padding=14,
        ),
    )


def _kv(k: str, v: str) -> ft.Control:
    return ft.Row(
        [
            ft.Text(k, size=13, color=ft.Colors.ON_SURFACE_VARIANT, width=90),
            ft.Text(v, size=13, selectable=True, expand=True),
        ],
    )
