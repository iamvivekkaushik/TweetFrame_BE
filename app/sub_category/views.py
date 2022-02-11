from typing import List, Optional

from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from app.database.core import get_db
from app.sub_category.models import (
    SubCategoryResponse,
    SubCategoryCreate,
    SubCategoryUpdate,
)
from app.sub_category.repository import SubCategoryRepository
from app.user.jwt import get_current_superuser
from app.utils import b2_helper
from app.utils import helper

sub_category_router = APIRouter()


@sub_category_router.get(
    "",
    response_model=List[SubCategoryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_sub_categories_by_id(
    category_id: Optional[int] = Query(None), db: Session = Depends(get_db)
):
    """
    Get all sub categories.
    """
    try:
        sub_category_repo = SubCategoryRepository(db)
        if category_id:
            sub_categories = sub_category_repo.get_by_category_id(category_id)
        else:
            sub_categories = sub_category_repo.get_all()

        return sub_categories
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@sub_category_router.post(
    "",
    response_model=SubCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(get_current_superuser),
    ],
)
async def create_sub_category(
    name: str = Form(...),
    category_id: int = Form(...),
    icon: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Create a new sub category.
    """
    try:
        file_size = helper.validate_file(icon)

        # save the frame to backblaze
        file_path = b2_helper.upload_file(
            db=db, file=icon, path="sub_category", file_size=file_size
        )

        sub_category_create: SubCategoryCreate = SubCategoryCreate(
            name=name,
            icon=file_path,
            category_id=category_id,
        )

        sub_category_repo = SubCategoryRepository(db)
        sub_category = sub_category_repo.create(object_in=sub_category_create)

        return sub_category
    finally:
        if icon and hasattr(icon, "file"):
            icon.file.close()


@sub_category_router.patch(
    "/{sub_category_id}",
    response_model=SubCategoryResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_superuser)],
)
async def update_sub_category(
    sub_category_id: int,
    name: Optional[str] = Form(None),
    icon: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    """
    Update a sub category.
    """
    try:
        file_path = None
        if icon:
            file_size = helper.validate_file(icon)

            # save the frame to backblaze
            file_path = b2_helper.upload_file(
                db=db, file=icon, path="sub_category", file_size=file_size
            )

        sub_category_update = SubCategoryUpdate(name=name, icon=file_path)

        sub_category_repo = SubCategoryRepository(db)
        sub_category = sub_category_repo.update(
            object_id=sub_category_id, obj_in=sub_category_update
        )
        return sub_category
    finally:
        if icon and hasattr(icon, "file"):
            icon.file.close()
