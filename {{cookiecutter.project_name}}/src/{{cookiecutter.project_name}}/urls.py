from django.urls import include, path

urlpatterns = [
    path("api/users/", include("{{cookiecutter.project_name}}.users.urls", namespace="users")),
]
