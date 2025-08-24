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

test-cov:
	@uv run pytest --cov=src/pysolarfocus --cov-report=term-missing

coverage:
	@uv run coverage run -m pytest
	@uv run coverage report --show-missing

coverage-html:
	@uv run coverage run -m pytest
	@uv run coverage html
	@echo "Coverage report generated in htmlcov/index.html"

run: 
	@uv run python3 example.py

.PHONY: check codefix test test-cov coverage coverage-html run