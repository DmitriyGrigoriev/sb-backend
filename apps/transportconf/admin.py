from django.contrib import admin

from .models import Terminal
from common.models import TemplateAdminModel

@admin.register(Terminal)
class TerminalAdmin(TemplateAdminModel):
    pass
