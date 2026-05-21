.PHONY: install run run-web test lint build-windows build-macos build-linux clean

install:
	uv sync

run:
	uv run flet run src/debian_migrate

run-web:
	uv run flet run src/debian_migrate --web --port 8080

test:
	uv run pytest -q

lint:
	uv run ruff check src tests

build-windows:
	uv run flet build windows

build-macos:
	uv run flet build macos

build-linux:
	uv run flet build linux

clean:
	rm -rf build dist .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
