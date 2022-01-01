from typing import List

from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import Purchase
from app.database.core import get_db
from app.enums import ScheduleType, FrameType
from app.frame import service as frame_service
from app.frame.models import FrameResponse, FrameCreate, FrameUpdate
from app.frame.repository import FrameRepository
from app.purchase.models import PurchaseUpdate
from app.purchase.repository import PurchaseRepository
from app.user.jwt import get_current_user
from app.user.models import User

frame_router = APIRouter()


@frame_router.get(
    "",
    response_model=List[FrameResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_frames(db: Session = Depends(get_db)):
    """
    Get all frames.
    """
    try:
        frame_repo = FrameRepository(db)
        frames = frame_repo.get_all_frames()
        for frame in frames:
            frame.url = frame_service.create_image_url(frame.url)
        return frames
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@frame_router.post(
    "", response_model=FrameResponse, status_code=status.HTTP_201_CREATED
)
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
        purchase_repo = PurchaseRepository(db)
        purchase: Purchase = purchase_repo.get_active_purchase(user)

        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No active purchase found for user",
            )

        remaining_custom_frames = purchase.remaining_custom_frames
        if not user.is_superuser and remaining_custom_frames <= 0:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="No more custom frames allowed. Please Upgrade your plan.",
            )

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

        remaining_custom_frames -= 1
        purchase_repo.update(
            object_id=purchase.id,
            obj_in=PurchaseUpdate(remaining_custom_frames=remaining_custom_frames),
        )
        return frame
    finally:
        if hasattr(frame, "file"):
            frame.file.close()


@frame_router.patch(
    "/{frame_id}", response_model=FrameResponse, status_code=status.HTTP_200_OK
)
async def update_frame(
    frame_id: int,
    name: str = Form(None),
    frame_type: FrameType = Form(None),
    schedule_type: ScheduleType = Form(None),
    settings: dict = Form(None),
    is_public: bool = Form(None),
    frame: UploadFile = File(None),
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

        frame_update = FrameUpdate(
            name=name,
            url=file_path,
            type=frame_type.value,
            schedule_type=schedule_type.value,
            settings=settings,
            is_public=is_public,
        )

        frame_repo = FrameRepository(db)
        frame = frame_repo.update(object_id=frame_id, obj_in=frame_update)
        return frame
    finally:
        if hasattr(frame, "file"):
            frame.file.close()
