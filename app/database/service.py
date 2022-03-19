from typing import List, Optional, Type

from fastapi import Depends, Query
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.types import Json, constr
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.database.core import get_db
from app.database.repository import BaseRepository
from sqlalchemy_filters import apply_pagination, apply_sort, apply_filters
from sqlalchemy_filters.exceptions import BadFilterFormat, FieldNotFound
from sqlalchemy.exc import ProgrammingError

from app.exceptions import FieldNotFoundError, InvalidFilterError
from app.social_login.models import SocialLogin
from app.user.models import User


QueryStr = constr(regex=r"^[ -~]+$", min_length=1)


def common_parameters(
    page: int = Query(1, gt=0, lt=2147483647),
    limit: int = Query(5, lt=100),
    query_str: QueryStr = Query(None, alias="q"),
    filters: Optional[Json] = Query([]),
    sort_by: List[str] = Query([], alias="sortBy[]"),
    descending: List[bool] = Query([], alias="descending[]"),
):
    return {
        "page": page,
        "limit": limit,
        "query_str": query_str,
        "filter_spec": filters,
        "sort_by": sort_by,
        "descending": descending,
    }


def search_filter_sort_paginate(
    repository: BaseRepository,
    query_str: str = None,
    filter_spec=[],
    page: int = 1,
    limit: int = 5,
    sort_by: List[str] = None,
    descending: List[bool] = None,
):
    """Common functionality for searching, filtering, sorting, and pagination."""
    try:
        query = repository.get_query()

        if query_str:
            for field in repository.model.searchable_fields():
                query = query.filter(
                    getattr(repository.model, field).contains(query_str)
                )

        for filter in filter_spec:
            for filterable_field in repository.model.filterable_fields():
                if filter["field"] != filterable_field:
                    continue

                if filter["op"] == "eq":
                    query = query.filter(
                        getattr(repository.model, filter["field"]) == filter["value"]
                    )
                elif filter["op"] == "ne":
                    query = query.filter(
                        getattr(repository.model, filter["field"]) != filter["value"]
                    )
                elif filter["op"] == "lt":
                    query = query.filter(
                        getattr(repository.model, filter["field"]) < filter["value"]
                    )
                elif filter["op"] == "lte":
                    query = query.filter(
                        getattr(repository.model, filter["field"]) <= filter["value"]
                    )
                elif filter["op"] == "gt":
                    query = query.filter(
                        getattr(repository.model, filter["field"]) > filter["value"]
                    )
                elif filter["op"] == "gte":
                    query = query.filter(
                        getattr(repository.model, filter["field"]) >= filter["value"]
                    )
                elif filter["op"] == "in":
                    query = query.filter(
                        getattr(repository.model, filter["field"]).in_(filter["value"])
                    )
                elif filter["op"] == "nin":
                    query = query.filter(
                        getattr(repository.model, filter["field"]).notin_(
                            filter["value"]
                        )
                    )
                elif filter["op"] == "startswith":
                    query = query.filter(
                        getattr(repository.model, filter["field"]).startswith(
                            filter["value"]
                        )
                    )
                elif filter["op"] == "endswith":
                    query = query.filter(
                        getattr(repository.model, filter["field"]).endswith(
                            filter["value"]
                        )
                    )

        if sort_by:
            query = apply_sort(query, sort_by)

    except FieldNotFound as e:
        raise ValidationError(
            [
                ErrorWrapper(FieldNotFoundError(msg=str(e)), loc="filter"),
            ],
            model=repository.model,
        )
    except BadFilterFormat as e:
        raise ValidationError(
            [ErrorWrapper(InvalidFilterError(msg=str(e)), loc="filter")],
            model=repository.model,
        )

    if limit == -1:
        limit = None

    # sometimes we get bad input for the search function
    # TODO investigate moving to a different way to parsing queries that won't through errors
    # e.g. websearch_to_tsquery
    # https://www.postgresql.org/docs/current/textsearch-controls.html
    try:
        query, pagination = apply_pagination(query, page_number=page, page_size=limit)
    except ProgrammingError as e:
        return {
            "items": [],
            "current": page,
            "next": None,
            "total_results": 0,
            "total_pages": 0,
        }

    next_page = pagination.page_number + 1
    if pagination.page_number == pagination.num_pages or pagination.num_pages == 0:
        next_page = None

    return {
        "items": query.all(),
        "current": pagination.page_number,
        "next": next_page,
        "total_results": pagination.total_results,
        "total_pages": pagination.num_pages,
    }


def get_db_request(request: Request) -> Session:
    return request.state.db


def get_repository(repo_type: Type[BaseRepository]):
    def _get_repo(
        session: Session = Depends(get_db_request),
    ) -> BaseRepository:
        return repo_type(session)

    return _get_repo
