import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..services.settings.exceptions import ParameterValueError


class BillingSetupQuerySet(models.QuerySet):
    def get_series_no_setup(self):
        return self.model.objects.latest('service_no_series')


class NoSeriesQuerySet(models.QuerySet):
    def get_latest_no(self):
        return self.model.objects.all().earlylatest('date_order')


class NoSeriesLineQuerySet(models.QuerySet):
    def get_series_no_id_from_code(self, code: str) -> int:
        try:
            series_no_id: int = self.model.objects.filter(series_no_id__code=code)[0].series_no.id
        except:
            series_no_id: int = -1
        return series_no_id

    def get_latest_code(self, series_no: int, starting_date: datetime.date, blocked: bool = False):
        # series_no_id:int  = self.get_series_no_id_from_code(code)
        # if series_no_id < 0:
        #     raise ParameterValueError(_(f'Не настроена Серия Номеров {code} на дату {starting_date}'))

        return self.model.objects.filter(
            series_no_id=series_no,
            starting_date__lte=starting_date,
            blocked=blocked
        ).latest('starting_date')


class ServiceQuerySet(models.QuerySet):
    def bloked(self):
        return self.model.objects.filter(bloked=True)

class ServicePriceQuerySet(models.QuerySet):
    def fresh_price(self, code, unit_price):
        return self.model.objects.filter(
            code=code,
            unit_price=unit_price
        ).earlylatest('start_date')


# class ServiceTypeQuerySet(models.QuerySet):
#     def all(self):
#         return self.model.objects.all().order_by('-code')
#
#
class UnitOfMeasureQuerySet(models.QuerySet):
    def okei_code(self, okei_code):
        return self.model.objects.filter(okei_code=okei_code).order_by('-code')


class VatPostingGroupQuerySet(models.QuerySet):
    def vat_extemt(self):
        return self.model.objects.filter(vat_extemt=True).order_by('-code')
