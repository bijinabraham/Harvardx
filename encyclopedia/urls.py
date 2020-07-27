from django.urls import path

from . import views, util

app_name = "wiki"

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/new", views.new, name="new"),
    path("wiki/rando", views.getrandompage, name="getrandompage"),
    path("wiki/<str:title>", views.greet, name="greet"),
    path("wiki/search/", views.searchstr, name="searchstr"),
    path("edit/<str:title>", views.edit, name="edit"),
]
