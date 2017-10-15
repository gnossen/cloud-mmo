SHELL := /bin/bash
.PHONY: run
run:
	python src/mmo.py

venv: test-requirements.lock
	virtualenv -p /usr/bin/python3 venv
	source venv/bin/activate
	pip install -r test-requirements.lock

.ONESHELL:
test-requirements.lock: test-requirements.txt requirements.lock
	rm -rf .autovenv
	virtualenv -p /usr/bin/python3 .autovenv
	source .autovenv/bin/activate
	pip3 install -r test-requirements.txt
	pip3 freeze > test-requirements.lock

.ONESHELL:
requirements.lock: requirements.txt
	rm -rf .autovenv
	virtualenv -p /usr/bin/python3 .autovenv
	source .autovenv/bin/activate
	pip3 install -r requirements.txt
	pip3 freeze > requirements.lock

.PHONY: test
test:
	PYTHONPATH=src py.test test

.PHONY: requirements
requirements: venv

.PHONY: freeze
freeze: requirements.lock test-requirements.lock

.PHONY: clean
clean:
	rm -rf venv
	rm requirements.lock
	rm test-requirements.lock
