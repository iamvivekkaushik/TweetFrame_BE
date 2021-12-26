from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database.core import get_db
import app.social_login.service as social_service
from app.social_login.models import RequestTokenCreate, AccessTokenGenerate, \
    SocialLoginResponse
from app.social_login.repository import SocialLoginRepository

social_router = APIRouter(
    tags=["social_login"],
)


@social_router.get("", response_model=SocialLoginResponse,
                   status_code=status.HTTP_200_OK)
def get_social_tokens(db: Session = Depends(get_db)):
    """
    Get the social tokens
    """
    social_login_repo = SocialLoginRepository(session=db)
    social_login = social_login_repo.get(1)

    if social_login is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Either token or verifier is invalid/expired.",
        )

    return social_login


@social_router.get(
    "/twitter/request_token",
    response_model=RequestTokenCreate,
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
    response = RequestTokenCreate(request_token=request_token,
                                  auth_url=auth_url)
    return response


@social_router.post("/twitter/verify", response_model=SocialLoginResponse,
                    status_code=status.HTTP_201_CREATED)
def verify_twitter_token(body: AccessTokenGenerate, db: Session = Depends(get_db)):
    """
    Verify the oauth token and verifier
    """
    # get the request secret from database for the given request token
    response = social_service.verify_token(db, body)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either token or verifier is invalid/expired.",
        )

    # Save api key
    # generate login token
    return response
