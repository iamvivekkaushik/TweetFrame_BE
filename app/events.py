from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.database.events import close_db_connection, connect_to_db


def app_startup_event_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch()
    async def start_app() -> None:
        await connect_to_db(app)

    return start_app


def app_stop_event_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app
