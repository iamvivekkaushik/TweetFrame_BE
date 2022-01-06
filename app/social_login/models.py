from typing import Optional

from app.models import TweetFrameBase
from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.core import Base
from app.models import BaseIdMixin, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
class SocialLogin(BaseIdMixin, Base):
    request_token = Column(Text(), unique=True, nullable=False)
    request_secret = Column(Text(), nullable=False)
    request_verifier = Column(Text(), nullable=True)
    access_token = Column(Text(), nullable=True)
    access_secret = Column(Text(), nullable=True)

    # Relationships
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    created_by = relationship("User", back_populates="social_login")


# response Model
class SocialLoginBase(TweetFrameBase):
    request_token: str
    request_secret: str
    request_verifier: str
    access_token: str
    access_secret: str


class SocialLoginCreate(SocialLoginBase):
    request_verifier: Optional[str]
    access_token: Optional[str]
    access_secret: Optional[str]


class SocialLoginUpdate(SocialLoginCreate):
    request_token: Optional[str]
    request_secret: Optional[str]


class RequestTokenCreate(TweetFrameBase):
    oauth_callback: str


class RequestTokenResponse(TweetFrameBase):
    request_token: str
    auth_url: str


class AccessTokenCreate(TweetFrameBase):
    request_token: str
    verifier: str
