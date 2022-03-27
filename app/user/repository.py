from typing import List
from fastapi import Query
from sqlalchemy import true
from sqlalchemy.orm import Session

from app.database.repository import BaseRepository
from app.purchase.repository import PurchaseRepository
from app.user.models import (
    User,
    UserBase,
    UserCreate,
)


class UserRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=User, model_base=UserBase)

    def get_all_users(self) -> List[User]:
        """
        Get all users
        """
        query: Query = self.session.query(self.model).filter(
            self.model.is_active == true()
        )
        return query.all()
    

    def get_by_username(self, username) -> User:
        """
        Get user by username
        """
        query: Query = self.session.query(self.model).filter(
            self.model.username == username, self.model.is_active == true()
        )
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
        user = super().create(object_in=object_in)

        purchase_repo = PurchaseRepository(self.session)
        purchase_repo.set_free_plan(user=user)
        return user
