"""Entry point — `uv run flet run src/debian_migrate` or built binary."""

from __future__ import annotations

import flet as ft

from debian_migrate.app import App


def main() -> None:
    ft.run(lambda page: page.render(App))


if __name__ == "__main__":
    main()
