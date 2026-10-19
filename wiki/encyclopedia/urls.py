from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.view_page, name="wiki"),
    path("search/", views.search, name="search"),
    path("create_page/", views.create_page, name="create_page"),
    path("edit/<str:title>", views.edit_page, name="edit_page"),
    path("random/", views.random_page, name="random_page")
]
