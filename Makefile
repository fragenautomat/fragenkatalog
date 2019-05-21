run:
	pipenv run ./fragenkatalog/manage.py runserver
migrations:
	pipenv run ./fragenkatalog/manage.py makemigrations
	pipenv run ./fragenkatalog/manage.py migrate --run-syncdb