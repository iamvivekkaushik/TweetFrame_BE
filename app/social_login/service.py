import requests
from fastapi import HTTPException, status
from requests_oauthlib import OAuth1
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.config import TWITTER_API_KEY, TWITTER_API_SECRET
from app.social_login.models import SocialLogin, AccessTokenGenerate, \
    SocialLoginUpdate, SocialLoginCreate
from app.social_login.repository import SocialLoginRepository


def generate_request_token(db: Session):
    # obtain request token
    oauth = OAuth1(TWITTER_API_KEY, TWITTER_API_SECRET)

    response = requests.post(
        url="https://api.twitter.com/oauth/request_token", auth=oauth
    )
    body = response.content
    status_code = response.status_code

    if status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=body)

    request_token = body.decode().split("&")[0].split("=")[1]
    request_secret = body.decode().split("&")[1].split("=")[1]

    social_login_object = SocialLoginCreate(request_token=request_token,
                                            request_secret=request_secret)
    social_login_repo = SocialLoginRepository(session=db)
    social_login = social_login_repo.create(social_login_object)
    return social_login


def verify_token(db, request_body: AccessTokenGenerate):
    social_login_repo = SocialLoginRepository(session=db)

    request_token = request_body.request_token
    verifier = request_body.verifier

    # get the social login object from the database
    try:
        social_login: SocialLogin = social_login_repo.get_by_request_token(request_token)
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request token"
        )

    request_secret = social_login.request_secret

    # obtain access token
    oauth = OAuth1(
        TWITTER_API_KEY,
        TWITTER_API_SECRET,
        request_token,
        request_secret,
        verifier=verifier,
    )
    response = requests.post(
        url="https://api.twitter.com/oauth/access_token", auth=oauth
    )

    body = response.content
    status_code = response.status_code

    if status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Some Error Occurred while exchanging the request token.")

    access_token_key = body.decode().split("&")[0].split("=")[1]
    access_token_secret = body.decode().split("&")[1].split("=")[1]

    social_obj_in = SocialLoginUpdate(
        request_verifier=verifier,
        access_token=access_token_key,
        access_secret=access_token_secret,
    )

    social_login = social_login_repo.update(object_id=social_login.id,
                                            obj_in=social_obj_in)
    return social_login
