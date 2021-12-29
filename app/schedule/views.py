from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from starlette import status

from app.database.core import get_db
from app.schedule.models import (
    ScheduleResponse,
    ScheduleCreate,
    ScheduleUpdateResponse,
    ScheduleUpdate,
)

from app.schedule.repository import ScheduleRepository
from app.user.models import UserBase, User
from app.user.jwt import get_current_user

schedule_router = APIRouter()


@schedule_router.get("", response_model=List[ScheduleResponse])
def get_all_schedule(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Returns all the schedule available for a user."""
    schedule_repo = ScheduleRepository(session=db)
    schedule_list = schedule_repo.get_all(user=user)
    return schedule_list


@schedule_router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get a single Schedule using Object ID."""
    try:
        schedule_repo = ScheduleRepository(session=db)
        schedule = schedule_repo.get(schedule_id, user=user)
        return schedule
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The Schedule you're looking for doesn't exist.",
        )


@schedule_router.post("", response_model=ScheduleResponse)
def create_schedule(
    data: ScheduleCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Handle request to create a new Schedule."""
    data.user_id = user.id

    schedule_repo = ScheduleRepository(session=db)
    schedule = schedule_repo.create(data)
    return schedule


@schedule_router.patch("/{schedule_id}", response_model=ScheduleUpdateResponse)
def update_schedule(
    schedule_id: int,
    schedule_in: ScheduleUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Handle request to update a Schedule."""
    schedule_in.user_id = user.id

    schedule_repo = ScheduleRepository(session=db)
    schedule = schedule_repo.update(
        object_id=schedule_id, obj_in=schedule_in, user=user
    )
    return schedule
