import requests
from django.conf import settings
from lxml import html


def search_books(query):
    try:
        proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050",
        }
        search_url = f"{settings.FLIBUSTA_ONION_URL}/booksearch"
        params = {"ask": query}
        response = requests.get(search_url, params=params, proxies=proxies, timeout=30)
        response.raise_for_status()

        tree = html.fromstring(response.content)
        books = []
        for book_element in tree.xpath("//li"):
            title_element = book_element.xpath('.//a[contains(@href, "/b/")]')
            author_element = book_element.xpath('.//a[contains(@href, "/a/")]')

            if title_element and author_element:
                title = title_element[0].text_content().strip()
                author = author_element[0].text_content().strip()
                flibusta_id = title_element[0].get("href").split("/")[-1]

                books.append(
                    {
                        "title": title,
                        "author": author,
                        "flibusta_id": flibusta_id,
                    }
                )
        return books
    except requests.exceptions.RequestException as e:
        # For development, if Tor is not available, return mock data
        if settings.DEBUG:
            return [
                {"title": "Mock Book 1", "author": "Mock Author 1", "flibusta_id": "1"},
                {"title": "Mock Book 2", "author": "Mock Author 2", "flibusta_id": "2"},
            ]
        return []


def download_book(flibusta_id, book_format="fb2"):
    try:
        proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050",
        }
        download_url = f"{settings.FLIBUSTA_ONION_URL}/b/{flibusta_id}/{book_format}"
        response = requests.get(download_url, proxies=proxies, timeout=60)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        return None
