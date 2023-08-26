check: check-pylint check-black

check-pylint:
	@poetry run pylint pysolarfocus/*

check-black:
	@poetry run black --check pysolarfocus/*

codefix:
	@poetry run isort pysolarfocus/*
	@poetry run black pysolarfocus/*

test:
	@poetry run pytest

.PHONY: check codefix test