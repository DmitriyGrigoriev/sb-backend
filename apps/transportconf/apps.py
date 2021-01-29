from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class TransportConfig(AppConfig):
    name = 'apps.transportconf'
    verbose_name = _('Конфигурирование стоянок и стояночных мест')
