from djoser.serializers import UserSerializer
from djoser.serializers import UserCreateSerializer
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.validators import UniqueValidator

User = get_user_model()
class CreateGroupSerializer(serializers.ModelSerializer):
    queryset = Group.objects.all()
    class Meta:
        # https://stackoverflow.com/questions/59885543/problem-reusing-serializers-with-django-and-drf-yasg
        ref_name = "CreateGroupSerializer"
        model = Group
        fields = ('id', 'name',)

class GroupSerializer(serializers.ModelSerializer):
    queryset = Group.objects.all()
    class Meta:
        # https://stackoverflow.com/questions/59885543/problem-reusing-serializers-with-django-and-drf-yasg
        ref_name = "GroupSerializer"
        model = Group
        fields = ('id', 'name',)


### «Role» («Роли»)
class RoleListSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
    """Список возможных ролей для пользователя"""
    queryset = Group.objects.all()
    class Meta:
        model = Group
        fields = (
            'id', 'name',
        )

### «Role» («Роли»)
class RoleCreateSerializer(serializers.ModelSerializer):
    """Добавление новой роли"""
    class Meta:
        model = Group
        fields = (
            'name',
        )
        validators=[
            UniqueValidator(
                queryset=Group.objects.all(),
                message=_("Такая роль у пользователя уже существует.")
            )
        ]


### «User Role» («Пользователи роли»)
class UserRoleListSerializer(serializers.ModelSerializer):
    """Пользователи роли"""
    role = RoleListSerializer(source='groups', many=True)
    class Meta:
        model = User
        fields = ('id', 'role',)


### «User Role» («Пользователи роли»)
class UserRoleUpdateSerializer(serializers.ModelSerializer):
    role = RoleListSerializer(source='groups', many=True)
    class Meta:
        model = User
        fields = ('id', 'role',)


class UserCreateSerializer(UserCreateSerializer):
    registered_at = serializers.DateTimeField(format='%H:%M %d.%m.%Y', read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.SerializerMethodField(read_only=True)
    short_name = serializers.SerializerMethodField(read_only=True)
    role = CreateGroupSerializer(source='groups', many=True)

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else ''
        #settings.STATIC_URL + 'images/default_avatar.png'

    def get_full_name(self, obj):
        return obj.full_name

    def get_short_name(self, obj):
        return obj.short_name

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'id',
            User.USERNAME_FIELD,
            'avatar',
            'first_name',
            'middle_name',
            'last_name',
            'short_name',
            'full_name',
            'position',
            'phone',
            'mobile',
            'is_active',
            'registered_at',
            'role'
        ]


class UserSerializer(UserSerializer):
    is_admin = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    role = GroupSerializer(source='groups', many=True)
    # permission = serializers.SerializerMethodField(read_only=True)
    #
    # def get_permission(self, obj):
    #     return []

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'avatar',
            'short_name',
            'full_name',
            'is_admin',
            'is_superuser',
            'role',
            # 'permission'
        )

        read_only_fields = tuple('email, groups')

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if instance.is_active:
            if instance.role is not None:
                for item in instance.role:
                    Group.objects.get_or_create(name=item.name)