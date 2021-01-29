from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth import logout
#from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from config.api import api

# from apps.transportconf.views import TokenObtainPairView

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls, name='admin'),
    path('logout/', logout, {'next_page': '/'}, name='logout'),

    #path to djoser end points
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # path('api/auth/', include('djoser.urls.authtoken')),
    # path('api/token/', TokenObtainPairView.as_view()),
    # path('api/token-refresh/', TokenRefreshView.as_view()),

    # path('api/', include(api.urls)),
    # path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/config/', include('apps.transportconf.urls')),

]