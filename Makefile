check: check-pylint check-black

check-pylint:
	@uv run pylint --errors-only pysolarfocus/*

check-black:
	@uv run black --check pysolarfocus/*

codefix:
	@uv run isort pysolarfocus/*
	@uv run black pysolarfocus/*

test:
	@uv run pytest

run: 
	@uv run python3 example.py

.PHONY: check codefix test run