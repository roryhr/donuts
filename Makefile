.PHONY: dev test

dev:
	source activate py312 && export DEBUG=True && python manage.py runserver

test:
	source activate py312 && export DEBUG=True && python manage.py test
