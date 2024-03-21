runserver:
	make db
	python3 manage.py runserver

db:
	python3 manage.py makemigrations
	python3 manage.py migrate

setup:
	python3 -m pip install poetry
	python3 -m poetry config virtualenvs.in-project true
	cp .env.example .env
	python3 -m poetry install --no-root
