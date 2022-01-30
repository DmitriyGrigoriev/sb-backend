from typing import Any
from djoser.serializers import UserSerializer
from djoser.serializers import UserCreateSerializer
from djoser.serializers import SendEmailResetSerializer
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ErrorDetail, ValidationError
from djoser.conf import settings

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
    nickname = serializers.CharField()
    avatar = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.SerializerMethodField(read_only=True)
    short_name = serializers.SerializerMethodField(read_only=True)
    role = CreateGroupSerializer(source='groups', many=True)
    registered_at = serializers.DateTimeField(format='%H:%M %d.%m.%Y', read_only=True)

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else ''
        #settings.STATIC_URL + 'images/default_avatar.png'

    def get_full_name(self, obj):
        return obj.full_name

    def get_short_name(self, obj):
        return obj.short_name

    class Meta(UserCreateSerializer.Meta):
        model = User
        # Don't remove fields after password (needs for manage users Quasar page)
        fields = tuple(User.REQUIRED_FIELDS) + (
            'nickname',
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            'password',
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
        )


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
            'nickname',
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


class SendEmailResetSerializer(SendEmailResetSerializer):
    """Seek user by nickname and get email address"""
    nickname = serializers.CharField(required=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        user = self.get_nickname(data=kwargs.get('data'))

        if user:
            email = getattr(user, user.EMAIL_FIELD, None)

        if not kwargs.get('data').get(user.EMAIL_FIELD):
            kwargs['data'][user.EMAIL_FIELD] = email

        super(SendEmailResetSerializer, self).__init__(*args, **kwargs)


    def get_nickname(self, data, is_active=True):
        try:
            user = User._default_manager.get(
                is_active=is_active,
                **{'nickname': data.get('nickname', "")},
            )
            if user.has_usable_password():
                return user
        except User.DoesNotExist:
            pass
            errors_nickname = [
                ErrorDetail(_('Пользователь с таким псевдонимом не найден.'),
                            code='nickname_not_found')
            ]
            raise ValidationError({'nickname': errors_nickname})
