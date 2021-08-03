.PHONY: help venv install run
.DEFAULT: help

VENV=venv
PYTHON=$(VENV)/bin/python3
PIP=$(PYTHON) -m pip
INSTALLED=$(VENV)/installed
MODULE=solanches

help:
	@echo "uso: make [ venv | run ]"

venv: $(VENV)/bin/activate
$(VENV)/bin/activate: requirements.txt
	test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install --requirement requirements.txt
	touch $(VENV)/bin/activate

run: venv
	$(PYTHON) -m $(MODULE)
