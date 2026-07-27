"""ようこそ画面 — wizard の入口."""

from __future__ import annotations

import flet as ft

from debian_migrate.pages._common import (
    navigate,
    page_intro,
    primary_button,
    section_title,
)


@ft.component
def WelcomePage() -> ft.Control:
    return ft.Column(
        [
            section_title("ようこそ"),
            page_intro(
                "このアプリは、いま使っている Windows / macOS / Linux から "
                "Debian Linux への移行を「始める前」に走らせる準備ツールです。"
            ),
            ft.Container(height=8),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "このアプリでやること",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                            _bullet(
                                "1. 今のアプリを検出 → Debian で動く代替を提案 (4 章)"
                            ),
                            _bullet(
                                "2. ハードウェアを見て、Debian が動きそうか判定 (6 章)"
                            ),
                            _bullet(
                                "3. USB インストーラ作成の手順を OS に合わせて案内 (7 章)"
                            ),
                            _bullet(
                                "4. インストール直後に出がちなトラブルを先に頭に入れる (8 章)"
                            ),
                            _bullet(
                                "5. デスクトップ環境 / 日本語入力 / アプリの導入計画 (9〜11 章)"
                            ),
                            _bullet(
                                "6. dotfiles + アップデートで長く使う設計 (12 章 + 17 章)"
                            ),
                            _bullet(
                                "7. 詰まったら「Claude 用プロンプトをコピー」ボタンで claude.ai に貼って相談"
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=16,
                ),
            ),
            ft.Container(height=8),
            ft.Container(
                content=ft.Text(
                    "このアプリは何も書き換えません。検出と提案だけを行います。"
                    "USB への書き込みも、最後はあなたが選んだツールで実行してください。",
                    size=12,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                padding=8,
                bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
                border_radius=8,
            ),
            ft.Container(height=16),
            ft.Row(
                [
                    primary_button(
                        "始める", on_click=lambda _: navigate("/inventory")
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Container(height=24),
            ft.Text(
                "底本: aiseed.dev 連載「Claudeと一緒に学ぶDebian」(全24章)",
                size=11,
                color=ft.Colors.ON_SURFACE_VARIANT,
                italic=True,
            ),
        ],
        spacing=6,
    )


def _bullet(text: str) -> ft.Control:
    return ft.Row(
        [
            ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color=ft.Colors.GREEN),
            ft.Text(text, size=13, expand=True),
        ],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )
