from django.urls import reverse_lazy
from config.settings import *
from config.function import set_classes
#from config.group import CreateTestGroup
# Create test groups
# CreateTestGroup()

DEBUG = True

DOMAIN = env.str('DEVDOMAIN')
ALLOWED_HOSTS = env.list('DEVALLOWED_HOSTS', default=['*'])
SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(minutes=25)
# Add some classes to REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']
# that give an ability to perform REST queries without JWT tokens
auth_classes = set_classes(
    REST_FRAMEWORK,
    'DEFAULT_AUTHENTICATION_CLASSES',
    (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
     )
)
if len(auth_classes) > 0:
    del REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = auth_classes

# Set AllowAny permission for REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES']
del REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES']
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = tuple(['rest_framework.permissions.AllowAny',])

INSTALLED_APPS += [
    # 'corsheaders',
    #'drf_yasg',
]
###  How to integrate swagger with JWT
SWAGGER_SETTINGS = {
    'LOGIN_URL': reverse_lazy('rest_framework:login'),
    'LOGOUT_URL': reverse_lazy('rest_framework:logout'),
    # 'USE_SESSION_AUTH': False,
    # 'DOC_EXPANSION': 'list',
    # 'APIS_SORTER': 'alpha',
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            "description": "JWT authorization"
        }
    },
}

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_HOST = env.str('DEVEMAIL_HOST', default='mailhog')
EMAIL_PORT = env.int('DEVEMAIL_PORT', default='1025')
EMAIL_HOST_USER = env.str('DEVEMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env.str('DEVEMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = env.bool('DEVEMAIL_USE_TLS', default=True)

CORS_ORIGIN_ALLOW_ALL = True
# CorsHeaders settings from django-cors-headers
CORS_ORIGIN_WHITELIST = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:1313",
    "http://localhost:1313",
    "http://192.168.177.130",
    "http://192.168.177.130:8000"
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        }
    },
    "loggers": {
        "django.request": {"handlers": ["mail_admins"], "level": "ERROR", "propagate": True}
    },
}
