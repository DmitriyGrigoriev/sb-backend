from djoser.views import UserViewSet
from rest_framework import viewsets, permissions
from rest_framework import filters
from common.mixins import MixedPermission
from common.viewsets import *
from .serializers import *
# from .token import rest_authtoken_generator

class UserViewSet(UserViewSet):
    filter_backends = [filters.SearchFilter]
    # search_fields = ['nickname', 'first_name', 'middle_name', 'last_name', 'email', 'groups__name']
    # Add support rest_framework.authtoken.models.Token
    # token_generator = rest_authtoken_generator

    # def perform_create(self, serializer):
    #     super(UserViewSet, self).perform_create(serializer)
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = UserFilter
    # pagination_class = PaginationData

# Todo: The best decision may to disable this feature in future
### «Role» («Роли»)
class RoleModelViewSet(AtomicModelViewSet, MixedPermission, viewsets.ModelViewSet):
    """Создание, удаление или изменение справочника GROUP (роли)"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    serializer_classes = {
        'create': RoleCreateSerializer,
        'update': RoleCreateSerializer,
    }
    pagination_class = None
    """Only Django admin users can update or destroy record in GROUP model"""
    permission_classes = [permissions.IsAuthenticated,]
    permission_classes_by_action = {'get': [permissions.IsAuthenticated],
                                    'update': [permissions.IsAdminUser],
                                    'destroy': [permissions.IsAdminUser]}

    class Meta:
        model = Group
        fields = ('id', 'name',)


### «User Role» («Пользователи роли»)
class UserRoleModelViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRoleListSerializer
    serializer_classes = {
        'update': UserRoleUpdateSerializer,
    }

    class Meta:
        model = User
        fields = ('id', 'groups__id',)


# class ResetPasswordViewSet(AtomicModelViewSet, viewsets.ModelViewSet):
#     class Meta:
#         model = User
#         fields = ('id', 'nickname', 'first_name', 'middle_name', 'last_name', 'email', 'groups__name',)
