from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.contrib.auth import login
from django.contrib.auth import logout
from django.conf.urls.static import static
from .yasg import urlpatterns as doc_api_urls

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from apps.api.v1.token.views import (
    DecoratedTokenObtainPairView, DecoratedTokenRefreshView
)

# from config.api import api

# from apps.transportconf.views import TokenObtainPairView

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    # path('login/', login, {'next_page': '/'}, name='login'),
    # path('logout/', logout, {'next_page': '/'}, name='logout'),
    path('admin/', admin.site.urls, name='admin'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #path to djoser end points
    path('api/auth/', include('djoser.urls')),
    ### https://djoser.readthedocs.io/en/latest/authentication_backends.html
    ### Disable Token Based Authentication
    # path('api/auth/', include('djoser.urls.authtoken')),

    ### https://djoser.readthedocs.io/en/latest/jwt_endpoints.html
    ### JSON Web Token Authentication
    path('api/auth/', include('djoser.urls.jwt')),

    ### https://django-rest-framework-simplejwt.readthedocs.io
    ### https://github.com/axnsan12/drf-yasg/issues/407
    ### I don't understand why that Decorated Views needs
    # path('api/token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/', include('apps.api.v1.settings.urls'))

]
# Todo Решить позже делать ли документацию api публичной
if settings.DEBUG:
    urlpatterns += doc_api_urls
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)