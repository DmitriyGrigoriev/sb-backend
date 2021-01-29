from typing import Optional
# from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .querysets import *
# from common.managers import CustomManager

class NoSeriesManager(models.Manager):
    def get_queryset(self):
        return NoSeriesQuerySet(self.model, using=self._db)

    def get_latest_no(self):
        return self.get_queryset().get_latest_no()

class NoSeriesLineManager(models.Manager):
    def get_queryset(self):
        return NoSeriesLineQuerySet(self.model, using=self._db)

    def get_latest_code(self, code: str, starting_date: datetime.date, blocked: bool = False) -> Optional['NoSeriesLine']:
        return self.get_queryset().get_latest_code(code, starting_date, blocked)


class ServiceManager(models.Manager):
    def get_queryset(self):
        return ServiceQuerySet(self.model, using=self._db)

    def bloked(self):
        return self.get_queryset().bloked()


# class ServiceTypeManager(models.Manager):
#     def get_queryset(self):
#         return ServiceTypeQuerySet(self.model, using=self._db)


class UnitOfMeasureManager(models.Manager):
    def get_queryset(self):
        return UnitOfMeasureQuerySet(self.model, using=self._db)

    def okei_code(self,okei_code):
        return self.get_queryset().okei_code(okei_code=okei_code)


class VatPostingGroupManager(models.Manager):
    def get_queryset(self):
        return VatPostingGroupQuerySet(self.model, using=self._db)

    def vat_extemt(self):
        return self.get_queryset().vat_extemt()
