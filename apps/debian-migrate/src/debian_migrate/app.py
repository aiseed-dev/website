"""Top-level App component — wizard layout + router."""

from __future__ import annotations

import flet as ft

from debian_migrate.pages.desktop_env import DesktopEnvPage
from debian_migrate.pages.export import ExportPage
from debian_migrate.pages.hardware import HardwarePage
from debian_migrate.pages.ime import ImePage
from debian_migrate.pages.install_plan import InstallPlanPage
from debian_migrate.pages.inventory import InventoryPage
from debian_migrate.pages.replacements import ReplacementsPage
from debian_migrate.pages.troubleshooting import TroubleshootingPage
from debian_migrate.pages.usb_installer import UsbInstallerPage
from debian_migrate.pages.welcome import WelcomePage


STEPS = [
    ("/", "ようこそ"),
    ("/inventory", "アプリ棚卸し"),
    ("/replacements", "代替候補"),
    ("/hardware", "ハードウェア確認"),
    ("/usb", "USB 作成"),
    ("/troubleshooting", "トラブル予防"),
    ("/desktop", "デスクトップ環境"),
    ("/ime", "日本語入力"),
    ("/install-plan", "アプリ導入計画"),
    ("/export", "まとめ"),
]


@ft.component
def StepIndicator() -> ft.Control:
    """Show the wizard step bar at the top of every page."""
    page = ft.context.page
    current_path = page.route or "/"
    current_index = next(
        (i for i, (p, _) in enumerate(STEPS) if p == current_path), 0
    )

    items: list[ft.Control] = []
    for i, (path, label) in enumerate(STEPS):
        is_done = i < current_index
        is_current = i == current_index
        if is_current:
            color = ft.Colors.PRIMARY
            weight = ft.FontWeight.BOLD
        elif is_done:
            color = ft.Colors.GREEN
            weight = ft.FontWeight.NORMAL
        else:
            color = ft.Colors.OUTLINE
            weight = ft.FontWeight.NORMAL
        items.append(
            ft.Container(
                content=ft.Text(
                    f"{i + 1}. {label}", size=12, color=color, weight=weight
                ),
                padding=ft.padding.symmetric(horizontal=8, vertical=4),
            )
        )
        if i < len(STEPS) - 1:
            items.append(ft.Text("›", size=12, color=ft.Colors.OUTLINE))

    return ft.Container(
        content=ft.Row(items, alignment=ft.MainAxisAlignment.CENTER, wrap=True),
        bgcolor=ft.Colors.SURFACE_BRIGHT,
        padding=10,
    )


@ft.component
def AppLayout() -> ft.Control:
    """Shared chrome wrapping all wizard pages."""
    outlet = ft.use_route_outlet()
    return ft.Column(
        [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            "Debian 移行ウィザード",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(expand=True),
                        ft.Text(
                            "aiseed.dev",
                            size=12,
                            color=ft.Colors.OUTLINE,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                padding=16,
            ),
            StepIndicator(),
            ft.Container(
                content=outlet,
                padding=24,
                expand=True,
            ),
        ],
        expand=True,
        spacing=0,
    )


@ft.component
def App() -> ft.Control:
    """Application root."""
    return ft.Router(
        [
            ft.Route(
                component=AppLayout,
                children=[
                    ft.Route(index=True, component=WelcomePage),
                    ft.Route(path="inventory", component=InventoryPage),
                    ft.Route(path="replacements", component=ReplacementsPage),
                    ft.Route(path="hardware", component=HardwarePage),
                    ft.Route(path="usb", component=UsbInstallerPage),
                    ft.Route(path="troubleshooting", component=TroubleshootingPage),
                    ft.Route(path="desktop", component=DesktopEnvPage),
                    ft.Route(path="ime", component=ImePage),
                    ft.Route(path="install-plan", component=InstallPlanPage),
                    ft.Route(path="export", component=ExportPage),
                ],
            )
        ]
    )
