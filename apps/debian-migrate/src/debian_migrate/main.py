"""Entry point — `uv run flet run src/debian_migrate` or built binary."""

from __future__ import annotations

import flet as ft

from debian_migrate.app import App
from debian_migrate.theme import configure_page


def _start(page: ft.Page) -> None:
    configure_page(page)
    page.render(App)


def main() -> None:
    ft.run(_start)


if __name__ == "__main__":
    main()
