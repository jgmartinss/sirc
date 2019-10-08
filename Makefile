run:
	python3 manage.py runserver
createuser:
	python3 manage.py createsuperuser
migrations:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
shell:
	python3 manage.py shell
test:
	python3 manage.py test 
initdb:
	python3 manage.py loaddata sirc/core/fixtures/data.json
backup:
	heroku run python manage.py dumpdata --all --indent 4 > sirc/core/fixtures/data.json
