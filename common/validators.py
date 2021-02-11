from datetime import date
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.utils.representation import smart_repr
from rest_framework.validators import qs_exists, qs_filter
from apps.settings.models import BillingSetup, NoSeriesLine

__all__ = ['SeriesCodeValidator',]


class SeriesCodeValidator:
    message = None
    missing_message = _('Наличие поля «Код Серия Номеров» обязательно.')
    requires_context = True

    def __init__(self, queryset, field='code', date_field=None, message=None):
        self.queryset = queryset
        self.lookup: str = 'exact'
        self.series_no: str = None
        self.field: str = field
        self.field_name: str = None
        self.field_value: str = None
        self.date_field: str = date_field
        self.date_field_value: date = None
        self.fields: list = [[self.field], ]
        self.required_fields: list = [self.field]
        self.message: str = message or self.message

        if date_field is None:
            self.date_field = date.today()
        elif isinstance(date_field, date):
            self.date_field = date_field
        else:
            self.required_fields = [self.field, self.date_field]

    def enforce_required_fields(self, attrs, serializer):
        """
        The `SeriesCodeValidator` classes always force an implied
        'required' state on the fields they are applied to.
        """
        missing_items = {
            field_name: self.missing_message
            for field_name in self.required_fields
            if field_name not in attrs
        }
        if missing_items:
            raise ValidationError(missing_items, code='required')
        elif not hasattr(serializer, 'RequiredValidatorClass'):
            raise ValidationError(
                _(f'Для валидатора {self.__class__.__name__} использование миксина SeriesCreateSerializerMixin обязательно.'),
                code='required'
            )

    def filter_queryset(self, value, queryset):
        """
        Filter the queryset to all instances matching the given attribute.
        """
        filter_kwargs = {'%s__%s' % (self.field_name, self.lookup): value}
        return qs_filter(queryset, **filter_kwargs)

    def exclude_current_instance(self, attrs, queryset, instance):
        """
        If an instance is being updated, then do not include
        that instance itself as a uniqueness conflict.
        """
        if instance is not None:
            return queryset.exclude(pk=instance.pk)
        return queryset

    def __call__(self, attrs, serializer):
        # Determine the underlying model field names. These may not be the
        # same as the serializer field names if `source=<>` is set.
        self.field_name = serializer.fields[self.field].source_attrs[-1]
        self.field_value = serializer._context['request'].data[self.field]

        if self.date_field in self.required_fields:
            date_field_value = serializer._context['request'].data[self.date_field]
        else:
            date_field_value = self.date_field

        self.date_field_value = date_field_value
        self.enforce_required_fields(attrs, serializer)
        self.validate_setup()
        self.validate_field_attr(self.field_value, self.date_field_value)
        # Validate the uniqueness of the serial number was entered by user
        self.validate_unique(attrs, serializer)
        self.validate_series_order_date()


    def validate_unique(self, attrs, serializer):
        queryset = self.queryset
        queryset = self.filter_queryset(attrs, queryset)
        queryset = self.exclude_current_instance(attrs, queryset, serializer.instance)
        if qs_exists(queryset):
            message = self.message.format(date_field=self.date_field)
            raise ValidationError({
                self.field: message
            }, code='unique')

        return True

    def validate_field_attr(self, code:str, dt: date=None)  -> None:
        if not isinstance(code, str):
            raise ValidationError({
                self.field:_('«Код Серия Номеров» аргумент должнен быть строкой')
            }, code='series_no')

        if dt is None:
            dt = date.today()

        if not isinstance(dt, date):
            raise ValidationError({
                self.field: _('«Серия Номеров Дата начала» аргумент должнен быть датой')
            }, code='series_no')

    """
    https://dimag.atlassian.net/wiki/spaces/SBP/pages/405733400
    Если строка настройки не найдена (или найдена, но начальный номер = ‘’ (пусто, null)), 
    то ошибка «не настроена Серия номеров %1 на дату %2» (%1 = SeriesCode, %2 = SeriesDate)
    """
    def validate_setup(self) -> None:
        try:
            self.series_no = BillingSetup.billind_setup.get_series_no_setup().service_no_series_id
        except:
            self.series_no = None

        if self.series_no is None:
            raise ValidationError({
                self.field:_('Не настроена «Серия Номеров» в «Биллинг Настройка»'),
            }, code='series_no')

    """
    https://dimag.atlassian.net/wiki/spaces/SBP/pages/405733400
    Если в «No. Series». «Date Order» = TRUE AND «Last Date Used» <> ‘’ (пусто, null)  
    AND SeriesDate < «Last Date Used», то ошибка «Вы не можете присвоить новые номера 
    из серии номеров %1 до даты %2.» (%1 = SeriesCode, %2 = «Last Date Used»)
    """
    def validate_series_order_date(self):
        queryset = NoSeriesLine.series_line.get_latest_code(
            series_no=self.series_no, starting_date=self.date_field_value
        )
        if queryset.series_no.date_order \
                and queryset.last_date_used is not None \
                and self.date_field_value < queryset.last_date_used:
            raise ValidationError({
                self.field: _(f'Вы не можете присвоить новые номера из «Серии Номеров» {queryset.series_no.code} до даты '
                  f'{queryset.last_date_used}')
            }, code='series_no')

    def __repr__(self):
        return '<%s(queryset=%s, field=%s, date_field=%s)>' % (
            self.__class__.__name__,
            smart_repr(self.queryset),
            smart_repr(self.field),
            smart_repr(self.date_field)
        )