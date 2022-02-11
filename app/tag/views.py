from typing import List

from fastapi import APIRouter, Depends, HTTPException, p
from sqlalchemy.orm import Session
from starlette import status

from app.database.core import get_db
from app.tag.models import TagResponse, TagCreate, TagUpdate, Tag
from app.tag.repository import TagRepository
from app.user.jwt import get_current_superuser

tag_router = APIRouter()


@tag_router.get(
    "",
    response_model=List[TagResponse],
    status_code=status.HTTP_200_OK,
)
async def search_tags(query: str, page=0, db: Session = Depends(get_db)):
    """
    Search all tags.
    """
    try:
        tag_repo = TagRepository(db)
        tags = tag_repo.search(query, skip=page * 20, limit=20)

        return tags
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@tag_router.post(
    "",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_superuser)],
)
async def create_tag(tag_in: TagCreate, db: Session = Depends(get_db)):
    """
    Create a new category.
    """
    tag_repo = TagRepository(db)
    tag: Tag = tag_repo.create(tag_in)
    return tag


@tag_router.patch(
    "/{tag_id}",
    response_model=TagResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_superuser)],
)
async def update_frame(tag_id: int, tag_in: TagUpdate, db: Session = Depends(get_db)):
    """
    Update a tag.
    """
    tag_repo = TagRepository(db)
    tag = tag_repo.update(object_id=tag_id, obj_in=tag_in)
    return tag
