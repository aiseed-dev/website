"""第 10 章: 日本語入力 (Fcitx5 + Mozc) の設定."""

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
from debian_migrate.prompts.templates import ime_prompt
from debian_migrate.state import STATE


INSTALL_CMDS = [
    (
        "1. Fcitx5 + Mozc を入れる",
        "sudo apt install fcitx5 fcitx5-mozc fcitx5-config-qt",
    ),
    (
        "2. 既定の IM を Fcitx5 に",
        "im-config -n fcitx5",
    ),
    (
        "3. 環境変数を一度だけ追加 (~/.profile に書く)",
        "cat >> ~/.profile <<'EOF'\nexport GTK_IM_MODULE=fcitx\nexport QT_IM_MODULE=fcitx\nexport XMODIFIERS=@im=fcitx\nEOF",
    ),
    (
        "4. ログアウト → ログインして反映",
        "loginctl terminate-user $USER",
    ),
]


TIPS = [
    ("半角/全角キー", "Ctrl+Space または Zenkaku_Hankaku で切替。設定ツールから割り当て可。"),
    ("変換キー (スペース) / 無変換キー", "Mozc 設定 → 一般 → キー設定の選択で MS-IME 風 / ATOK 風が選べる。"),
    ("辞書登録", "Mozc 設定ツール (fcitx5-mozc-tool) で個人辞書を編集できる。"),
    ("Wayland で動かない時", "fcitx5 を環境変数なしで起動して fcitx5-diagnose で確認。"),
    ("Electron アプリで入力できない時", "--enable-wayland-ime フラグ、または .desktop の Exec に環境変数追加。"),
]


@ft.component
def ImePage() -> ft.Control:
    return ft.Column(
        [
            section_title("7. 日本語入力 (Fcitx5 + Mozc)"),
            page_intro(
                "Debian 13 では、インストーラで言語に「日本語」を選んだ時点で"
                " Fcitx5 + Mozc が自動的に入ることが多くなりました。"
                "まずは「入っているか」を確認し、入っていなければ手動で入れます。"
                "本書 第 10 章「まず確認 — たぶん既に入っている」と整合します。"
            ),
            ft.Container(height=8),
            _check_first_card(),
            ft.Container(height=8),
            _install_card(),
            ft.Container(height=8),
            _tips_card(),
            ft.Container(height=8),
            _diagnose_card(),
            ft.Container(height=16),
            ft.Row(
                [
                    secondary_button(
                        "戻る",
                        on_click=lambda _: navigate("/desktop"),
                        icon=ft.Icons.ARROW_BACK,
                    ),
                    ft.Container(expand=True),
                    copy_prompt_button(
                        lambda: ime_prompt(STATE.hardware, STATE.chosen_desktop)
                    ),
                    primary_button(
                        "アプリ導入計画へ", on_click=lambda _: navigate("/install-plan")
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        spacing=6,
    )


def _check_first_card() -> ft.Control:
    """Step 0: まず確認 — Debian 13 では既に入っていることが多い."""
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "ステップ 0: まず確認 (これで済むことが多い)",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "Debian 13 起動後に次の 2 行を実行してください。"
                        "両方が出力されて、半角/全角キーで日本語入力ができていれば、"
                        "下の「ステップ 1〜4」は不要です。第 10 章 第二節「基本のキーバインド」へ進めます。",
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Container(height=6),
                    _cmd_row(
                        "Fcitx5 + Mozc が入っているか",
                        "dpkg -l | grep -E '^ii  (fcitx5|fcitx5-mozc)'",
                    ),
                    _cmd_row(
                        "既定の IM が fcitx5 になっているか",
                        "im-config -l",
                    ),
                ],
                spacing=8,
            ),
            padding=14,
        )
    )


def _install_card() -> ft.Control:
    rows: list[ft.Control] = []
    for label, cmd in INSTALL_CMDS:
        rows.append(_cmd_row(label, cmd))

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "入っていなかった場合に走らせる 4 手順",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "ステップ 0 で確認が取れなかった時だけ、上から順に実行してください。"
                        "3 番目はホームの ~/.profile に環境変数を 3 行追加します。",
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Container(height=8),
                    *rows,
                ],
                spacing=10,
            ),
            padding=14,
        )
    )


def _cmd_row(label: str, cmd: str) -> ft.Control:
    def copy_cmd(_):
        page = ft.context.page
        page.clipboard.set(cmd)
        page.show_dialog(
            ft.SnackBar(content=ft.Text("コマンドをコピー"), duration=2000)
        )

    return ft.Column(
        [
            ft.Text(label, size=12, color=ft.Colors.ON_SURFACE_VARIANT,
                    weight=ft.FontWeight.BOLD),
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
        ],
        spacing=2,
    )


def _tips_card() -> ft.Control:
    items = [
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(body, size=12),
                ],
                spacing=2,
            ),
            padding=ft.padding.symmetric(vertical=6),
        )
        for title, body in TIPS
    ]
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "よくある困りごと",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=4),
                    *items,
                ],
                spacing=4,
            ),
            padding=14,
        )
    )


def _diagnose_card() -> ft.Control:
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "うまく動かないときの診断",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "次のコマンドを実行して、出力を Claude にそのまま渡せます。",
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Container(height=6),
                    _cmd_row("環境変数の確認",
                             "echo $XMODIFIERS $GTK_IM_MODULE $QT_IM_MODULE"),
                    _cmd_row("Fcitx5 の総合診断",
                             "fcitx5-diagnose"),
                ],
                spacing=8,
            ),
            padding=14,
        )
    )
