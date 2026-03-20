# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr, field_validator
from typing import Optional
from typing_extensions import Annotated
from openapi_server.models.book_detail import BookDetail
from openapi_server.models.book_input import BookInput
from openapi_server.models.book_list_response import BookListResponse
from openapi_server.models.problem_detail import ProblemDetail


class BaseBooksApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseBooksApi.subclasses = BaseBooksApi.subclasses + (cls,)
    async def search_books(
        self,
        keyword: Annotated[StrictStr, Field(description="検索キーワード（タイトル・著者名など）")],
        per_page: Annotated[Optional[Annotated[int, Field(le=40, strict=True, ge=1)]], Field(description="1ページあたりの取得件数（1〜40）")],
        page: Annotated[Optional[Annotated[int, Field(strict=True, ge=1)]], Field(description="ページ番号（1始まり）")],
    ) -> BookListResponse:
        """キーワードで書籍を検索します。 内部で Book Search API の &#x60;GET /v1/search&#x60; を呼び出し、レスポンスを変換して返します。 """
        ...


    async def create_book(
        self,
        book_input: BookInput,
    ) -> BookDetail:
        """書籍を新規登録します。 内部で Book Search API の &#x60;POST /v1/books&#x60; を呼び出し、レスポンスを変換して返します。 """
        ...


    async def get_book(
        self,
        isbn: Annotated[str, Field(strict=True, description="ISBN-13（ハイフンなし13桁）")],
    ) -> BookDetail:
        """ISBNを指定して書籍の詳細情報を取得します。 内部で Book Search API の &#x60;GET /v1/books/{isbn}&#x60; を呼び出し、レスポンスを変換して返します。 """
        ...
