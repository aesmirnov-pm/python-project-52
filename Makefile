reset_db:
	poetry run python3 manage.py migrate user zero
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

migrate_db:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

start:
	poetry run python3 manage.py migrate
	poetry run gunicorn -w 5 task_manager.wsgi:application

lint:
	poetry run python3 -m flake8 task_manager
