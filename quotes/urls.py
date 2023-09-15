from django.urls import path

from . import views
from .apps import QuotesConfig


app_name = QuotesConfig.name

urlpatterns = [
    path("", views.main, name="index"),
    path("<int:page>/", views.main, name="index"),
    path("add_author/", views.add_author, name="add_author"),
    path("author/<int:author_id>/", views.get_author, name="get_author"),
    path("add_quote1/", views.add_quote_1, name="add_quote1"),
]
