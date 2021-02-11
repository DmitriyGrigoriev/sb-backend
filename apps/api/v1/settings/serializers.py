from rest_framework import serializers
from apps.settings.models import *
from common.validators import SeriesCodeValidator
from common.mixins import SeriesCreateSerializerMixin


### «Unit of Measure» («Единица Измерения»)
class UnitOfMeasureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = (
            '__all__',
        )

class UnitOfMeasureDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = (
            'code', 'description', 'okei_code',
        )


### «Service Type» («Тип Услуги»)
class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = (
            'id', 'code', 'description',
        )


### «VAT Posting Group» («НДС  Учетная Группа»)
class VatPostingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = VatPostingGroup
        fields = (
            'id', 'code', 'description', 'vat', 'vatextempt',
        )


### «Billing Setup» («Биллинг Настройка»)
class BillingSetupSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    service_no_series = serializers.SlugRelatedField(slug_field='code', read_only=True)

    class Meta:
        model = Service
        fields = (
            'id', 'code', 'service_no_series',
        )


### «Service» («Услуга»)
class ServiceListSerializer(serializers.ModelSerializer):
    service_type = serializers.SlugRelatedField(slug_field='code', read_only=True)
    unit_of_measure = serializers.SlugRelatedField(slug_field='code', read_only=True)
    vat_posting_group = serializers.SlugRelatedField(slug_field='vat', read_only=True)

    class Meta:
        model = Service
        fields = (
            'id', 'code', 'description', 'full_name', 'service_type',
            'unit_of_measure', 'vat_posting_group', 'unit_price',
            'external_service_code',
        )

### «Service» («Услуга»)
class ServiceCreateSerializer(SeriesCreateSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'id', 'code', 'description', 'full_name', 'service_type',
            'unit_of_measure', 'vat_posting_group', 'unit_price',
            'external_service_code',
        )
        validators = [
            SeriesCodeValidator(
                queryset=Service.sevice_manager.all(),
            )
        ]

### «Service Price» («Услуга, цена»)
class ServicePriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePrice
        fields = (
            'id', 'service_code', 'unit_price', 'start_date',
        )


### NoSeries «No. Series» («Серия Номеров»)
class NoSeriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoSeries
        fields = ( 'id', 'code', 'description', 'date_order', )

### NoSeries «No. Series» («Серия Номеров»)
class NoSeriesCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = NoSeries
        fields = ( 'id', 'code', 'description', 'date_order', )


### NoSeriesLine «No. Series Line» («Серия Номеров Строка»)
class NoSeriesLineCommonSerializer(serializers.ModelSerializer):
    series_no = serializers.SlugRelatedField(slug_field='code', read_only=True)
    class Meta:
        model = NoSeriesLine
        fields = (
            'id', 'starting_date', 'starting_no',
            'ending_no', 'last_date_used', 'warning_no',
            'last_no_used', 'increment_by', 'series_no',
            'blocked',
        )

### NoSeriesLine «No. Series Line» («Серия Номеров Строка»)
class NoSeriesLineCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = NoSeriesLine
        fields = (
            'id','starting_date', 'starting_no',
            'ending_no', 'last_date_used', 'warning_no',
            'last_no_used', 'increment_by', 'series_no',
            'blocked',
        )


class NoSeriesLineUnblockedDetailSerializer(serializers.ModelSerializer):
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
            'id', 'starting_date', 'starting_no',
            'ending_no', 'last_date_used', 'warning_no',
            'last_no_used', 'increment_by', 'series_no',
            'blocked',
        )


### «Billing Setup» («Биллинг Настройка»)
class BillingSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingSetup
        fields = ( 'id', 'code', 'service_no_series',)
        read_only_fields = ('code',)
