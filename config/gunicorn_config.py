import environ
# https://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/
BASE_DIR = environ.Path(__file__) - 2
# Load operating system environment variables and then prepare to use them
env = environ.Env()
environ.Env.read_env(BASE_DIR('config/.env'))

command = env.str('GUNICORN_COMMAND')
pythonpath = env.str('GUNICORN_PYTHONPATH')
bind = env.str('GUNICORN_BIND')
workers = env.int('GUNICORN_WORKERS')
user = env.str('GUNICORN_USER')
limit_request_fields = env.int('GUNICORN_LIMIT_REQUEST_FIELDS')
limit_request_fields_SIZE = env.int('GUNICORN_LIMIT_REQUEST_FIELDS_SIZE')
raw_env = env.str('GUNICORN_RAW_ENV')
stdout_logfile = env.str('GUNICORN_STDOUT_LOGFILE')
redirect_stderr = True