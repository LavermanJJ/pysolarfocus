check: check-pylint check-black

check-pylint:
	@uv run pylint --errors-only src/pysolarfocus/*

check-black:
	@uv run black --check src/pysolarfocus/*

codefix:
	@uv run isort src/pysolarfocus/*
	@uv run black src/pysolarfocus/*

test:
	@uv run pytest

run: 
	@uv run python3 example.py

.PHONY: check codefix test run