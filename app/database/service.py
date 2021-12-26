from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.database.repository import BaseRepository


def get_db_request(request: Request) -> Session:
    return request.state.db


def get_repository(repo_type: Type[BaseRepository]):
    def _get_repo(
        session: Session = Depends(get_db_request),
    ) -> BaseRepository:
        return repo_type(session)

    return _get_repo
