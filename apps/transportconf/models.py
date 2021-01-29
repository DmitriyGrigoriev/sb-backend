from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import TemplateModel

"""
Наименование таможенного терминала, таблица используется для
привязки терминала к номеру лицензии
"""
class Terminal(TemplateModel):
    name = models.CharField(max_length=140, verbose_name=_('Название терминала'))

    class Meta:
        db_table = 'terminal'
        ordering = ['name']
        verbose_name = _('Терминал')
        verbose_name_plural = _('терминалы')

    def __str__(self):
        return self.name


# class License(models.Model):
#     number = models.CharField(max_length=50, verbose_name=_('Номер лицензии'))
#     terminal = models.ForeignKey(to=Terminal,
#                                  verbose_name=_('Терминал'),
#                                  related_name='terminal',
#                                  on_delete=models.RESTRICT(),
#                                  )
#     due_to = models.DateField(verbose_name=_('Действует до'), null=True, blank=True)
#     post_name = models.CharField(max_length=150, verbose_name=_('Пост'))
#     post_code = models.CharField(max_length=50, verbose_name=_('Код поста'))
#
#     class Meta:
#         db_table = 'license'
#         unique_together = ('number',)
#         verbose_name = _('Лицензия')
#         verbose_name_plural = _('лицензии')
#
#     def __str__(self):
#         return '{}'.format(self.post_name)