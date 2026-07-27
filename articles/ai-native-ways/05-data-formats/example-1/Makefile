SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

XLSX := xlsx
CSV  := csv
OUT  := out

.PHONY: all xlsx convert measure aggregate query clean

all: $(XLSX)/.stamp $(CSV)/.stamp measure aggregate query

$(XLSX)/.stamp: generate_sales.py
	@python3 generate_sales.py
	@touch $(XLSX)/.stamp

$(CSV)/.stamp: $(XLSX)/.stamp
	@mkdir -p $(CSV)
	@echo "=== xlsx → csv 変換 (pandas) ==="
	@python3 -c "import glob, pandas as pd, os; \
files=sorted(glob.glob('$(XLSX)/*.xlsx')); \
[pd.read_excel(f).to_csv('$(CSV)/'+os.path.splitext(os.path.basename(f))[0]+'.csv', index=False) for f in files]; \
print(f'  {len(files)} ファイルを CSV に変換')"
	@touch $(CSV)/.stamp

measure: $(CSV)/.stamp
	@mkdir -p $(OUT)
	@echo
	@echo "=== サイズ比較 ==="
	@xlsx_total=$$(du -bc $(XLSX)/*.xlsx | tail -1 | cut -f1); \
	 csv_total=$$(du -bc $(CSV)/*.csv | tail -1 | cut -f1); \
	 ratio=$$(python3 -c "print(f'{$$xlsx_total / $$csv_total:.1f}')"); \
	 printf "  Excel (.xlsx) 合計: %'d bytes (%d KB)\n" $$xlsx_total $$(($$xlsx_total / 1024)); \
	 printf "  CSV 合計          : %'d bytes (%d KB)\n" $$csv_total $$(($$csv_total / 1024)); \
	 printf "  Excel / CSV       : %s 倍\n" "$$ratio"; \
	 echo "$$ratio" > $(OUT)/size-ratio.txt

aggregate: $(CSV)/.stamp
	@python3 aggregate.py | tee $(OUT)/aggregate.log

query: $(CSV)/.stamp
	@echo
	@echo "=== awk で 100 ファイルから「キャベツ」だけ抽出 ==="
	@t=$$( { time awk -F, '$$3=="キャベツ"' $(CSV)/*.csv > $(OUT)/cabbage.csv; } 2>&1 | grep real | awk '{print $$2}'); \
	 lines=$$(wc -l < $(OUT)/cabbage.csv); \
	 printf "  抽出行数: %s 行  /  実行時間: %s\n" $$lines "$$t"
	@echo
	@echo "=== xlsx を直接 grep しようとすると ==="
	@if grep -l "キャベツ" $(XLSX)/*.xlsx 2>/dev/null | head -1; then \
	  echo "  (バイナリだけど grep にヒットすることがある ── 文字列はあるが構造としては取れない)"; \
	else \
	  echo "  → ヒットしない / 信頼できない(.xlsx は ZIP+XML)"; \
	fi

clean:
	rm -rf $(XLSX) $(CSV) $(OUT)
