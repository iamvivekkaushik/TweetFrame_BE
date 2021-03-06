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

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

# Database
DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)

# Twitter API Keys
TWITTER_API_KEY: str = config("TWITTER_API_KEY")
TWITTER_API_SECRET: str = config("TWITTER_API_SECRET")

# Backblaze B2
B2_BUCKET_NAME: str = config("B2_BUCKET_NAME")
B2_KEY_ID: str = config("B2_KEY_ID")
B2_APP_KEY: str = config("B2_APP_KEY")
B2_ENDPOINT: str = config("B2_ENDPOINT")
CDN_ENDPOINT: str = config("CDN_ENDPOINT")

# Spaces
S3_BUCKET_NAME: str = config("S3_BUCKET_NAME")
S3_ACCESS_KEY_ID: str = config("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY: str = config("S3_SECRET_ACCESS_KEY")
S3_ENDPOINT: str = config("S3_ENDPOINT")

# Discord
DISCORD_APP_ID: str = config("DISCORD_APP_ID")
DISCORD_CLIENT_SECRET: str = config("DISCORD_CLIENT_SECRET")
DISCORD_PUBLIC_KEY: str = config("DISCORD_PUBLIC_KEY")
DISCORD_TOKEN: str = config("DISCORD_TOKEN")
