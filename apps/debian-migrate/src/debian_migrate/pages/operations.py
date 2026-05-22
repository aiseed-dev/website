"""第 12 章 + 第 17 章: dotfiles 管理 + アップデートとメンテナンス."""

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
from debian_migrate.prompts.templates import operations_prompt
from debian_migrate.state import STATE


DOTFILES_TARGETS = [
    ("~/.bashrc / ~/.zshrc", "シェル設定 (alias / PROMPT / 環境変数)"),
    ("~/.profile", "ログイン時の環境変数 (IME 連携など)"),
    ("~/.config/", "ほとんどの DE / アプリの設定が入る"),
    ("~/.ssh/config", "SSH 接続先の名前付け (秘密鍵は別管理)"),
    ("~/.gitconfig", "Git の名前・エイリアス・コミット署名"),
    ("~/.config/nvim/", "Neovim の設定"),
    ("~/.config/Code/User/settings.json", "VSCode / VSCodium の設定"),
]


DOTFILES_INIT_SCRIPT = """\
# 一度だけやる: dotfiles リポジトリの初期化
mkdir -p ~/dotfiles && cd ~/dotfiles
git init
git remote add origin git@github.com:<USER>/dotfiles.git  # 任意

# 既存ファイルをコピーして symlink に置き換え
for f in .bashrc .profile .gitconfig; do
  [ -f ~/$f ] && cp ~/$f ./$f && ln -sf ~/dotfiles/$f ~/$f
done

# .config 配下は選んでコピー
mkdir -p .config/nvim
cp -r ~/.config/nvim ./.config/

git add -A
git commit -m "initial dotfiles"
git push -u origin main   # 任意
"""


MAINTENANCE_CMDS = [
    ("通常のアップデート (週 1)",
     "sudo apt update && sudo apt upgrade -y"),
    ("不要パッケージの掃除 (月 1)",
     "sudo apt autoremove --purge && sudo apt clean"),
    ("Flatpak のアップデート",
     "flatpak update -y"),
    ("ディスクの使用量を確認",
     "df -h && sudo du -sh /var/cache/apt/archives /var/log"),
    ("メジャーアップグレードの前にバックアップ",
     "sudo apt install timeshift && sudo timeshift --create --comments 'before upgrade'"),
]


@ft.component
def OperationsPage() -> ft.Control:
    return ft.Column(
        [
            section_title("9. 運用と長期メンテ"),
            page_intro(
                "Debian は入れて終わりではなく、設定を Git で管理し、"
                "定期的にアップデートしていきます。本書 第 12 章と第 17 章を"
                "コンパクトにまとめたガイドです。"
            ),
            ft.Container(height=8),
            _dotfiles_card(),
            ft.Container(height=8),
            _maintenance_card(),
            ft.Container(height=16),
            ft.Row(
                [
                    secondary_button(
                        "戻る",
                        on_click=lambda _: navigate("/install-plan"),
                        icon=ft.Icons.ARROW_BACK,
                    ),
                    ft.Container(expand=True),
                    copy_prompt_button(
                        lambda: operations_prompt(STATE.chosen_desktop)
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


def _dotfiles_card() -> ft.Control:
    target_rows = [
        ft.Row(
            [
                ft.Text(
                    path,
                    size=12,
                    font_family="JetBrains Mono, monospace",
                    width=250,
                ),
                ft.Text(desc, size=12, expand=True),
            ],
            spacing=12,
        )
        for path, desc in DOTFILES_TARGETS
    ]
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "設定ファイルを Git で管理する (第 12 章)",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "Debian は設定がテキストファイルとして残るので、"
                        "Git で履歴管理すれば「いつ何を変えたか」が分かる。"
                        "次のマシンに移るときも、リポジトリを clone するだけ。",
                        size=13,
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "管理対象になりやすいファイル / フォルダ:",
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Container(height=4),
                    *target_rows,
                    ft.Container(height=10),
                    ft.Text(
                        "初期化スクリプト例 (コピーして自分用に書き換える):",
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    _script_box(DOTFILES_INIT_SCRIPT),
                    ft.Container(height=4),
                    ft.Text(
                        "💡 秘密鍵 (~/.ssh/id_*) や API トークンを含むファイルは"
                        " **絶対にコミットしない**。.gitignore に "
                        "`id_*`, `*.pem`, `*token*` を入れておく。",
                        size=11,
                        color=ft.Colors.ORANGE,
                    ),
                ],
                spacing=4,
            ),
            padding=14,
        )
    )


def _maintenance_card() -> ft.Control:
    rows = [_cmd_row(label, cmd) for label, cmd in MAINTENANCE_CMDS]
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "アップデートとメンテナンス (第 17 章)",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "週次・月次でやるコマンドの目安です。"
                        "Debian は「壊れにくい OS」と言われますが、"
                        "それは定期メンテをした人の感想です。",
                        size=13,
                    ),
                    ft.Container(height=8),
                    *rows,
                ],
                spacing=8,
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


def _script_box(script: str) -> ft.Control:
    def copy_script(_):
        page = ft.context.page
        page.clipboard.set(script)
        page.show_dialog(
            ft.SnackBar(content=ft.Text("スクリプトをコピー"), duration=2000)
        )

    return ft.Container(
        content=ft.Row(
            [
                ft.Text(
                    script,
                    selectable=True,
                    font_family="JetBrains Mono, monospace",
                    size=11,
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.Icons.CONTENT_COPY,
                    tooltip="コピー",
                    on_click=copy_script,
                ),
            ],
        ),
        padding=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        border_radius=8,
    )
