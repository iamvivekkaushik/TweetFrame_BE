import logging
import os
from typing import List

from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

log = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = Config(".env")

# Project Configurations
PROJECT_NAME: str = config("PROJECT_NAME", default="TweetFrames")
API_PREFIX = "/api/v1"
JWT_TOKEN_PREFIX = "Token"
VERSION = "0.0.0"
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)
ENVIRONMENT: str = config("ENVIRONMENT", default="development")
DOMAIN: str = config("DOMAIN", default="localhost")
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
DEBUG: bool = config("DEBUG", cast=bool, default=False)

RESET_PASSWORD_TOKEN_SECRET: Secret = config("RESET_PASSWORD_TOKEN_SECRET", cast=Secret)
VERIFICATION_TOKEN_SECRET: Secret = config("VERIFICATION_TOKEN_SECRET", cast=Secret)

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")


# Database
DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

# Twitter API Keys
TWITTER_API_KEY: str = config("TWITTER_API_KEY", default="")
TWITTER_API_SECRET: str = config("TWITTER_API_SECRET", default="")
TWITTER_ACCESS_TOKEN: str = config("TWITTER_ACCESS_TOKEN", default="")
TWITTER_ACCESS_TOKEN_SECRET: str = config("TWITTER_ACCESS_TOKEN_SECRET", default="")
