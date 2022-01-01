from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.config import SECRET_KEY
from app.user.jwt import generate_jwt, VERIFY_USER_TOKEN_AUDIENCE
from app.user.models import UserCreate, User
from app.user.repository import UserRepository


def login_create_user(db: Session, user_create: UserCreate):
    user_repo = UserRepository(db)
    account_id = user_create.account_id
    try:
        user = user_repo.get_by_oauth_account(account_id)

        print("USER FOUND")
        # user found
        user_create.original_image = None
        user_create.image = None
        user = user_repo.update(object_id=user.id, obj_in=user_create)
        token = generate_token(user)
        return token, user
    except NoResultFound as e:
        print("=======================")
        print("User not found, creating ...")
        print("=======================")
        # User doesn't exist, create it
        user = user_repo.create(user_create)
        token = generate_token(user)
        return token, user


def generate_token(user: User) -> str:
    """
    Verify user and generate jwt token
    """
    print("GENERATING USER TOKEN")
    if not user.is_active:
        raise Exception("User is not active")

    token_data = {
        "user_id": str(user.id),
        "username": user.username,
        "account_id": user.account_id,
        "aud": VERIFY_USER_TOKEN_AUDIENCE,
    }
    token = generate_jwt(
        token_data,
        SECRET_KEY,
        36000,
    )
    return token


def refresh_user_profile(db: Session, user: User, user_create: UserCreate):
    user_repo = UserRepository(db)
    user = user_repo.update(object_id=user.id, obj_in=user_create)
    return user
