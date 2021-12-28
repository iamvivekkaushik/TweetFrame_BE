from fastapi import APIRouter, Depends, status

from app.user.jwt import get_current_user
from app.user.models import User, UserResponse

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
