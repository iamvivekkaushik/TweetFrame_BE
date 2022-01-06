from typing import TypeVar, List, Dict, Any, Union

from fastapi import Query, HTTPException, status
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.core import Base
from app.models import TweetFrameBase
from app.user.models import User

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository:
    def __init__(
        self,
        session: Session,
        model: ModelType,
        model_base,  # This is of type BaseModel of pydantic model
    ) -> None:
        self._session: Session = session
        self.model = model
        self.model_base = model_base

    @property
    def session(self) -> Session:
        return self._session

    def get_all(self, user: User = None, skip=0, limit=100) -> List[ModelType]:
        """Returns all the available objects for a user."""
        query: Query = self.session.query(self.model)

        if user:
            query = query.filter(self.model.user_id == user.id)

        query = query.offset(skip).limit(limit)
        return query.all()

    def get(self, object_id: int, user: User = None) -> ModelType:
        """Returns a single model object using its ID."""
        query: Query = self.session.query(self.model).filter(self.model.id == object_id)

        if user:
            query = query.filter(self.model.user_id == user.id)
        return query.one()

    def create(self, object_in: TweetFrameBase):
        obj_in_data = object_in.dict(exclude_unset=True)

        db_obj = self.model(**obj_in_data)

        logger.debug("===============")
        logger.debug(f"db_obj: {db_obj.__dict__}")
        logger.debug("===============")

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)

        return db_obj

    def update(
        self,
        *,
        object_id: int,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        db_obj = self.get(object_id)

        obj_data = db_obj.__dict__

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                # logger.debug(field, update_data[field])
                setattr(db_obj, field, update_data[field])

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)

        return db_obj

    def delete(self, object_id: int):
        db_obj = self.get(object_id)

        if db_obj:
            self.session.delete(db_obj)
            self.session.commit()
