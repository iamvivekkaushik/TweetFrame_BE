from datetime import datetime, timezone

from pydantic import BaseModel, BaseConfig, Field, validator
from sqlalchemy import Column, Integer


def convert_datetime_to_real_world(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


# SQLAlchemy model...
class BaseIdMixin(object):
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    def filterable_fields():
        return []

    def searchable_fields():
        return []


# Pydantic model...
class IDModelMixin(BaseModel):
    id: int = Field(0, alias="id")


class DateTimeModelMixin(BaseModel):
    created_at: datetime = Field(..., alias="created_at")
    updated_at: datetime = Field(..., alias="updated_at")

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


class TweetFrameBase(BaseModel):
    class Config(BaseConfig):
        # allow_population_by_field_name = True
        # json_encoders = {datetime: convert_datetime_to_real_world}
        orm_mode = True
