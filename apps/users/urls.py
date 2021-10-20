from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = DefaultRouter()
router.register("users", views.UserViewSet)

# «Role»
role_list = views.RoleModelViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
role_detail = views.RoleModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'putch': 'partial_update',
    'delete': 'destroy'
})
# «User Role»
user_role = views.UserRoleModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
})

urlpatterns = format_suffix_patterns([
    # «Role» («Роли»)
    path('roles/', role_list, name='role_list'),
    path('roles/<int:pk>/', role_detail, name='role_detail'),
    # «User Role» («Пользователи роли»)
    path('user-role/<int:pk>/', user_role, name='user_role'),
])

urlpatterns += router.urls
