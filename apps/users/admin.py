from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from apps.users.models import User
from apps.users.forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['nickname', 'email', 'last_login']
    fieldsets = [
        [_('Аутентификация'), {'fields': ['nickname', 'email', 'password']}],
        [_('Персональная информация'), {'fields': ['middle_name', 'first_name', 'last_name', 'avatar']}],
        [_('Настройки'), {'fields': ['groups', 'is_admin', 'is_active', 'is_staff', 'is_superuser']}],
        [_('Важные даты'), {'fields': ['last_login', 'registered_at']}],
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        [None, {'classes': ['wide'],
                'fields': ['nickname', 'email', 'password1', 'password2']}],
    ]
    search_fields = ['nickname', 'email']
    ordering = ['email']
    readonly_fields = ['last_login', 'registered_at']


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# Unregister the Group model from admin.
#admin.site.unregister(Group)

