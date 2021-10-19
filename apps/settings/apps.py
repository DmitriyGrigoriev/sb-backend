from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'apps.settings'
    verbose_name = _('Настройки')
