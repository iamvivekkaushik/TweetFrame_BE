from fastapi import FastAPI
from loguru import logger
from app.config import DATABASE_URL


async def connect_to_db(app: FastAPI) -> None:
    database_ = app.state.database
    if not database_.is_connected:
        logger.info("Connecting to database")
        await database_.connect()
        logger.info("Connection established")
    else:
        logger.info("Database was already Connected")


async def close_db_connection(app: FastAPI) -> None:
    database_ = app.state.database
    if database_.is_connected:
        logger.info("Closing connection to database")
        await database_.disconnect()
        logger.info("Connection closed")
    else:
        logger.info("Database connection was already closed")
