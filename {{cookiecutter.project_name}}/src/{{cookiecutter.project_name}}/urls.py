from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("{{cookiecutter.project_name}}.home.urls", namespace="home")),
]
