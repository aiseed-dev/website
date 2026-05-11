SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

PDF := pdf
OUT := out

.PHONY: all extract clean

all: $(PDF)/.stamp extract

$(PDF)/.stamp: generate_invoices.py
	@python3 generate_invoices.py
	@touch $(PDF)/.stamp

extract: $(PDF)/.stamp
	@mkdir -p $(OUT)
	@python3 extract_amounts.py | tee $(OUT)/run.log

clean:
	rm -rf $(PDF) $(OUT)
