"""第 11 章: 代替候補からアプリ導入コマンドを生成する."""

from __future__ import annotations

import flet as ft

from debian_migrate.data.install_commands import find_install
from debian_migrate.pages._common import (
    copy_prompt_button,
    navigate,
    page_intro,
    primary_button,
    secondary_button,
    section_title,
)
from debian_migrate.prompts.templates import install_plan_prompt
from debian_migrate.state import STATE


def _build_install_lines() -> list[tuple[str, str, str, str]]:
    """Return (label, alt_name, command, note) per selected alternative.

    第 3 ステップで「OK」「検討中」を選んだ Replacement の各 alternative を
    走査して、Debian での入れ方を引く。完全一致しない代替は
    method='manual' + URL ヒントの note にする。"""
    out: list[tuple[str, str, str, str]] = []
    seen: set[str] = set()
    for rep in STATE.replacements:
        if not rep.user_choice:
            continue
        # 「OK」なら最初の代替、「検討中」なら最初の代替を取る (UI 簡素化)
        if not rep.alternatives:
            continue
        alt = rep.alternatives[0]
        if alt.lower() in seen:
            continue
        seen.add(alt.lower())
        entry = find_install(alt)
        if entry:
            label = f"{rep.detected} → {alt}"
            out.append((label, alt, entry["command"], entry["note"]))
        else:
            label = f"{rep.detected} → {alt}"
            out.append(
                (
                    label,
                    alt,
                    "(公式サイトを確認)",
                    "テーブル未登録。Claude にこの代替の Debian 導入方法を聞くのが早い。",
                )
            )
    return out


def _build_batch_script(lines: list[tuple[str, str, str, str]]) -> str:
    """apt 系のコマンドを 1 行に集約したスクリプトを返す."""
    apt_pkgs: list[str] = []
    flatpak_apps: list[str] = []
    others: list[str] = []
    for _label, _alt, cmd, _note in lines:
        if cmd.startswith("sudo apt install "):
            apt_pkgs.extend(cmd[len("sudo apt install "):].split())
        elif cmd.startswith("flatpak install"):
            # `flatpak install -y flathub <id>`
            parts = cmd.split()
            if len(parts) >= 4:
                flatpak_apps.append(parts[-1])
        else:
            others.append(cmd)
    out: list[str] = []
    if apt_pkgs:
        out.append("# apt パッケージ")
        out.append("sudo apt update")
        out.append(
            "sudo apt install -y " + " ".join(sorted(set(apt_pkgs)))
        )
        out.append("")
    if flatpak_apps:
        out.append("# Flatpak (初回のみ flathub を登録)")
        out.append(
            "flatpak remote-add --if-not-exists flathub "
            "https://flathub.org/repo/flathub.flatpakrepo"
        )
        for app in sorted(set(flatpak_apps)):
            out.append(f"flatpak install -y flathub {app}")
        out.append("")
    if others:
        out.append("# 手動 (公式 .deb / インストールスクリプト)")
        for cmd in others:
            out.append(f"# {cmd}")
        out.append("")
    return "\n".join(out).strip() or "# (選択された代替がありません — 前のステップで「OK」を押してください)"


@ft.component
def InstallPlanPage() -> ft.Control:
    lines = _build_install_lines()

    return ft.Column(
        [
            section_title("8. Debian でのアプリ導入計画"),
            page_intro(
                "ステップ 3 (代替候補) で「OK」を押した代替について、"
                "Debian での入れ方をまとめます。Debian 起動後、ターミナル"
                "にそのまま貼れる形にしてあります。"
            ),
            ft.Container(height=8),
            _summary_card(lines),
            ft.Container(height=8),
            _detail_list(lines),
            ft.Container(height=8),
            _batch_card(lines),
            ft.Container(height=16),
            ft.Row(
                [
                    secondary_button(
                        "戻る",
                        on_click=lambda _: navigate("/ime"),
                        icon=ft.Icons.ARROW_BACK,
                    ),
                    ft.Container(expand=True),
                    copy_prompt_button(
                        lambda: install_plan_prompt(lines)
                    ),
                    primary_button(
                        "運用とメンテへ",
                        on_click=lambda _: navigate("/operations"),
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        spacing=6,
    )


def _summary_card(lines: list[tuple[str, str, str, str]]) -> ft.Control:
    apt_count = sum(1 for _, _, c, _ in lines if c.startswith("sudo apt"))
    flat_count = sum(1 for _, _, c, _ in lines if c.startswith("flatpak"))
    manual = len(lines) - apt_count - flat_count

    return ft.Card(
        content=ft.Container(
            content=ft.Row(
                [
                    _stat("対象アプリ", str(len(lines))),
                    _stat("apt で入る", str(apt_count)),
                    _stat("Flatpak", str(flat_count)),
                    _stat("手動", str(manual)),
                ],
                spacing=12,
                wrap=True,
            ),
            padding=14,
        )
    )


def _stat(label: str, value: str) -> ft.Control:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(label, size=11, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Text(value, size=20, weight=ft.FontWeight.BOLD),
            ],
            spacing=0,
        ),
        padding=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        border_radius=10,
        width=140,
    )


def _detail_list(lines: list[tuple[str, str, str, str]]) -> ft.Control:
    if not lines:
        return ft.Card(
            content=ft.Container(
                content=ft.Text(
                    "代替候補で「OK」を押した項目がありません。"
                    "前のステップに戻って選択してください。",
                    size=13,
                ),
                padding=14,
            )
        )

    items: list[ft.Control] = []
    for label, alt, cmd, note in lines:
        items.append(_install_row(label, alt, cmd, note))
    return ft.Column(items, spacing=8, scroll=ft.ScrollMode.AUTO, height=320)


def _install_row(label: str, alt: str, cmd: str, note: str) -> ft.Control:
    def copy_cmd(_):
        page = ft.context.page
        page.clipboard.set(cmd)
        page.show_dialog(
            ft.SnackBar(content=ft.Text(f"コピー: {alt}"), duration=2000)
        )

    method_badge = _method_badge(cmd)

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                label,
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                            ),
                            method_badge,
                        ],
                    ),
                    ft.Container(
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
                    ),
                    (
                        ft.Text(
                            f"💡 {note}",
                            size=11,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        )
                        if note
                        else ft.Container()
                    ),
                ],
                spacing=4,
            ),
            padding=12,
        )
    )


def _method_badge(cmd: str) -> ft.Control:
    if cmd.startswith("sudo apt"):
        return _badge("apt", ft.Colors.PRIMARY)
    if cmd.startswith("flatpak"):
        return _badge("Flatpak", ft.Colors.BLUE)
    if cmd.startswith("("):
        return _badge("手動", ft.Colors.ORANGE)
    return _badge("script", ft.Colors.GREEN)


def _badge(text: str, color) -> ft.Control:
    return ft.Container(
        content=ft.Text(text, size=10, color=ft.Colors.WHITE),
        bgcolor=color,
        padding=ft.padding.symmetric(horizontal=8, vertical=2),
        border_radius=10,
    )


def _batch_card(lines: list[tuple[str, str, str, str]]) -> ft.Control:
    script = _build_batch_script(lines)

    def copy_script(_):
        page = ft.context.page
        page.clipboard.set(script)
        page.show_dialog(
            ft.SnackBar(content=ft.Text("一括スクリプトをコピー"), duration=2500)
        )

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "一括インストールスクリプト",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                            ),
                            ft.OutlinedButton(
                                "全部コピー",
                                icon=ft.Icons.CONTENT_COPY,
                                on_click=copy_script,
                            ),
                        ],
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "Debian 起動後にターミナルに貼ると、apt と Flatpak をまとめて入れます。"
                        "手動分はコメントとして残します。",
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Container(height=8),
                    ft.Container(
                        content=ft.Text(
                            script,
                            selectable=True,
                            font_family="JetBrains Mono, monospace",
                            size=11,
                        ),
                        padding=10,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                        border_radius=8,
                    ),
                ],
                spacing=4,
            ),
            padding=14,
        )
    )
