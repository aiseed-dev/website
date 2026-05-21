"""最終画面: まとめ + Claude 用プロンプト + Markdown レポートのエクスポート."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import flet as ft

from debian_migrate.pages._common import (
    copy_prompt_button,
    navigate,
    page_intro,
    secondary_button,
    section_title,
)
from debian_migrate.prompts.templates import summary_prompt
from debian_migrate.state import STATE


@ft.component
def ExportPage() -> ft.Control:
    saved_path, set_saved_path = ft.use_state(None)

    def save_report(_):
        try:
            home = Path.home()
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            path = home / f"debian-migrate-report-{stamp}.md"
            path.write_text(_render_markdown(), encoding="utf-8")
            set_saved_path(str(path))
        except Exception as exc:
            ft.context.page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"保存に失敗しました: {exc}"))
            )

    return ft.Column(
        [
            section_title("5. まとめ"),
            page_intro(
                "ここまでの内容を一覧にしました。Markdown ファイルに保存して"
                "おけば、いつでも見返せます。Claude に渡すプロンプトも一括で"
                "コピーできます。"
            ),
            ft.Container(height=8),
            _summary_cards(),
            ft.Container(height=12),
            _next_steps(),
            ft.Container(height=12),
            ft.Row(
                [
                    secondary_button(
                        "戻る",
                        on_click=lambda _: navigate("/usb"),
                        icon=ft.Icons.ARROW_BACK,
                    ),
                    ft.Container(expand=True),
                    ft.OutlinedButton(
                        "Markdown レポートを保存",
                        icon=ft.Icons.SAVE,
                        on_click=save_report,
                    ),
                    copy_prompt_button(
                        lambda: summary_prompt(
                            STATE.detected_apps,
                            STATE.replacements,
                            STATE.hardware,
                            STATE.selected_usb,
                        )
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            (
                ft.Container(
                    content=ft.Text(
                        f"保存しました: {saved_path}",
                        size=12,
                        color=ft.Colors.GREEN,
                        selectable=True,
                    ),
                    padding=ft.padding.only(top=8),
                )
                if saved_path
                else ft.Container()
            ),
        ],
        spacing=6,
    )


def _summary_cards() -> ft.Control:
    apps = STATE.detected_apps
    reps = STATE.replacements
    hw = STATE.hardware
    decided = sum(1 for r in reps if r.user_choice)
    review = sum(1 for r in reps if r.confidence in ("review", "missing"))

    items = [
        _stat("検出アプリ", f"{len(apps)} 個"),
        _stat("代替を確認", f"{decided} / {len(reps)} 件"),
        _stat("要検討", f"{review} 件"),
        _stat("ハードウェア警告", f"{len(hw.warnings)} 件"),
        _stat("選択した USB", STATE.selected_usb or "(未選択)"),
    ]
    return ft.Row(items, wrap=True, spacing=8, run_spacing=8)


def _stat(label: str, value: str) -> ft.Control:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(label, size=11, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Text(value, size=18, weight=ft.FontWeight.BOLD),
            ],
            spacing=2,
        ),
        padding=12,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        border_radius=10,
        width=180,
    )


def _next_steps() -> ft.Control:
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "このあとの進め方", size=16, weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(height=4),
                    _step(
                        "1.",
                        "「Claude 用プロンプトをコピー」で claude.ai に貼り、"
                        "全体プランをチェックしてもらう。",
                    ),
                    _step(
                        "2.",
                        "Markdown レポートを保存して、移行作業中も手元に置いておく。",
                    ),
                    _step(
                        "3.",
                        "本書 第 7 章「インストール実行の対話」を開き、"
                        "実際のインストールに進む。",
                    ),
                    _step(
                        "4.",
                        "Debian が立ち上がったら、第 9 章 (デスクトップ)、"
                        "第 10 章 (日本語入力)、第 11 章 (アプリ選択) に進む。",
                    ),
                    ft.Container(height=4),
                    ft.Row(
                        [
                            ft.OutlinedButton(
                                "「Claudeと一緒に学ぶDebian」を開く",
                                icon=ft.Icons.OPEN_IN_NEW,
                                on_click=lambda _: ft.context.page.launch_url(
                                    "https://aiseed.dev/claude-debian/"
                                ),
                            ),
                        ]
                    ),
                ],
                spacing=4,
            ),
            padding=14,
        )
    )


def _step(num: str, text: str) -> ft.Control:
    return ft.Row(
        [
            ft.Text(num, size=13, weight=ft.FontWeight.BOLD, width=24),
            ft.Text(text, size=13, expand=True),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


def _render_markdown() -> str:
    """フル状態を Markdown 化."""
    hw = STATE.hardware
    apps = STATE.detected_apps
    reps = STATE.replacements

    lines: list[str] = [
        "# Debian 移行レポート",
        f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## ハードウェア",
        f"- OS: {hw.os_name} {hw.os_version}",
        f"- アーキ: {hw.arch}",
        f"- CPU: {hw.cpu_model} ({hw.cpu_cores} コア)",
        f"- メモリ: {hw.ram_gb} GB",
        f"- GPU: {hw.gpu}",
    ]
    if hw.disks:
        lines.append("- ディスク:")
        for d in hw.disks:
            lines.append(
                f"  - {d['device']} ({d['fstype']}): "
                f"全 {d['total_gb']}GB / 空き {d['free_gb']}GB"
            )
    if hw.warnings:
        lines += ["", "### 注意点"]
        for w in hw.warnings:
            lines.append(f"- ⚠ {w}")

    lines += ["", "## 代替検討", ""]
    if reps:
        lines.append("| 検出アプリ | Debian 側候補 | 評価 | 選択 | 注 |")
        lines.append("|---|---|---|---|---|")
        for r in reps:
            alts = " / ".join(r.alternatives) or "—"
            choice = r.user_choice or "—"
            note = r.note.replace("|", "\\|")
            lines.append(
                f"| {r.detected} | {alts} | {r.confidence} | {choice} | {note} |"
            )
    else:
        lines.append("(検討対象なし)")

    lines += ["", f"## 検出アプリ ({len(apps)} 件)", ""]
    for a in apps:
        suffix = []
        if a.version:
            suffix.append(a.version)
        if a.publisher:
            suffix.append(a.publisher)
        tail = f" ({', '.join(suffix)})" if suffix else ""
        lines.append(f"- {a.name}{tail}")

    lines += [
        "",
        "## インストール先 USB",
        f"- 選択: {STATE.selected_usb or '(未選択)'}",
    ]
    if STATE.usb_devices:
        lines.append("- 候補:")
        for d in STATE.usb_devices:
            lines.append(
                f"  - {d.path}: {d.label} ({d.size_gb}GB)"
            )

    lines += [
        "",
        "## 次のステップ",
        "1. Claude にこのレポートを渡して、全体プランをチェックしてもらう。",
        "2. 本書 第 7 章「インストール実行の対話」に進む。",
        "3. Debian が立ち上がったら 第 9-11 章 (デスクトップ・IME・アプリ)。",
        "",
        "---",
        "生成元: Debian 移行ウィザード (aiseed.dev)",
    ]
    return "\n".join(lines)
