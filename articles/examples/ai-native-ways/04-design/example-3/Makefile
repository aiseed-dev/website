# 名刺サンプル: Python と HTML の二経路で同じ名刺 PDF を生成
#
# 必要なツール:
#   - python3
#   - pip install reportlab weasyprint
#   - (任意) Noto CJK フォント: sudo apt install fonts-noto-cjk
#
# 使い方:
#   make all         # 全 PDF を生成 + 計測
#   make python      # Python (ReportLab) 経路のみ
#   make html        # HTML + Weasyprint 経路のみ
#   make clean       # out/ を消す

SHELL := /bin/bash
OUT := out

.PHONY: all python html clean measure

all: python html measure

$(OUT):
	mkdir -p $(OUT)

# ── 経路 A: Python (ReportLab) で直接 PDF を組む ──
python: $(OUT)
	@echo "[A] Python (ReportLab) で名刺 PDF を生成"
	@python3 business_card.py

# ── 経路 B: HTML + CSS を WeasyPrint で PDF に焼く ──
# (ブラウザで開いて Ctrl+P → PDF に保存 と等価。WeasyPrint は
#  ヘッドレスでこれを自動化するだけ。)
html: $(OUT)
	@echo "[B] HTML + WeasyPrint で名刺 PDF を生成"
	@python3 -c "from weasyprint import HTML; \
HTML('business-card.html').write_pdf('$(OUT)/business-card-html.pdf'); \
print('  wrote $(OUT)/business-card-html.pdf')"
	@python3 -c "from weasyprint import HTML; \
HTML('business-card-sheet.html').write_pdf('$(OUT)/business-card-sheet-html.pdf'); \
print('  wrote $(OUT)/business-card-sheet-html.pdf')"

measure:
	@echo ""
	@echo "==== 計測 ===="
	@ls -la $(OUT)/*.pdf 2>/dev/null | awk '{printf "  %-44s %6s bytes\n", $$NF, $$5}'

clean:
	rm -rf $(OUT)
