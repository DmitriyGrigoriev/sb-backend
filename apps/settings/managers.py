from .querysets import *


class NoSeriesLineManager(models.Manager):
    def get_queryset(self):
        return NoSeriesLineQuerySet(self.model, using=self._db)

    def get_latest_code(self, series_no: int, starting_date: datetime.date, blocked: bool = False):
        return self.get_queryset().get_latest_code(series_no, starting_date, blocked)


class ServiceManager(models.Manager):
    def get_queryset(self):
        return ServiceQuerySet(self.model, using=self._db)

    def bloked(self):
        return self.get_queryset().bloked()


class ServicePriceManager(models.Manager):
    def get_queryset(self):
        return ServicePriceQuerySet(self.model, using=self._db)

    def fresh_prices(self, service_pk):
        return self.get_queryset().fresh_prices(service_pk=service_pk)


class UnitOfMeasureManager(models.Manager):
    def get_queryset(self):
        return UnitOfMeasureQuerySet(self.model, using=self._db)

    def okei_code(self, okei_code):
        return self.get_queryset().okei_code(okei_code=okei_code)


class VatPostingGroupManager(models.Manager):
    def get_queryset(self):
        return VatPostingGroupQuerySet(self.model, using=self._db)

    def vat_extemt(self):
        return self.get_queryset().vat_extemt()
