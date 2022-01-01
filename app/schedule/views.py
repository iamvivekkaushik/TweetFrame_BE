from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from starlette import status

from app import Purchase
from app.database.core import get_db
from app.purchase.models import PurchaseUpdate
from app.purchase.repository import PurchaseRepository
from app.schedule.job_handler import handle_schedule
from app.schedule.models import (
    ScheduleResponse,
    ScheduleCreate,
    ScheduleUpdateResponse,
    ScheduleUpdate,
)
from app.schedule.repository import ScheduleRepository
from app.scheduler import scheduler
from app.user.jwt import get_current_user
from app.user.models import User

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
    try:
        purchase_repo = PurchaseRepository(db)
        purchase: Purchase = purchase_repo.get_active_purchase(user)

        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No active purchase found for user",
            )

        remaining_active_schedules = purchase.remaining_active_schedules
        if not user.is_superuser and remaining_active_schedules <= 0:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Active schedules limit reached. Please Upgrade your plan.",
            )

        schedule_repo = ScheduleRepository(session=db)
        data.user_id = user.id
        schedule = schedule_repo.create(data)

        scheduler.add_job(
            func=handle_schedule,
            kwargs={"schedule_id": schedule.id},
            max_instances=1,
            id=str(schedule.id),
            replace_existing=True,
        )

        remaining_active_schedules -= 1
        purchase_repo.update(
            object_id=purchase.id,
            obj_in=PurchaseUpdate(
                remaining_active_schedules=remaining_active_schedules
            ),
        )
        return schedule
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


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
