.PHONY: format lint type-check all

format:
	black .
	isort .

lint:
	flake8 .

type-check:
	mypy .

all: format lint type-check
