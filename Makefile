SHELL 	:= /bin/bash
PYTHON 	:= python3.5
PIP		:= pip3.5

.PHONY: run
run:
	$(PYTHON) src/mmo.py

venv: test-requirements.lock
	virtualenv -p $(PYTHON) venv
	source venv/bin/activate
	$(PIP) install -r test-requirements.lock

.ONESHELL:
test-requirements.lock: test-requirements.txt requirements.lock
	rm -rf .autovenv
	virtualenv -p $(PYTHON) .autovenv
	source .autovenv/bin/activate
	$(PIP) install -r test-requirements.txt
	$(PIP) freeze > test-requirements.lock

.ONESHELL:
requirements.lock: requirements.txt
	rm -rf .autovenv
	virtualenv -p $(PYTHON) .autovenv
	source .autovenv/bin/activate
	$(PIP) install -r requirements.txt
	$(PIP) freeze > requirements.lock

.PHONY: test
test:
	PYTHONPATH=src $(PYTHON) -m pytest test

.PHONY: requirements
requirements: venv

.PHONY: freeze
freeze: requirements.lock test-requirements.lock

.PHONY: clean
clean:
	rm -rf venv
	rm requirements.lock
	rm test-requirements.lock
