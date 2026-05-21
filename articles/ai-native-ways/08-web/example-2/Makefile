SHELL := /bin/bash
export LANG := C.UTF-8
export LC_ALL := C.UTF-8

.PHONY: all test serve clean

all: test

test:
	@mkdir -p out
	@python3 test_api.py

serve:
	@echo "Starting on http://localhost:8000  (Swagger: http://localhost:8000/docs)"
	@uvicorn app:app --reload --port 8000

clean:
	rm -rf out
