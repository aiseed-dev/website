SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

OUT := out

.PHONY: all legacy new diff clean

all: legacy new diff

legacy:
	@mkdir -p $(OUT)
	@echo "=== 1. 既存システム (PL/SQL 風) を SQLite で実行 ==="
	@cd $(OUT) && rm -f legacy_output.csv && sqlite3 :memory: < ../legacy.sql
	@echo "  → $(OUT)/legacy_output.csv ($$(wc -l < $(OUT)/legacy_output.csv) 行)"

new:
	@mkdir -p $(OUT)
	@echo
	@echo "=== 2. 新エンジン (Python) を実行 ==="
	@python3 new_engine.py

diff: legacy new
	@echo
	@echo "=== 3. 並行稼働: 出力差分を取る ==="
	@if diff -u $(OUT)/legacy_output.csv $(OUT)/new_output.csv > $(OUT)/diff.txt; then \
	  echo "  ✓ 完全一致 ── 並行稼働 OK、新エンジンに切り替え可能"; \
	  echo "  完全一致: $$(wc -l < $(OUT)/legacy_output.csv) 行"; \
	else \
	  echo "  ✗ 差分あり ── 業務ルールの違いを確認してください"; \
	  cat $(OUT)/diff.txt; \
	fi
	@echo
	@echo "=== 4. 業務ルール (Markdown) ==="
	@echo "  RULES.md に抽出済み:"
	@head -20 RULES.md | sed 's/^/    /'

clean:
	rm -rf $(OUT)
