# articles/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.article_list, name="article_list"),
    path("new/", views.article_create, name="article_create"),
    path("<str:public_id>/", views.article_detail, name="article_detail"),
    path("<str:public_id>/edit/", views.article_update, name="article_update"),
    path("<str:public_id>/delete/", views.article_delete, name="article_delete"),
]
