import datetime
from django.db import models
from django.db.models import Case, When, Value, IntegerField


class NoSeriesQuerySet(models.QuerySet):
    def get_latest_no(self):
        return self.model.objects.all().earliest('date_order')


class NoSeriesLineQuerySet(models.QuerySet):
    def get_series_no_id_from_code(self, code: str) -> int:
        try:
            series_no_id: int = self.model.objects.filter(series_no_id__code=code)[0].series_no.id
        except:
            series_no_id: int = -1
        return series_no_id


    def get_latest_code(self, series_no: int, starting_date: datetime.date, blocked: bool = False):
        return self.model.objects.filter(
            series_no_id=series_no,
            starting_date__lte=starting_date,
            blocked=blocked
        ).latest('starting_date')


class ServiceQuerySet(models.QuerySet):
    def bloked(self):
        return self.model.objects.filter(bloked=True)

class ServicePriceQuerySet(models.QuerySet):
    # https://stackoverflow.com/questions/33162688/django-queryset-place-of-none-null-in-orderby-in-postgresql
    def fresh_prices(self, service_pk: int):
        return self.model.objects.filter(service=service_pk) \
            .annotate(
            nulls_last=Case(
                When(start_date__isnull=True, then=Value(1)),
                When(start_date__isnull=False, then=Value(0)),
                output_field=IntegerField()
            )
        ).order_by('nulls_last', '-start_date')


class UnitOfMeasureQuerySet(models.QuerySet):
    def okei_code(self, okei_code):
        return self.model.objects.filter(okei_code=okei_code).order_by('-code')


class VatPostingGroupQuerySet(models.QuerySet):
    def vat_extemt(self):
        return self.model.objects.filter(vat_extemt=True).order_by('-code')