from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from starlette import status

from app.database.core import get_db
from app.schedule.models import ScheduleResponse, ScheduleCreate

from app.schedule.repository import ScheduleRepository
from app.user.models import UserBase
from app.user.views import current_active_user

schedule_router = APIRouter()


@schedule_router.get("", response_model=List[ScheduleResponse])
def get_schedule_list(
    db: Session = Depends(get_db),
    user: UserBase = Depends(current_active_user),
):
    """Returns all the schedule available for a user."""
    schedule_repo = ScheduleRepository(session=db)
    schedule_list = schedule_repo.get_all(user)
    return schedule_list


@schedule_router.get("/{object_id}", response_model=ScheduleResponse)
def get_schedule(
    object_id: int,
    db: Session = Depends(get_db),
    user: UserBase = Depends(current_active_user),
):
    """Get's a single Schedule object using Object ID."""
    try:
        schedule_repo = ScheduleRepository(session=db)
        schedule = schedule_repo.get(object_id, user)
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
    user: UserBase = Depends(current_active_user),
):
    """Handle request to create a new Schedule."""
    data.user_id = user.id

    schedule_repo = ScheduleRepository(session=db)
    schedule = schedule_repo.create(data)
    return schedule
