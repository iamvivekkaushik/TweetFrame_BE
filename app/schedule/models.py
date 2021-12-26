from datetime import date
from typing import Optional

from pydantic import Field
from sqlalchemy import Column, Text, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import JSONType

from app.database.core import Base
from app.enums import FrameType, ScheduleType, ScheduleStatus
from app.models import TweetFrameBase, BaseIdMixin, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
class Schedule(BaseIdMixin, Base):
    name = Column(Text(), nullable=False)
    type = Column(Text(), default=FrameType.FREE, nullable=False)
    schedule_type = Column(Text(), default=ScheduleType.ONE_TIME, nullable=False)
    status = Column(Text(), default=ScheduleStatus.CREATED, nullable=False)
    settings = Column(JSONType(), nullable=False, default={})
    message = Column(Text(), nullable=True, default="")
    start_date = Column(Date, default=0, nullable=True)
    end_date = Column(Date, default=0, nullable=True)
    start_time = Column(Text(), default=0, nullable=True)
    end_time = Column(Text(), default=0, nullable=True)

    # Relationships
    user_id = Column(Integer, ForeignKey("user.id"))
    created_by = relationship("User", back_populates="schedules")

    frame_id = Column(Integer, ForeignKey("frame.id"))
    frame = relationship("Frame", back_populates="schedules")


# Pydantic models...
class ScheduleBase(TweetFrameBase):
    name: str
    type: str
    schedule_type: str
    status: str
    settings: dict
    message: Optional[str]
    start_date: date
    end_date: date
    start_time: str
    end_time: str
    frame_id: int


class ScheduleResponse(IDModelMixin, DateTimeModelMixin, ScheduleBase):
    is_active: bool


class ScheduleCreate(ScheduleBase):
    frame_id: int
    is_active: bool = Field(default=True)


class ScheduleCreateResponse(IDModelMixin, DateTimeModelMixin, ScheduleCreate):
    pass


class ScheduleUpdate(TweetFrameBase):
    # name = Optional[str]
    # type: Optional[str]
    # schedule_type: Optional[str]
    # status: Optional[str]
    # settings: Optional[dict]
    # message: Optional[str]
    # start_date: Optional[date]
    # end_date: Optional[date]
    # start_time: Optional[str]
    # end_time: Optional[str]
    # is_active = Optional[bool]
    # frame_id: Optional[int]
    pass


class ScheduleUpdateResponse(IDModelMixin, DateTimeModelMixin, ScheduleUpdate):
    pass
