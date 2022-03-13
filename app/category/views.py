from typing import List, Optional

from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.category.models import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
)
from app.category.repository import CategoryRepository
from app.database.core import get_db
from app.user.jwt import get_current_superuser
from app.utils import helper, b2_helper

category_router = APIRouter()


@category_router.get(
    "",
    response_model=List[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_categories(db: Session = Depends(get_db)):
    """
    Get all Categories.
    """
    try:
        category_repo = CategoryRepository(db)
        categories = category_repo.get_all()

        return categories
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@category_router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(get_current_superuser),
    ],
)
async def create_category(
    name: str = Form(...),
    slug: str = Form(...),
    icon: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Create a new category.
    """
    try:
        file_size = helper.validate_file(icon)

        # save the frame to backblaze
        file_path = b2_helper.upload_file(
            db=db, file=icon, path="category", file_size=file_size
        )

        category_create: CategoryCreate = CategoryCreate(
            name=name,
            slug=slug,
            icon=file_path,
        )

        category_repo = CategoryRepository(db)
        category = category_repo.create(object_in=category_create)

        return category
    finally:
        if icon and hasattr(icon, "file"):
            icon.file.close()


@category_router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_superuser)],
)
async def update_sub_category(
    category_id: int,
    name: Optional[str] = Form(None),
    slug: Optional[str] = Form(None),
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
                db=db, file=icon, path="category", file_size=file_size
            )

        category_update = CategoryUpdate(name=name, slug=slug, icon=file_path)

        category_repo = CategoryRepository(db)
        category = category_repo.update(object_id=category_id, obj_in=category_update)
        return category
    finally:
        if icon and hasattr(icon, "file"):
            icon.file.close()
