from django.db import models
from common.models import TemplateModel
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ErrorDetail, ValidationError
from django.db import IntegrityError, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from common.constants import (
    MAX_DIGITS,
    MAX_DECIMAL,
)

from .managers import (
    VatPostingGroupManager,
    UnitOfMeasureManager,
    ServiceManager,
    ServicePriceManager,
    # NoSeriesManager,
    NoSeriesLineManager,
)


# «Unit of Measure» («Единица Измерения»)
class UnitOfMeasure(TemplateModel):
    class Meta:
        db_table = 'unit_of_measure'
        ordering = ['code']
        verbose_name = _('Единица Измерения')
        verbose_name_plural = _('Единицы Измерения')

    def __str__(self):
        return f'{self.code}'

    code = models.CharField(verbose_name=_('Код Ед. Измерения'), unique=True, max_length=20)
    description = models.CharField(verbose_name=_('Описание'), max_length=50)
    okei_code = models.CharField(verbose_name=_('Код ОКЕИ'), max_length=3, blank=True, default='')
    objects = models.Manager() # default manager
    unit_of_measure = UnitOfMeasureManager()


class ServiceType(TemplateModel):
    """«Service Type» («Тип Услуги»)"""
    class Meta:
        db_table = 'service_type'
        verbose_name = _('Тип Услуги')
        verbose_name_plural = _('Тип Услуг')

    def __str__(self):
        return f'{self.code}'

    code = models.CharField(verbose_name=_('Код Типа Услуг'), max_length=20)
    description = models.CharField(verbose_name=_('Описание услуги'),
                                   max_length=50,
                                   blank=False,
                                   error_messages={'requared': _('Необходимо заполнить описание услуги')}
                                   )
    objects = models.Manager() # default manager


class VatPostingGroup(TemplateModel):
    """«VAT Posting Group» («НДС  Учетная Группа»)"""
    class Meta:
        db_table = 'vat_posting_group'
        ordering = ['code']
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


class NoSeries(TemplateModel):
    """«No. Series» («Серия Номеров»), списочная (только чтение) + карточная формы"""
    class Meta:
        db_table = 'no_series'
        ordering = ['code']
        verbose_name = _('Серия Номеров')
        verbose_name_plural = _('Серии Номеров')

    def __str__(self):
        return f'{self.code}'

    code = models.CharField(verbose_name=_('Код'), unique=True, max_length=20)
    description = models.CharField(verbose_name=_('Описание'), max_length=100)
    date_order = models.BooleanField(verbose_name=_('Порядок Дат'), default=False)

    objects = models.Manager() # default manager
    # no_series = NoSeriesManager()


class NoSeriesLine(TemplateModel):
    """«No. Series Line» («Серия Номеров Строка»), списочная субформа (поле Код не отображаем)"""
    class Meta:
        db_table = 'no_series_line'
        unique_together = ['series_no', 'starting_date']
        ordering = ['-starting_date']
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
    starting_no = models.CharField(verbose_name=_('Начальный Но'), max_length=20, blank=False)
    ending_no = models.CharField(verbose_name=_('Конечный Но'), max_length=20)
    last_date_used = models.DateField(verbose_name=_('Посл.Исп. Дата'),
                                      blank=True, null=True,)
    warning_no = models.CharField(verbose_name=_('Предупредительный Но'),
                                  default='', blank=True, max_length=20)
    last_no_used = models.CharField(verbose_name=_('Посл.Исп. Но'),
                                    default='', blank=True, max_length=20,)
    increment_by = models.PositiveIntegerField(verbose_name=_('Увеличивать На'), default=1)
    blocked = models.BooleanField(verbose_name=_('Заблокирована'), default=False)
    # Below have a list of common and specific managers
    objects = models.Manager() # default manager
    series_line = NoSeriesLineManager()


class NoSeriesSetup(TemplateModel):
    """«No Series Setup» («Биллинг Настройка»)"""
    class Meta:
        db_table = 'noseries_setup'
        verbose_name = _('Настройка Серии Номеров')
        verbose_name_plural = _('Настройка Серии Номеров')

    def __str__(self):
        return f'Серия Номеров: {self.setup_series_no}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if NoSeriesSetup.objects.count() <= 1:
            super().save(force_insert=False, force_update=False, using=None,
                         update_fields=None)
        else:
            errors = [
                ErrorDetail(_('Вы не можете сохранить в "Настройка Серии Номеров" более чем одну «Серию Номеров»'),
                            code='error_non_unique_series')
            ]
            raise ValidationError({ 'prices': errors })
            # raise ValidationError(_('Вы не можете сохранить в "Настройка Серии Номеров" более чем одну «Серию Номеров»'))

    setup_series_no = models.ForeignKey(to=NoSeries,
                                          verbose_name=_('Серия Номеров Строка'),
                                          related_name = 'setup_series_no',
                                          blank=False,
                                          on_delete = models.PROTECT)

    objects = models.Manager() # default manager
    # noseries_setup = NoSeriesSetupManager()


class Service(TemplateModel):
    """«Service» («Услуга»)"""
    class Meta:
        db_table = 'service'
        ordering = ['-code']
        verbose_name = _('Услуга и цена')
        verbose_name_plural = _('Услуги и цены')

    def __str__(self):
        return f'Код: {self.code} : Услуга: {self.description} : Цена: {self.unit_price}'

    code = models.CharField(verbose_name=_('Код Услуги'),
                            unique=True,
                            max_length=20,
                            blank=True,
                            default=''
                            )
    description = models.CharField(verbose_name=_('Краткое описание'),
                                   max_length=50,
                                   blank=False,
                                   error_messages={'requared': _('Необходимо заполнить описание услуги')}
                                   )
    full_name = models.CharField(verbose_name=_('Полное наименование'),
                                 max_length=1000,
                                 blank=True,
                                 default=''
                                 )
    unit_price = models.DecimalField(verbose_name=_('Цена Единицы'),
                                     max_digits=MAX_DIGITS,
                                     decimal_places=MAX_DECIMAL,
                                     default=0,
                                     blank=False,
                                     error_messages={'requared': _('Необходимо указать цену услуги')}
                                     )
    price_date = models.DateField(verbose_name=_('Дата начала'),
                                  unique=False, null=True, blank=True,
                                  auto_now_add=False
                                  )
    service_type = models.ForeignKey(to=ServiceType, verbose_name=_('Тип Услуги'),
                                     on_delete=models.PROTECT,
                                     related_name='service_types',
                                     blank=False,
                                     error_messages={'requared': _('Необходимо указать тип услуги')}
                                     )
    unit_of_measure = models.ForeignKey(to=UnitOfMeasure, verbose_name=_('Единица Измерения'),
                                        on_delete=models.PROTECT,
                                        related_name='measures',
                                        blank=False,
                                        error_messages={'requared': _('Необходимо указать еденицу измерения')}
                                        )
    vat_posting_group = models.ForeignKey(to=VatPostingGroup, verbose_name=_('НДС Учетная Группа'),
                                          on_delete=models.PROTECT,
                                          related_name='vat_groups',
                                          blank=False,
                                          error_messages={'requared': _('Необходимо указать учетную группу')}
                                          )
    external_service_code = models.CharField(verbose_name=_('Внешний Код Услуги'),
                                                            blank=True,
                                                            default='',
                                                            max_length=50
                                             )
    blocked = models.BooleanField(verbose_name=_('Блокирована'), default=False)

    objects = models.Manager() # default manager
    service_manager = ServiceManager()


class ServicePrice(TemplateModel):
    """«Service Price» («Услуга, цена»)"""
    # https://stackoverflow.com/questions/4443190/djangos-manytomany-relationship-with-additional-fields
    non_unique_date_message = _('Значение полей Код услуги+Дата начала для таблицы «Цены» не уникальны.')
    class Meta:
        db_table = 'service_price'
        ordering = ['start_date']
        unique_together = ('service', 'start_date')
        verbose_name = _('Цена')
        verbose_name_plural = _('Цены')
        # Check the price should be >= '0.01' !important
        constraints = [
            models.UniqueConstraint(fields=['service', 'start_date'],
                                    name=_('unique_start_date')),
            models.CheckConstraint(check=models.Q(price__gte='0.01'),
                                   name=_('price_must_be_greater_than_0')),
        ]

    def __str__(self):
        return f'Цена: {self.price} : Дата начала: {"-" if self.start_date is None else self.start_date}'

    def validate_unique(self, exclude=None):
        # Check the unique together with nullable a date field
        # https://stackoverflow.com/questions/33307892/django-unique-together-with-nullable-foreignkey
        non_unique_date = True
        if self.start_date:
           non_unique_date = ServicePrice.objects.exclude(id=self.id).filter(
               service_id=self.service.pk, start_date=self.start_date
           ).exists()
        if self.start_date is None:
            non_unique_date = ServicePrice.objects.exclude(id=self.id).filter(
                service_id=self.service.pk, start_date__isnull=True
            ).exists()

        if non_unique_date:
            errors = [
                ErrorDetail(self.non_unique_date_message, code='error_uniquetogether')
            ]
            raise ValidationError({ 'prices': errors })
            # raise ValidationError({'prices': self.non_unique_date_message}, code='error_uniquetogether')

        super(ServicePrice, self).validate_unique(exclude=None)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.validate_unique()

        super(ServicePrice, self).save(force_insert=force_insert, force_update=force_update, using=using,
             update_fields=update_fields)

    service = models.ForeignKey(to=Service, verbose_name=_('Услуги'),
                                      related_name='prices',
                                      null=False, blank=False,
                                      on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name=_('Цена Единицы'),
                                default=0.00,
                                max_digits=MAX_DIGITS,
                                decimal_places=MAX_DECIMAL,
                                blank=False,
                                error_messages={'requared': _('Необходимо указать цену услуги')}
                                )
    start_date = models.DateField(verbose_name=_('Дата начала'),
                                  unique=False, null=True, blank=True,
                                  auto_now_add=False
                                  )

    objects = models.Manager() # default manager
    service_price = ServicePriceManager()


@transaction.atomic
def update_unit_price(instance):
    service = Service.objects.get(pk=instance.service.pk)
    # getting price on the max possible date
    service_price = ServicePrice.service_price.fresh_prices(service_pk=instance.service.pk).first()

    if (service_price.price != service.unit_price):
        service.unit_price = service_price.price
        service.price_date = service_price.start_date
        try:
            with transaction.atomic():
                # To update a subset of fields, you can use update_fields
                service.save(update_fields=['unit_price', 'price_date'])
        except IntegrityError as error:
            raise


@receiver(post_save, sender=ServicePrice, dispatch_uid='service_price_max_price')
def service_price_post_save(sender, instance, created, **kwargs):
    """Update unit_price field by max price"""

    # Sometimes you need to perform an action related to the current
    # database transaction, but only if the transaction successfully commits.
    # https://docs.djangoproject.com/en/3.2/topics/db/transactions/#django.db.transaction.on_commit
    transaction.on_commit(lambda: update_unit_price(instance))
