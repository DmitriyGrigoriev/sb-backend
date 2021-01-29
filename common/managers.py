# https://adw0rd.com/2012/08/24/django-custom-queryset-and-manager-for-chainable-methods/
from django.db import models


class CustomManager(models.Manager):
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)