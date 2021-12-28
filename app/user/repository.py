from fastapi import Query
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.database.repository import BaseRepository
from app.user.models import (
    User,
    UserBase,
    UserCreate,
    UserUpdate,
)


class UserRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=User, model_base=UserBase)

    def get(self, object_id: UUID4) -> User:
        """Returns a single model object using its ID."""
        query: Query = self.session.query(self.model).filter(self.model.id == object_id)
        return query.one()

    def get_by_oauth_account(self, account_id) -> User:
        """
        Get user by oauth account id
        """
        query: Query = self.session.query(self.model).filter(
            self.model.account_id == account_id
        )
        return query.one()

    def create(self, object_in: UserCreate) -> User:
        obj_in_data = object_in.dict(exclude_unset=True)

        db_obj = self.model(**obj_in_data)

        print("===============")
        print(f"db_obj: Creating User")
        print("===============")

        self.session.add(db_obj)
        self.session.commit()
        # self.session.refresh(db_obj)
        print("User created")
        return db_obj

    def update(self, object_id: UUID4, obj_in: UserUpdate) -> User:
        db_obj = self.get(object_id)

        obj_data = db_obj.__dict__

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)

        return db_obj
