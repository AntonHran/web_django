from django.forms import ModelForm, CharField, TextInput, DateField, DateInput, ModelChoiceField

from .models import Quote, Tag, Author


class AddQuoteForm(ModelForm):
    quote = CharField(max_length=200, required=True, widget=TextInput(attrs={"class": "form-control"}))
    author = ModelChoiceField(queryset=Author.objects.all(),
                              empty_label="Select an author",
                              blank=True, required=False)

    class Meta:
        model = Quote
        fields = ["quote", "author"]
        exclude = ["tags"]


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


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=60, required=True,
                     widget=TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Tag
        fields = ["name"]
