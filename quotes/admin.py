from django.contrib import admin
from .models import Author, Tag, Quote, MtM


admin.site.register(Author)
admin.site.register(Quote)
admin.site.register(Tag)
admin.site.register(MtM)
