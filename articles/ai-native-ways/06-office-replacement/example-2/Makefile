SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

.PHONY: all merge clean

all: merge

merge:
	@mkdir -p out
	@python3 mailmerge.py | tee out/run.log

clean:
	rm -rf out
