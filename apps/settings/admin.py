from django.contrib import admin
from .forms import ServiceModelAdminForm, ServicePriceModelAdminForm

from .models import (
    UnitOfMeasure,
    ServiceType,
    VatPostingGroup,
    Service,
    ServicePrice,
    NoSeries,
    NoSeriesLine,
    NoSeriesSetup
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


@admin.register(Service)
class ServiceAdmin(TemplateAdminModel):
    ordering = ('-created',)
    readonly_fields = ('unit_price', 'price_date')
    search_fields = ('code',)
    list_filter = [
        'code', 'description',
    ]
    form = ServiceModelAdminForm

    class ServicePriceAdmin(admin.TabularInline):
        model = ServicePrice
        ordering = ['start_date']
        max_num = 2
        # min_num = 1
        # extra = 1
        formset = ServicePriceModelAdminForm
    inlines = [ServicePriceAdmin,]


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


@admin.register(NoSeriesSetup)
class NoSeriesSetupAdmin(TemplateAdminModel):
    # This code's gets from:
    # https://newbedev.com/limit-a-single-record-in-model-for-django-app
    raw_id_fields = ('setup_series_no',)
    # Restrict add more than 1 record
    def has_add_permission(self, request):
        base_add_permission = super(NoSeriesSetupAdmin, self).has_add_permission(request)
        if base_add_permission:
            # if there's already an entry, do not allow adding
            count = NoSeriesSetup.objects.all().count()
            if count == 0:
                return True
        return False
