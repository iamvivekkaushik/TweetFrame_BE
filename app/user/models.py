from typing import Optional

from fastapi_users import models
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import GUID
from pydantic import Field
from sqlalchemy import Column, Text, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import JSONType

from app.database.core import Base, database
from app.models import TweetFrameBase


# SQLAlchemy Model
class User(Base):
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True, index=True)
    oauth_name = Column(String(length=100), index=True, nullable=False)
    access_token = Column(String(length=1024), unique=True, nullable=False)
    expires_at = Column(Integer, nullable=True)
    refresh_token = Column(String(length=1024), nullable=True)
    account_id = Column(String(length=320), index=True, nullable=False)
    account_email = Column(String(length=320), nullable=True)
    full_name = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    original_image = Column(Text, nullable=True)
    username = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    timezone = Column(String(100), nullable=True)
    twitter_response = Column(JSONType(), nullable=True)

    # Relationship...
    social_login = relationship("SocialLogin", back_populates="created_by")
    purchases = relationship("Purchase", back_populates="created_by")
    frames = relationship("Frame", back_populates="created_by")
    schedules = relationship("Schedule", back_populates="created_by")


# Pydantic models...
class UserBase(TweetFrameBase):
    oauth_name: Optional[str] = Field("Twitter")
    access_token: str
    expires_at: Optional[int] = None
    refresh_token: Optional[str] = None
    account_id: str
    account_email: Optional[str]
    full_name: Optional[str]
    image: Optional[str]
    original_image: Optional[str]
    username: str
    description: Optional[str]
    timezone: Optional[str]


class UserCreate(UserBase):
    account_email: Optional[str]
    twitter_response: dict


class UserCreateResponse(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserDB(UserBase, models.BaseUserDB):
    twitter_response: dict


async def get_user_db():
    users = User.__table__
    yield SQLAlchemyUserDatabase(UserDB, database, users)
