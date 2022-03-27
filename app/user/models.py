from typing import List, Optional

from pydantic import Field
from sqlalchemy import Column, Text, String, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import JSONType

from app.database.core import Base
from app.models import TweetFrameBase, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
class User(Base):
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True, index=True)
    account_id = Column(String(length=320), unique=True, index=True, nullable=False)
    oauth_name = Column(String(length=100), index=True, nullable=False)
    access_token = Column(String(length=100), unique=True, nullable=False)
    access_secret = Column(String(length=100), unique=True, nullable=False)
    expires_at = Column(Integer, nullable=True)
    email = Column(String(length=320), nullable=True)
    full_name = Column(String(length=320), nullable=True)
    image = Column(Text, nullable=True)  # This will be updated on every login
    original_image = Column(
        Text, nullable=True
    )  # This will contain our copy of original image
    username = Column(String(length=150), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    timezone = Column(String(length=100), nullable=True)
    twitter_response = Column(JSONType(), nullable=True)
    is_superuser = Column(Boolean, default=False, nullable=False)

    # Relationship...
    social_login = relationship("SocialLogin", back_populates="created_by")
    purchases = relationship("Purchase", back_populates="created_by")
    frames = relationship("Frame", back_populates="created_by")
    schedules = relationship("Schedule", back_populates="created_by")

    def filterable_fields():
        return ["is_superuser"]

    def searchable_fields():
        return ["full_name"]


# Pydantic models...
class UserBase(TweetFrameBase):
    email: Optional[str]
    full_name: Optional[str]
    image: Optional[str]
    original_image: Optional[str]
    username: str
    description: Optional[str]
    timezone: Optional[str]


class UserResponse(DateTimeModelMixin, UserBase, IDModelMixin):
    account_id: str
    is_superuser: bool


class UserPublicResponse(TweetFrameBase):
    full_name: Optional[str]
    image: Optional[str]
    original_image: Optional[str]
    username: str
    description: Optional[str]


class UserDashboardResponse(TweetFrameBase):
    full_name: str
    image: str
    original_image: str
    username: str
    followers: int
    is_superuser: bool
    profile: str


class UserPaginate(TweetFrameBase):
    items: List[UserDashboardResponse]
    current: int
    next_page: Optional[int] = Field(None, alias="next")
    total_results: int
    total_pages: int


class UserCreate(UserBase):
    account_id: str
    oauth_name: Optional[str] = Field("Twitter")
    access_token: str
    access_secret: str
    expires_at: Optional[int] = None
    twitter_response: dict


class UserUpdate(UserBase):
    account_id: Optional[str]
    access_token: Optional[str]
    access_secret: Optional[str]
    email: Optional[str]
    full_name: Optional[str]
    image: Optional[str]
    original_image: Optional[str]
    username: Optional[str]
    description: Optional[str]
    timezone: Optional[str]


class UserSuperAdminUpdate(TweetFrameBase):
    is_superuser: Optional[bool]


class UserDB(UserBase):
    account_id: str
    twitter_response: dict
