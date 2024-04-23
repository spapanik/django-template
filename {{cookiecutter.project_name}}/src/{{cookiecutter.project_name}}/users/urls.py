from django.urls import path

from {{cookiecutter.project_name}}.users import views

app_name = "users"
urlpatterns = [
    path("", views.UserAPIView.as_view(), name="users"),
    path(
        "confirm-email/<int:token>",
        views.ConfirmEmailAPIView.as_view(),
        name="confirm-email",
    ),
    path("token/", views.ObtainTokensView.as_view(), name="obtain_tokens"),
    path("token/refresh", views.RefreshTokenView.as_view(), name="refresh_token"),
]
