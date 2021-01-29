from django.db import models
from django.contrib import admin


class TemplateModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class TemplateAdminModel(admin.ModelAdmin):
    list_display = ['__str__']

    class Meta:
        abstract = True


class TemplateUserAdminModel(admin.ModelAdmin):
    list_display = ['__str__']
    exclude = ['id', 'created', 'modified', ]

    class Meta:
        abstract = True
