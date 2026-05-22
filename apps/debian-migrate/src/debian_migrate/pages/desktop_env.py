"""第 9 章: デスクトップ環境の選択."""

from __future__ import annotations

import flet as ft

from debian_migrate.pages._common import (
    copy_prompt_button,
    navigate,
    page_intro,
    primary_button,
    secondary_button,
    section_title,
)
from debian_migrate.prompts.templates import desktop_env_prompt
from debian_migrate.state import STATE


# DE 一覧。重さの指標は GiB 単位の RAM 推奨下限。
DESKTOP_ENVS = [
    {
        "id": "gnome",
        "name": "GNOME",
        "ram_gb": 4.0,
        "tasksel": "task-gnome-desktop",
        "summary": "Debian 既定。シンプルで一貫した UI、Wayland に強い。",
        "pros": ["既定なので情報が豊富", "Wayland 対応が成熟", "拡張機能の生態系が大きい"],
        "cons": ["メモリ消費がやや多い", "カスタマイズは拡張機能経由"],
    },
    {
        "id": "kde",
        "name": "KDE Plasma",
        "ram_gb": 4.0,
        "tasksel": "task-kde-desktop",
        "summary": "Windows / macOS から移ってきた人に親しみやすい。",
        "pros": ["設定項目が豊富", "見た目を細かく調整できる", "アプリ群が揃っている (Dolphin / Konsole / Kate)"],
        "cons": ["設定が多く迷いやすい", "Wayland はまだ場面で不安定"],
    },
    {
        "id": "xfce",
        "name": "XFCE",
        "ram_gb": 2.0,
        "tasksel": "task-xfce-desktop",
        "summary": "軽量・古典的なデスクトップ。古い PC でも快適。",
        "pros": ["軽い (RAM 4GB でも快適)", "癖が少ない", "壊れにくい"],
        "cons": ["Wayland 対応がまだ", "見た目が地味"],
    },
    {
        "id": "cinnamon",
        "name": "Cinnamon",
        "ram_gb": 3.0,
        "tasksel": "task-cinnamon-desktop",
        "summary": "Windows っぽい操作感。Linux Mint で有名。",
        "pros": ["Windows から来た人に直感的", "GNOME より軽い"],
        "cons": ["Debian 標準より Mint 寄りの情報が多い"],
    },
    {
        "id": "lxqt",
        "name": "LXQt",
        "ram_gb": 1.0,
        "tasksel": "task-lxqt-desktop",
        "summary": "最軽量級。古い PC / メモリ 2GB 以下向け。",
        "pros": ["とにかく軽い", "リソースを最小限に使う"],
        "cons": ["見た目が古風", "情報が他より少なめ"],
    },
]


def _recommend(ram_gb: float) -> str:
    """推奨 DE の id を返す."""
    if ram_gb <= 2:
        return "lxqt"
    if ram_gb <= 4:
        return "xfce"
    if ram_gb <= 6:
        return "cinnamon"
    return "gnome"


@ft.component
def DesktopEnvPage() -> ft.Control:
    ram = STATE.hardware.ram_gb or 0.0
    recommended = _recommend(ram)
    choice, set_choice = ft.use_state(STATE.chosen_desktop or recommended)

    def pick(de_id: str) -> None:
        STATE.chosen_desktop = de_id
        set_choice(de_id)

    # 一度も選択していない場合は推奨値を初期選択として STATE にも入れる
    if not STATE.chosen_desktop:
        STATE.chosen_desktop = recommended

    return ft.Column(
        [
            section_title("6. デスクトップ環境の選択"),
            page_intro(
                "Debian インストール中に「どんな見た目で使うか」を選びます。"
                "後でも変えられるけれど、最初は一つ選んでおくとスムーズです。"
            ),
            ft.Container(height=8),
            _ram_summary(ram, recommended),
            ft.Container(height=8),
            _de_grid(choice, pick, recommended, ram),
            ft.Container(height=8),
            _install_commands(choice),
            ft.Container(height=16),
            ft.Row(
                [
                    secondary_button(
                        "戻る",
                        on_click=lambda _: navigate("/troubleshooting"),
                        icon=ft.Icons.ARROW_BACK,
                    ),
                    ft.Container(expand=True),
                    copy_prompt_button(
                        lambda: desktop_env_prompt(STATE.hardware, STATE.chosen_desktop)
                    ),
                    primary_button(
                        "日本語入力へ", on_click=lambda _: navigate("/ime")
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        spacing=6,
    )


def _ram_summary(ram_gb: float, recommended: str) -> ft.Control:
    rec_name = next(d["name"] for d in DESKTOP_ENVS if d["id"] == recommended)
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.MEMORY, size=20, color=ft.Colors.PRIMARY),
                ft.Text(
                    f"メモリ {ram_gb} GB の構成では、**{rec_name}** がバランス良いです。",
                    size=13,
                ),
            ],
            spacing=10,
        ),
        padding=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
        border_radius=8,
    )


def _de_grid(choice: str, pick, recommended: str, ram_gb: float) -> ft.Control:
    cards: list[ft.Control] = []
    for de in DESKTOP_ENVS:
        cards.append(_de_card(de, choice == de["id"], recommended == de["id"],
                              ram_gb, pick))
    return ft.Column(cards, spacing=8, scroll=ft.ScrollMode.AUTO, height=380)


def _de_card(de: dict, selected: bool, is_recommended: bool,
             ram_gb: float, pick) -> ft.Control:
    fits = ram_gb >= de["ram_gb"] if ram_gb else True
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                de["name"],
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                            (
                                ft.Container(
                                    content=ft.Text(
                                        "オススメ",
                                        size=10,
                                        color=ft.Colors.WHITE,
                                    ),
                                    bgcolor=ft.Colors.PRIMARY,
                                    padding=ft.padding.symmetric(
                                        horizontal=8, vertical=2
                                    ),
                                    border_radius=8,
                                )
                                if is_recommended
                                else ft.Container()
                            ),
                            (
                                ft.Container(
                                    content=ft.Text(
                                        f"⚠ メモリ {de['ram_gb']}GB+ 推奨",
                                        size=10,
                                        color=ft.Colors.WHITE,
                                    ),
                                    bgcolor=ft.Colors.ORANGE,
                                    padding=ft.padding.symmetric(
                                        horizontal=8, vertical=2
                                    ),
                                    border_radius=8,
                                )
                                if not fits
                                else ft.Container()
                            ),
                            ft.Container(expand=True),
                            ft.FilledButton(
                                "選択中" if selected else "これにする",
                                disabled=selected,
                                on_click=lambda _, i=de["id"]: pick(i),
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Text(de["summary"], size=12),
                    ft.Container(height=2),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "○ いいところ",
                                        size=11,
                                        color=ft.Colors.GREEN,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    *[
                                        ft.Text(f"  {p}", size=11)
                                        for p in de["pros"]
                                    ],
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "△ 注意点",
                                        size=11,
                                        color=ft.Colors.ORANGE,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    *[
                                        ft.Text(f"  {c}", size=11)
                                        for c in de["cons"]
                                    ],
                                ],
                                spacing=2,
                                expand=True,
                            ),
                        ],
                    ),
                ],
                spacing=4,
            ),
            padding=12,
            bgcolor=(
                ft.Colors.PRIMARY_CONTAINER if selected else None
            ),
            border_radius=8,
        ),
    )


def _install_commands(choice: str) -> ft.Control:
    de = next((d for d in DESKTOP_ENVS if d["id"] == choice), DESKTOP_ENVS[0])
    cmd1 = f"sudo apt update && sudo apt install {de['tasksel']}"
    cmd2 = f"sudo tasksel install {de['tasksel'].replace('task-', '').replace('-desktop', '-desktop')}"

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        f"{de['name']} を後から入れるコマンド",
                        size=15,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "Debian インストール中に DE を選び忘れた場合や、"
                        "別の DE を試したい場合に。",
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Container(height=8),
                    _cmd_box(cmd1),
                ],
            ),
            padding=14,
        )
    )


def _cmd_box(cmd: str) -> ft.Control:
    def copy_cmd(_):
        page = ft.context.page
        page.clipboard.set(cmd)
        page.show_dialog(
            ft.SnackBar(content=ft.Text("コマンドをコピー"), duration=2000)
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
        padding=ft.padding.symmetric(horizontal=10, vertical=4),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        border_radius=8,
    )
