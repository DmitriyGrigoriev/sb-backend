import environ

BASE_DIR = environ.Path(__file__) - 2
# Load operating system environment variables and then prepare to use them
env = environ.Env()
# reading .env file ~/projects/broker/config/.env
env_file = env.str('GUNICORN_COMMAND')+'/.env'
environ.Env.read_env(env_file)

command = env.str('GUNICORN_COMMAND')
pythonpath = env.str('GUNICORN_PYTHONPATH')
bind = env.str('GUNICORN_BIND')
workers = env.int('GUNICORN_WORKERS')
user = env.str('GUNICORN_USER')
limit_request_fields = env.int('GUNICORN_LIMIT_REQUEST_FIELDS')
limit_request_fields_SIZE = env.int('GUNICORN_LIMIT_REQUEST_FIELDS_SIZE')
raw_env = env.str('GUNICORN_RAW_ENV')