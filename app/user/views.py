from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.database.core import get_db
from app.database.service import common_parameters, search_filter_sort_paginate
from app.social_login.repository import SocialLoginRepository
from app.twitter import service as twitter_service
from app.user import service as user_service
from app.user.jwt import get_current_superuser, get_current_user
from app.user.models import (
    User,
    UserDashboardResponse,
    UserPaginate,
    UserResponse,
    UserCreate,
    UserPublicResponse,
    UserSuperAdminUpdate,
)
from app.user.repository import UserRepository

user_router = APIRouter()


@user_router.get(
    "",
    response_model=UserPaginate,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_current_superuser),
    ],
)
async def get_users(
    db: Session = Depends(get_db), common: dict = Depends(common_parameters)
):
    """
    Get all users
    """
    try:
        user_repository = UserRepository(db)

        data = search_filter_sort_paginate(repository=user_repository, **common)

        for user in data["items"]:
            response = user.twitter_response
            user.followers = response["followers_count"]
            user.profile = "https://twitter.com/{}".format(user.username)

        return data
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Account Doesn't exist or inactive",
        )


@user_router.get(
    "/public/{username}",
    response_model=UserPublicResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_profile(username: str, db: Session = Depends(get_db)):
    """
    Get the user profile
    """
    try:
        user_repository = UserRepository(db)

        user = user_repository.get_by_username(username)
        return user
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Account Doesn't exist or inactive",
        )


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
async def refresh_profile(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    """
    Verify the oauth token and verifier
    """
    # get the request secret from database for the given request token
    social_login_repo = SocialLoginRepository(db)
    social_login = social_login_repo.get_by_access_token(user.access_token)
    user_create: UserCreate = twitter_service.verify_credentials(social_login)

    user = user_service.refresh_user_profile(db, user, user_create)
    return user


@user_router.get(
    "/superuser",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def superuser(db: Session = Depends(get_db)):
    """
    make vivek superuser
    """
    user_repository = UserRepository(db)

    user = user_repository.get_by_username("iamvivekkaushik")
    super_admin_update = UserSuperAdminUpdate(is_superuser=True)
    user_repository.update(object_id=user.id, obj_in=super_admin_update)
    return user


@user_router.get(
    "/superuser/{username}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(get_current_superuser),
    ],
)
async def make_superuser(username: str, db: Session = Depends(get_db)):
    """
    Make someone a superuser
    """
    user_repository = UserRepository(db)

    user = user_repository.get_by_username(username=username)
    super_admin_update = UserSuperAdminUpdate(is_superuser=True)
    user_repository.update(object_id=user.id, obj_in=super_admin_update)
    return user
