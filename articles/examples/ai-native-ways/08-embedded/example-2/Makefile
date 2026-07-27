SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

.PHONY: all collect analyze clean

all: collect analyze

collect:
	@mkdir -p out
	@python3 collect.py

analyze: collect
	@python3 analyze.py

clean:
	rm -rf out
