from typing import List, Optional

from fastapi import APIRouter, Form, Depends, HTTPException, Query
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

sub_category_router = APIRouter()


@sub_category_router.get(
    "",
    response_model=List[SubCategoryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_sub_categories_by_cateogry(
    category_id: Optional[int] = Query(None),
    category_slug: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Get all sub categories.
    """
    try:
        sub_category_repo = SubCategoryRepository(db)
        if category_id:
            sub_categories = sub_category_repo.get_by_category_id(category_id)
        elif category_slug:
            sub_categories = sub_category_repo.get_by_slug(category_slug)
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
    sub_category_create: SubCategoryCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new sub category.
    """
    sub_category_repo = SubCategoryRepository(db)
    sub_category = sub_category_repo.create(object_in=sub_category_create)

    return sub_category


@sub_category_router.patch(
    "/{sub_category_id}",
    response_model=SubCategoryResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_superuser)],
)
async def update_sub_category(
    sub_category_id: int,
    sub_category_update: SubCategoryUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a sub category.
    """
    sub_category_repo = SubCategoryRepository(db)
    sub_category = sub_category_repo.update(
        object_id=sub_category_id, obj_in=sub_category_update
    )
    return sub_category
