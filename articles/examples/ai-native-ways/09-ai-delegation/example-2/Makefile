SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

LOG := access.log
OUT := out

.PHONY: all gen analyze clean

all: $(LOG) analyze

$(LOG): generate_log.py
	@python3 generate_log.py

analyze: $(LOG)
	@mkdir -p $(OUT)
	@echo "=== Q1: 総リクエスト数とステータスコード分布 ==="
	@time awk '{c[$$9]++; n++} END {for (s in c) printf "  %s : %s 件 (%.1f%%)\n", s, c[s], 100*c[s]/n; printf "\n  total: %s 件\n", n}' $(LOG) | tee $(OUT)/q1-status.txt
	@echo
	@echo "=== Q2: アクセス上位 10 IP ==="
	@time { awk '{print $$1}' $(LOG) | sort | uniq -c | sort -rn | head -10; } | tee $(OUT)/q2-top-ips.txt
	@echo
	@echo "=== Q3: 5xx エラーが起きた時間帯 ==="
	@time awk '$$9 ~ /^5/ {print substr($$4, 14, 5)}' $(LOG) | sort | uniq -c | sort -rn | head -10 | tee $(OUT)/q3-5xx-hours.txt
	@echo
	@echo "=== Q4: 404 になった URL 上位 10 ==="
	@time awk '$$9 == 404 {print $$7}' $(LOG) | sort | uniq -c | sort -rn | head -10 | tee $(OUT)/q4-404-paths.txt
	@echo
	@echo "=== Q5: 攻撃疑いの IP 検出(2 種類以上の攻撃 URL を試行)==="
	@time awk '$$7 ~ /(\.env|wp-login|admin|config\.php)/ {print $$1, $$7}' $(LOG) | sort -u | awk '{c[$$1]++} END {for (i in c) if (c[i] >= 2) printf "  %-15s 攻撃 URL %d 種\n", i, c[i]}' | sort -k4 -rn | tee $(OUT)/q5-attackers.txt
	@echo
	@echo "=== Q6: 1 分間のリクエスト数推移(上位 10 分)==="
	@awk '{print substr($$4, 14, 5)}' $(LOG) | sort | uniq -c | sort -rn | head -10 | tee $(OUT)/q6-rps.txt

clean:
	rm -f $(LOG)
	rm -rf $(OUT)
