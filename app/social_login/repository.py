from sqlalchemy.orm import Session

from app.social_login.models import SocialLogin, SocialLoginBase
from app.database.repository import BaseRepository
from fastapi import Query


class SocialLoginRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=SocialLogin, model_base=SocialLoginBase)

    def get_by_request_token(self, request_token: str) -> SocialLogin:
        """Returns a single model object using its ID."""
        query: Query = self.session.query(self.model).filter(
            self.model.request_token == request_token
        )
        return query.one()

    def get_by_access_token(self, access_token: str) -> SocialLogin:
        """Returns a single model object using its ID."""
        query: Query = self.session.query(self.model).filter(
            self.model.access_token == access_token
        )
        return query.first()
