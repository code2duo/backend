"""code2duo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from code2duo.views import render_react

schema_view = get_schema_view(
    openapi.Info(
        title="Code2Duo API",
        default_version="v1",
        description="Contains API Documentations",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

admin = [
    path("admin/", admin.site.urls),
]

api = [
    path("api/v1/", include("core.urls")),
]

documentation = [
    path(
        "playground/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

react = [
    re_path(r"^$", render_react),
    re_path(r"^(?:.*)/?$", render_react),
]

urlpatterns = admin + api + documentation + react
