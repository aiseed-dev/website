"""第 4 章: Debian での代替候補を提案する画面."""

from __future__ import annotations

import flet as ft

from debian_migrate.data.replacements import find_replacement
from debian_migrate.pages._common import (
    confidence_chip,
    copy_prompt_button,
    navigate,
    page_intro,
    primary_button,
    secondary_button,
    section_title,
)
from debian_migrate.prompts.templates import replacements_prompt
from debian_migrate.state import STATE, Replacement


def _build_replacements() -> list[Replacement]:
    """検出アプリ × 代替テーブル → 表示用 Replacement リスト."""
    out: list[Replacement] = []
    seen: set[str] = set()
    for app in STATE.detected_apps:
        entry = find_replacement(app.name)
        if not entry:
            continue
        key = entry["match"]
        if key in seen:
            continue
        seen.add(key)
        out.append(
            Replacement(
                detected=app.name,
                alternatives=list(entry["alternatives"]),
                confidence=entry["confidence"],
                note=entry["note"],
            )
        )
    return out


@ft.component
def ReplacementsPage() -> ft.Control:
    if not STATE.replacements:
        STATE.replacements = _build_replacements()
    reps, set_reps = ft.use_state(list(STATE.replacements))

    def set_choice(rep_index: int, choice: str | None) -> None:
        STATE.replacements[rep_index].user_choice = choice
        set_reps(list(STATE.replacements))

    return ft.Column(
        [
            section_title("2. Debian での代替候補"),
            page_intro(
                "検出したアプリのうち、移行で気をつけたほうがいいものを表にしました。"
                "「OK」「検討中」を選んで、次の画面に進みます。"
            ),
            ft.Container(height=8),
            _legend(),
            ft.Container(height=8),
            _body(reps, set_choice),
            ft.Container(height=16),
            ft.Row(
                [
                    secondary_button(
                        "戻る",
                        on_click=lambda _: navigate("/inventory"),
                        icon=ft.Icons.ARROW_BACK,
                    ),
                    ft.Container(expand=True),
                    copy_prompt_button(
                        lambda: replacements_prompt(STATE.replacements)
                    ),
                    primary_button(
                        "ハードウェアを確認",
                        on_click=lambda _: navigate("/hardware"),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        spacing=6,
    )


def _legend() -> ft.Control:
    return ft.Container(
        content=ft.Row(
            [
                confidence_chip("ok"),
                ft.Text(": Debian でほぼそのまま置き換えられる", size=12),
                ft.Container(width=12),
                confidence_chip("review"),
                ft.Text(": 動くが運用が変わる、要試用", size=12),
                ft.Container(width=12),
                confidence_chip("missing"),
                ft.Text(": 完全な代替なし、VM 等の検討が必要", size=12),
            ],
            wrap=True,
            spacing=6,
            run_spacing=8,
        ),
        padding=8,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
        border_radius=8,
    )


def _body(reps: list[Replacement], set_choice) -> ft.Control:
    if not reps:
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.INFO, size=36, color=ft.Colors.PRIMARY),
                        ft.Text(
                            "代替テーブルに登録されているアプリは見つかりませんでした。",
                            size=14,
                        ),
                        ft.Text(
                            "重要なアプリの代替は「Claude 用プロンプトをコピー」で"
                            "相談するのが確実です。",
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

    cards: list[ft.Control] = []
    for i, r in enumerate(reps):
        cards.append(_replacement_row(i, r, set_choice))
    return ft.Column(
        cards,
        scroll=ft.ScrollMode.AUTO,
        height=400,
        spacing=8,
    )


def _replacement_row(
    index: int, rep: Replacement, set_choice
) -> ft.Control:
    alt_chips = [
        ft.Container(
            content=ft.Text(alt, size=12),
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=8,
        )
        for alt in rep.alternatives
    ]

    def toggle_ok(_):
        new = None if rep.user_choice == "ok" else "ok"
        set_choice(index, new)

    def toggle_review(_):
        new = None if rep.user_choice == "review" else "review"
        set_choice(index, new)

    ok_selected = rep.user_choice == "ok"
    review_selected = rep.user_choice == "review"

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                rep.detected,
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                            ),
                            confidence_chip(rep.confidence),
                        ],
                    ),
                    ft.Container(height=4),
                    ft.Text("Debian 側の代替:", size=12,
                            color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Row(alt_chips, wrap=True, spacing=6, run_spacing=6),
                    (
                        ft.Container(
                            content=ft.Text(
                                f"💡 {rep.note}",
                                size=11,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                            padding=ft.padding.only(top=6),
                        )
                        if rep.note
                        else ft.Container()
                    ),
                    ft.Container(height=4),
                    ft.Row(
                        [
                            ft.FilledTonalButton(
                                "OK にする" if not ok_selected else "OK ✓",
                                icon=ft.Icons.CHECK,
                                on_click=toggle_ok,
                            ),
                            ft.OutlinedButton(
                                "検討中" if not review_selected else "検討中 ✓",
                                icon=ft.Icons.HELP_OUTLINE,
                                on_click=toggle_review,
                            ),
                        ],
                        spacing=8,
                    ),
                ],
            ),
            padding=14,
        ),
    )
