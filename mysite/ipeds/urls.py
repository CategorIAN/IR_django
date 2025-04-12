from django.urls import path

from . import views

app_name = "ipeds"

urlpatterns = [
    path("", views.index, name="index"),
    path("ftug/", views.ftug, name="ftug"),
    path("ftug/<cip>/", views.ftug_by_cip, name="ftug_by_cip"),
    path("ptug/", views.ptug, name="ptug"),
]