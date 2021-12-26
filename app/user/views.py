from fastapi_users import FastAPIUsers

from app.config import (
    auth_backends,
    jwt_authentication,
)
from app.user.models import (
    UserBase,
    UserDB,
    UserCreate,
    UserUpdate,
)
from app.user.repository import get_user_manager

fastapi = FastAPIUsers(
    get_user_manager,
    auth_backends,
    UserBase,
    UserCreate,
    UserUpdate,
    UserDB,
)


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
