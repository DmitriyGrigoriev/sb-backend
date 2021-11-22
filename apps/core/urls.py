# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    # path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")),   # Auth routes - login / register
    path("", include("apps.core.urls"))         # UI Kits Html files
]