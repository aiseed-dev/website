"""アプリ全体の見た目 (テーマ + ウィンドウ設定)。

aiseed.dev の朱色 (#c8442a) を Material 3 のシード色として渡し、
明朝系の落ち着いた印象に近づける。フォントは OS の標準明朝/Serif を
そのまま使う (Flet desktop ではカスタムフォントを同梱すると配布が
重くなるため、v1 ではシステム依存)。
"""

from __future__ import annotations

import flet as ft


ACCENT_HEX = "#c8442a"


def configure_page(page: ft.Page) -> None:
    page.title = "Debian 移行ウィザード"
    page.window.width = 980
    page.window.height = 760
    page.window.min_width = 760
    page.window.min_height = 600
    page.window.center()

    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = _theme()
    page.dark_theme = _theme(dark=True)


def _theme(dark: bool = False) -> ft.Theme:
    return ft.Theme(
        color_scheme_seed=ACCENT_HEX,
        use_material3=True,
        visual_density=ft.VisualDensity.STANDARD,
    )
