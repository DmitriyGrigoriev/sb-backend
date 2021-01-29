from django.urls import path
from .views import TerminalView

urlpatterns = [
    path('terminal/', TerminalView.as_view()),
]