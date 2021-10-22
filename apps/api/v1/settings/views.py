from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from common.viewsets import *
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import *


### «Unit of Measure» («Единица Измерения»)
class UnitOfMeasureViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    queryset = UnitOfMeasure.objects.all().order_by('code')
    serializer_class = UnitOfMeasureListSerializer
    # pagination_class = PaginationData
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'okei_code', 'description']
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ['code', 'okei_code']

    def validate_code(self, value):
        if len(value) > 0 :
            value = value.lower()
        return value


### «Service Type» («Тип Услуги»)
class ServiceTypeModelViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    """
    View: «Тип Услуги»
    """
    """
    Model :model:`settings.servicetype`
    """
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer


### «VAT Posting Group» («НДС  Учетная Группа»)
class VatPostingGroupModelViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    queryset = VatPostingGroup.vat_posting_group.all()
    serializer_class = VatPostingGroupSerializer


### «Service» («Услуга, цена»)
class ServiceModelViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    queryset = Service.service_manager.all()
    serializer_class = ServiceListSerializer

    serializer_classes = {
        'create': ServiceCreateSerializer,
        'update': ServiceUpdateSerializer,
        'retrieve': ServiceUpdateSerializer,
    }


### «Service Price» («Услуга, цена»)
class ServicePriceModelViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    SERVICE_LIST = 'service_list'
    SERVICE_CREATE = 'service_create'

    queryset = ServicePrice.objects.all()
    serializer_classes = {
        'service_list': ServicePriceSerializer,
    }
    serializer_class = ServicePriceSerializer

    @action(detail=False)
    def service_list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False)
    def service_create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        if self.action == self.SERVICE_LIST:
            self.queryset = self.get_service_queryset()
        elif self.action == self.SERVICE_CREATE:
            self.queryset = self.get_service_queryset()

        return super().get_queryset()

    def get_service_queryset(self):
        return ServicePrice.service_price.fresh_prices(service_pk=self.kwargs['pk'])


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description=_("«No. Series» («Серия Номеров») код серий номеров"),
    operation_summary=_("Код серий номеров (список)"),
    responses={status.HTTP_200_OK: openapi.Response(_('Код серии номеров'), NoSeriesSerializer)}
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description=_('«No. Series» («Серия Номеров») редактировать код серий номеров'),
    operation_summary=_('Изменение кода серийного номера по id'),
    responses={status.HTTP_200_OK: openapi.Response(_('Измененный код серии номеров'), NoSeriesSerializer)}
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description=_('«No. Series» («Серия Номеров») создать новый код серии номеров'),
    operation_summary=_('Создать новый код серии номеров'),
    responses={status.HTTP_201_CREATED: openapi.Response(_('Новый код серии номеров'), NoSeriesSerializer)}
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description=_('«No. Series» («Серия Номеров») код серии номеров'),
    operation_summary=_('Получить код серии номеров по id:'),
    responses={status.HTTP_200_OK: openapi.Response(_('Код серии номеров'), NoSeriesSerializer)}
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description=_('«No. Series» («Серия Номеров») удаление кода серии номеров'),
    operation_summary=_('Удаление кода серии номеров по id:'),
    responses={status.HTTP_204_NO_CONTENT: openapi.Response(_('Код серии номеров для удаления'), NoSeriesSerializer)}
))
class NoSeriesViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    queryset = NoSeries.objects.all()
    serializer_class = NoSeriesSerializer
    serializer_classes = {
        'create': NoSeriesSerializer,
        'update': NoSeriesSerializer,
    }


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description=_('«No. Series Line» («Серия Номеров Строка») актуальные серии номеров blocked=False'),
    operation_summary=_("Актуальные серии номеров (список)"),
    responses={status.HTTP_200_OK: openapi.Response(_('Список актуальных серий номеров'), NoSeriesLineCommonSerializer)}
))
@method_decorator(name='blocked_list', decorator=swagger_auto_schema(
    operation_description=_('«No. Series Line» («Серия Номеров Строка») не актуальные серии номеров blocked=True'),
    operation_summary=_("Заблокированные Серии Номеров (список)"),
    responses={status.HTTP_200_OK: openapi.Response(_('Список заблокированных серий номеров'), NoSeriesLineCommonSerializer)}
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description=_('«No. Series Line» («Серия Номеров Строка») редактировать серийный номер'),
    operation_summary=_('Изменение серийного номера по его ID'),
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
    operation_summary=_('Удаление серии номеров по ID:'),
    responses={status.HTTP_204_NO_CONTENT: openapi.Response(_('Серия номеров для удаления'), NoSeriesLineCommonSerializer)}
))


### https://stackoverflow.com/questions/52092805/add-swagger-description-in-comments
class NoSeriesLineViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    BLOCKED_LIST = 'blocked_list'
    BLOCKED_UPDATE = 'blocked_update'
    BLOCKED_RETRIEVE = 'blocked_retrieve'
    BLOCKED_DESTROY = 'blocked_destroy'

    queryset = NoSeriesLine.series_line.filter(blocked=False).order_by('-starting_date')
    serializer_classes = {
        'create': NoSeriesLineCreateSerializer,
        'update': NoSeriesLineCreateSerializer,
        'blocked_update': NoSeriesLineCreateSerializer,
        'blocked_retrieve': NoSeriesLineCreateSerializer,
        'blocked_destroy': NoSeriesLineCreateSerializer,
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
        operation_summary=_('Обновить заблокированный Серийный Номер по его ID:'),
        responses={status.HTTP_200_OK: openapi.Response(_('Заблокированная серия номеров'), NoSeriesLineBlockedDetailSerializer)}
    )
    @action(detail=False)
    def blocked_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=_('«No. Series Line» («Серия Номеров Строка») не актуальный серийный номер'),
        operation_summary=_('Получить заблокированный Серийный Номер по его ID:'),
        responses={status.HTTP_200_OK: openapi.Response(_('Заблокированная серия номеров'), NoSeriesLineBlockedDetailSerializer)}
    )
    @action(detail=False)
    def blocked_retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=_('«No. Series Line» («Серия Номеров Строка») не актуальный серийный номер'),
        operation_summary=_('Удалить заблокированный Серийный Номер по его ID:'),
        responses={status.HTTP_200_OK: openapi.Response(_('Заблокированная серия номеров'), NoSeriesLineBlockedDetailSerializer)}
    )
    @action(detail=False)
    def blocked_destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


    def get_queryset(self):
        if self.action == self.BLOCKED_LIST:
            self.queryset = self.get_blocked_queryset()
        elif self.action == self.BLOCKED_RETRIEVE:
            self.queryset = self.get_blocked_retrieve_queryset()
        elif self.action == self.BLOCKED_UPDATE:
            self.queryset = self.get_blocked_retrieve_queryset()
        elif self.action == self.BLOCKED_DESTROY:
            self.queryset = self.get_blocked_retrieve_queryset()

        return super().get_queryset()

    def get_blocked_queryset(self):
        return NoSeriesLine.series_line.filter(blocked=True).order_by('-starting_date')

    def get_blocked_retrieve_queryset(self):
        return NoSeriesLine.series_line.filter(pk=self.kwargs.get(self.lookup_field), blocked=True)


### Setup «NoSeriesSetup» («Настройка Биллинга»)
class NoSeriesSetupModelViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    # queryset = NoSeriesSetup.objects.none()
    serializer_class = NoSeriesSetupSerializer

    serializer_classes = {
        'create': NoSeriesSetupSerializer,
        'update': NoSeriesSetupSerializer,
    }
    def get_queryset(self):
        queryset = NoSeriesSetup.objects.none()
        if self.action == 'retrieve':
            queryset = self.retrieve_queryset()
        elif self.action == 'update':
            queryset = self.update_queryset()
        elif self.action == 'create':
            queryset = self.create_queryset()
        return queryset

    def retrieve_queryset(self):
        count = NoSeriesSetup.objects.count()
        pk = 0
        if count != 0:
            pk = NoSeriesSetup.objects.first().pk

        self.kwargs.update({'pk': pk})
        queryset = NoSeriesSetup.objects.filter(pk=pk)

        return queryset

    def update_queryset(self):
        return NoSeriesSetup.objects.all()

    def create_queryset(self):
        return NoSeriesSetup.objects.all()
