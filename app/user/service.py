from sqlalchemy.orm import Session

from fastapi_users.jwt import generate_jwt
from fastapi_users.manager import VERIFY_USER_TOKEN_AUDIENCE, UserInactive
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.config import jwt_authentication, VERIFICATION_TOKEN_SECRET
from app.user.models import UserCreate, User, UserUpdate
from app.user.repository import UserRepository


def login_create_user(db: Session, user_create: UserCreate):
    user_repo = UserRepository(db)
    account_id = user_create.account_id
    try:
        user = user_repo.get_by_oauth_account(account_id)

        print("USER FOUND")
        # user found
        user_update = UserUpdate(**user_create.__dict__)
        user = user_repo.update(user.id, user_update)
        token = request_verify(user)
        return token
    except NoResultFound as e:
        print("=======================")
        print("Result not found, user creating ...")
        print("=======================")
        # User doesn't exist, create it
        user = user_repo.create(user_create)
        print("USER CREATED")
        print(user)
        token = request_verify(user)
        return token


def request_verify(user: User) -> str:
    """
    Verify user and generate jwt token
    """
    print("GENERATING USER TOKEN")
    if not user.is_active:
        raise UserInactive()

    token_data = {
        "user_id": str(user.id),
        "username": user.username,
        "account_id": user.account_id,
        "aud": VERIFY_USER_TOKEN_AUDIENCE,
    }
    token = generate_jwt(
        token_data,
        str(VERIFICATION_TOKEN_SECRET),
        jwt_authentication.lifetime_seconds,
    )
    return token
