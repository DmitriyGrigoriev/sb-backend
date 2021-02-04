from djoser.serializers import UserSerializer
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import Group
# from apps.users.models import User

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserCreateSerializer(UserCreateSerializer):
    registered_at = serializers.DateTimeField(format='%H:%M %d.%m.%Y', read_only=True)

    avatar = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    full_name = serializers.SerializerMethodField(read_only=True)
    short_name = serializers.SerializerMethodField(read_only=True)

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else settings.STATIC_URL + 'images/default_avatar.png'

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
            'is_active',
            'registered_at'
        ]


class UserSerializer(UserSerializer):
    groups = GroupSerializer(many=True)
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'groups')

        read_only_fields = tuple('email, groups')
