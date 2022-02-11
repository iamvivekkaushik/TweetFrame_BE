from typing import List

from fastapi import Query
from sqlalchemy import true
from sqlalchemy.orm import Session

from app.associative_tables.models import AssocTagFrames
from app.database.repository import BaseRepository
from app.enums import FrameType
from app.frame.models import Frame, FrameBase, FrameCreate
from app.user.models import User


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

    def create(self, object_in: FrameCreate) -> Frame:
        """Creates a new object."""
        frame: Frame = super().create(object_in)

        # for tag in object_in.tags_list:
        #     self.session.add(
        #         AssocTagFrames(
        #             frame_id=frame.id,
        #             tag_id=tag,
        #         )
        #     )
        #
        # # Create and entry in associated table
        # self.session.commit()

        return frame
