SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

OUT := out

.PHONY: all report html pdf clean

all: report html pdf

report:
	@mkdir -p $(OUT)
	@echo "=== 1. CSV → Markdown 報告書 ==="
	@python3 build_report.py

html: report
	@echo
	@echo "=== 2. Markdown → HTML(配布用) ==="
	@time pandoc $(OUT)/report.md -o $(OUT)/report.html --standalone --toc 2>&1 | tail -3
	@echo "  → $(OUT)/report.html ($$(stat -c%s $(OUT)/report.html) bytes)"

pdf: report
	@echo
	@echo "=== 3. Markdown → PDF(印刷用) ==="
	@pandoc $(OUT)/report.md -o $(OUT)/_for_pdf.html --standalone
	@time python3 -c "from weasyprint import HTML; HTML('$(OUT)/_for_pdf.html', base_url='.').write_pdf('$(OUT)/report.pdf')" 2>&1 | tail -3
	@echo "  → $(OUT)/report.pdf ($$(stat -c%s $(OUT)/report.pdf) bytes, $$(pdfinfo $(OUT)/report.pdf 2>/dev/null | grep Pages | awk '{print $$2}') ページ)"
	@rm -f $(OUT)/_for_pdf.html

clean:
	rm -rf $(OUT)
