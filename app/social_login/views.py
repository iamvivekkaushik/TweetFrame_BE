from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import app.social_login.service as social_service
from app.database.core import get_db
from app.social_login.models import (
    RequestTokenResponse,
    AccessTokenCreate,
)

social_router = APIRouter(
    tags=["social_login"],
)


@social_router.get(
    "/twitter/request_token",
    response_model=RequestTokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_twitter_request_url(db: Session = Depends(get_db)):
    """
    Generate the oauth request token and url
    """
    social_login = social_service.generate_request_token(db)

    if social_login is None:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Unable to generate request token",
        )

    request_token = social_login.request_token
    auth_url = "https://api.twitter.com/oauth/authorize?oauth_token={}".format(
        request_token
    )
    response = RequestTokenResponse(request_token=request_token, auth_url=auth_url)
    return response


@social_router.post(
    "/twitter/verify",
    status_code=status.HTTP_201_CREATED,
)
async def verify_twitter_token(body: AccessTokenCreate, db: Session = Depends(get_db)):
    """
    Verify the oauth token and verifier
    """
    # get the request secret from database for the given request token
    social_login = social_service.verify_token(db, body)

    if social_login is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token/Verifier is invalid or expired.",
        )

    # generate login session token
    session_token = social_service.generate_session_token(db, social_login)
    return session_token
