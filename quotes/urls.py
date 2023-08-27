from django.urls import path

from . import views
from .apps import QuotesConfig


app_name = QuotesConfig.name

urlpatterns = [
    path("", views.main, name="index"),
    path("<int:page>", views.main, name="root_paginate"),
    path("add_author/", views.add_author, name="add_author"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("add_tags/", views.add_tags, name="add_tags"),
    path("author/<int:author_id>/", views.get_author, name="get_author"),
]
