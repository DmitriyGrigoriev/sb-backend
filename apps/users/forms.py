from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from apps.users.models import User


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users.
    Includes all the required fields, plus a repeated password
    """
    # first_name = forms.CharField(label=_('Имя'))
    # middle_name = forms.CharField(label=_('Фамилия'))
    # last_name = forms.CharField(label=_('Отчество'))

    password1 = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Подтверждение пароля'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['nickname','email',]
        # fields = ['email', 'first_name', 'middle_name', 'last_name']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Пароли не совпадают"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    help_text = """Необработанные пароли не сохраняются, поэтому нет возможности увидеть пароль этого пользователя,
                   но вы можете изменить пароль с помощью <a href="../password/">этой формы</a>."""
    password = ReadOnlyPasswordHashField(label=_('Пароль'), help_text=help_text)

    class Meta:
        model = User
        fields = ['nickname', 'email', 'password', 'is_active', 'is_admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
