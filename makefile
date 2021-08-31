clean:
	rm -rf .venv .pytest_cache .coverage

init: clean
	pip install poetry
	poetry-install
	pre-commit install

test:
	poetry run python -m pytest

test-coverage:
	poetry run python -m pytest --cov tests/

format: 
	poetry run black tabular_time_series/ tests/

publish:
	poetry publish --build -u PYPI_USERNAME -p PYPI_PASSWORD

ci-setup:
	pip install poetry
	poetry install

ci-test: test

.PHONY:
	clean
	init
	test
	test-coverage
	format
	ci-setup
	ci-test