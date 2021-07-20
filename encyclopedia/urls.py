from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.newEntry, name="new_entry"),
    path("wiki/<str:page_name>/", views.viewEntry, name="view_entry"),
    path("wiki/<str:page_name>/edit", views.editEntry, name="edit_entry"),
    path("search", views.search, name="search"),
    path("random", views.randomPageView, name="random"),
]
