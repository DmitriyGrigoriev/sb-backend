#!/bin/bash
NAME="smart-billing"                              # Name of the application
DJANGODIR=/home/www/code/backend/sb               # Django project directory

echo "Starting $NAME"

# Activate the virtual environment
cd $DJANGODIR

source ../env/bin/activate
exec gunicorn -c "../config/gunicorn_config.py" config.wsgi

# source /home/www/code/backend/sb/env/bin/activate
#cd /home/www/code/backend/sb
#exec gunicorn -c "/home/www/code/backend/sb/config/gunicorn_config.py" config.wsgi