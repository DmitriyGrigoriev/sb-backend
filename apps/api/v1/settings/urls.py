from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# «Billing Setup» («Биллинг Настройка»)
billing_setup_list = views.BillingSetupModelViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
billing_setup_detail = views.BillingSetupModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'putch': 'partial_update',
    'delete': 'destroy'
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
    'putch': 'partial_update',
    'delete': 'destroy'
})
### end of # «No. Series Line»

urlpatterns = format_suffix_patterns([
    # «Billing Setup» («Биллинг Настройка»)
    path('setup/', billing_setup_list, name='billing_setup_list'),
    path('setup/<int:pk>/', billing_setup_detail, name='billing_setup_detail'),
    # «No. Series» («Серия Номеров») код серии номеров
    path('service/', service_list, name='service_list'),
    path('service/<int:pk>/', service_detail, name='service_detail'),
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
    path('noseriesline/blocked-list/', noseriesline_blocked, name='noseriesline_blocked'),
    path('noseriesline/<int:pk>/blocked-detail/', noseriesline_unblocked, name='noseriesline_unblocked'),
    ### «Unit of Measure» («Единица Измерения»)
    path('unitofmeasure/', unitofmeasure_list, name='unitofmeasure_list'),
    path('unitofmeasure/<int:pk>/', unitofmeasure_detail, name='unitofmeasure_detail'),
    ### «VAT Posting Group» («НДС  Учетная Группа»)
    path('vat/', vatposting_group_list, name='vatposting_group_list'),
    path('vat/<int:pk>/', vatposting_group_detail, name='vatposting_group_detail'),
])
