from djmoney.models.fields import Decimal
from django.db import models
from django.utils.translation import ugettext_lazy as _

class SexChoise(models.IntegerChoices):
    UNKNOWN = 0, _('Не указан')
    MEN = 1, _('Мужской')
    WOMEN = 2, _('Женский')

# MONEYFILED
MAX_DIGITS = 18
MAX_DECIMAL = 2
MAX_CURRENCY_DECIMAL = Decimal(0.01)
DEFAULT_CURRENCY = 'RUB'