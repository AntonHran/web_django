from django.forms import ModelForm, CharField, TextInput, DateField, DateInput, ModelChoiceField, Select
from django.db import models

from .models import Quote, Tag, Author


class AddAuthorForm(ModelForm):
    full_name = CharField(
        max_length=60, required=True, widget=TextInput(attrs={"class": "form-control"})
    )
    birth_date = DateField(required=True, widget=DateInput(attrs={"class": "form-control"}))
    birth_place = CharField(
        max_length=100, required=True, widget=TextInput(attrs={"class": "form-control"})
    )
    biography = CharField(
        max_length=2000, required=True, widget=TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Author
        fields = ["full_name", "birth_date", "birth_place", "biography"]


class AddQuoteForm1(ModelForm):
    new_quote = CharField(max_length=200, required=True, widget=TextInput(attrs={"class": "form-control"}))
    author_choose = ModelChoiceField(queryset=Author.objects.values_list("full_name", flat=True), empty_label="author",
                                     required=True, widget=Select({"class": "form-control"}))

    class Meta:
        model = Quote
        fields = ["new_quote", "author_choose"]


class AddTagForm1(ModelForm):
    new_tag = CharField(min_length=3, max_length=60, required=False,
                        widget=TextInput(attrs={"class": "form-control"}))
    tag_choose = ModelChoiceField(queryset=Tag.objects.values_list("name", flat=True),
                                  empty_label="tag", required=False,
                                  widget=Select({"class": "form-control"}),)

    class Meta:
        model = Tag
        fields = ["new_tag", "tag_choose"]
