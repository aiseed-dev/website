SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

J := python3 journal.py

.PHONY: all demo help clean

all: demo

demo:
	@mkdir -p out
	@rm -f out/journal.db
	@echo "=== journal.py CLI デモ ==="
	@echo
	@echo "--- 1. メモを追加 ---"
	@$(J) add "山田農園と打ち合わせ。来月から週次納品" --tag meeting
	@$(J) add "経費レポートを Claude に作らせた、20 分で完了" --tag review
	@$(J) add "新規顧客 C016 が問い合わせ、料金で要確認" --tag lead
	@$(J) add "サーバ再起動 04:00 完了、ダウンタイム 12 秒" --tag ops
	@$(J) add "今月の MRR が目標に到達"
	@$(J) add "山田農園に来週納品手配のメールを送る" --tag todo
	@$(J) add "Mochi.ai の LP に「365 日返金保証」を追記"
	@$(J) add "経理: 4 月分の領収書を Claude に分類させた、3 分"
	@echo
	@echo "--- 2. 最新 5 件 ---"
	@$(J) list --limit 5
	@echo
	@echo "--- 3. 'meeting' タグだけ ---"
	@$(J) list --tag meeting
	@echo
	@echo "--- 4. '山田' を検索 ---"
	@$(J) search 山田
	@echo
	@echo "--- 5. タグ別集計 (JSON) ---"
	@$(J) stats | tee out/stats.json
	@echo
	@echo "--- 6. Markdown エクスポート ---"
	@$(J) export --out out/journal.md
	@echo
	@echo "--- 7. ヘルプ ---"
	@$(J) --help

help:
	@$(J) --help
	@for sub in add list search stats export; do \
	  echo; echo "=== $$sub ==="; $(J) $$sub --help; \
	done

clean:
	rm -rf out
