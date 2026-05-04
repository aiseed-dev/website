SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

SRC := src
OUT := out

.PHONY: all generate convert measure cost clean

all: $(SRC)/.stamp convert measure cost

$(SRC)/.stamp: generate_images.py
	@python3 generate_images.py
	@touch $(SRC)/.stamp

convert: $(SRC)/.stamp
	@mkdir -p $(OUT)/webp
	@echo "=== 1,000 ファイルを WebP に変換 (cwebp + xargs -P) ==="
	@time (find $(SRC) -name "*.png" -print0 | xargs -0 -n1 -P 8 -I{} sh -c \
	  'cwebp -quiet -resize 800 0 -q 80 "{}" -o "$(OUT)/webp/$$(basename "{}" .png).webp"') 2>&1 | tail -5

measure: convert
	@echo
	@echo "=== サイズ削減 ==="
	@in=$$(du -sb $(SRC) | cut -f1); \
	 out=$$(du -sb $(OUT)/webp | cut -f1); \
	 ratio=$$(python3 -c "print(f'{$$in / $$out:.1f}')"); \
	 printf "  入力 (PNG) : %s MB\n" $$(python3 -c "print(f'{$$in/1024/1024:.1f}')"); \
	 printf "  出力 (WebP): %s MB\n" $$(python3 -c "print(f'{$$out/1024/1024:.1f}')"); \
	 printf "  削減        : %s 倍\n" "$$ratio"
	@echo
	@echo "=== サンプルを out/sample/ に 50 枚コピー(コミット用)==="
	@mkdir -p $(OUT)/sample
	@ls $(OUT)/webp/*.webp | head -50 | xargs -I{} cp {} $(OUT)/sample/
	@printf "  サンプル %s ファイル / %s\n" "$$(ls $(OUT)/sample | wc -l)" "$$(du -sh $(OUT)/sample | cut -f1)"

cost: measure
	@echo
	@echo "=== コスト試算 ==="
	@printf "  この方式 (Linux + cwebp + xargs):\n"
	@printf "    実行時間   : 上記の通り\n"
	@printf "    AI 利用料  : 0 円(コードを 1 回書いてもらった以外は API を呼ばない)\n"
	@printf "  AI エージェント方式(参考値、章本文より):\n"
	@printf "    実行時間   : 約 60 分(LLM の応答待ちが支配的)\n"
	@printf "    AI 利用料  : 約 \$$5(1,000 ファイル × ツール呼び出し往復)\n"
	@printf "  年間で同じ処理を毎日:\n"
	@printf "    シェル方式: \$$5〜10/年(初回コード生成のみ)\n"
	@printf "    エージェント: \$$1,825〜2,400/年\n"

clean:
	rm -rf $(SRC) $(OUT)
