from typing import Optional, List

from sqlalchemy import Column, Text, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType, JSONType

from app.database.core import Base
from app.enums import FrameType, ScheduleType
from app.models import TweetFrameBase, BaseIdMixin, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
from app.tag.models import TagBase


class Frame(BaseIdMixin, Base):
    name = Column(Text(), nullable=False)
    url = Column(URLType(), nullable=False)
    type = Column(Text(), default=FrameType.FREE, nullable=False)
    schedule_type = Column(Text(), default=ScheduleType.ONE_TIME, nullable=False)
    settings = Column(JSONType(), nullable=False, default={})
    is_public = Column(Boolean, default=False, nullable=False)

    # Relationships
    user_id = Column(Integer, ForeignKey("user.id"))
    created_by = relationship("User", back_populates="frames")

    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="frames")

    sub_category_id = Column(Integer, ForeignKey("sub_category.id"))
    sub_category = relationship("SubCategory", back_populates="frames")

    schedules = relationship("Schedule", back_populates="frame")
    # tags = relationship("AssocTagFrames", back_populates="frames")


# Pydantic models...
class FrameBase(TweetFrameBase):
    name: str
    url: str
    type: str
    schedule_type: str
    settings: Optional[dict]
    is_public: bool
    category_id: int
    sub_category_id: int


class FrameResponse(DateTimeModelMixin, FrameBase, IDModelMixin):
    type: Optional[str]
    category_id: Optional[int]
    sub_category_id: Optional[int]
    tags: Optional[List[TagBase]]


class FrameCreate(FrameBase):
    user_id: Optional[int]
    tags_list: Optional[List[int]]


class FrameCreateResponse(DateTimeModelMixin, FrameCreate, IDModelMixin):
    pass


class FrameUpdate(FrameBase):
    name: Optional[str]
    url: Optional[str]
    type: Optional[str]
    schedule_type: Optional[str]
    settings: Optional[dict]
    is_public: Optional[bool]
    is_active: Optional[bool]
    category_id: Optional[int]
    sub_category_id: Optional[int]


class FrameUpdateResponse(DateTimeModelMixin, FrameUpdate, IDModelMixin):
    pass
