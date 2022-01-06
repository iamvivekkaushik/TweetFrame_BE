from typing import List

from fastapi import Query
from sqlalchemy.orm import Session

from sqlalchemy import true

from app.enums import FrameType
from app.user.models import User
from app.frame.models import Frame, FrameBase
from app.database.repository import BaseRepository


class FrameRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Frame, model_base=FrameBase)

    def get_all_frames(
        self, user: User = None, type: FrameType = None, skip=0, limit=100
    ) -> List[Frame]:
        """Returns all the available objects for a user."""
        query: Query = self.session.query(self.model).filter(
            self.model.is_public == true(),
            self.model.is_active == true(),
        )

        if type:
            query = query.filter(self.model.type == type.value)

        if user:
            query = query.filter(self.model.user_id == user.id)

        query = query.offset(skip).limit(limit)
        return query.all()
