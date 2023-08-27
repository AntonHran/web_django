from django import template

from ..models import Author


register = template.Library()


def get_author(author_obj):
    return author_obj.full_name


register.filter("author_", get_author)
