check: check-pylint check-black

check-pylint:
	@poetry run pylint pysolarfocus/*.py

check-black:
	@poetry run black --check pysolarfocus/*.py

codefix:
	@poetry run isort pysolarfocus/*.py
	@poetry run black pysolarfocus/*.py

test:
	@poetry run pytest

.PHONY: check codefix test