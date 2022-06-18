from typing import List

from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from starlette import status

from app import Purchase
from app.category.repository import CategoryRepository
from app.database.core import get_db
from app.enums import ScheduleType, FrameType
from app.frame.models import FrameResponse, FrameCreate, FrameUpdate
from app.frame.repository import FrameRepository
from app.purchase.models import PurchaseUpdate
from app.purchase.repository import PurchaseRepository
from app.sub_category.repository import SubCategoryRepository
from app.user.jwt import get_current_user
from app.user.models import User
from app.user.repository import UserRepository
from app.utils import b2_helper, helper

frame_router = APIRouter()


@frame_router.get(
    "",
    response_model=List[FrameResponse],
    status_code=status.HTTP_200_OK,
)
async def get_frames(
    category_slug: str = Query(None),
    sub_category_slug: str = Query(None),
    category_id: int = Query(None),
    sub_category_id: int = Query(None),
    db: Session = Depends(get_db),
):
    """
    Get all frames.
    """
    try:
        if category_slug:
            category_repo = CategoryRepository(db)
            category_id = category_repo.get_by_slug(category_slug).id
        if sub_category_slug:
            sub_category_repo = SubCategoryRepository(db)
            sub_category_id = sub_category_repo.get_by_slug(sub_category_slug).id

        frame_repo = FrameRepository(db)
        frames = frame_repo.get_by_category(category_id, sub_category_id)

        return frames
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@frame_router.get(
    "/popular",
    response_model=List[FrameResponse],
    status_code=status.HTTP_200_OK,
)
async def get_frames(
    db: Session = Depends(get_db),
):
    """
    Get popular frames.
    """
    try:
        frame_repo = FrameRepository(db)
        frames = frame_repo.get_by_popularity()
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
    category_id: int = Form(...),
    sub_category_id: int = Form(...),
    frame: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Create a new frame.
    """
    try:
        file_size = helper.validate_file(frame)
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

        # save the frame to backblaze
        file_path = b2_helper.upload_frame(db, frame, file_size)

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
            category_id=category_id,
            sub_category_id=sub_category_id,
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
    category_id: int = Form(None),
    sub_category_id: int = Form(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Update a frame.
    """
    try:
        file_path = None
        if frame:
            file_size = helper.validate_file(frame)

            # save the frame to backblaze
            file_path = b2_helper.upload_frame(db, frame, file_size)

        if not user.is_superuser:
            frame_type = FrameType.CUSTOM

        frame_data = {
            "name": name,
            "url": file_path,
            "is_public": is_public,
            "category_id": category_id,
            "sub_category_id": sub_category_id,
        }

        if frame_type:
            frame_data["type"] = frame_type.value
        if schedule_type:
            frame_data["schedule_type"] = schedule_type.value

        for key, value in dict(frame_data).items():
            if value is None:
                del frame_data[key]

        frame_update = FrameUpdate(**frame_data)

        frame_repo = FrameRepository(db)
        frame = frame_repo.update(object_id=frame_id, obj_in=frame_update)
        return frame
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Frame not found"
        )
    finally:
        if hasattr(frame, "file"):
            frame.file.close()


@frame_router.get(
    "/public/{username}",
    response_model=List[FrameResponse],
    status_code=status.HTTP_200_OK,
)
async def get_public_frames(username: str, db: Session = Depends(get_db)):
    """
    Get all public frames by a user.
    """
    try:
        user_repo = UserRepository(db)
        user: User = user_repo.get_by_username(username)

        frame_repo = FrameRepository(db)
        frames = frame_repo.get_all_frames(user=user)

        return frames
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with provided username not found.",
        )
