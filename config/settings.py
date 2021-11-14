"""
Django settings for terminal project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
import environ
from datetime import timedelta

# from corsheaders.defaults import default_headers
# ROOT_DIR = /home/www/projects/broker
ROOT_DIR = environ.Path(__file__) - 3
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = /home/www/projects/broker/backend
BASE_DIR = environ.Path(__file__) - 2

# Load operating system environment variables and then prepare to use them
env = environ.Env()
# reading .env file ~/projects/broker/config/.env
environ.Env.read_env(BASE_DIR('config/.env'))

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # rest API implementation library for django
    'rest_framework',
    # JWT authentication backend library
    'rest_framework_simplejwt'
]

THIRD_PARTY_APPS = [
    'django_filters',
    'django_extensions',
    # 'djmoney',
    # 'rest_framework.authtoken',
    'djoser',
    # 'rest_framework_simplejwt.token_blacklist',
]

LOCAL_APPS = [
    'apps.users.apps.UsersConfig',
    # 'apps.transportconf.apps.TransportConfig',
    'apps.settings.apps.SettingsConfig',
    # 'phonenumber_field',
    # 'apps.cms.apps.CmsConfig',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.contrib.admindocs.middleware.XViewMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'concurrency.middleware.ConcurrencyMiddleware',
    # 'common.middleware.ConcurrencyMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # middleware from django-cors-headers
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CONCURRENCY_HANDLER409 = 'common.handlers.conflict'
CONCURRENCY_POLICY = 2
# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DEBUG')
SECRET_KEY = env.str('SECRET_KEY')
# DOMAINS
DOMAIN = env.str('DOMAIN')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', )
# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_HOST = env.str('EMAIL_HOST', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default='587')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ('dimag', 'dimag@ntbroker.ru'),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': 5432,
    },
}

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'ru'
get_text = lambda s: s
LANGUAGES = (
    ('ru', get_text('Russia')),
    ('ru', get_text('English')),
)
# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

SITE = 1

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
# ~projects/broker/backend/static
# STATIC_ROOT = str(BASE_DIR('static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
# Настройка STATICFILES_DIRS указывает каталоги, которые проверяются на наличие статических файлов.
# может содержать статические файлы, которые не относятся ни к одному из приложений.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
# MEDIA_ROOT = str(BASE_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': STATICFILES_DIRS,
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',
]

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'

# DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Json Web Token Authentication
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # Token Base Authentication
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    # 'DEFAULT_PAGINATION_CLASS':
    #     'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 10,
    # 'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M:%S",
    # 'EXCEPTION_HANDLER': 'common.exps_handler.drf_exception_handler',
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# https://www.youtube.com/watch?v=CC3uxnYYdMM&list=PLJRGQoqpRwdfoa9591BcUS6NmMpZcvFsM&index=3&t=2s
DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': '/password-reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '/username-reset/confirm/{uid}/{token}',

    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}/',
    'SERIALIZERS': {
        'user_create': 'apps.users.serializers.UserCreateSerializer',
        'user': 'apps.users.serializers.UserCreateSerializer',
        'current_user': 'apps.users.serializers.UserSerializer',
        'user_delete': 'apps.users.serializers.UserDeleteSerializer',
    },
    'TOKEN_MODEL': None,
    'HIDE_USERS': False
    # 'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
}

# if not DEBUG:
#     # raven sentry client
#     # See https://docs.sentry.io/clients/python/integrations/django/
#     INSTALLED_APPS += ['raven.contrib.django.raven_compat']
#     RAVEN_MIDDLEWARE = ['raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware']
#     MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE
#
#     # Host adress for right auth
#     # CORS_ORIGIN_WHITELIST = [
#     #     'http://10.20.2.19',
#     # ]
#     # CORS_ALLOW_HEADERS = list(default_headers) + [
#     #     'content-type',
#     # ]
#
#     # Sentry Configuration
#     SENTRY_DSN = env.str('SENTRY_DSN')
#     SENTRY_CLIENT = 'raven.contrib.django.raven_compat.DjangoClient'
#     LOGGING = {
#         'version': 1,
#         'disable_existing_loggers': True,
#         'root': {
#             'level': 'WARNING',
#             'handlers': ['sentry'],
#         },
#         'formatters': {
#             'verbose': {
#                 'format': '%(levelname)s %(asctime)s %(module)s '
#                           '%(process)d %(thread)d %(message)s'
#             },
#         },
#         'handlers': {
#             'sentry': {
#                 'level': 'ERROR',
#                 'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
#             },
#             'console': {
#                 'level': 'DEBUG',
#                 'class': 'logging.StreamHandler',
#                 'formatter': 'verbose'
#             }
#         },
#         'loggers': {
#             'django.db.backends': {
#                 'level': 'ERROR',
#                 'handlers': ['console'],
#                 'propagate': False,
#             },
#             'raven': {
#                 'level': 'DEBUG',
#                 'handlers': ['console'],
#                 'propagate': False,
#             },
#             'sentry.errors': {
#                 'level': 'DEBUG',
#                 'handlers': ['console'],
#                 'propagate': False,
#             },
#             'django.security.DisallowedHost': {
#                 'level': 'ERROR',
#                 'handlers': ['console', 'sentry'],
#                 'propagate': False,
#             },
#         },
#     }
#
#     RAVEN_CONFIG = {
#         'DSN': SENTRY_DSN
#     }
# else:

