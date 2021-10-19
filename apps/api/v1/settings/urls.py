from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# «Billing Setup» («Биллинг Настройка»)
noseries_setup = views.NoSeriesSetupModelViewSet.as_view({
    'get': 'retrieve',
    # 'get': 'list',
    'post': 'create',
})
noseries_setup_detail = views.NoSeriesSetupModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'putch': 'partial_update',
})
# «VAT Posting Group» («НДС  Учетная Группа»)
vatposting_group_list = views.VatPostingGroupModelViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
vatposting_group_detail = views.VatPostingGroupModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'putch': 'partial_update',
    'delete': 'destroy'
})

# «Service Type» («Тип Услуги»)
servicetype_list = views.ServiceTypeModelViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
servicetype_detail = views.ServiceTypeModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'putch': 'partial_update',
    'delete': 'destroy'
})
# «Service» («Услуга»)
service_list = views.ServiceModelViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
service_detail = views.ServiceModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'putch': 'partial_update',
    'delete': 'destroy'
})
# «Service Price» («Услуга цена»)
service_price_list = views.ServicePriceModelViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
service_price_detail = views.ServicePriceModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'putch': 'partial_update',
    'delete': 'destroy'
})
service_price_by_service_list = views.ServicePriceModelViewSet.as_view({
    'get': 'service_list',
    'post': 'service_create',
})
# «Unit of Measure» («Единица Измерения»)
unitofmeasure_list = views.UnitOfMeasureViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
unitofmeasure_detail = views.UnitOfMeasureViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'putch': 'partial_update',
    'delete': 'destroy'
})
# «No. Series»
noseries_list = views.NoSeriesViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
noseries_detail = views.NoSeriesViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'putch': 'partial_update',
    'delete': 'destroy'
})
# «No. Series Line»
noseriesline_list = views.NoSeriesLineViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
noseriesline_detail = views.NoSeriesLineViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'putch': 'partial_update',
    'delete': 'destroy'
})
noseriesline_blocked_list = views.NoSeriesLineViewSet.as_view({
    'get': 'blocked_list',
})
noseriesline_blocked_detail = views.NoSeriesLineViewSet.as_view({
    'get': 'blocked_retrieve',
    'put': 'blocked_update',
    'delete': 'blocked_destroy'
})

# noseriesline_blocked_detail = views.NoSeriesLineViewSet.as_view({
#     'get': 'blocked_detail',
#     'put': 'blocked_detail',
#     'delete': 'blocked_detail'
# })
### end of # «No. Series Line»

urlpatterns = format_suffix_patterns([
    # «NoSeries Setup» («Биллинг Настройка»)
    path('setup/', noseries_setup, name='noseries_setup'),
    path('setup/<int:pk>/', noseries_setup_detail, name='noseries_detail'),
    # «No. Series» («Серия Номеров») код серии номеров
    path('service/', service_list, name='service_list'),
    path('service/<int:pk>/', service_detail, name='service_detail'),
    # «Service Price» («Услуга, цена»)
    path('serviceprice/', service_price_list, name='service_price_list'),
    path('serviceprice/<int:pk>/', service_price_detail, name='service_price_detail'),
    # «Service Price» («Услуга, цена») фильт по service_id
    path('serviceprice/<int:pk>/service', service_price_by_service_list, name='service_price_by_service_list'),
    # «Service Type» («Тип Услуги»)
    path('servicetype/', servicetype_list, name='servicetype_list'),
    path('servicetype/<int:pk>/', servicetype_detail, name='servicetype_detail'),
    # «No. Series» («Серия Номеров») код серии номеров
    path('noseries/', noseries_list, name='noseries_list'),
    path('noseries/<int:pk>/', noseries_detail, name='noseries_detail'),
    # «No. Series Line» («Серия Номеров Строка») не заблокированные серии номеров
    path('noseriesline/', noseriesline_list, name='noseriesline_list'),
    path('noseriesline/<int:pk>/', noseriesline_detail, name='noseriesline_detail'),
    # «No. Series Line» («Серия Номеров Строка») заблокированные серии номеров
    path('noseriesline/blocked/', noseriesline_blocked_list, name='noseriesline_blocked_list'),
    path('noseriesline/blocked/<int:pk>/', noseriesline_blocked_detail, name='noseriesline_blocked_detail'),
    # path('noseriesline/blocked/<int:pk>/', noseriesline_blocked_detail, name='noseriesline_blocked_detail'),
    ### «Unit of Measure» («Единица Измерения»)
    path('unitofmeasure/', unitofmeasure_list, name='unitofmeasure_list'),
    path('unitofmeasure/<int:pk>/', unitofmeasure_detail, name='unitofmeasure_detail'),
    ### «VAT Posting Group» («НДС  Учетная Группа»)
    path('vat/', vatposting_group_list, name='vatposting_group_list'),
    path('vat/<int:pk>/', vatposting_group_detail, name='vatposting_group_detail'),
])
