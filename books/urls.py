from django.urls import path

from .views import (
    BookDetailView,
    BookListView,
    book_content,
    download_book,
    get_settings,
    read_book,
    save_progress,
    search,
    update_settings,
)

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="book-list"),
    path("books/", BookListView.as_view(), name="book-list-htmx"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/read/", read_book, name="read-book"),
    path("books/<int:pk>/content/", book_content, name="book-content"),
    path("books/<int:pk>/progress/", save_progress, name="save-progress"),
    path("search/", search, name="search"),
    path("books/download/", download_book, name="download-book"),
    path("settings/", get_settings, name="get-settings"),
    path("settings/", update_settings, name="update-settings"),
]
