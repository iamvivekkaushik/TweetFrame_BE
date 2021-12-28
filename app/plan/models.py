from typing import Optional

from sqlalchemy import Column, Text, Integer, Float, String
from sqlalchemy.orm import relationship

from app.database.core import Base
from app.models import TweetFrameBase, BaseIdMixin, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
class Plan(BaseIdMixin, Base):
    name = Column(String(30), nullable=False)
    max_custom_frames = Column(Integer, default=0, nullable=False)
    max_frame_usage = Column(Integer, default=0, nullable=False)
    max_active_schedules = Column(Integer, default=0, nullable=False)
    price = Column(Float, default=0.0, nullable=True)
    currency = Column(String(length=5), default="USD", nullable=False)

    # Relationship...
    purchases = relationship("Purchase", back_populates="plan")


# Pydantic models...
class PlanBase(TweetFrameBase):
    name: str
    max_custom_frames: int
    max_frame_usage: int
    max_active_schedules: int
    price: float
    currency: str


class PlanResponse(IDModelMixin, DateTimeModelMixin, PlanBase):
    pass


class PlanCreate(PlanBase):
    pass


class PlanCreateResponse(IDModelMixin, DateTimeModelMixin, PlanCreate):
    pass


class PlanUpdate(TweetFrameBase):
    # name = Optional[str]
    # max_custom_frames = Optional[int]
    # max_frame_usage = Optional[int]
    # max_active_schedules = Optional[int]
    # is_active = Optional[bool]
    pass


class PlanUpdateResponse(IDModelMixin, DateTimeModelMixin, PlanUpdate):
    pass