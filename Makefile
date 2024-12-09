start:
	poetry run gunicorn -w 5 task_manager.wsgi:application

lint:
	poetry run python3 -m flake8 task_manager
