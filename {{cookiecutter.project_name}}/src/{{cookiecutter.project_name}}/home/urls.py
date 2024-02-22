from django.urls import path

from cc_bz_project_name.home import views

app_name = "home"
urlpatterns = [path("", views.HomeView.as_view(), name="home")]
