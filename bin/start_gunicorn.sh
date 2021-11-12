#!/bin/bash
source /home/www/code/backend/sb/env/bin/activate
exec gunicorn -c "/home/www/code/backend/sb/config/gunicorn_config.py" config.wsgi