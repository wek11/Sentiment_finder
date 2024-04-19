from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.url_display, name="link-view"),
    path("results/", views.show_results, name="show-results"),
]