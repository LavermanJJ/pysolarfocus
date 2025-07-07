check: check-pylint check-black

check-pylint:
	@uv run pylint --errors-only src/pysolarfocus/* tests/*

check-black:
	@uv run black --check src/pysolarfocus/* tests/*

codefix:
	@uv run isort src/pysolarfocus/* tests/*
	@uv run black src/pysolarfocus/* tests/*

test:
	@uv run pytest

run: 
	@uv run python3 example.py

.PHONY: check codefix test run