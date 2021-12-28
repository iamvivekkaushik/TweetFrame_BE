from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.datastructures import Secret
from starlette.requests import Request

from app.config import SECRET_KEY
from app.database.core import get_db
from app.user.models import User
from app.user.repository import UserRepository

SecretType = Union[str, Secret]
JWT_ALGORITHM = "HS256"
VERIFY_USER_TOKEN_AUDIENCE = "fastapi-users:verify"


def _get_secret_value(secret: SecretType) -> str:
    if isinstance(secret, Secret):
        return str(secret)
    return secret


def generate_jwt(
    data: dict,
    secret: SecretType,
    lifetime_seconds: Optional[int] = None,
    algorithm: str = JWT_ALGORITHM,
) -> str:
    payload = data.copy()
    if lifetime_seconds:
        expire = datetime.utcnow() + timedelta(seconds=lifetime_seconds)
        payload["exp"] = expire
    return jwt.encode(payload, _get_secret_value(secret), algorithm=algorithm)


def decode_jwt(
    encoded_jwt: str,
    secret: SecretType,
    audience: List[str],
) -> Dict[str, Any]:
    return jwt.decode(
        encoded_jwt,
        _get_secret_value(secret),
        audience=audience,
        algorithms=[JWT_ALGORITHM],
    )


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    try:
        token = request.headers.get("Authorization")
        print(request.headers)
        # remove bearer from token
        token = token.split(" ")[1]
        print("==================")
        payload = decode_jwt(token, SECRET_KEY, [VERIFY_USER_TOKEN_AUDIENCE])
        print("==================")
        print("payload", payload)
        print(payload)
        user_repo = UserRepository(db)
        account_id = payload["account_id"]
        valid_upto = payload["exp"]
        print(valid_upto)
        user: User = user_repo.get_by_oauth_account(account_id)

        # if user is not active throw error
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not active",
            )
        return user
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def get_current_superuser(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user.is_superuser:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not a superuser"
    )
