SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

PHOTOS := photos
OUT    := out

.PHONY: all samples organize verify clean

all: samples organize verify

samples:
	@python3 generate_samples.py

organize: samples
	@echo
	@echo "=== 撮影日でフォルダ分け ==="
	@mkdir -p $(OUT)
	@rm -rf $(OUT)/by-month
	@time python3 photo_organizer.py $(PHOTOS) -o $(OUT)/by-month --copy 2>&1 | tail -5
	@echo

verify:
	@echo "=== 結果 ==="
	@for d in $(OUT)/by-month/*/; do \
	  printf "  %s : %s 枚\n" "$$(basename $$d)" "$$(ls $$d | wc -l)"; \
	done | sort
	@printf "  ── 合計 %s 枚を %s フォルダに振り分け\n" \
	  "$$(find $(OUT)/by-month -type f | wc -l)" \
	  "$$(ls -d $(OUT)/by-month/*/ | wc -l)"

clean:
	rm -rf $(PHOTOS) $(OUT)
