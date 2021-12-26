from typing import Optional

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType, JSONType

from app.database.core import Base
from app.enums import FrameType, ScheduleType
from app.models import TweetFrameBase, BaseIdMixin, IDModelMixin, \
    DateTimeModelMixin


# SQLAlchemy Model
class Frame(BaseIdMixin, Base):
    name = Column(Text(), nullable=False)
    url = Column(URLType(), nullable=False)
    type = Column(Text(), default=FrameType.FREE, nullable=False)
    schedule_type = Column(Text(), default=ScheduleType.ONE_TIME,
                           nullable=False)
    settings = Column(JSONType(), nullable=False, default={})
    is_public = Column(Boolean, default=False, nullable=False)

    # Relationships
    user_id = Column(GUID, ForeignKey("user.id"))
    created_by = relationship("User", back_populates="frames")

    schedules = relationship("Schedule", back_populates="frame")


# Pydantic models...
class FrameBase(TweetFrameBase):
    name: str
    url: str
    type: FrameType
    schedule_type: ScheduleType
    settings: Optional[dict]
    is_public: bool


class FrameResponse(IDModelMixin, DateTimeModelMixin, FrameBase):
    pass


class FrameCreate(FrameBase):
    user_id: Optional[int]


class FrameCreateResponse(IDModelMixin, DateTimeModelMixin, FrameCreate):
    pass


class FrameUpdate(TweetFrameBase):
    # name = Optional[str]
    # url: Optional[str]
    # type: Optional[FrameType]
    # schedule_type: Optional[ScheduleType]
    # settings: Optional[dict]
    # is_public: Optional[bool]
    # is_active = Optional[bool]
    pass


class FrameUpdateResponse(IDModelMixin, DateTimeModelMixin, FrameUpdate):
    pass
