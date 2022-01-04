import logging
import os

from databases import DatabaseURL
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

log = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Project Configurations
PROJECT_NAME: str = os.environ.get("PROJECT_NAME", default="TweetFrames")
API_PREFIX: str = os.environ.get("API_PREFIX", default="/api/v1")
JWT_TOKEN_PREFIX: str = os.environ.get("JWT_TOKEN_PREFIX", default="Bearer")
VERSION: str = os.environ.get("VERSION", default="0.0.0")

ALLOWED_HOSTS: str = os.environ.get(
    "ALLOWED_HOSTS",
    default="*"
)
ENVIRONMENT: str = os.environ.get("ENVIRONMENT", default="development")
DOMAIN: str = os.environ.get("DOMAIN", default="localhost")
SECRET_KEY: str = os.environ.get("SECRET_KEY")
DEBUG: bool = os.environ.get("DEBUG", default=True)

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

# Database
DATABASE_URL: DatabaseURL = DatabaseURL(os.environ.get("DB_CONNECTION"))

# Twitter API Keys
TWITTER_API_KEY: str = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET: str = os.environ.get("TWITTER_API_SECRET")
