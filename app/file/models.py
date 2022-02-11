from typing import Optional

from sqlalchemy import Column, Integer, String, Text

from app.database.core import Base
from app.models import TweetFrameBase, BaseIdMixin, IDModelMixin, DateTimeModelMixin


# SQLAlchemy Model
class File(BaseIdMixin, Base):
    name = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    path = Column(Text, nullable=False)
    mimetype = Column(String(50), nullable=False)
    size = Column(Integer, nullable=False)


# Pydantic models...
class FileBase(TweetFrameBase):
    name: str
    url: str
    path: str
    mimetype: str
    size: int


class FileResponse(DateTimeModelMixin, FileBase, IDModelMixin):
    pass


class FileCreate(FileBase):
    pass


class FileCreateResponse(DateTimeModelMixin, FileBase, IDModelMixin):
    pass


class FileUpdate(FileBase):
    name: Optional[str]
    url: Optional[str]
    path: Optional[str]
    mimetype: Optional[str]
    size: Optional[int]


class FileUpdateResponse(DateTimeModelMixin, FileBase, IDModelMixin):
    pass
