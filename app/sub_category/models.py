from typing import Optional

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from app.database.core import Base
from app.models import TweetFrameBase, BaseIdMixin, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
class SubCategory(BaseIdMixin, Base):
    name = Column(String(255), nullable=False)
    icon = Column(URLType(), nullable=False)

    # Relationship
    frames = relationship("Frame", back_populates="sub_category")

    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="sub_categories")


# Pydantic models...
class SubCategoryBase(TweetFrameBase):
    name: str
    icon: str


class SubCategoryResponse(DateTimeModelMixin, SubCategoryBase, IDModelMixin):
    pass


class SubCategoryCreate(SubCategoryBase):
    category_id: int


class FileCreateResponse(DateTimeModelMixin, SubCategoryCreate, IDModelMixin):
    pass


class SubCategoryUpdate(SubCategoryBase):
    name: Optional[str]
    icon: Optional[str]


class CategoryUpdateResponse(DateTimeModelMixin, SubCategoryUpdate, IDModelMixin):
    pass
