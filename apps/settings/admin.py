from django.contrib import admin
from .forms import ServiceModelAdminForm

from .models import (
    UnitOfMeasure,
    ServiceType,
    VatPostingGroup,
    Service,
    ServicePrice,
    NoSeries,
    NoSeriesLine,
    BillingSetup
)

from common.models import TemplateAdminModel

@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(TemplateAdminModel):
    list_display = [
        'code', 'description', 'okei_code'
    ]
    list_filter = [
        'code', 'description', 'okei_code'
    ]
    search_fields = ('code',)
    ordering = ('code',)


@admin.register(ServiceType)
class ServiceTypeAdmin(TemplateAdminModel):
    list_display = [
        'code', 'description',
    ]
    list_filter = [
        'code', 'description',
    ]
    search_fields = ('code',)
    ordering = ('code',)


# @admin.register(Service)
class ServiceAdmin(TemplateAdminModel):
    list_display = [
        'code', 'description', 'service_type', 'unit_of_measure',
        'vat_posting_group', 'unit_price',
    ]
    search_fields = ('code',)
    list_filter = [
        'code', 'service_type__code', 'unit_of_measure__code',
        'vat_posting_group__code', 'blocked'
    ]
    ordering = ('-created',)
    form = ServiceModelAdminForm

admin.site.register(Service, ServiceAdmin)


@admin.register(ServicePrice)
class ServicePriceAdmin(TemplateAdminModel):
    pass


@admin.register(VatPostingGroup)
class VatPostingGroup(TemplateAdminModel):
    list_display = [
        'code', 'description', 'vat', 'vatextempt'
    ]
    list_filter = [
        'code', 'description',
    ]
    search_fields = ('code',)
    ordering = ('code',)

@admin.register(NoSeries)
class NoSeriesAdmin(TemplateAdminModel):
    list_display = [
        'code', 'description',
    ]
    list_filter = [
        'code', 'description',
    ]
    search_fields = ('code',)
    ordering = ('code',)


@admin.register(NoSeriesLine)
class NoSeriesLineAdmin(TemplateAdminModel):
    list_display = [
        'series_no', 'starting_date', 'starting_no', 'ending_no',
        'last_no_used', 'last_date_used', 'blocked'
    ]
    list_filter = [
        'series_no', 'starting_date', 'starting_no', 'ending_no',
        'last_no_used', 'last_date_used', 'blocked'
    ]
    search_fields = ('series_no', 'starting_no')
    ordering = ('-starting_date',)


@admin.register(BillingSetup)
class BillingSetupAdmin(TemplateAdminModel):
    raw_id_fields = ('service_no_series',)
    # related_lookup_fields = {
    #     'fk': ['service_no_series', 'starting_no'],
    # }
