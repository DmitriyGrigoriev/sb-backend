from django.db import models
# from django.db.models.deletion import get_candidate_relations_to_delete
from django.contrib import admin
from django.db.models import ProtectedError
from django.utils.translation import ugettext_lazy as _

from concurrency.fields import IntegerVersionField

from common.exceptions import AppsProtectedError

class TemplateModel(models.Model):
    created = models.DateTimeField(verbose_name=_('Создана'), auto_now_add=True, auto_now=False, editable=False)
    modified = models.DateTimeField(verbose_name=_('Изменена'), auto_now=True, editable=False)
    # Optimistic lock version
    version = IntegerVersionField(verbose_name=_('Версия'), default=0)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        try:
            super(TemplateModel, self).delete(using=using, keep_parents=keep_parents)
        except ProtectedError as exc:
            # https://github.com/aris-creator/shuupe/blob/161af6727176135ddb163bc185dc2e1eaddc1925/shuup/api/mixins.py
            ref_obj = list(exc.protected_objects)[0]._meta.verbose_name_plural
            raise AppsProtectedError(
                detail=_(f'Невозможно удалить данные, т.к на них имеется ссылка в таблице: «{ref_obj}».')
            )
        # if self.can_delete():
        #     super(TemplateModel, self).delete(using=using, keep_parents=keep_parents)
        # else:
        #     raise AppsProtectedError(
        #         _(f'Не удается удалить некоторые записи таблицы «{self._meta.verbose_name}».'),
        #     )

    # def can_delete(self):
    #     # https://stackoverflow.com/questions/26659023/deletion-objects-that-is-used-as-foreign-key
    #     # get all the related object to be deleted
    #     for related in get_candidate_relations_to_delete(self._meta):
    #         field = related.field
    #         if field.remote_field.on_delete == models.PROTECT:
    #             # check for relationship with at least one related object
    #             related = related.related_model.objects.filter(**{related.field.name: self})
    #             if related.exists():
    #                 return False
    #     return True

    # def clean(self):
    #     """
    #     Check for instances with null values in unique_together fields.
    #     https://code.djangoproject.com/ticket/28545
    #     https://stackoverflow.com/questions/3488264/django-unique-together-doesnt-work-with-foreignkey-none/4805581#4805581
    #     """
    #
    #     super(TemplateModel, self).clean()
    #
    #     for field_tuple in self._meta.unique_together[:]:
    #         unique_filter = {}
    #         unique_fields = []
    #         null_found = False
    #         for field_name in field_tuple:
    #             field_value = getattr(self, field_name)
    #             if getattr(self, field_name) is None:
    #                 unique_filter['%s__isnull' % field_name] = True
    #                 null_found = True
    #             else:
    #                 unique_filter['%s' % field_name] = field_value
    #                 unique_fields.append(field_name)
    #         if null_found:
    #             unique_queryset = self.__class__.objects.filter(**unique_filter)
    #             if self.pk:
    #                 unique_queryset = unique_queryset.exclude(pk=self.pk)
    #             if unique_queryset.exists():
    #                 msg = self.unique_error_message(self.__class__, tuple(unique_fields))
    #                 raise ValidationError(msg)


class TemplateAdminModel(admin.ModelAdmin):
    list_display = ['__str__']

    class Meta:
        abstract = True


class TemplateUserAdminModel(admin.ModelAdmin):
    list_display = ['__str__']
    exclude = ['id', 'created', 'modified', ]

    class Meta:
        abstract = True
