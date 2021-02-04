from django.utils.decorators import method_decorator
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import *
# from apps.settings.models import UnitOfMeasure
# from django.shortcuts import get_object_or_404
# from rest_framework.response import Response


### «Unit of Measure» («Единица Измерения»)
class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureDetailSerializer
    filterset_fields = ['code', 'okei_code']

# class UnitOfMeasureDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UnitOfMeasure.unit_of_measure.all()
#     serializer_class = UnitOfMeasureListSerializer


### «Service Type» («Тип Услуги»)
class ServiceTypeList(generics.ListAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeListSerializer


### «VAT Posting Group» («НДС  Учетная Группа»)
class VatPostingGroupList(generics.ListAPIView):
    queryset = VatPostingGroup.vat_posting_group.all()
    serializer_class = VatPostingGroupListSerializer


### «Service» («Услуга, цена»)
class ServiceList(generics.ListAPIView):
    queryset = Service.sevice.all()
    serializer_class = ServiceListSerializer


### «Service Price» («Услуга, цена»)
class ServicePriceList(generics.ListAPIView):
    queryset = ServicePrice.objects.all()
    serializer_class = ServicePriceListSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="«No. Series» («Серия Номеров») код серий номеров",
    operation_summary="Код серий номеров (список)",
    responses={'200': 'Код серий номеров'}
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="«No. Series» («Серия Номеров») редактировать код серий номеров",
    operation_summary="Изменение кода серийного номера по id",
    responses={'200': 'Код серийного номера изменен'}
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="«No. Series» («Серия Номеров») создать новый код серии номеров",
    operation_summary="Создать новый код серии номеров",
    responses={'200': 'создан новый код серии номеров'}
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="«No. Series» («Серия Номеров») код серии номеров",
    operation_summary="Получить код серии номеров по id:",
    responses={'200': 'код серии номеров'}
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="«No. Series» («Серия Номеров») удаление кода серии номеров",
    operation_summary="Удаление кода серии номеров по id:",
    responses={'200': 'код серии номеров удален'}
))
### NoSeries «No. Series» («Серия Номеров»)
class NoSeriesViewSet(viewsets.ModelViewSet):
    queryset = NoSeries.no_series.all()
    serializer_class = NoSeriesListSerializer
    serializer_classes = {
        'create': NoSeriesCreateSerializer,
        'update': NoSeriesCreateSerializer,
    }


# @method_decorator(name='list', decorator=swagger_auto_schema(
#     operation_description="Заблокированные серии номеров",
#     operation_id="Method1asdas ID",
#     operation_summary="Заблокированные серии номеров",
#     manual_parameters=[
#         openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='Первичный ключ')
#     ],
#     responses={'200': 'Response description'}
# ))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="«No. Series Line» («Серия Номеров Строка») актуальные серии номеров blocked=False",
    operation_summary="Актуальные серии номеров (список)",
    responses={'200': 'коллекция актуальных серий номеров'}
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="«No. Series Line» («Серия Номеров Строка») редактировать серийный номер",
    operation_summary="Изменение серийного номера по его id",
    responses={'200': 'Cерийный номер изменен'}
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="«No. Series Line» («Серия Номеров Строка») создать новую серию номеров",
    operation_summary="Создать новую серию номеров",
    responses={'200': 'создана новая серия номеров'}
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="«No. Series Line» («Серия Номеров Строка») актуальная серия номеров",
    operation_summary="Получить серию номеров по id:",
    responses={'200': 'актуальная серия номеров'}
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="«No. Series Line» («Серия Номеров Строка») удаление серии номеров",
    operation_summary="Удаление серии номеров по id:",
    responses={'200': 'серия номеров удалена'}
))
### https://stackoverflow.com/questions/52092805/add-swagger-description-in-comments
class NoSeriesLineViewSet(viewsets.ModelViewSet):
    BLOCKED_LIST = 'blocked_list'
    BLOCKED_DETAIL = 'blocked_detail'

    queryset = NoSeriesLine.series_line.filter(blocked=False).order_by('-starting_date')
    serializer_classes = {
        'create': NoSeriesLineCreateSerializer,
        'update': NoSeriesLineCreateSerializer,
        'blocked_detail': NoSeriesUnblockedDetailSerializer,
    }
    serializer_class = NoSeriesLineListSerializer

    @swagger_auto_schema(
        operation_description="«No. Series Line» («Серия Номеров Строка») не актуальные серии номеров blocked=True",
        operation_summary="Не актуальные серии номеров (список)",
        responses={'200': 'коллекция не актуальных серий номеров'}
    )
    @action(detail=False)
    def blocked_list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="«No. Series Line» («Серия Номеров Строка») не актуальный серийный номер",
        operation_summary="Получить не актуальный серийный номер по его id:",
        responses={'200': 'не актуальный серийный номер'}
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

    def get_serializer_class(self):
        if self.serializer_classes.get(self.action):
            serializer = self.serializer_classes.get(self.action)
        else:
            serializer = self.serializer_class

        return serializer