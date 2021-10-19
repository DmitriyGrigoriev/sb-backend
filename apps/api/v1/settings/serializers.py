from typing import List, Any, Dict
from rest_framework import serializers
# from rest_framework.exceptions import ValidationError
from common.fields import VirtualBooleanField
from common.exceptions import FieldValidationError
from common.validators import SeriesCodeValidator
from common.mixins import SeriesCreateSerializerMixin
from common.serializers import TemplateSerializer
from django.utils.translation import ugettext_lazy as _
from apps.settings.models import *


### «Unit of Measure» («Единица Измерения»)
class UnitOfMeasureListSerializer(TemplateSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = (
            'id', 'code', 'description', 'okei_code', 'version',
        )


### «Service Type» («Тип Услуги»)
class ServiceTypeSerializer(TemplateSerializer[ServiceType]):
    class Meta:
        model = ServiceType
        fields = (
            'id', 'code', 'description', 'version',
        )


### «VAT Posting Group» («НДС  Учетная Группа»)
class VatPostingGroupSerializer(TemplateSerializer[VatPostingGroup]):
    class Meta:
        model = VatPostingGroup
        fields = (
            'id', 'code', 'description', 'vat', 'vatextempt', 'version',
        )


### «Service Price» («Услуга, цена»)
class ServicePriceSerializer(TemplateSerializer[ServicePrice]):
    price = serializers.DecimalField(max_digits=MAX_DIGITS,
                                     decimal_places=MAX_DECIMAL,
                                     coerce_to_string=False
                                     )
    service = serializers.SlugRelatedField(slug_field='id', read_only=True)
    deleted = VirtualBooleanField() # get_deleted() return default value if custom method is omit


    class Meta:
        model = ServicePrice
        fields = (
            'id', 'service', 'price', 'start_date', 'deleted', 'version',
        )

    def get_deleted(self, instance):
        """ Default value for field deleted"""
        return False


class ServicePriceCreateSerializer(ServicePriceSerializer[ServicePrice]):
    id = serializers.ReadOnlyField()
    version = serializers.ReadOnlyField()
    price = serializers.DecimalField(max_digits=MAX_DIGITS,
                                     decimal_places=MAX_DECIMAL,
                                     coerce_to_string=False
                                     )
    deleted = VirtualBooleanField()

    class Meta:
        model = ServicePrice
        fields = (
            'id', 'service', 'price', 'start_date', 'deleted', 'version',
        )
        extra_kwargs = {
            'service': {'allow_null': True, 'required': True},
        }


class ServicePriceUpdateSerializer(ServicePriceSerializer[ServicePrice]):
    # Don't set id = serializers.ReadOnlyField(), it needs for update
    id = serializers.IntegerField()
    version = serializers.ReadOnlyField()
    price = serializers.DecimalField(max_digits=MAX_DIGITS,
                                     decimal_places=MAX_DECIMAL,
                                     coerce_to_string=False
                                     )
    deleted = VirtualBooleanField()

    class Meta:
        model = ServicePrice
        fields = (
            'id', 'service', 'price', 'start_date', 'deleted', 'version',
        )


    def __init__(self, *args, **kwargs):
        super(ServicePriceUpdateSerializer, self).__init__(*args, **kwargs)
        self.fields['id'].allow_null = True
        self.fields['service'].allow_null = True


class ServiceListSerializer(TemplateSerializer[Service]):
    service_type = serializers.SlugRelatedField(slug_field='code', read_only=True)
    unit_of_measure = serializers.SlugRelatedField(slug_field='code', read_only=True)
    vat_posting_group = serializers.SlugRelatedField(slug_field='code', read_only=True)
    unit_price = serializers.DecimalField(read_only=True,
                                          max_digits=MAX_DIGITS,
                                          decimal_places=MAX_DECIMAL,
                                          )
    price_date = serializers.DateField(read_only=True)
    prices = ServicePriceSerializer(many=True)
    # prices = serializers.PrimaryKeyRelatedField(label=_('НаServiceCreateSerializerстройка цены'), read_only=True, many=True,)

    class Meta:
        model = Service
        fields = (
            'id', 'code', 'description', 'full_name', 'service_type',
            'unit_of_measure', 'vat_posting_group', 'unit_price', 'price_date',
            'external_service_code', 'prices', 'version',
        )

### «Service» («Услуга»)
class ServiceCreateSerializer(SeriesCreateSerializerMixin, TemplateSerializer[Service]):
    unit_price = serializers.ReadOnlyField()
    price_date = serializers.DateField(read_only=True)
    prices = ServicePriceCreateSerializer(many=True)

    class Meta:
        model = Service
        fields = (
            'id', 'code', 'description', 'full_name', 'service_type',
            'unit_of_measure', 'vat_posting_group', 'prices', 'unit_price', 'price_date',
            'external_service_code', 'version'
        )
        extra_kwargs = {
            'external_service_code': {'required': False},
        }
        validators = [
            SeriesCodeValidator(
                queryset=Service.service_manager.all(),
            ),
        ]

    class Store:
        prices: [ServicePrice] = []

        @classmethod
        def _store_prices_data(self, validated_data: [Service]) -> [Service]:
            self.prices = validated_data.pop('prices', [])
            return validated_data

        # @classmethod
        # def _extract_prices_data(self) -> Generator[ServicePriceRow]:
        #     for price in self.prices:
        #         yield ServicePriceRow(
        #             pk=price.id,
        #             service=price.service,
        #             price=price.price,
        #             start_date=price.start_date,
        #             deleted=price.deleted,
        #             version=price.version,
        #         )

        @classmethod
        def get_prices(self) -> [ServicePrice]:
            return self.prices

    def _get_value(self, record: Dict, field: str) -> Any:
        result = None
        if record.get(field):
            result = record[field]
        return result

    def _validate_prices(self) -> None:
        prices = self.Store.get_prices()
        if (len(prices) == 0 or prices is None):
            raise FieldValidationError(
                'prices',
                _('Таблица «Услуги» должна иметь хотя бы одну запись в таблице «Услуги, цена»'),
                code='error_create_prices'
            )

    def _validate_price_record(self, record: [ServicePrice]) -> None:
        """Validate price > 0.
            Arguments:
                record: A `ServicePrice` instance.
        """
        price = self._get_value(record, 'price')
        if (price is None or price <= 0):
            raise FieldValidationError(
                'prices',
                _(f'Значения поля «Цена» в таблице «Услуги, цена» должно быть больше 0.'),
                code='price_must_be_greater_than_0'
            )

    def _delete_prices_records(self, deleted: [ServicePrice]) -> None:
        """Delete prices which marked deleted=True
            Arguments:
                deleted: A `ServicePrice` instance which consist info for deleted.
        """
        for record in deleted:
            pk = self._get_value(record, 'pk')
            if pk:
                ServicePrice.objects.get(pk=pk).delete()
                del self.Store.prices[record['index']]

    def _remove_delete_mark(self) -> [ServicePrice]:
        prices = self.Store.get_prices()
        for i in range(len(prices)):
            del prices[i]['deleted']
        return prices


    def _update_prices(self, instance: [ServicePrice]) -> None:
        """Create,Update prices.
            Arguments:
                instance: A `ServicePrice` instance.
        """
        self._delete_prices_records(
            deleted=[{'pk': x['id'], 'index': i} for i, x in enumerate(self.Store.get_prices()) if x.get('deleted') and x['deleted']],
        )
        self._validate_prices()
        data = self._remove_delete_mark()

        for record in data:
            record['service'] = instance
            update_mode = self._get_value(record, 'id') is not None

            self._validate_price_record(record=record)

            if update_mode:
                pk = self._get_value(record, 'id')
                obj = ServicePrice.objects.get(pk=pk)
                for key, value in record.items():
                    setattr(obj, key, value)
                obj.save()

            if not update_mode:
                record['id'] = None
                obj = ServicePrice(**record)
                obj.save()

    def _store_data(self, instance: [Service]=None, validated_data: List=None, action: str='') -> [Service]:
        """Store prices data and try to perform create or update.
            Arguments:
                instance: A `Service` instance.
                validated_data: A data instance for the validate.
                action: Only consist a key `create` or `update`.
        """
        data = self.Store._store_prices_data(validated_data=validated_data)

        if action == 'create':
            instance = super(ServiceCreateSerializer, self).create(data)
            instance.save()
        if action == 'update':
            instance = super(ServiceCreateSerializer, self).update(instance, data)

        # if get SERVICE we may start to save child records
        try:
            self._update_prices(instance=instance)
        except IntegrityError as exc:
            raise ValidationError(detail=exc)

        return instance

    def create(self, validated_data: List) -> [Service] :
        return self._store_data(validated_data=validated_data, action='create')

    def update(self, instance: [Service], validated_data: List) -> [Service] :
        return self._store_data(instance=instance, validated_data=validated_data, action='update')


class ServiceUpdateSerializer(ServiceCreateSerializer[Service]):
    unit_price = serializers.ReadOnlyField()
    price_date = serializers.DateField(read_only=True)
    prices = ServicePriceUpdateSerializer(many=True)

    class Meta:
        model = Service
        fields = (
            'id', 'code', 'description', 'full_name', 'service_type',
            'unit_of_measure', 'vat_posting_group', 'prices', 'unit_price', 'price_date',
            'external_service_code', 'version'
        )
        validators = [
            SeriesCodeValidator(
                queryset=Service.service_manager.all(),
            ),
        ]


class NoSeriesSerializer(TemplateSerializer[NoSeries]):
    class Meta:
        model = NoSeries
        fields = ( 'id', 'code', 'description', 'date_order', 'version', )


### NoSeriesLine «No. Series Line» («Серия Номеров Строка»)
class NoSeriesLineCommonSerializer(TemplateSerializer[NoSeriesLine]):
    series_no = serializers.SlugRelatedField(slug_field='code', read_only=True)

    class Meta:
        model = NoSeriesLine
        fields = (
            'id', 'series_no', 'starting_date', 'starting_no',
            'ending_no', 'last_date_used', 'warning_no',
            'last_no_used', 'increment_by',
            'blocked', 'version',
        )


### NoSeriesLine «No. Series Line» («Серия Номеров Строка»)
class NoSeriesLineCreateSerializer(TemplateSerializer[NoSeriesLine]):
    class Meta:
        model = NoSeriesLine
        fields = (
            'id', 'series_no', 'starting_date', 'starting_no',
            'ending_no', 'last_date_used', 'warning_no',
            'last_no_used', 'increment_by', 'series_no',
            'blocked', 'version',
        )


class NoSeriesLineBlockedDetailSerializer(TemplateSerializer[NoSeriesLine]):
    series_no = serializers.SlugRelatedField(slug_field='code', read_only=True)
    starting_date = serializers.DateField(read_only=True)
    starting_no = serializers.CharField(read_only=True)
    ending_no = serializers.CharField(read_only=True)
    last_date_used = serializers.DateField(read_only=True)
    warning_no = serializers.CharField(read_only=True)
    last_no_used = serializers.CharField(read_only=True)
    increment_by = serializers.IntegerField(read_only=True)

    class Meta:
        model = NoSeriesLine
        fields = (
            'id', 'series_no', 'starting_date', 'starting_no',
            'ending_no', 'last_date_used', 'warning_no',
            'last_no_used', 'increment_by', 'series_no',
            'blocked', 'version',
        )


### «Billing Setup» («Биллинг Настройка»)
class NoSeriesSetupSerializer(TemplateSerializer[NoSeriesSetup]):
    class Meta:
        model = NoSeriesSetup
        fields = ( 'id', 'setup_series_no', 'version' )