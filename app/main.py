import os.path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app import config
from app.api import router as api_router
from app.config import BASE_DIR
from app.database.core import database, get_db
from app.events import app_startup_event_handler, app_stop_event_handler
from app.scheduler import init_scheduler

app = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION)

app.state.database = database

# add middlewares here
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    Gets a new Session from the SessionLocal Pool and closes it at the end of
    each request.
    Also look at app.database.service.py file for its use in dependency
    injection for getting a Repository Object.
    Implementation found at:
    https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-middleware
    """
    try:
        request.state.db = next(get_db())
        response = await call_next(request)
    finally:
        request.state.db.close()

    return response


# here we start/stop connection to the database as the app starts or stops
app.add_event_handler("startup", app_startup_event_handler(app))
app.add_event_handler("shutdown", app_stop_event_handler(app))

# here we add exception handlers
# app.add_exception_handler(HTTPException, http_error_handler)
# app.add_exception_handler(RequestValidationError, http422_error_handler)

# we add all API routes to the Web API framework
app.include_router(api_router, prefix=config.API_PREFIX)


# For media files
app.mount(
    "/media", StaticFiles(directory=os.path.join(BASE_DIR, "media")), name="media"
)

# Start the scheduler
init_scheduler()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
