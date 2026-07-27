# 序章の実例: 1つのMarkdownから5つの形式を生成する
#
# 必要なツール:
#   - pandoc 2.x+
#   - python3 + weasyprint (pip install weasyprint)
#   - Noto Serif CJK JP フォント (sudo apt install fonts-noto-cjk)
#
# 使い方:
#   make all       # 全形式を生成して計測
#   make html      # HTML だけ
#   make epub      # EPUB だけ
#   make slides    # reveal.js スライドだけ
#   make plain     # プレーンテキストだけ
#   make pdf       # PDF だけ
#   make clean     # out/ をクリア

SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8
OUT := out
SRC := source.md

.PHONY: all html epub slides plain pdf clean measure

all: html epub slides plain pdf measure

$(OUT):
	mkdir -p $(OUT)

html: $(OUT)
	@echo "→ HTML"
	@time pandoc $(SRC) -o $(OUT)/prologue.html --standalone --toc --css=book-style.css

epub: $(OUT)
	@echo "→ EPUB"
	@time pandoc $(SRC) -o $(OUT)/prologue.epub --metadata title="序章"

slides: $(OUT)
	@echo "→ reveal.js slides"
	@time pandoc $(SRC) -o $(OUT)/slides.html -t revealjs --standalone --slide-level=2

plain: $(OUT)
	@echo "→ plain text"
	@time pandoc $(SRC) -o $(OUT)/plain.txt -t plain --wrap=none

pdf: $(OUT)
	@echo "→ PDF (weasyprint)"
	@pandoc $(SRC) -o $(OUT)/body.html --standalone --css=book-style.css --metadata title="序章"
	@time python3 -c "from weasyprint import HTML; HTML('$(OUT)/body.html', base_url='.').write_pdf('$(OUT)/prologue.pdf')"

measure:
	@echo
	@echo "=== サイズ計測 ==="
	@du -h $(SRC) $(OUT)/*.html $(OUT)/*.epub $(OUT)/*.pdf $(OUT)/*.txt 2>/dev/null | sort -h
	@echo
	@echo "=== 行数 ==="
	@wc -l $(SRC) $(OUT)/*.html $(OUT)/*.txt 2>/dev/null

clean:
	rm -rf $(OUT)
