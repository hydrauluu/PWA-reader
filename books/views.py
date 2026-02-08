from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"

    def get_template_names(self):
        if self.request.htmx:
            return ["books/partials/book_grid.html"]
        return ["books.html"]


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"


def read_book(request, pk):
    return HttpResponse(f"Reading book {pk}")


def book_content(request, pk):
    return HttpResponse(f"Content for book {pk}")


def save_progress(request, pk):
    return HttpResponse(f"Saving progress for book {pk}")


def search(request):
    return HttpResponse("Search results")


def download_book(request):
    return HttpResponse("Downloading book")


def get_settings(request):
    return HttpResponse("Settings")


def update_settings(request):
    return HttpResponse("Updating settings")
