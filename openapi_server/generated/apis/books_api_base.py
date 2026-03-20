# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr, field_validator
from typing import Optional
from typing_extensions import Annotated
from generated.models.book_detail import BookDetail
from generated.models.book_input import BookInput
from generated.models.book_list_response import BookListResponse
from generated.models.problem_detail import ProblemDetail


class BaseBooksApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseBooksApi.subclasses = BaseBooksApi.subclasses + (cls,)
    async def search_books(
        self,
        title: Annotated[Optional[StrictStr], Field(description="タイトルの部分一致")],
        author_name: Annotated[Optional[StrictStr], Field(description="著者名の部分一致（外部APIの `author` パラメータにマッピング）")],
        per_page: Annotated[Optional[Annotated[int, Field(le=40, strict=True, ge=1)]], Field(description="1ページあたりの取得件数（1〜40）")],
        page: Annotated[Optional[Annotated[int, Field(strict=True, ge=1)]], Field(description="ページ番号（1始まり）")],
    ) -> BookListResponse:
        """タイトル・著者名で書籍を検索します。 内部で Book Search API の &#x60;GET /v1/search&#x60; を呼び出し、レスポンスを変換して返します。 &#x60;title&#x60; と &#x60;author_name&#x60; のうち少なくとも1つを指定してください。 """
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
