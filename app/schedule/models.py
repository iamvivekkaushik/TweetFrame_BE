from datetime import date
from typing import Optional

from pydantic import Field
from sqlalchemy import Column, Text, Date, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import JSONType

from app.database.core import Base
from app.enums import FrameType, ScheduleType, ScheduleStatus
from app.models import TweetFrameBase, BaseIdMixin, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
class Schedule(BaseIdMixin, Base):
    name = Column(String(length=320), nullable=False)
    type = Column(String(length=20), default=FrameType.FREE, nullable=False)
    schedule_type = Column(
        String(length=20), default=ScheduleType.ONE_TIME, nullable=False
    )
    status = Column(String(length=20), default=ScheduleStatus.CREATED, nullable=False)
    settings = Column(JSONType(), nullable=False, default={})
    message = Column(Text(), nullable=True, default="")
    start_date = Column(Date, default=0, nullable=True)
    end_date = Column(Date, default=0, nullable=True)
    start_time = Column(String(length=20), default=0, nullable=True)
    end_time = Column(String(length=20), default=0, nullable=True)

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


class ScheduleResponse(DateTimeModelMixin, ScheduleBase, IDModelMixin):
    is_active: bool


class ScheduleCreate(ScheduleBase):
    user_id: Optional[int]
    frame_id: int
    is_active: bool = Field(default=True)


class ScheduleCreateResponse(DateTimeModelMixin, ScheduleCreate, IDModelMixin):
    pass


class ScheduleUpdate(TweetFrameBase):
    name: Optional[str]
    type: Optional[str]
    schedule_type: Optional[str]
    status: Optional[str]
    settings: Optional[dict]
    message: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    start_time: Optional[str]
    end_time: Optional[str]
    frame_id: Optional[int]
    is_active: Optional[bool]


class ScheduleUpdateResponse(DateTimeModelMixin, ScheduleUpdate, IDModelMixin):
    pass
