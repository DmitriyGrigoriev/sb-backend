from uuid import uuid4
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from common.constants import SexChoise


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(email=self.normalize_email(email),
                          is_active=False,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          last_login=timezone.now(),
                          registered_at=timezone.now(),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        is_staff = extra_fields.pop('is_staff', False)
        is_superuser = extra_fields.pop('is_superuser', False)
        return self._create_user(email, password, is_staff, is_superuser, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('Почта'), unique=True, max_length=255)
    first_name = models.CharField(verbose_name=_('Имя'), max_length=30, default='')
    middle_name = models.CharField(verbose_name=_('Фамилия'), max_length=80, default='', blank=True,)
    last_name = models.CharField(verbose_name=_('Отчество'), max_length=30, default='', blank=True,)
    avatar = models.ImageField(verbose_name=_('Фото профиля'), blank=True)
    token = models.UUIDField(verbose_name=_('Токен'), default=uuid4, editable=False)

    position = models.CharField('Должность', max_length=120, blank=True,)
    phone = PhoneNumberField(_('Телефон'), null=True, blank=True,)
    mobile = PhoneNumberField(_('Мобильный'), null=True, blank=True,)
    location = models.CharField(_('Место расположения'), max_length=100, null=True, blank=True,)
    birthday = models.DateField(_('Дата рождения'), null=True, blank=True,)
    sex = models.PositiveSmallIntegerField(_("Пол"),choices=SexChoise.choices, null=True, blank=True,)

    is_admin = models.BooleanField(verbose_name=_('Администратор'), default=False)
    is_active = models.BooleanField(verbose_name=_('Пользователь активен'), default=True)
    is_staff = models.BooleanField(verbose_name=_('Сотрудник'), default=False)
    registered_at = models.DateTimeField(verbose_name=_('Дата регистрации'), auto_now_add=timezone.now)
    last_login = models.DateTimeField(_('Последний вход в систему'), blank=True, null=True)

    # Fields settings
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    @property
    def full_name(self):
        return f'{self.middle_name} {self.first_name} {self.last_name}'.strip()
    full_name.fget.short_description = _('ФИО')

    @property
    def short_name(self):
        result = ''
        if (len(self.middle_name) > 0):
            result = f'{self.middle_name} '
        if (len(self.first_name) > 0):
            result = result + f'{self.first_name[0]}.'
        if (len(self.last_name) > 0):
            result = result + f'{self.last_name[0]}.'
        return result

    short_name.fget.short_description = _('Имя и инициалы')

    @property
    def unused_name(self):
        return f'<{self.id}> пользователь не завершил регистрацию'

    def full_or_unused_name(self):
        if self.full_name:
            return f'<{self.id}> {self.full_name}'
        return self.unused_name
    full_or_unused_name.short_description = _('ID ФИО')

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def __str__(self):
        return self.full_name
