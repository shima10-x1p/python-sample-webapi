# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr, field_validator  # noqa: F401
from typing import Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.book_detail import BookDetail  # noqa: F401
from openapi_server.models.book_input import BookInput  # noqa: F401
from openapi_server.models.book_list_response import BookListResponse  # noqa: F401
from openapi_server.models.problem_detail import ProblemDetail  # noqa: F401


def test_search_books(client: TestClient):
    """Test case for search_books

    書籍を検索する
    """
    params = [("keyword", 'Python'),     ("per_page", 10),     ("page", 1)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/books",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_book(client: TestClient):
    """Test case for create_book

    書籍を登録する
    """
    book_input = {"summary":"Pythonのデータモデルを深く理解し、より慣用的なコードを書くための実践的なガイド。","published_year":2022,"isbn":"9784873119328","publisher":"O'Reilly Media","categories":["Programming","Python"],"title":"Fluent Python","thumbnail_url":"https://example.com/books/9784873119328/thumbnail.jpg","published_date":"2022-04-26","page_count":1012,"authors":[{"name":"Luciano Ramalho","role":"author"}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/books",
    #    headers=headers,
    #    json=book_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_book(client: TestClient):
    """Test case for get_book

    ISBNで書籍詳細を取得する
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/books/{isbn}".format(isbn='9784873119328'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

