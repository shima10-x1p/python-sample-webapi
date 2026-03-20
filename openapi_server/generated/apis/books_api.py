# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from generated.apis.books_api_base import BaseBooksApi
import generated.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from generated.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictStr, field_validator
from typing import Optional
from typing_extensions import Annotated
from generated.models.book_detail import BookDetail
from generated.models.book_input import BookInput
from generated.models.book_list_response import BookListResponse
from generated.models.problem_detail import ProblemDetail


router = APIRouter()

ns_pkg = generated.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/books",
    responses={
        200: {"model": BookListResponse, "description": "検索成功"},
        400: {"model": ProblemDetail, "description": "リクエストパラメータが不正"},
        502: {"model": ProblemDetail, "description": "外部API呼び出しに失敗"},
    },
    tags=["books"],
    summary="書籍を検索する",
    response_model_by_alias=True,
)
async def search_books(
    title: Annotated[Optional[StrictStr], Field(description="タイトルの部分一致")] = Query(None, description="タイトルの部分一致", alias="title"),
    author_name: Annotated[Optional[StrictStr], Field(description="著者名の部分一致（外部APIの `author` パラメータにマッピング）")] = Query(None, description="著者名の部分一致（外部APIの &#x60;author&#x60; パラメータにマッピング）", alias="author_name"),
    per_page: Annotated[Optional[Annotated[int, Field(le=40, strict=True, ge=1)]], Field(description="1ページあたりの取得件数（1〜40）")] = Query(10, description="1ページあたりの取得件数（1〜40）", alias="per_page", ge=1, le=40),
    page: Annotated[Optional[Annotated[int, Field(strict=True, ge=1)]], Field(description="ページ番号（1始まり）")] = Query(1, description="ページ番号（1始まり）", alias="page", ge=1),
) -> BookListResponse:
    """タイトル・著者名で書籍を検索します。 内部で Book Search API の &#x60;GET /v1/search&#x60; を呼び出し、レスポンスを変換して返します。 &#x60;title&#x60; と &#x60;author_name&#x60; のうち少なくとも1つを指定してください。 """
    if not BaseBooksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseBooksApi.subclasses[0]().search_books(title, author_name, per_page, page)


@router.post(
    "/books",
    responses={
        201: {"model": BookDetail, "description": "登録成功"},
        400: {"model": ProblemDetail, "description": "リクエストボディが不正"},
        409: {"model": ProblemDetail, "description": "同じISBNの書籍がすでに存在する"},
        502: {"model": ProblemDetail, "description": "外部API呼び出しに失敗"},
    },
    tags=["books"],
    summary="書籍を登録する",
    response_model_by_alias=True,
)
async def create_book(
    book_input: BookInput = Body(None, description=""),
) -> BookDetail:
    """書籍を新規登録します。 内部で Book Search API の &#x60;POST /v1/books&#x60; を呼び出し、レスポンスを変換して返します。 """
    if not BaseBooksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseBooksApi.subclasses[0]().create_book(book_input)


@router.get(
    "/books/{isbn}",
    responses={
        200: {"model": BookDetail, "description": "取得成功"},
        400: {"model": ProblemDetail, "description": "ISBNの形式が不正"},
        404: {"model": ProblemDetail, "description": "書籍が見つからない"},
        502: {"model": ProblemDetail, "description": "外部API呼び出しに失敗"},
    },
    tags=["books"],
    summary="ISBNで書籍詳細を取得する",
    response_model_by_alias=True,
)
async def get_book(
    isbn: Annotated[str, Field(strict=True, description="ISBN-13（ハイフンなし13桁）")] = Path(..., description="ISBN-13（ハイフンなし13桁）", regex=r"^\d{13}$"),
) -> BookDetail:
    """ISBNを指定して書籍の詳細情報を取得します。 内部で Book Search API の &#x60;GET /v1/books/{isbn}&#x60; を呼び出し、レスポンスを変換して返します。 """
    if not BaseBooksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseBooksApi.subclasses[0]().get_book(isbn)
