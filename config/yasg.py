from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from rest_framework import status
# from drf_yasg.utils import swagger_auto_schema
# from apps.api.v1.token.serializers import (
#     TokenObtainPairResponseSerializer, TokenRefreshResponseSerializer,
# )
# from apps.api.v1.token.views import (
#     TokenObtainPairView, TokenRefreshView
# )


schema_view = get_schema_view(
   openapi.Info(
       title="Умный Биллинг",
       default_version='api v1',
       description="Test description",
       # Todo Прописать реальный e-mail
       contact=openapi.Contact(email="admin@smart-billing.ru"),
       license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# decorated_token_obtain_pair_view = (
#     swagger_auto_schema(
#         method='post',
#         responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer}
#     )(TokenObtainPairView.as_view())
# )
#
# decorated_token_refresh_view = (
#     swagger_auto_schema(
#         method='post',
#         responses={status.HTTP_200_OK: TokenRefreshResponseSerializer}
#     )(TokenRefreshView.as_view())
# )

# urlpatterns = [
#     url(
#         r"^swagger/$",decorated_token_obtain_pair_view,
#         name="schema-swagger-ui",
#     ),
#     url(
#         r"^swagger-refresh/$",decorated_token_refresh_view,
#         name="schema-swagger-refresh-ui",
#     ),
# ]

urlpatterns = [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]