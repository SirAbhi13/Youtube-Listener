
db:
	python3 manage.py makemigrations
	python3 manage.py migrate

setup:
	python3 -m pip install poetry
	poetry install
	cp .env.example .env
