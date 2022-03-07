SHELL=/bin/bash

.PHONY: install
install:
	pip install --upgrade black requests jsonschema ruamel.yaml

.PHONY: format
format:
	black .

.PHONY: validate
validate:
	python .ci/validate-examples.py
