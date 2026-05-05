SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

.PHONY: all samples process clean

all: src/.stamp process

src/.stamp: generate_samples.py
	@python3 generate_samples.py
	@touch src/.stamp

process: src/.stamp
	@mkdir -p out
	@python3 process.py | tee out/run.log
	@echo
	@echo "=== サンプルを out/sample/ に 6 枚コピー(コミット用)==="
	@mkdir -p out/sample
	@for d in resized thumbs watermarked; do \
	  cp out/$$d/img_000.jpg out/sample/$$d-img_000.jpg; \
	  cp out/$$d/img_050.jpg out/sample/$$d-img_050.jpg; \
	done
	@printf "  サンプル %s ファイル / %s\n" "$$(ls out/sample | wc -l)" "$$(du -sh out/sample | cut -f1)"

clean:
	rm -rf src out
