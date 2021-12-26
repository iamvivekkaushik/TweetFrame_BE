from typing import Optional

from fastapi import Depends, Request
from fastapi_users import FastAPIUsers, BaseUserManager
from fastapi_users.db import SQLAlchemyUserDatabase

from app.config import (
    auth_backends,
    jwt_authentication,
    RESET_PASSWORD_TOKEN_SECRET,
    VERIFICATION_TOKEN_SECRET,
)
from app.user.models import (
    get_user_db,
    UserBase,
    UserDB,
    UserCreate,
    UserUpdate,
)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


fastapi = FastAPIUsers(
    get_user_manager,
    auth_backends,
    UserBase,
    UserCreate,
    UserUpdate,
    UserDB,
)


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = VERIFICATION_TOKEN_SECRET

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


# provides /login and /logout
auth_router = fastapi.get_auth_router(
    backend=jwt_authentication, requires_verification=False
)

# provides /register for user sign up
register_router = fastapi.get_register_router()


# provides routes to manage user
# provides /request-verify-token and /verify
verify_router = fastapi.get_verify_router()

user_router = fastapi.get_users_router(requires_verification=False)

# Dependencies
current_active_user = fastapi.current_user(active=True)
