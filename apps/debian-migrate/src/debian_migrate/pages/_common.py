"""Shared UI helpers for the wizard pages."""

from __future__ import annotations

import flet as ft


def primary_button(label: str, on_click) -> ft.Control:
    return ft.FilledButton(label, on_click=on_click, icon=ft.Icons.ARROW_FORWARD)


def secondary_button(label: str, on_click, icon=None) -> ft.Control:
    return ft.OutlinedButton(label, on_click=on_click, icon=icon)


def section_title(text: str) -> ft.Control:
    return ft.Text(text, size=20, weight=ft.FontWeight.BOLD)


def page_intro(text: str) -> ft.Control:
    return ft.Container(
        content=ft.Text(text, size=14, color=ft.Colors.ON_SURFACE_VARIANT),
        padding=ft.padding.symmetric(vertical=8),
    )


def copy_prompt_button(prompt_factory) -> ft.Control:
    """A button that puts the result of `prompt_factory()` on the clipboard.

    The factory is called at click time so it sees the latest state.
    """

    def _click(e: ft.ControlEvent) -> None:
        text = prompt_factory()
        page = ft.context.page
        page.clipboard.set(text)
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(
                    "Claude 用のプロンプトをクリップボードにコピーしました。"
                    " claude.ai を開いて貼り付けてください。"
                ),
                duration=4000,
            )
        )

    return ft.OutlinedButton(
        "Claude 用プロンプトをコピー",
        icon=ft.Icons.CONTENT_COPY,
        on_click=_click,
    )


def confidence_chip(level: str) -> ft.Control:
    if level == "ok":
        return ft.Container(
            content=ft.Text("そのまま置換可", size=11, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN,
            padding=ft.padding.symmetric(horizontal=8, vertical=2),
            border_radius=10,
        )
    if level == "review":
        return ft.Container(
            content=ft.Text("要検討", size=11, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.ORANGE,
            padding=ft.padding.symmetric(horizontal=8, vertical=2),
            border_radius=10,
        )
    if level == "missing":
        return ft.Container(
            content=ft.Text("代替なし", size=11, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED,
            padding=ft.padding.symmetric(horizontal=8, vertical=2),
            border_radius=10,
        )
    return ft.Text("?", size=11)


def navigate(path: str) -> None:
    ft.context.page.navigate(path)
