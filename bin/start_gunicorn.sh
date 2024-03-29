#!/bin/bash

# https://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/
NAME="smart-billing"                              # Name of the application
DJANGODIR=/home/www/code/backend/sb               # Django project directory

echo "Starting $NAME"

# Activate the virtual environment
cd $DJANGODIR

source ./env/bin/activate
exec gunicorn -c "./config/gunicorn_config.py" config.wsgi