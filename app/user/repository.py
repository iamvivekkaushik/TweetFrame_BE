from sqlalchemy.orm import Session

from app.database.repository import BaseRepository
from app.user.models import User, UserBase


class UserRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=User, model_base=UserBase)
