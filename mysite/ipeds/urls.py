from django.urls import path

from . import views

app_name = "ipeds"

urlpatterns = [
    path("", views.index, name="index"),
    path("ftug/", views.ftug, name="ftug"),
]