"""第 4 章: インストール済みアプリの棚卸し."""

from __future__ import annotations

import flet as ft

from debian_migrate import scanners
from debian_migrate.pages._common import (
    copy_prompt_button,
    navigate,
    page_intro,
    primary_button,
    secondary_button,
    section_title,
)
from debian_migrate.prompts.templates import inventory_prompt
from debian_migrate.state import STATE


@ft.component
def InventoryPage() -> ft.Control:
    scanned, set_scanned = ft.use_state(bool(STATE.detected_apps))
    scanning, set_scanning = ft.use_state(False)
    apps, set_apps = ft.use_state(list(STATE.detected_apps))

    def run_scan(_):
        set_scanning(True)
        try:
            found = scanners.scan()
        except Exception:
            found = []
        STATE.detected_apps = found
        set_apps(found)
        set_scanning(False)
        set_scanned(True)

    return ft.Column(
        [
            section_title("1. アプリの棚卸し"),
            page_intro(
                "いま PC に入っているアプリを一覧にします。次の画面で、"
                "Debian で動く代替を候補表から提案します。"
            ),
            ft.Container(height=8),
            _scan_card(scanned, scanning, apps, run_scan),
            ft.Container(height=16),
            ft.Row(
                [
                    secondary_button(
                        "戻る",
                        on_click=lambda _: navigate("/"),
                        icon=ft.Icons.ARROW_BACK,
                    ),
                    ft.Container(expand=True),
                    copy_prompt_button(lambda: inventory_prompt(STATE.detected_apps)),
                    primary_button(
                        "代替候補を見る",
                        on_click=lambda _: navigate("/replacements"),
                    )
                    if scanned
                    else ft.Container(),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        spacing=6,
    )


def _scan_card(scanned: bool, scanning: bool, apps: list, on_scan) -> ft.Control:
    if scanning:
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ProgressRing(),
                        ft.Text("検出中...", size=14),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                padding=32,
                alignment=ft.alignment.center,
            )
        )
    if not scanned:
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.SEARCH, size=48, color=ft.Colors.PRIMARY),
                        ft.Text(
                            "「アプリを検出する」を押してください。",
                            size=14,
                        ),
                        ft.Text(
                            "OS によって調べる場所が違うので、"
                            "場合によっては数秒〜十数秒かかります。",
                            size=12,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                        ft.Container(height=8),
                        ft.FilledButton(
                            "アプリを検出する",
                            icon=ft.Icons.PLAY_ARROW,
                            on_click=on_scan,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                padding=32,
                alignment=ft.alignment.center,
            )
        )
    # scanned
    if not apps:
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.INFO,
                            size=36,
                            color=ft.Colors.ORANGE,
                        ),
                        ft.Text(
                            "アプリを自動検出できませんでした。",
                            size=14,
                        ),
                        ft.Text(
                            "次の画面で重要なアプリを手入力するか、Claude に"
                            "現状を伝えて代替を相談する方法もあります。",
                            size=12,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=24,
                alignment=ft.alignment.center,
            )
        )
    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(a.name)),
                ft.DataCell(ft.Text(a.publisher or "—", size=12)),
                ft.DataCell(ft.Text(a.version or "—", size=12)),
            ]
        )
        for a in apps
    ]
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.CHECK_CIRCLE,
                                size=20,
                                color=ft.Colors.GREEN,
                            ),
                            ft.Text(
                                f"{len(apps)} 個のアプリを検出しました。",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=4),
                    ft.Column(
                        [
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("アプリ名")),
                                    ft.DataColumn(ft.Text("提供元")),
                                    ft.DataColumn(ft.Text("バージョン")),
                                ],
                                rows=rows,
                            )
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        height=380,
                    ),
                ]
            ),
            padding=16,
        )
    )
