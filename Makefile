.PHONY: help venv run test
.DEFAULT: help

include .env

VENV=venv
PYTHON=$(VENV)/bin/python3
PIP=$(PYTHON) -m pip
TESTS-REQS-INSTALLED=$(VENV)/tests-requirements-updated
INSTALLED=$(VENV)/installed
MODULE=solanches
BIND=$(SOLANCHES_HOST):$(SOLANCHES_PORT)

help:
	@echo "uso: make [ venv | run ]"

venv: $(VENV)/bin/activate
$(VENV)/bin/activate: requirements.txt
	test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install --requirement requirements.txt
	touch $(VENV)/bin/activate

run: venv
	gunicorn --bind=$(BIND) solanches.rest:app


run-dev: venv
	$(PYTHON) -m $(MODULE)

test: venv $(TESTS-REQS-INSTALLED)
	$(PYTHON) -m pytest

$(TESTS-REQS-INSTALLED): tests-requirements.txt
	$(PIP) install --upgrade pip
	$(PIP) install --requirement tests-requirements.txt
	touch $(TESTS-REQS-INSTALLED)
