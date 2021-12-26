from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.social_login.models import (
    SocialLogin,
    AccessTokenGenerate,
    SocialLoginUpdate,
    SocialLoginCreate,
)
from app.social_login.repository import SocialLoginRepository
from app.twitter import service as twitter_service
from app.user.models import UserCreate
from app.user import service as user_service


def generate_request_token(db: Session) -> SocialLogin:
    social_object: SocialLoginCreate = twitter_service.generate_request_token()
    social_login_repo = SocialLoginRepository(session=db)
    social_login = social_login_repo.create(social_object)
    return social_login


def verify_token(db, request_body: AccessTokenGenerate) -> SocialLogin:
    try:
        social_login_repo = SocialLoginRepository(session=db)
        request_token = request_body.request_token
        verifier = request_body.verifier

        # get the social login object from the database
        try:
            social_login: SocialLogin = social_login_repo.get_by_request_token(
                request_token
            )
        except NoResultFound as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request token"
            )

        # get the access token from twitter
        social_obj: SocialLoginUpdate = twitter_service.exchange_access_token(
            social_login, verifier
        )
        social_login = social_login_repo.update(
            object_id=social_login.id, obj_in=social_obj
        )
        return social_login
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def generate_jwt_token(db):
    request_token = "SnMmhgAAAAABVFMqAAABffbjl9o"
    social_repo: SocialLoginRepository = SocialLoginRepository(db)
    social_login = social_repo.get_by_request_token(request_token)

    user_create = twitter_service.verify_credentials(social_login)
    user = user_service.login_create_user(db, user_create)
    return user
