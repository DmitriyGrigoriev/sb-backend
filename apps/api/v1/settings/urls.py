from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# «Unit of Measure» («Единица Измерения»)
unitofmeasure_list = views.UnitOfMeasureViewSet.as_view({
    'get': 'list',
})
unitofmeasure_detail = views.UnitOfMeasureViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'post': 'create',
    'putch': 'partial_update',
    'delete': 'destroy'
})
# «No. Series»
noseries_list = views.NoSeriesViewSet.as_view({
    'get': 'list',
})
noseries_detail = views.NoSeriesViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'post': 'create',
    'putch': 'partial_update',
    'delete': 'destroy'
})
# «No. Series Line»
noseriesline_list = views.NoSeriesLineViewSet.as_view({
    'get': 'list',
})
noseriesline_blocked = views.NoSeriesLineViewSet.as_view({
    'get': 'blocked_list',
})
noseriesline_unblocked = views.NoSeriesLineViewSet.as_view({
    'get': 'blocked_detail',
    'put': 'blocked_detail',
})
noseriesline_detail = views.NoSeriesLineViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'post': 'create',
    'putch': 'partial_update',
    'delete': 'destroy'
})
### end of # «No. Series Line»

urlpatterns = format_suffix_patterns([
    ### «Unit of Measure» («Единица Измерения»)
    path('unitofmeasure/', unitofmeasure_list, name='unitofmeasure_list'),
    path('unitofmeasure/<int:pk>/', unitofmeasure_detail, name='unitofmeasure_detail'),
    # «No. Series» («Серия Номеров») код серии номеров
    path('noseries/', noseries_list, name='noseries_list'),
    path('noseries/<int:pk>/', noseries_detail, name='noseries_detail'),
    # «No. Series Line» («Серия Номеров Строка») не заблокированные серии номеров
    path('noseriesline/', noseriesline_list, name='noseriesline_list'),
    path('noseriesline/<int:pk>/', noseriesline_detail, name='noseriesline_detail'),
    # «No. Series Line» («Серия Номеров Строка») заблокированные серии номеров
    path('noseriesline/blocked-list/', noseriesline_blocked, name='noseriesline_blocked'),
    path('noseriesline/<int:pk>/blocked-detail/', noseriesline_unblocked, name='noseriesline_unblocked'),
])
# urlpatterns = [
#     path('series-list/', views.NoSeriesList.as_view()),
#     path('series-line-list/', views.NoSeriesLineList.as_view()),
#     path('service-list/', views.ServiceList.as_view()),
#     path('service-type-list/', views.ServiceTypeList.as_view()),
#     path('service-price-list/', views.ServicePriceList.as_view()),
#     path('vat-posting-group-list/', views.VatPostingGroupList.as_view()),
#
# ]