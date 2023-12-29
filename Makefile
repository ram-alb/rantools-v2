dev-start:
	poetry run python manage.py runserver

install:
	poetry install

migrate:
	poetry run python manage.py migrate

isort:
	poetry run isort .

lint:
	poetry run flake8

selfcheck:
	poetry check

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=. --cov-report xml

check: selfcheck lint test

shell:
	poetry run python manage.py shell_plus --plain


.PHONY: dev-start install migrate isort lint selfcheck check test-coverage