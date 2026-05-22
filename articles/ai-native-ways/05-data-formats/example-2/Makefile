SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

OUT := out

.PHONY: all convert query clean

all: convert query

convert:
	@mkdir -p $(OUT)
	@python3 convert.py

query: convert
	@echo
	@echo "=== jq クエリ 1: プロプランだけ抽出 ==="
	@time jq '.[] | select(.plan == "プロ") | {name, region, monthly_yen}' $(OUT)/customers.json | tee $(OUT)/q-pro.json
	@echo
	@echo "=== jq クエリ 2: 地域別の MRR 合計 ==="
	@jq 'group_by(.region) | map({region: .[0].region, customers: length, mrr: (map(.monthly_yen) | add)}) | sort_by(-.mrr)' \
	   $(OUT)/customers.json | tee $(OUT)/q-region-mrr.json
	@echo
	@echo "=== jq クエリ 3: 全顧客の MRR 合計 ==="
	@jq '[.[] | .monthly_yen] | add' $(OUT)/customers.json
	@echo
	@echo "=== awk で同じことを CSV に直接 ==="
	@awk -F, 'NR>1 {a[$$3]+=$$5; n[$$3]++} END {for (r in a) printf "  %s : %d 顧客 / MRR %d 円\n", r, n[r], a[r]}' \
	   data/customers.csv | sort

clean:
	rm -rf $(OUT)
