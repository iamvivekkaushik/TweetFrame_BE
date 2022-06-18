from typing import List

from fastapi import Query
from sqlalchemy import true
from sqlalchemy.orm import Session

from app.associative_tables.models import AssocTagFrames
from app.database.repository import BaseRepository
from app.enums import FrameType
from app.frame.models import Frame, FrameBase, FrameCreate

# from app.schedule.models import Schedule
from app.user.models import User


class FrameRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Frame, model_base=FrameBase)

    def get_by_popularity(self, limit=20) -> List[Frame]:
        query = f"""SELECT 
        frame.id AS frame_id, 
        frame.name AS frame_name, 
        frame.url AS frame_url, 
        frame.schedule_type AS frame_schedule_type, 
        frame.category_id AS frame_category_id, 
        frame.sub_category_id AS frame_sub_category_id, 
        frame.is_public AS frame_is_public, 
        frame.is_active AS frame_is_active, 
        frame.created_at AS frame_created_at, 
        frame.updated_at AS frame_updated_at, 
        frame.settings AS frame_settings, 
        frame.user_id AS frame_user_id 
        FROM frame 
        join (SELECT distinct frame_id, count(frame_id) from schedule GROUP BY frame_id) as SC on SC.frame_id = frame.id 
        WHERE is_active=true ORDER BY SC.count desc LIMIT {limit};"""
        query_result = self.session.execute(query).fetchall()

        frame_list = []

        for item in query_result:
            frame = Frame(
                id=item[0],
                name=item[1],
                url=item[2],
                schedule_type=item[3],
                category_id=item[4],
                sub_category_id=item[5],
                is_public=item[6],
                is_active=item[7],
                created_at=item[8],
                updated_at=item[9],
                settings=item[10],
                user_id=item[11],
            )
            frame_list.append(frame)
        return frame_list

    def get_by_category(self, category_id=None, sub_category_id=None) -> List[Frame]:
        """Returns all the available objects for a user."""
        query: Query = self.session.query(self.model).filter(
            self.model.is_public == true(),
            self.model.is_active == true(),
        )

        if category_id:
            query = query.filter(self.model.category_id == category_id)

        if sub_category_id:
            query = query.filter(self.model.sub_category_id == sub_category_id)

        return query.all()

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
