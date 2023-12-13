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

check: selfcheck lint


.PHONY: dev-start install migrate isort lint selfcheck check