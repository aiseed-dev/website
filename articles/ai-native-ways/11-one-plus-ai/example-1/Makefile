SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

.PHONY: all build summary clean

all: build summary

build:
	@python3 build_all.py

summary:
	@echo
	@echo "=== 出力ファイル一覧 ==="
	@find out -type f | sort | xargs -I{} sh -c 'printf "  %-32s %8s B\n" "{}" "$$(stat -c%s {})"'
	@echo
	@total=$$(du -sb out | cut -f1); \
	 printf "  合計: %s KB\n" $$(python3 -c "print(f'{$$total/1024:.1f}')")

clean:
	rm -rf out
