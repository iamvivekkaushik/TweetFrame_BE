from fastapi import Depends
from fastapi import Query
from fastapi_users import BaseUserManager
from fastapi_users.db import SQLAlchemyUserDatabase
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.config import RESET_PASSWORD_TOKEN_SECRET, VERIFICATION_TOKEN_SECRET
from app.database.repository import BaseRepository
from app.user.models import (
    User,
    get_user_db,
    UserBase,
    UserDB,
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


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = VERIFICATION_TOKEN_SECRET


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
