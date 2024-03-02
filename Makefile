check: check-pylint check-black

check-pylint:
	@poetry run pylint --errors-only pysolarfocus/*

check-black:
	@poetry run black --check pysolarfocus/*

codefix:
	@poetry run isort pysolarfocus/*
	@poetry run black pysolarfocus/*

test:
	@poetry run pytest

run: 
	@poetry run python3 example.py

.PHONY: check codefix test run