from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.core import get_db
from app.social_login.repository import SocialLoginRepository
from app.twitter import service as twitter_service
from app.user import service as user_service
from app.user.jwt import get_current_user
from app.user.models import User, UserResponse, UserCreate

user_router = APIRouter()


@user_router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_user_profile(user: User = Depends(get_current_user)):
    """
    Get the current user profile
    """
    return user


@user_router.get(
    "/refresh",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_twitter_token(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    """
    Verify the oauth token and verifier
    """
    # get the request secret from database for the given request token
    social_login_repo = SocialLoginRepository(db)
    social_login = social_login_repo.get_by_access_token(user.access_token)
    print(social_login)
    user_create: UserCreate = twitter_service.verify_credentials(social_login)

    user = user_service.refresh_user_profile(db, user, user_create)
    return user
