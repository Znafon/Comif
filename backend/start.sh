#!/bin/sh

python manage.py migrate
#exec gunicorn --bind 0.0.0.0:8000 --log-file=- comif.wsgi
python manage.py runserver 0.0.0.0:8000
