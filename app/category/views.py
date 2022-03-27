from typing import List

from fastapi import APIRouter, Depends, HTTPException
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
    category_create: CategoryCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new category.
    """
    category_repo = CategoryRepository(db)
    category = category_repo.create(object_in=category_create)

    return category


@category_router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_superuser)],
)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a category.
    """
    category_repo = CategoryRepository(db)
    category = category_repo.update(object_id=category_id, obj_in=category_update)
    return category
