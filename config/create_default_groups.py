from django.contrib.auth.models import Group
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()
from django.contrib.auth.models import Group


def CreateTestGroup():
    GROUPS = ['administrator', 'superuser', 'guest', 'reviewer', 'encoder', 'menu_edit']
    MODELS = ['user']

    for group in GROUPS:
        new_group, created = Group.objects.get_or_create(name=group)
