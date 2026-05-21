"""第 7 章: USB インストーラの作成ガイド (書き込みは外部ツールに委ねる)."""

from __future__ import annotations

import platform

import flet as ft

from debian_migrate.pages._common import (
    copy_prompt_button,
    navigate,
    page_intro,
    primary_button,
    secondary_button,
    section_title,
)
from debian_migrate.prompts.templates import usb_prompt
from debian_migrate.state import STATE
from debian_migrate.usb import creator


@ft.component
def UsbInstallerPage() -> ft.Control:
    scanned, set_scanned = ft.use_state(bool(STATE.usb_devices))
    scanning, set_scanning = ft.use_state(False)
    selected, set_selected = ft.use_state(STATE.selected_usb)

    def run_scan(_=None):
        set_scanning(True)
        try:
            STATE.usb_devices = creator.list_usb_devices()
        except Exception:
            STATE.usb_devices = []
        set_scanning(False)
        set_scanned(True)

    def pick(device_path: str) -> None:
        STATE.selected_usb = device_path
        set_selected(device_path)

    if not scanned and not scanning:
        run_scan()

    return ft.Column(
        [
            section_title("4. USB インストーラを作る"),
            page_intro(
                "Debian の ISO ファイルを入手して、USB メモリに書き込みます。"
                "書き込みは間違えるとデータが消えるので、このアプリは"
                "「コマンドや手順を表示するだけ」にしてあります。"
            ),
            ft.Container(height=8),
            _step1_download(),
            ft.Container(height=8),
            _step2_select_usb(scanning, STATE.usb_devices, selected, pick, run_scan),
            ft.Container(height=8),
            _step3_write(selected),
            ft.Container(height=16),
            ft.Row(
                [
                    secondary_button(
                        "戻る",
                        on_click=lambda _: navigate("/hardware"),
                        icon=ft.Icons.ARROW_BACK,
                    ),
                    ft.Container(expand=True),
                    copy_prompt_button(
                        lambda: usb_prompt(STATE.usb_devices, STATE.selected_usb)
                    ),
                    primary_button(
                        "まとめへ", on_click=lambda _: navigate("/export")
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        spacing=6,
    )


def _step1_download() -> ft.Control:
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            _step_badge("①"),
                            ft.Text(
                                "Debian の ISO ファイルをダウンロード",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=6),
                    ft.Text(
                        "初心者には「ネットインストーラ (netinst)」がおすすめです。"
                        "300〜500MB と小さく、必要なものだけ後でネットから入れます。",
                        size=13,
                    ),
                    ft.Container(height=8),
                    ft.Row(
                        [
                            ft.FilledTonalButton(
                                "ネットインストーラの配布ページを開く",
                                icon=ft.Icons.OPEN_IN_NEW,
                                on_click=lambda _: ft.context.page.launch_url(
                                    creator.DEBIAN_NETINST_URL
                                ),
                            ),
                            ft.OutlinedButton(
                                "Debian トップへ",
                                icon=ft.Icons.OPEN_IN_NEW,
                                on_click=lambda _: ft.context.page.launch_url(
                                    creator.DEBIAN_ISO_URL
                                ),
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=6),
                    ft.Text(
                        "ダウンロードした .iso ファイルの場所を覚えておいてください。",
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                ],
            ),
            padding=14,
        )
    )


def _step2_select_usb(
    scanning: bool,
    devices: list,
    selected: str | None,
    pick,
    on_rescan,
) -> ft.Control:
    if scanning:
        inner: ft.Control = ft.Row(
            [ft.ProgressRing(width=20, height=20), ft.Text("USB を探しています...")],
            spacing=10,
        )
    elif not devices:
        inner = ft.Column(
            [
                ft.Text(
                    "USB メモリが見つかりません。差し込んでから「再スキャン」を押してください。",
                    size=13,
                ),
                ft.Container(height=4),
                ft.OutlinedButton(
                    "再スキャン", icon=ft.Icons.REFRESH, on_click=on_rescan
                ),
            ],
        )
    else:
        items: list[ft.Control] = []
        for d in devices:
            chosen = selected == d.path
            items.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.USB,
                                color=ft.Colors.PRIMARY if chosen else ft.Colors.OUTLINE,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        d.label or d.path,
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        f"{d.path} · {d.size_gb} GB"
                                        + (f" · {d.vendor}" if d.vendor else ""),
                                        size=11,
                                        color=ft.Colors.ON_SURFACE_VARIANT,
                                    ),
                                ],
                                expand=True,
                                spacing=2,
                            ),
                            ft.FilledButton(
                                "選択中" if chosen else "これを使う",
                                disabled=chosen,
                                on_click=lambda _, p=d.path: pick(p),
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=10,
                    bgcolor=(
                        ft.Colors.PRIMARY_CONTAINER
                        if chosen
                        else ft.Colors.SURFACE_CONTAINER_LOWEST
                    ),
                    border_radius=8,
                )
            )
        items.append(
            ft.Row(
                [
                    ft.OutlinedButton(
                        "再スキャン", icon=ft.Icons.REFRESH, on_click=on_rescan
                    )
                ]
            )
        )
        inner = ft.Column(items, spacing=8)

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            _step_badge("②"),
                            ft.Text(
                                "書き込み先の USB を選ぶ",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=6),
                    ft.Container(
                        content=ft.Text(
                            "⚠ 選んだ USB の中身はすべて消えます。"
                            "大事なファイルが入っていないか、もう一度確認してください。",
                            size=12,
                            color=ft.Colors.ERROR,
                        ),
                        padding=8,
                        bgcolor=ft.Colors.ERROR_CONTAINER,
                        border_radius=8,
                    ),
                    ft.Container(height=8),
                    inner,
                ],
            ),
            padding=14,
        )
    )


def _step3_write(selected: str | None) -> ft.Control:
    info = creator.write_command(
        selected or "/dev/sdX", "/path/to/debian.iso"
    )
    system = platform.system()

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            _step_badge("③"),
                            ft.Text(
                                "USB に書き込む", size=15,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=6),
                    ft.Text(
                        f"あなたの OS: {system}",
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Container(height=4),
                    ft.Text("おすすめの GUI ツール:", size=13),
                    ft.Text(
                        info["gui"],
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        selectable=True,
                    ),
                    ft.Row(
                        [
                            ft.OutlinedButton(
                                "Balena Etcher のページを開く",
                                icon=ft.Icons.OPEN_IN_NEW,
                                on_click=lambda _: ft.context.page.launch_url(
                                    "https://etcher.balena.io/"
                                ),
                            )
                        ]
                    ),
                    ft.Container(height=10),
                    ft.Text("または、ターミナルで:", size=13),
                    _command_card(info["command"]),
                    ft.Container(height=4),
                    ft.Text(
                        f"({info['tool']} を使う)",
                        size=11,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Container(height=8),
                    ft.Container(
                        content=ft.Text(
                            "⚠ コマンドの `of=` に書く USB デバイスは"
                            " **絶対に間違えない** でください。"
                            " 間違えると Mac/PC 本体のディスクが消えます。"
                            " 上で「これを使う」を押した USB の名前を確認して、"
                            " 落ち着いて貼り付けてください。",
                            size=12,
                        ),
                        padding=10,
                        bgcolor=ft.Colors.ERROR_CONTAINER,
                        border_radius=8,
                    ),
                ],
            ),
            padding=14,
        )
    )


def _command_card(cmd: str) -> ft.Control:
    def copy_cmd(_):
        page = ft.context.page
        page.set_clipboard(cmd)
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("コマンドをコピーしました。"),
                duration=2500,
            )
        )

    return ft.Container(
        content=ft.Row(
            [
                ft.Text(
                    cmd,
                    selectable=True,
                    font_family="JetBrains Mono, monospace",
                    size=12,
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.Icons.CONTENT_COPY,
                    tooltip="コピー",
                    on_click=copy_cmd,
                ),
            ],
        ),
        padding=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        border_radius=8,
    )


def _step_badge(text: str) -> ft.Control:
    return ft.Container(
        content=ft.Text(text, size=16, weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE),
        bgcolor=ft.Colors.PRIMARY,
        width=28,
        height=28,
        border_radius=14,
        alignment=ft.alignment.center,
    )
