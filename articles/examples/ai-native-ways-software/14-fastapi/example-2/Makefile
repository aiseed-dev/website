SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

.PHONY: all extract preview clean

all: extract preview

extract:
	@mkdir -p out
	@python3 extract_rules.py

preview:
	@echo
	@echo "=== 抽出された RULES.md(先頭 40 行)==="
	@head -40 out/RULES.md
	@echo
	@echo "(全文は out/RULES.md)"

clean:
	rm -rf out
