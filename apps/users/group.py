import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()
from django.contrib.auth.models import Group


GROUPS = ['administrator', 'superuser']
MODELS = ['user']

for group in GROUPS:
    new_group, created = Group.objects.get_or_create(name=group)