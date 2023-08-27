from datetime import date
from django.core.exceptions import ValidationError

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=60, null=False, unique=True)


def validate_date(value: date):
    if value >= value.today():
        raise ValidationError(f"{value} must be in the past!!!")


class Author(models.Model):
    full_name = models.CharField(max_length=60, null=False, unique=True)
    birth_date = models.DateField(null=False, validators=[validate_date])
    birth_place = models.CharField(max_length=100, null=False)
    biography = models.TextField(max_length=2000, null=False)


class Quote(models.Model):
    quote = models.TextField(max_length=400, null=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)


class MtM(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('quote', 'tag')
