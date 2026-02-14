import logging
import os
from pathlib import Path

from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView

from .models import Book
from .services.fb2_parser import FB2Parser
from .services.flibusta_service import FlibustaService

logger = logging.getLogger(__name__)


class BookListView(ListView):
    model = Book
    context_object_name = "books"

    def get_template_names(self):
        if self.request.htmx:
            return ["books/partials/book_grid.html"]
        return ["books/book_list.html"]


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"


def book_content(request, pk):
    book = get_object_or_404(Book, pk=pk)
    try:
        parser = FB2Parser(book.file.path)
        data = parser.parse()
        html_content = data["text"]
        return HttpResponse(html_content)
    except Exception as e:
        return HttpResponse(f"<p>Error loading book content: {e}</p>")


@require_http_methods(["GET"])
def search(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return render(request, "books/partials/search_results.html", {"results": []})

    try:
        service = FlibustaService()
        results = service.search(query)
        return render(
            request,
            "books/partials/search_results.html",
            {"results": results, "query": query},
        )
    except Exception as e:
        # It's good practice to log the error
        # logger.error(f"Flibusta search failed: {e}")
        return HttpResponse(
            '<div class="text-red-500 p-4">Error searching Flibusta. Please check the connection and try again.</div>'
        )


@require_http_methods(["POST"])
def download_book(request):
    logger.info("Download book request received")
    flibusta_id = request.POST.get("flibusta_id")
    if not flibusta_id:
        logger.warning("Missing flibusta_id in POST request")
        return HttpResponse("Missing flibusta_id", status=400)

    if Book.objects.filter(flibusta_id=flibusta_id).exists():
        logger.info(f"Book with flibusta_id {flibusta_id} already exists. Redirecting.")
        response = redirect("books:book-list")
        response["HX-Redirect"] = request.build_absolute_uri(response["Location"])
        return response

    try:
        logger.info(f"Starting download for flibusta_id: {flibusta_id}")
        service = FlibustaService()
        temp_path = service.download_book(flibusta_id)
        logger.info(f"Book downloaded to temporary path: {temp_path}")

        parser = FB2Parser(temp_path)
        book_data = parser.parse()
        logger.info("FB2 file parsed")

        with open(temp_path, "rb") as f:
            book_file = File(f, name=Path(temp_path).name)

            book = Book(
                title=book_data["title"] or "No Title",
                author=book_data["author"] or "Unknown Author",
                flibusta_id=flibusta_id,
                file=book_file,
                file_size=os.path.getsize(temp_path),
            )

            if book_data.get("cover"):
                logger.info("Cover found, saving.")
                book.cover.save(book_data["cover"].name, book_data["cover"], save=False)

            book.save()
            logger.info(f"Book '{book.title}' saved to database with ID: {book.id}")

        os.remove(temp_path)
        logger.info(f"Temporary file {temp_path} removed")

        response = redirect("books:book-list")
        response["HX-Redirect"] = request.build_absolute_uri(response["Location"])
        logger.info("Redirecting to book list.")
        return response

    except Exception as e:
        logger.exception(f"Error downloading book with flibusta_id {flibusta_id}")
        return HttpResponse(f"Error downloading book: {e}", status=500)


# --- Placeholder views from the initial setup ---


def read_book(request, pk):
    return HttpResponse(f"Reading book {pk}")


def save_progress(request, pk):
    return HttpResponse(f"Saving progress for book {pk}")


def get_settings(request):
    return HttpResponse("Settings")


def update_settings(request):
    return HttpResponse("Updating settings")
