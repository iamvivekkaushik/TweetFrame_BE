import os
from typing import List

from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from starlette import status

from app.config import BASE_DIR
from app.database.core import get_db
from app.enums import ScheduleType, FrameType
from app.frame.models import FrameResponse, FrameCreate
from app.frame.repository import FrameRepository
from app.frame import service as frame_service
from app.user.jwt import get_current_user
from app.user.models import User

frame_router = APIRouter()


@frame_router.post("", response_model=FrameResponse, status_code=status.HTTP_201_CREATED)
async def create_frame(
    name: str = Form(...),
    frame_type: FrameType = Form(...),
    schedule_type: ScheduleType = Form(...),
    settings: dict = Form({}),
    is_public: bool = Form(...),
    frame: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Create a new frame.
    """
    try:
        frame_service.validate_file(frame)
        # save the frame to /media/frames/
        file_path = frame_service.save_image(frame)

        if not user.is_superuser:
            frame_type = FrameType.CUSTOM

        frame_create = FrameCreate(
            name=name,
            url=file_path,
            type=frame_type.value,
            schedule_type=schedule_type.value,
            settings=settings,
            is_public=is_public,
            user_id=user.id,
        )

        frame_repo = FrameRepository(db)
        frame = frame_repo.create(object_in=frame_create)
        return frame
    finally:
        if hasattr(frame, "file"):
            frame.file.close()
