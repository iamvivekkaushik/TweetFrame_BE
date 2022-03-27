from typing import Optional

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from app.database.core import Base
from app.models import TweetFrameBase, BaseIdMixin, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
class SubCategory(BaseIdMixin, Base):
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=True)
    icon = Column(URLType(), nullable=True)

    # Relationship
    frames = relationship("Frame", back_populates="sub_category")

    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="sub_categories")


# Pydantic models...
class SubCategoryBase(TweetFrameBase):
    name: str
    slug: Optional[str]


class SubCategoryResponse(DateTimeModelMixin, SubCategoryBase, IDModelMixin):
    category_id: int


class SubCategoryCreate(SubCategoryBase):
    category_id: int
    slug: str


class FileCreateResponse(DateTimeModelMixin, SubCategoryCreate, IDModelMixin):
    pass


class SubCategoryUpdate(SubCategoryBase):
    name: Optional[str]
    category_id: Optional[int]


class CategoryUpdateResponse(DateTimeModelMixin, SubCategoryUpdate, IDModelMixin):
    pass
