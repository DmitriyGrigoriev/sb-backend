from django.db import models
from common.models import TemplateModel
from django.utils.translation import ugettext_lazy as _

from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from common.constants import (
    MAX_DIGITS,
    MAX_DECIMAL,
    MAX_CURRENCY_DECIMAL,
    DEFAULT_CURRENCY,
)

from .managers import (
    VatPostingGroupManager,
    UnitOfMeasureManager,
    # ServiceTypeManager,
    ServiceManager,
    NoSeriesManager,
    NoSeriesLineManager
)


# «Unit of Measure» («Единица Измерения»)
class UnitOfMeasure(TemplateModel):
    class Meta:
        db_table = 'unit_of_measure'
        verbose_name = _('Единица Измерения')
        verbose_name_plural = _('Единицы Измерения')

    def __str__(self):
        return f'{self.code}'

    code = models.CharField(verbose_name=_('Код Ед. Измерения'), unique=True, max_length=20)
    description = models.CharField(verbose_name=_('Описание'), max_length=50)
    okei_code = models.CharField(verbose_name=_('Код ОКЕИ'), max_length=3, blank=True, default='')
    objects = models.Manager() # default manager
    unit_of_measure = UnitOfMeasureManager()


# «Service Type» («Тип Услуги»)
class ServiceType(TemplateModel):
    class Meta:
        db_table = 'service_type'
        verbose_name = _('Тип Услуги')
        verbose_name_plural = _('Тип Услуг')

    def __str__(self):
        return f'{self.code}'

    code = models.CharField(verbose_name=_('Код Типа Услуг'), max_length=20)
    description = models.CharField(verbose_name=_('Описание'),
                                   max_length=50,
                                   blank=False,
                                   error_messages={'requared': _('Необходимо заполнить описание услуги')}
                                   )
    objects = models.Manager() # default manager


# «VAT Posting Group» («НДС  Учетная Группа»)
class VatPostingGroup(TemplateModel):
    class Meta:
        db_table = 'vat_posting_group'
        verbose_name = _('НДС Учетная Группа')
        verbose_name_plural = _('НДС Учетные Группы')

    def __str__(self):
        return f'{self.code}'

    code = models.CharField(verbose_name=_('Код Учетной Группы'), unique=True, max_length=20)
    description = models.CharField(verbose_name=_('Описание'), max_length=50)
    vat = models.DecimalField(verbose_name=_('НДС %'), max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    vatextempt = models.BooleanField(verbose_name=_('Освоб. от НДС'))
    objects = models.Manager() # default manager
    vat_posting_group = VatPostingGroupManager()


# «Service» («Услуга»)
class Service(TemplateModel):
    class Meta:
        db_table = 'service'
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')

    def __str__(self):
        return f'{self.code} - {self.description}'

    code = models.CharField(verbose_name=_('Код'), unique=True, max_length=20)
    description = models.CharField(verbose_name=_('Краткое описание'), max_length=50)
    full_name = models.CharField(verbose_name=_('Полное наименование'),
                                 max_length=1000,
                                 blank=True,
                                 default=''
                                 )
    service_type = models.ForeignKey(to=ServiceType, verbose_name=_('Тип Услуги'),
                                     on_delete=models.PROTECT,
                                     related_name='service_type'
                                     )
    unit_of_measure = models.ForeignKey(to=UnitOfMeasure, verbose_name=_('Единица Измерения'),
                                     on_delete=models.PROTECT)
    vat_posting_group = models.ForeignKey(to=VatPostingGroup, verbose_name=_('НДС Учетная Группа'),
                                     on_delete=models.PROTECT)
    unit_price = MoneyField(verbose_name=_('Цена Единицы'),
                            default=0,
                            max_digits=MAX_DIGITS,
                            decimal_places=MAX_DECIMAL,
                            default_currency=DEFAULT_CURRENCY,
                            validators=[MinMoneyValidator(MAX_CURRENCY_DECIMAL)]
                            )
    external_service_code = models.CharField(verbose_name=_('Внешний Код Услуги'),
                                                            blank=True,
                                                            default='',
                                                            max_length=50
                                             )
    blocked = models.BooleanField(verbose_name=_('Блокирована'))
    objects = models.Manager() # default manager
    sevice = ServiceManager()


# «Service» («Услуга, цена»)
class ServicePrice(TemplateModel):
    class Meta:
        db_table = 'service_price'
        verbose_name = _('Услуга Цена')
        verbose_name_plural = _('Услуги Цены')

    def __str__(self):
        return f'{self.service_code} | {self.unit_price} | {self.start_date}'

    start_date = models.DateField(verbose_name=_('Дата начала'),
                                  unique=True, null=True, blank=True,
                                  auto_now_add=True
                                  )
    service_code = models.CharField(verbose_name=_('Код услуги'), max_length=20)
    unit_price = MoneyField(verbose_name=_('Цена Единицы'),
                            default=0,
                            max_digits=MAX_DIGITS,
                            decimal_places=MAX_DECIMAL,
                            default_currency=DEFAULT_CURRENCY,
                            validators=[MinMoneyValidator(MAX_CURRENCY_DECIMAL)]
                            )
    objects = models.Manager() # default manager


# «No. Series» («Серия Номеров»), списочная (только чтение) + карточная формы
class NoSeries(TemplateModel):
    class Meta:
        db_table = 'no_series'
        verbose_name = _('Серия Номеров')
        verbose_name_plural = _('Серии Номеров')

    def __str__(self):
        return f'{self.code}'

    code = models.CharField(verbose_name=_('Код'), unique=True, max_length=20)
    description = models.CharField(verbose_name=_('Описание'), max_length=100)
    date_order = models.BooleanField(verbose_name=_('Порядок Дат'), default=False)

    objects = models.Manager() # default manager
    no_series = NoSeriesManager()


# «No. Series Line» («Серия Номеров Строка»), списочная субформа (поле Код не отображаем)
class NoSeriesLine(TemplateModel):
    class Meta:
        db_table = 'no_series_line'
        verbose_name = _('Серия Номеров Строка')
        verbose_name_plural = _('Серия Номеров Строки')

    def __str__(self):
        return f'{self.series_no} | Начальный Но: ' \
               f'{self.starting_no} | Посл.Исп. Но: {self.last_no_used}'


    series_no = models.ForeignKey(to=NoSeries, verbose_name=_('Код'),
                                  related_name='noseriesline',
                                  on_delete=models.PROTECT)
    starting_date = models.DateField(verbose_name=_('Дата начала'),
                                     unique=True, blank=False,)
    starting_no = models.CharField(verbose_name=_('Начальный Но'), max_length=20)
    ending_no = models.CharField(verbose_name=_('Конечный Но'), max_length=20)
    last_date_used = models.DateField(verbose_name=_('Посл.Исп. Дата'),
                                      blank=True, null=True,)
    warning_no = models.CharField(verbose_name=_('Предупредительный Но'),
                                  default='', blank=True, max_length=20)
    last_no_used = models.CharField(verbose_name=_('Посл.Исп. Но'),
                                    default='', blank=True, max_length=20,)
    increment_by = models.PositiveIntegerField(verbose_name=_('Увеличивать На'), default=1)
    blocked = models.BooleanField(verbose_name=_('Заблокирована'), default=False)
    # It's list of commons and specific managers
    objects = models.Manager() # default manager
    series_line = NoSeriesLineManager()


# «Billing Setup» («Биллинг Настройка»)
class BillingSetup(TemplateModel):
    class Meta:
        db_table = 'billing_setup'
        verbose_name = _('Биллинг Настройка')
        verbose_name_plural = _('Биллинг Настройки')

    def __str__(self):
        return f'{self.code} | Услуга Серия Номеров: ' \
               f'{self.service_no_series}'

    code = models.CharField(verbose_name=_('Код'), unique=True, max_length=20)
    service_no_series = models.ForeignKey(to=NoSeriesLine,
                                          verbose_name=_('Услуга Серия Номеров'),
                                          related_name = 'noseriesline',
                                          on_delete = models.PROTECT)

