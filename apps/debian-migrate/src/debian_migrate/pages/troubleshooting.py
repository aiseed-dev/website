"""第 8 章: 事前トラブル予防 — 七つのカテゴリと診断テンプレート."""

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
from debian_migrate.prompts.templates import troubleshooting_prompt
from debian_migrate.state import STATE


# 章 8 の七つのカテゴリ。各カテゴリは:
#  - slug
#  - title (画面表示)
#  - 説明 (一文)
#  - predict(hw) → 「あなたで当たりそう」かどうか (heuristic)
#  - 診断コマンド (Debian 起動後にコピペで使う)
CATEGORIES = [
    {
        "slug": "display",
        "title": "ディスプレイ",
        "desc": "解像度・スケーリング・外部モニター。",
        "diag": [
            "lspci -nnk | grep -A 2 VGA",
            "xrandr",
            "journalctl -b -p err | grep -i -E 'drm|gpu|nouveau|nvidia'",
        ],
        "predict": lambda hw: any(
            x in hw.gpu.lower() for x in ("nvidia", "amd", "radeon")
        ),
        "predict_note": "独立 GPU (NVIDIA / AMD) ではドライバ周りで詰まりがち。",
    },
    {
        "slug": "wifi",
        "title": "Wi-Fi",
        "desc": "繋がらない / 速度が出ない / 切れる。",
        "diag": [
            "ip a",
            "nmcli device status",
            "lspci -nnk | grep -A 2 -i wireless",
            "journalctl -b -u NetworkManager",
        ],
        # ノート PC (バッテリーあり = 暫定) なら Wi-Fi が関係する可能性が高い
        "predict": lambda hw: hw.os_name == "Darwin"
        or any("laptop" in d.get("device", "").lower() for d in hw.disks),
        "predict_note": "ノート PC / Mac は Wi-Fi 必須。Debian 13 の netinst は firmware 同梱なので大半は初回起動から繋がる。極端に新しいチップだけ手動で firmware-* を追加。",
    },
    {
        "slug": "bluetooth",
        "title": "Bluetooth",
        "desc": "マウス / キーボード / イヤホンが認識されない。",
        "diag": [
            "rfkill list",
            "bluetoothctl show",
            "systemctl status bluetooth",
            "journalctl -b -u bluetooth",
        ],
        "predict": lambda hw: hw.os_name == "Darwin",
        "predict_note": "Mac から移行する人は周辺機器が Bluetooth 多め。",
    },
    {
        "slug": "sound",
        "title": "サウンド",
        "desc": "音が出ない / マイクが拾わない。",
        "diag": [
            "pactl list short sinks",
            "pactl list short sources",
            "wpctl status",
            "journalctl -b -u pipewire",
        ],
        "predict": lambda hw: True,  # ほぼ全員が当たる
        "predict_note": "PipeWire / PulseAudio の切り替えでつまずきがち。",
    },
    {
        "slug": "suspend",
        "title": "サスペンド / 復帰",
        "desc": "蓋を閉じて開くと真っ黒。バッテリーの減りが速い。",
        "diag": [
            "systemctl status suspend.target",
            "journalctl -b | grep -i -E 'suspend|resume|wakeup'",
            "cat /sys/power/mem_sleep",
        ],
        "predict": lambda hw: True,  # ノート PC ならほぼ確実
        "predict_note": "ノート PC のサスペンドは BIOS と DE の組合せで挙動が変わる。",
    },
    {
        "slug": "ime",
        "title": "日本語入力",
        "desc": "Fcitx5 + Mozc が一部アプリで動かない。",
        "diag": [
            "fcitx5-diagnose",
            "echo $XMODIFIERS $GTK_IM_MODULE $QT_IM_MODULE",
        ],
        "predict": lambda hw: True,
        "predict_note": "本書 第 10 章で詳細。Wayland / Electron 系で挙動が違うので注意。",
    },
    {
        "slug": "peripherals",
        "title": "周辺機器",
        "desc": "プリンタ / ウェブカメラ / USB 機器が認識されない。",
        "diag": [
            "lsusb",
            "lpstat -p -d",
            "v4l2-ctl --list-devices",
        ],
        "predict": lambda hw: False,  # 機種依存、自動予測は精度が出ない
        "predict_note": "",
    },
]


@ft.component
def TroubleshootingPage() -> ft.Control:
    return ft.Column(
        [
            section_title("5. 事前トラブル予防"),
            page_intro(
                "Debian 13 では「初回起動からほぼ全部動く」機種が増えました。"
                "本章は『今あなたが詰まっている章』ではなく『詰まったときに開く章』として頭に入れておきます。"
                "ここでは、あなたのハードウェアから当たりそうな項目だけ予測しておきます。"
                "本書 第 8 章「まず、Debian 13 では『ほぼ全部動く』」と整合します。"
            ),
            ft.Container(height=8),
            _categories_card(),
            ft.Container(height=8),
            _diagnostic_basics(),
            ft.Container(height=8),
            _claude_template_card(),
            ft.Container(height=16),
            ft.Row(
                [
                    secondary_button(
                        "戻る",
                        on_click=lambda _: navigate("/usb"),
                        icon=ft.Icons.ARROW_BACK,
                    ),
                    ft.Container(expand=True),
                    copy_prompt_button(
                        lambda: troubleshooting_prompt(STATE.hardware)
                    ),
                    primary_button(
                        "デスクトップ環境へ",
                        on_click=lambda _: navigate("/desktop"),
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        spacing=6,
    )


def _categories_card() -> ft.Control:
    hw = STATE.hardware
    rows: list[ft.Control] = []
    for cat in CATEGORIES:
        likely = bool(cat["predict"](hw))
        icon = (
            ft.Icon(ft.Icons.WARNING_AMBER, color=ft.Colors.ORANGE, size=18)
            if likely
            else ft.Icon(ft.Icons.CIRCLE_OUTLINED, color=ft.Colors.OUTLINE, size=14)
        )
        sub = (
            ft.Text(
                cat["predict_note"],
                size=11,
                color=ft.Colors.ORANGE_700,
                italic=True,
            )
            if likely and cat["predict_note"]
            else ft.Container()
        )
        rows.append(
            ft.Container(
                content=ft.Row(
                    [
                        icon,
                        ft.Column(
                            [
                                ft.Text(
                                    cat["title"],
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(cat["desc"], size=12),
                                sub,
                            ],
                            spacing=1,
                            expand=True,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=ft.padding.symmetric(vertical=6, horizontal=6),
                bgcolor=(
                    ft.Colors.SURFACE_CONTAINER_HIGH
                    if likely
                    else ft.Colors.SURFACE_CONTAINER_LOWEST
                ),
                border_radius=8,
            )
        )

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "頭に入れておく 7 カテゴリ",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "⚠ 印は、いまの環境で残りやすいと予測したもの。"
                        "Debian 13 ではどれも初回から動くことが多いが、機種依存で稀に当たる (本書 第 8 章)。",
                        size=11,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Container(height=8),
                    ft.Column(rows, spacing=6),
                ],
            ),
            padding=14,
        )
    )


def _diagnostic_basics() -> ft.Control:
    """Debian 起動後にコピペで使える共通診断コマンド."""
    cmds = [
        ("システムログ (今回起動以降のエラー)",
         "journalctl -b -p err"),
        ("ハードウェア認識 (PCI + ドライバ)",
         "lspci -nnk"),
        ("USB デバイス",
         "lsusb"),
        ("カーネルメッセージ末尾",
         "dmesg | tail -50"),
        ("失敗したサービス一覧",
         "systemctl --failed"),
    ]
    rows: list[ft.Control] = []
    for label, cmd in cmds:
        rows.append(_cmd_row(label, cmd))

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Debian 起動後に最初に走らせる診断コマンド",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "USB から起動したあと、ターミナルで上から順に走らせて、"
                        "出力を保存しておくと Claude に渡しやすい。",
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Container(height=8),
                    ft.Column(rows, spacing=8),
                ],
            ),
            padding=14,
        )
    )


def _cmd_row(label: str, cmd: str) -> ft.Control:
    def copy_cmd(_):
        page = ft.context.page
        page.clipboard.set(cmd)
        page.show_dialog(
            ft.SnackBar(content=ft.Text(f"コピー: {cmd}"), duration=2000)
        )

    return ft.Column(
        [
            ft.Text(label, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
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


def _claude_template_card() -> ft.Control:
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Claude にトラブルを聞くテンプレート",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "本書 第 8 章にある統一プロンプト。"
                        "「Claude 用プロンプトをコピー」ボタンを押すと、"
                        "あなたの環境情報込みでクリップボードに入ります。"
                        "あとは症状を 1 行書き足して claude.ai に貼るだけ。",
                        size=13,
                    ),
                ],
            ),
            padding=14,
        )
    )
