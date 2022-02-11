from typing import List

from sqlalchemy.orm import Session

from fastapi import Query

from app.database.repository import BaseRepository
from app.tag.models import Tag, TagBase


class TagRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Tag, model_base=TagBase)

    def search(self, search_query, skip=0, limit=20) -> List[Tag]:
        """Returns all the available objects for a user."""
        query: Query = self.session.query(self.model)

        query.filter(self.model.name.like(f"%{search_query}%"))
        query = query.offset(skip).limit(limit)
        return query.all()
