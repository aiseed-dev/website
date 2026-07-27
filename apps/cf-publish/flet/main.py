"""cf-publish (Flet) — a no-terminal GUI for publishing a folder to
Cloudflare Pages.

Built for designers: pick a folder, name the project, hit Publish. The
deploy logic lives in deploy_core.py (pure Python, httpx + blake3, ported
from tools/cloudflare_pages_deploy.py). This file is only the UI.

Flet 1.0 Beta declarative style: @ft.component + hooks (use_state,
use_dialog), FilePicker for the folder, and page.run_thread() to run the
blocking deploy off the UI thread.

Dev run (needs the Flutter SDK / Flet desktop client):
    uv run flet run

See README.md for build instructions.
"""

from __future__ import annotations

import json
from pathlib import Path

import flet as ft

import deploy_core

# Small JSON config remembering the last folder / project / branch.
CONFIG_FILE = (
    Path.home() / ".config" / "cloudflare" / "cf-publish-flet.json"
)

BRANCH_PRODUCTION = "main"
BRANCH_PREVIEW = "preview"


# ── tiny app-config persistence (separate from credentials) ────────────────


def load_config() -> dict:
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_config(data: dict) -> None:
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError:
        pass


# ── settings (credentials) dialog ──────────────────────────────────────────


@ft.component
def SettingsDialog(show: bool, on_close, on_saved):
    """Dialog to enter and save CLOUDFLARE_API_TOKEN / ACCOUNT_ID."""
    init_token, init_account = deploy_core.load_credentials()
    token, set_token = ft.use_state(init_token or "")
    account, set_account = ft.use_state(init_account or "")
    error, set_error = ft.use_state("")

    def handle_save(_e):
        if not token.strip() or not account.strip():
            set_error("Both the API token and account ID are required.")
            return
        deploy_core.save_credentials(token, account)
        set_error("")
        on_saved()

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("Cloudflare credentials"),
            content=ft.Column(
                [
                    ft.Text(
                        "Saved to ~/.config/cloudflare/pages.env "
                        "(chmod 600). Environment variables, if set, take "
                        "precedence.",
                        size=12,
                    ),
                    ft.TextField(
                        label="CLOUDFLARE_API_TOKEN",
                        value=token,
                        password=True,
                        can_reveal_password=True,
                        on_change=lambda e: set_token(e.control.value),
                    ),
                    ft.TextField(
                        label="CLOUDFLARE_ACCOUNT_ID",
                        value=account,
                        on_change=lambda e: set_account(e.control.value),
                    ),
                    ft.Text(error, color=ft.Colors.RED, size=12)
                    if error
                    else ft.Container(height=0),
                ],
                tight=True,
                width=460,
            ),
            actions=[
                ft.Button("Save", on_click=handle_save),
                ft.TextButton("Cancel", on_click=lambda _: on_close()),
            ],
            on_dismiss=lambda _: on_close(),
        )
        if show
        else None
    )
    return ft.Container(height=0)


# ── main app ───────────────────────────────────────────────────────────────


@ft.component
def App():
    cfg = load_config()

    project, set_project = ft.use_state(cfg.get("project", ""))
    folder, set_folder = ft.use_state(cfg.get("folder", ""))
    branch, set_branch = ft.use_state(cfg.get("branch", BRANCH_PRODUCTION))

    running, set_running = ft.use_state(False)
    log_lines, set_log_lines = ft.use_state([])
    result_url, set_result_url = ft.use_state("")
    error, set_error = ft.use_state("")

    show_settings, set_show_settings = ft.use_state(False)
    # On first run, if creds are missing, open settings automatically.
    first_check, set_first_check = ft.use_state(True)
    if first_check:
        set_first_check(False)
        tok, acct = deploy_core.load_credentials()
        if not tok or not acct:
            set_show_settings(True)

    page = ft.context.page

    def append_log(line: str) -> None:
        # Called from a worker thread; mutate then re-set to trigger render.
        set_log_lines(lambda prev: [*prev, line])

    def persist() -> None:
        save_config(
            {"project": project, "folder": folder, "branch": branch}
        )

    # FilePicker for the public directory. In Flet 0.85 the picker methods are
    # awaitable and RETURN the chosen path (there is no on_result callback /
    # FilePickerResultEvent). The picker must still live in the control tree.
    file_picker = ft.FilePicker()

    async def pick_folder(_e):
        path = await file_picker.get_directory_path(
            dialog_title="Choose public folder"
        )
        if path:
            set_folder(path)
            save_config(
                {"project": project, "folder": path, "branch": branch}
            )

    def do_publish() -> None:
        try:
            url = deploy_core.deploy(
                directory=folder,
                project=project.strip(),
                branch=branch,
                create=True,
                on_progress=append_log,
            )
            set_result_url(url)
        except Exception as exc:  # surface any failure in the UI
            append_log(f"ERROR: {exc}")
            set_error(str(exc))
        finally:
            set_running(False)

    def start_publish(_e):
        if not project.strip():
            set_error("Project name is required.")
            return
        if not folder or not Path(folder).is_dir():
            set_error("Choose a valid public folder.")
            return
        tok, acct = deploy_core.load_credentials()
        if not tok or not acct:
            set_error("Set credentials first (gear icon).")
            set_show_settings(True)
            return
        set_error("")
        set_result_url("")
        set_log_lines([])
        set_running(True)
        persist()
        # Run the blocking deploy off the UI thread.
        page.run_thread(do_publish)

    async def copy_url(_e):
        if result_url:
            # Flet 0.85: clipboard is an awaitable Page.clipboard.set(...).
            await page.clipboard.set(result_url)

    def open_url(_e):
        if result_url:
            page.launch_url(result_url)

    # ── build the tree ──────────────────────────────────────────────────
    log_view = ft.ListView(
        controls=[
            ft.Text(line, font_family="monospace", size=12)
            for line in log_lines
        ],
        spacing=2,
        auto_scroll=True,
        expand=True,
    )

    success_row = (
        ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                    ft.Text(
                        result_url,
                        selectable=True,
                        weight=ft.FontWeight.BOLD,
                        expand=True,
                    ),
                    ft.IconButton(
                        ft.Icons.CONTENT_COPY,
                        tooltip="Copy URL",
                        on_click=copy_url,
                    ),
                    ft.IconButton(
                        ft.Icons.OPEN_IN_NEW,
                        tooltip="Open in browser",
                        on_click=open_url,
                    ),
                ],
            ),
            padding=10,
            bgcolor=ft.Colors.GREEN_50,
            border_radius=8,
        )
        if result_url
        else ft.Container(height=0)
    )

    error_row = (
        ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED),
                    ft.Text(error, color=ft.Colors.RED, expand=True),
                ]
            ),
            padding=10,
            bgcolor=ft.Colors.RED_50,
            border_radius=8,
        )
        if error
        else ft.Container(height=0)
    )

    publish_button = ft.Button(
        content=ft.Row(
            [
                ft.ProgressRing(width=16, height=16, stroke_width=2),
                ft.Text("Publishing..."),
            ],
            tight=True,
        )
        if running
        else ft.Row(
            [ft.Icon(ft.Icons.CLOUD_UPLOAD), ft.Text("Publish")], tight=True
        ),
        disabled=running,
        on_click=start_publish,
    )

    return ft.Column(
        [
            file_picker,
            SettingsDialog(
                show=show_settings,
                on_close=lambda: set_show_settings(False),
                on_saved=lambda: set_show_settings(False),
            ),
            ft.Row(
                [
                    ft.Text(
                        "Publish to Cloudflare Pages",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        expand=True,
                    ),
                    ft.IconButton(
                        ft.Icons.SETTINGS,
                        tooltip="Credentials",
                        on_click=lambda _: set_show_settings(True),
                    ),
                ],
            ),
            ft.TextField(
                label="Site / project name",
                hint_text="e.g. aiseed-dev",
                value=project,
                on_change=lambda e: set_project(e.control.value),
                disabled=running,
            ),
            ft.Row(
                [
                    ft.TextField(
                        label="Public folder",
                        value=folder,
                        read_only=True,
                        expand=True,
                    ),
                    ft.Button(
                        "Choose...",
                        icon=ft.Icons.FOLDER_OPEN,
                        on_click=pick_folder,
                        disabled=running,
                    ),
                ],
            ),
            ft.Dropdown(
                label="Branch",
                value=branch,
                options=[
                    ft.dropdown.Option(
                        key=BRANCH_PRODUCTION, text="main (production)"
                    ),
                    ft.dropdown.Option(
                        key=BRANCH_PREVIEW, text="preview"
                    ),
                ],
                on_change=lambda e: set_branch(e.control.value),
                disabled=running,
            ),
            ft.Row([publish_button]),
            error_row,
            success_row,
            ft.Text("Log", weight=ft.FontWeight.BOLD),
            ft.Container(
                content=log_view,
                expand=True,
                border=ft.Border.all(1, ft.Colors.OUTLINE),
                border_radius=8,
                padding=8,
            ),
        ],
        expand=True,
        spacing=12,
    )


def main(page: ft.Page):
    page.title = "cf-publish"
    page.window.width = 640
    page.window.height = 760
    page.padding = 20
    page.render(App)


ft.run(main)
