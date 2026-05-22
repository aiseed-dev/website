SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

OUT := out

.PHONY: all build measure deps clean serve

all: build measure

build:
	@mkdir -p $(OUT)
	@echo "=== Markdown → HTML ビルド ==="
	@python3 build.py

measure: build
	@echo
	@echo "=== 規模を比較 ==="
	@echo "  ── Markdown ソース"
	@printf "    src/*.md     行数: %s\n" "$$(cat src/*.md | wc -l)"
	@printf "    src/*.md     合計: %s B\n" "$$(du -bc src/*.md | tail -1 | cut -f1)"
	@echo "  ── ビルドスクリプト"
	@printf "    build.py     行数: %s\n" "$$(wc -l < build.py)"
	@echo "  ── 出力 HTML"
	@printf "    out/*.html   合計: %s B\n" "$$(du -bc $(OUT)/*.html | tail -1 | cut -f1)"
	@echo "  ── 依存パッケージ"
	@printf "    本体    : markdown-it-py のみ (pip 1 個)\n"
	@printf "    ランタイム: ブラウザ + Mermaid CDN(node_modules ゼロ)\n"

deps:
	@pip install markdown-it-py 2>&1 | tail -3

serve: build
	@cd $(OUT) && python3 -m http.server 8765

clean:
	rm -rf $(OUT)
