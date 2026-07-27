SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8
# Marp needs Chromium for PDF/PNG export. Use puppeteer's bundled chrome
# if installed, else point CHROME_PATH to a system browser.
export CHROME_PATH ?= $(firstword $(wildcard $(HOME)/.cache/puppeteer/chrome/*/chrome-linux64/chrome) /usr/bin/chromium /usr/bin/google-chrome)
# Run headless chrome with --no-sandbox (root environment).
export PUPPETEER_ARGS := --no-sandbox

OUT := out

.PHONY: all html pdf pptx images clean

all: html pdf images

html:
	@mkdir -p $(OUT)
	@echo "=== Marp で HTML スライド生成 ==="
	@time marp deck.md -o $(OUT)/deck.html --html --no-stdin 2>&1 | tail -3

pdf:
	@mkdir -p $(OUT)
	@echo
	@echo "=== Marp で PDF スライド生成 ==="
	@time marp deck.md -o $(OUT)/deck.pdf --pdf --allow-local-files --no-stdin 2>&1 | tail -3
	@printf "  → %s (%s bytes, %s ページ)\n" "$(OUT)/deck.pdf" \
	  "$$(stat -c%s $(OUT)/deck.pdf)" \
	  "$$(pdfinfo $(OUT)/deck.pdf 2>/dev/null | grep Pages | awk '{print $$2}')"

images:
	@mkdir -p $(OUT)/png
	@echo
	@echo "=== Marp で各スライドを PNG に ==="
	@cd $(OUT)/png && time marp ../../deck.md --images png --image-scale 1.5 --no-stdin 2>&1 | tail -3
	@printf "  → %s 枚 / 合計 %s\n" "$$(ls $(OUT)/png | wc -l)" "$$(du -sh $(OUT)/png | cut -f1)"

pptx:
	@mkdir -p $(OUT)
	@echo
	@echo "=== Marp で PowerPoint 化(必要なら) ==="
	@marp deck.md -o $(OUT)/deck.pptx --pptx --no-stdin 2>&1 | tail -3 || true

clean:
	rm -rf $(OUT)
