import json

import requests
import sentry_sdk
from requests_oauthlib import OAuth1

from app.config import TWITTER_API_KEY, TWITTER_API_SECRET
from app.frame.models import Frame
from app.social_login.models import SocialLogin, SocialLoginCreate, \
    SocialLoginUpdate
from app.user.models import UserCreate, User
from app.utils.helper import generate_frame_image


def get_oauth_header(user: User) -> OAuth1:
    oauth: OAuth1 = OAuth1(
        TWITTER_API_KEY,
        TWITTER_API_SECRET,
        user.access_token,
        user.access_secret,
    )

    return oauth


def generate_request_token(oauth_callback: str) -> SocialLoginCreate:
    # obtain request token
    oauth = OAuth1(TWITTER_API_KEY, TWITTER_API_SECRET)

    response = requests.post(
        url="https://api.twitter.com/oauth/request_token",
        data={"oauth_callback": oauth_callback},
        auth=oauth,
    )
    body = response.content.decode()
    status_code = response.status_code

    if status_code != 200:
        raise Exception(body, status_code)

    request_token = body.split("&")[0].split("=")[1]
    request_secret = body.split("&")[1].split("=")[1]

    social_login_object = SocialLoginCreate(
        request_token=request_token, request_secret=request_secret
    )
    return social_login_object


def exchange_access_token(
    social_login: SocialLogin, verifier: str
) -> SocialLoginUpdate:
    request_token = social_login.request_token
    request_secret = social_login.request_secret

    oauth = OAuth1(
        TWITTER_API_KEY,
        TWITTER_API_SECRET,
        request_token,
        request_secret,
        verifier=verifier,
    )

    # obtain access token
    response = requests.post(
        url="https://api.twitter.com/oauth/access_token", auth=oauth
    )

    body = response.content.decode()
    status_code = response.status_code

    print("----------------------------------")
    print(body)
    print("----------------------------------")
    if status_code != 200:
        raise Exception(body, status_code)

    access_token_key = body.split("&")[0].split("=")[1]
    access_token_secret = body.split("&")[1].split("=")[1]

    social_obj = SocialLoginUpdate(
        request_verifier=verifier,
        access_token=access_token_key,
        access_secret=access_token_secret,
    )
    return social_obj


def verify_credentials(social_login: SocialLogin) -> UserCreate:
    oauth: OAuth1 = OAuth1(
        TWITTER_API_KEY,
        TWITTER_API_SECRET,
        social_login.access_token,
        social_login.access_secret,
    )

    response = requests.get(
        url="https://api.twitter.com/1.1/account/verify_credentials.json", auth=oauth
    )

    body = response.content.decode()
    status_code = response.status_code

    if status_code != 200:
        raise Exception(body, status_code)

    # convert bytes to string
    body = json.loads(body)
    profile_image: str = body["profile_image_url_https"]
    profile_image = profile_image.replace("_normal", "_400x400")

    user_obj = {
        "oauth_name": "Twitter",
        "access_token": social_login.access_token,
        "access_secret": social_login.access_secret,
        "account_id": body["id_str"],
        "email": None,
        "full_name": body["name"],
        "image": profile_image,
        "original_image": profile_image,
        "username": body["screen_name"],
        "description": body["description"],
        "timezone": body["time_zone"],
        "twitter_response": body,
    }
    return UserCreate(**user_obj)


def update_profile_image(user: User, frame: Frame) -> dict:
    oauth = get_oauth_header(user)
    base64_image = generate_frame_image(user, frame)

    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(
        url="https://api.twitter.com/1.1/account/update_profile_image.json",
        data={"image": base64_image},
        auth=oauth,
        headers=headers,
    )

    body = response.content.decode()
    status_code = response.status_code

    if status_code != 200:
        print(body)
        sentry_sdk.capture_exception(Exception(body, status_code))
        raise Exception(body, status_code)

    # parse json string
    body = json.loads(body)
    return body
