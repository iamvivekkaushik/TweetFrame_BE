from datetime import date

from sqlalchemy import Column, Text, Date, Integer, ForeignKey, String, Float
from sqlalchemy.orm import relationship

from app.database.core import Base
from app.models import TweetFrameBase, BaseIdMixin, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
class Purchase(BaseIdMixin, Base):
    name = Column(String(length=320), nullable=False)
    remaining_custom_frames = Column(Integer, default=0, nullable=False)
    remaining_frame_usage = Column(Integer, default=0, nullable=False)
    remaining_active_schedules = Column(Integer, default=0, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    start_time = Column(Text(), nullable=True)
    end_time = Column(Text(), nullable=True)
    amount_paid = Column(Float, default=0.0, nullable=False)
    currency = Column(String(length=15), nullable=False)
    payment_id = Column(String(length=320), unique=True, nullable=False)
    payment_status = Column(String(length=320), nullable=True)
    payment_method = Column(String(length=320), nullable=True)
    billing_address = Column(Text, nullable=True)
    shipping_address = Column(Text, nullable=True)

    # Relationships
    user_id = Column(Integer, ForeignKey("user.id"))
    created_by = relationship("User", back_populates="purchases")

    plan_id = Column(Integer, ForeignKey("plan.id"))
    plan = relationship("Plan", back_populates="purchases")


# Pydantic models...
class PurchaseBase(TweetFrameBase):
    name: str
    remaining_custom_frames: int
    remaining_frame_usage: int
    remaining_active_schedules: int
    start_date: date
    end_date: date
    start_time: str
    end_time: str


class PurchaseResponse(IDModelMixin, DateTimeModelMixin, PurchaseBase):
    is_active: bool


class PurchaseCreate(PurchaseBase):
    pass


class PurchaseCreateResponse(IDModelMixin, DateTimeModelMixin, PurchaseCreate):
    pass


class PurchaseUpdate(TweetFrameBase):
    # name = Optional[str]
    # remaining_custom_frames: Optional[int]
    # remaining_frame_usage: Optional[int]
    # remaining_active_schedules: Optional[int]
    # start_date: Optional[date]
    # end_date: Optional[date]
    # start_time: Optional[str]
    # end_time: Optional[str]
    # is_active = Optional[bool]
    pass


class PurchaseUpdateResponse(IDModelMixin, DateTimeModelMixin, PurchaseUpdate):
    pass
