from uuid import uuid4
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from rest_framework.exceptions import ErrorDetail, ValidationError
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from common.constants import SexChoise
from .validators import regex_nickname


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and return a `User` with email and password.
        """
        nickname = extra_fields.get('nickname')

        errors_nickname = [
            ErrorDetail(_('Для завершения регистрации необходимо указать псевдоним.'),
                        code='error_empty_nickname')
        ]
        errors_email = [
            ErrorDetail(_('Для завершения регистрации необходимо указать адрес электронной почты.'),
                        code='error_email')
        ]
        if not nickname:
            raise ValidationError({'nickname': errors_nickname})
        if not email:
            raise ValidationError({'email': errors_email})

        user = self.model(email=self.normalize_email(email),
                          last_login=timezone.now(),
                          registered_at=timezone.now(),
                          **extra_fields)
        user.set_password(password)

        try:
            user.save(using=self._db)
        except IntegrityError as exc:
            errors_nickname = [
                ErrorDetail(_(f'Пользователь с таким псевдонимом {nickname} уже существует.'),
                            code='error_integrity_nickname')
            ]
            if f'{nickname}' in str(exc):
                raise ValidationError({'nickname': errors_nickname})

            raise ValidationError(ErrorDetail(exc, code='user_integrity_error'))

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """Create `User` with email and password"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and return `User` with permission superuser (admin)"""
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_active=True.'))

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('Почта'), unique=True, max_length=255)
    nickname = models.CharField(verbose_name=_('Псевдоним'), max_length=20, unique=True, blank=False, validators=[regex_nickname])
    first_name = models.CharField(verbose_name=_('Имя'), max_length=30, default='', blank=True,)
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
        return f'<{self.niсkname}> пользователь не завершил регистрацию'

    def full_or_unused_name(self):
        if self.full_name:
            return f'<{self.niсkname}> {self.full_name}'
        return self.unused_name
    full_or_unused_name.short_description = _('<Псевдоним> ФИО')

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def __str__(self):
        return self.full_name
