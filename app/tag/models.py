from typing import Optional

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.core import Base
from app.models import TweetFrameBase, BaseIdMixin, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
class Tag(BaseIdMixin, Base):
    name = Column(String(255), nullable=False, unique=True)

    # Relationship
    # frames = relationship("AssocTagFrames", back_populates="tags")


# Pydantic models...
class TagBase(TweetFrameBase):
    name: str


class TagResponse(DateTimeModelMixin, TagBase, IDModelMixin):
    pass


class TagCreate(TagBase):
    pass


class TagCreateResponse(DateTimeModelMixin, TagCreate, IDModelMixin):
    pass


class TagUpdate(TagBase):
    pass


class TagUpdateResponse(DateTimeModelMixin, TagUpdate, IDModelMixin):
    pass
