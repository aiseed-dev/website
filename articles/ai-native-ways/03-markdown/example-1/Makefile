# 第 01 章の実例: 12 ヶ月分の Word 議事録を Markdown に変える
#
# 必要なツール:
#   - python3 + python-docx (pip install python-docx)
#   - pandoc 2.x+
#
# 使い方:
#   make all       # 入力生成 → 変換 → 計測 → 検索デモ
#   make docx      # 入力 .docx を生成
#   make convert   # docx/ → md/ を pandoc で変換
#   make measure   # サイズ比を集計
#   make search    # grep で「決定事項」を全 md から抽出
#   make clean     # 全部消す

SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

DOCX := docx
MD   := md
OUT  := out

.PHONY: all measure search clean

all: $(MD)/.stamp measure search

$(DOCX)/.stamp: generate_minutes.py
	@python3 generate_minutes.py
	@touch $(DOCX)/.stamp

$(MD)/.stamp: $(DOCX)/.stamp
	@mkdir -p $(MD)
	@echo "=== pandoc で .docx → .md に変換 ==="
	@for f in $(DOCX)/*.docx; do \
	  out=$(MD)/$$(basename $$f .docx).md; \
	  pandoc $$f -o $$out -t gfm --wrap=none; \
	  printf "  %s → %s (%s bytes)\n" $$f $$out $$(stat -c%s $$out); \
	done
	@touch $(MD)/.stamp

measure: $(MD)/.stamp
	@mkdir -p $(OUT)
	@echo "=== サイズ比較 ==="
	@docx_total=$$(du -bc $(DOCX)/*.docx | tail -1 | cut -f1); \
	 md_total=$$(du -bc $(MD)/*.md | tail -1 | cut -f1); \
	 ratio=$$(python3 -c "print(f'{$$docx_total / $$md_total:.1f}')"); \
	 printf "  Word (.docx) 合計: %'d bytes (%d KB)\n" $$docx_total $$(($$docx_total / 1024)); \
	 printf "  Markdown 合計   : %'d bytes (%d KB)\n" $$md_total $$(($$md_total / 1024)); \
	 printf "  Word / MD       : %s 倍\n" "$$ratio"; \
	 echo "$$ratio" > $(OUT)/size-ratio.txt
	@echo
	@echo "=== 文字数 ==="
	@docx_chars=$$(pandoc $(DOCX)/*.docx -t plain --wrap=none 2>/dev/null | wc -m); \
	 md_chars=$$(cat $(MD)/*.md | wc -m); \
	 printf "  Word 抽出後の文字数 : %'d\n" $$docx_chars; \
	 printf "  Markdown 文字数     : %'d\n" $$md_chars

search: $(MD)/.stamp
	@mkdir -p $(OUT)
	@echo "=== grep デモ 1: 全ての決定事項を 1 行ずつ抽出 ==="
	@grep -h "^\*\*決定:\*\*" $(MD)/*.md | sed 's/\*\*決定:\*\* //' | sort -u | tee $(OUT)/decisions.txt
	@printf "  → 12 ファイル × 4 議題 = 48 件 を grep + sed + sort -u で重複排除して "; \
	 t=$$( { time grep -h "^\*\*決定:\*\*" $(MD)/*.md | sed 's/\*\*決定:\*\* //' | sort -u >/dev/null; } 2>&1 | grep real | awk '{print $$2}'); \
	 echo "$$t で完了"
	@echo
	@echo "=== grep デモ 2: 「AI 活用方針」が議題に上がった月 ==="
	@grep -l "AI 活用方針" $(MD)/*.md | xargs -I{} basename {} .md | tee $(OUT)/ai-policy-months.txt
	@echo
	@echo "=== grep デモ 3: 「採用計画」が議題に上がった月 ==="
	@grep -l "採用計画" $(MD)/*.md | xargs -I{} basename {} .md | tee $(OUT)/hiring-months.txt
	@echo
	@echo "=== grep デモ 4: 各月の議題タイトルだけ一覧化 ==="
	@for f in $(MD)/*.md; do \
	  echo "── $$(basename $$f .md) ──"; \
	  grep "^## [0-9]\." $$f | sed 's/^## /  /'; \
	done | tee $(OUT)/all-topics.txt | head -40

clean:
	rm -rf $(DOCX) $(MD) $(OUT)
