SHELL=/bin/bash

.PHONY: format
format:
	black .

.PHONY: validate
validate:
	python .ci/validate-examples.py
