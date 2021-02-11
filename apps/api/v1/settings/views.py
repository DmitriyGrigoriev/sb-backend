from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from common.viewsets import *
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import *

### «Unit of Measure» («Единица Измерения»)
class UnitOfMeasureViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureDetailSerializer
    filterset_fields = ['code', 'okei_code']

# class UnitOfMeasureDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UnitOfMeasure.unit_of_measure.all()
#     serializer_class = UnitOfMeasureListSerializer


### «Service Type» («Тип Услуги»)
class ServiceTypeModelViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer


### «VAT Posting Group» («НДС  Учетная Группа»)
class VatPostingGroupModelViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    queryset = VatPostingGroup.vat_posting_group.all()
    serializer_class = VatPostingGroupSerializer


### «Service» («Услуга, цена»)
class BillingSetupModelViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    queryset = BillingSetup.billind_setup.get_series_no_setup()
    serializer_class = BillingSetupSerializer

    serializer_classes = {
        'create': BillingSetupSerializer,
        'update': BillingSetupSerializer,
    }


### «Service» («Услуга, цена»)
class ServiceModelViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    queryset = Service.sevice_manager.all()
    serializer_class = ServiceListSerializer

    serializer_classes = {
        'create': ServiceCreateSerializer,
        'update': ServiceCreateSerializer,
    }

### «Service Price» («Услуга, цена»)
class ServicePriceList(generics.ListAPIView):
    queryset = ServicePrice.objects.all()
    serializer_class = ServicePriceListSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description=_("«No. Series» («Серия Номеров») код серий номеров"),
    operation_summary=_("Код серий номеров (список)"),
    responses={status.HTTP_200_OK: openapi.Response(_('Код серии номеров'), NoSeriesListSerializer)}
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description=_('«No. Series» («Серия Номеров») редактировать код серий номеров'),
    operation_summary=_('Изменение кода серийного номера по id'),
    responses={status.HTTP_200_OK: openapi.Response(_('Измененный код серии номеров'), NoSeriesCreateSerializer)}
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description=_('«No. Series» («Серия Номеров») создать новый код серии номеров'),
    operation_summary=_('Создать новый код серии номеров'),
    responses={status.HTTP_201_CREATED: openapi.Response(_('Новый код серии номеров'), NoSeriesCreateSerializer)}
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description=_('«No. Series» («Серия Номеров») код серии номеров'),
    operation_summary=_('Получить код серии номеров по id:'),
    responses={status.HTTP_200_OK: openapi.Response(_('Код серии номеров'), NoSeriesListSerializer)}
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description=_('«No. Series» («Серия Номеров») удаление кода серии номеров'),
    operation_summary=_('Удаление кода серии номеров по id:'),
    responses={status.HTTP_204_NO_CONTENT: openapi.Response(_('Код серии номеров для удаления'), NoSeriesListSerializer)}
))
class NoSeriesViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    queryset = NoSeries.no_series.all()
    serializer_class = NoSeriesListSerializer
    serializer_classes = {
        'create': NoSeriesCreateSerializer,
        'update': NoSeriesCreateSerializer,
    }


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description=_('«No. Series Line» («Серия Номеров Строка») актуальные серии номеров blocked=False'),
    operation_summary=_("Актуальные серии номеров (список)"),
    responses={status.HTTP_200_OK: openapi.Response(_('Список серий номеров'), NoSeriesLineCommonSerializer)}
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description=_('«No. Series Line» («Серия Номеров Строка») редактировать серийный номер'),
    operation_summary=_('Изменение серийного номера по его id'),
    responses={status.HTTP_200_OK: openapi.Response(_('Измененная серия номеров'), NoSeriesLineCommonSerializer)}
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description=_('«No. Series Line» («Серия Номеров Строка») создать новую серию номеров'),
    operation_summary=_('Создать новую серию номеров'),
    responses={status.HTTP_201_CREATED: openapi.Response(_('Новая серия номеров'), NoSeriesLineCommonSerializer)}
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description=_('«No. Series Line» («Серия Номеров Строка») актуальная серия номеров'),
    operation_summary=_('Получить серию номеров по id:'),
    responses={status.HTTP_200_OK: openapi.Response(_('Актуальная серия номеров'), NoSeriesLineCommonSerializer)}
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description=_('«No. Series Line» («Серия Номеров Строка») удаление серии номеров'),
    operation_summary=_('Удаление серии номеров по id:'),
    responses={status.HTTP_204_NO_CONTENT: openapi.Response(_('Серия номеров для удаления'), NoSeriesLineCommonSerializer)}
))

### https://stackoverflow.com/questions/52092805/add-swagger-description-in-comments
class NoSeriesLineViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    BLOCKED_LIST = 'blocked_list'
    BLOCKED_DETAIL = 'blocked_detail'

    queryset = NoSeriesLine.series_line.filter(blocked=False).order_by('-starting_date')
    serializer_classes = {
        'create': NoSeriesLineCreateSerializer,
        'update': NoSeriesLineCreateSerializer,
        'blocked_detail': NoSeriesLineUnblockedDetailSerializer,
    }
    serializer_class = NoSeriesLineCommonSerializer

    @swagger_auto_schema(
        operation_description=_('«No. Series Line» («Серия Номеров Строка») не актуальные серии номеров blocked=True'),
        operation_summary=_('Не актуальные серии номеров (список)'),
        responses={status.HTTP_200_OK: openapi.Response(_('Заблокированная серия номеров'), NoSeriesLineCommonSerializer)}
    )
    @action(detail=False)
    def blocked_list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description=_('«No. Series Line» («Серия Номеров Строка») не актуальный серийный номер'),
        operation_summary=_('Получить не актуальный серийный номер по id:'),
        responses={status.HTTP_200_OK: openapi.Response(_('Заблокированная серия номеров'), NoSeriesLineUnblockedDetailSerializer)}
    )
    @action(detail=False)
    def blocked_detail(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        if self.action == self.BLOCKED_LIST:
            self.queryset = self.get_blocked_queryset()
        elif self.action == self.BLOCKED_DETAIL:
            self.queryset = self.get_blocked_detail_queryset()

        return super().get_queryset()

    def get_blocked_queryset(self):
        return NoSeriesLine.series_line.filter(blocked=True)

    def get_blocked_detail_queryset(self):
        return NoSeriesLine.series_line.filter(pk=self.kwargs.get(self.lookup_field), blocked=True)