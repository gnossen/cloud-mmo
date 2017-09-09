.PHONY: run
run:
	python src/mmo.py

.PHONY: requirements
requirements:
	pip install -r requirements.lock

.PHONY: freeze
freeze:
	pip freeze > requirements.lock
