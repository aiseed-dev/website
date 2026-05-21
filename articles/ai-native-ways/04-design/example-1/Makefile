SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

SRC := src
OUT := out

SOURCES := $(wildcard $(SRC)/*.mmd)
SVGS    := $(patsubst $(SRC)/%.mmd,$(OUT)/%.svg,$(SOURCES))
PNGS    := $(patsubst $(SRC)/%.mmd,$(OUT)/%.png,$(SOURCES))

.PHONY: all svg png measure clean

all: svg png measure

svg: $(SVGS)

png: $(PNGS)

$(OUT)/%.svg: $(SRC)/%.mmd | $(OUT)
	@echo "→ $@"
	@mmdc -i $< -o $@ -b transparent -t neutral -p puppeteer-config.json 2>/dev/null

$(OUT)/%.png: $(SRC)/%.mmd | $(OUT)
	@echo "→ $@"
	@mmdc -i $< -o $@ -b white -t neutral -w 1600 -p puppeteer-config.json 2>/dev/null

$(OUT):
	@mkdir -p $(OUT)

measure: svg png
	@echo
	@echo "=== サイズ計測 ==="
	@for f in $(SOURCES); do \
	  name=$$(basename $$f .mmd); \
	  src_size=$$(stat -c%s $$f); \
	  svg_size=$$(stat -c%s $(OUT)/$$name.svg 2>/dev/null || echo 0); \
	  png_size=$$(stat -c%s $(OUT)/$$name.png 2>/dev/null || echo 0); \
	  printf "  %-22s  src %5d B   svg %5d B   png %6d B\n" "$$name" $$src_size $$svg_size $$png_size; \
	done
	@echo
	@echo "=== 合計 ==="
	@printf "  Mermaid ソース 合計: %s bytes\n" $$(du -bc $(SRC)/*.mmd | tail -1 | cut -f1)
	@printf "  SVG 合計            : %s bytes\n" $$(du -bc $(OUT)/*.svg | tail -1 | cut -f1)
	@printf "  PNG 合計            : %s bytes\n" $$(du -bc $(OUT)/*.png | tail -1 | cut -f1)

clean:
	rm -rf $(OUT)
