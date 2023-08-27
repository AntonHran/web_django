from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Author, Quote, Tag, MtM
from .forms import AddQuoteForm, AddAuthorForm, TagForm


def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_per_page = paginator.page(page)
    return render(request, "quotes/index.html", context={
        "title": "QUOTES",
        "quotes": quotes_per_page,
    })


@login_required()
def add_author(request):
    if request.method == "POST":
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            # Перевірка чи автор з таким ім'ям вже існує
            full_name = form.cleaned_data["full_name"]
            if Author.objects.filter(full_name=full_name).exists():
                messages.error(request, "Author with this name already exists.")
            else:
                form.save()
                messages.success(request, "Author added successfully.")
                return redirect(to='quotes:index')
    else:
        form = AddAuthorForm()
    context = {"form": form}
    return render(request, "quotes/add_author.html", context)


@login_required
def add_quote(request):
    form = AddQuoteForm()
    tags = Tag.objects.all()

    if request.method == "POST":
        form = AddQuoteForm(request.POST)

        if form.is_valid():
            author = form.cleaned_data["author"]
            new_author = form.cleaned_data["new_author"]

            if author is None and new_author:
                author = Author.objects.create(full_name=new_author)
            elif author is None and not new_author:
                form.add_error(
                    "author",
                    "Please select an existing author or provide a new author name.",
                )
                return render(
                    request, "quotes/add_quote.html", {"tags": tags, "form": form}
                )

            new_quote = form.save()
            new_quote.author = author
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            new_quote.tags.set(choice_tags)

            return redirect(to="quotes:index")

    return render(request, "quotes/add_quote.html", {"tags": tags, "form": form})


@login_required
def add_tags(request):
    if request.method == "POST":
        form = TagForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to="quotes:index")

    return render(request, "quotes/add_tags.html", {"form": TagForm()})


def get_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, "quotes/get_author.html", context={
        "title": "authors",
        "author": author,
    })
