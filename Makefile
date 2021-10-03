.PHONY: help venv run run-dev test
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
	@echo "uso: make [ venv | run | run-dev | test | test-cov | checkstyle | deploy ]"

venv: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install --requirement requirements.txt
	touch $(VENV)/bin/activate

run: venv 
	$(VENV)/bin/gunicorn --bind=$(BIND) solanches.rest:app

run-dev: venv
	$(PYTHON) -m $(MODULE)

test: venv $(TESTS-REQS-INSTALLED)
	$(PYTHON) -m pytest

$(TESTS-REQS-INSTALLED): tests-requirements.txt
	$(PIP) install --upgrade pip
	$(PIP) install --requirement tests-requirements.txt
	touch $(TESTS-REQS-INSTALLED)

test-cov: venv $(TESTS-REQS-INSTALLED)
	$(VENV)/bin/pytest -v --cov-report html --cov=solanches

checkstyle: venv
	$(VENV)/bin/pylint solanches

deploy:
	./bin/make_deploy
