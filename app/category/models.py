from typing import Optional
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from app.database.core import Base
from app.models import TweetFrameBase, BaseIdMixin, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
class Category(BaseIdMixin, Base):
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=True)
    icon = Column(URLType(), nullable=True)

    # Relationship
    frames = relationship("Frame", back_populates="category")
    sub_categories = relationship("SubCategory", back_populates="category")


# Pydantic models...
class CategoryBase(TweetFrameBase):
    name: str
    slug: Optional[str]


class CategoryResponse(DateTimeModelMixin, CategoryBase, IDModelMixin):
    pass


class CategoryCreate(CategoryBase):
    slug: str


class FileCreateResponse(DateTimeModelMixin, CategoryCreate, IDModelMixin):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryUpdateResponse(DateTimeModelMixin, CategoryUpdate, IDModelMixin):
    pass
