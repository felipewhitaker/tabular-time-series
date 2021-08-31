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

ci-setup:
	pip install poetry
	poetry install

ci-test: test