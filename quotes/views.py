from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


from .models import Author, Quote, Tag, MtM
from .forms import (
    AddAuthorForm,
    AddQuoteForm1,
    AddTagForm1,
)


def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_per_page = paginator.page(page)
    return render(
        request,
        "quotes/index.html",
        context={
            "title": "QUOTES",
            "quotes": quotes_per_page,
        },
    )


@login_required()
def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            if Author.objects.filter(full_name=full_name).exists():
                messages.error(request, "Author with this name already exists.")
            else:
                form.save()
                messages.success(request, "Author added successfully.")
                return redirect(to="quotes:index")
    else:
        form = AddAuthorForm()
    context = {"form": form}
    return render(request, "quotes/add_author.html", context)


def get_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(
        request,
        "quotes/get_author.html",
        context={
            "title": "authors",
            "author": author,
        },
    )


@login_required
def add_quote_1(request):
    form_quote = AddQuoteForm1()
    form_tag = AddTagForm1()
    if request.method == "POST":

        new_quote = request.POST.get("new_quote")
        author_chosen = request.POST.get("author_choose")
        new_tag = request.POST.get("new_tag")
        tag_chosen = request.POST.get("tag_choose")

        if new_quote and author_chosen and tag_chosen:
            author = Author.objects.get(full_name=author_chosen)
            Quote(quote=new_quote, author=author).save()
            tag = Tag.objects.get(name=tag_chosen)
            MtM(
                quote=Quote.objects.get(quote=new_quote),
                tag=tag
               ).save()

        elif new_quote and author_chosen and new_tag:
            author = Author.objects.get(full_name=author_chosen)
            Quote(quote=new_quote, author=author).save()
            Tag(name=new_tag).save()
            MtM(
                quote=Quote.objects.get(quote=new_quote),
                tag=Tag.objects.get(name=new_tag),
                ).save()

        else:
            messages.error(request, "Fields Author, Quote and Tag must be filled in to add new quote!!!")

        return redirect(to="quotes:index")

    context = {
        "form_quote": form_quote,
        "form_tag": form_tag
    }

    return render(request, "quotes/add_quote1.html", context)
