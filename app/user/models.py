from typing import Optional

from fastapi_users import models
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database.core import Base, database
from app.models import TweetFrameBase


# SQLAlchemy Model
class User(Base, SQLAlchemyBaseUserTable):
    full_name = Column(String(length=255), nullable=True)

    # Relationship...
    social_login = relationship("SocialLogin", back_populates="created_by")
    purchases = relationship("Purchase", back_populates="created_by")
    frames = relationship("Frame", back_populates="created_by")
    schedules = relationship("Schedule", back_populates="created_by")


# Pydantic models...
class UserBase(TweetFrameBase, models.BaseUser):
    full_name: Optional[str]


class UserCreate(TweetFrameBase, models.BaseUserCreate):
    full_name: str


class UserUpdate(UserBase, models.BaseUserUpdate):
    pass


class UserDB(UserBase, models.BaseUserDB):
    pass


async def get_user_db():
    users = User.__table__
    yield SQLAlchemyUserDatabase(UserDB, database, users)
