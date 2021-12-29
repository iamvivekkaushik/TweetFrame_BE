from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database.core import get_db
from app.plan.models import (
    PlanCreate,
    PlanCreateResponse,
    Plan,
    PlanResponse,
    PlanUpdateResponse,
    PlanUpdate,
)
from app.plan.repository import PlanRepository
from app.user.jwt import get_current_superuser

plan_router = APIRouter()


@plan_router.get("", response_model=List[PlanResponse], status_code=status.HTTP_200_OK)
def get_all_plans(db: Session = Depends(get_db)):
    """Get all plans."""
    try:
        plan_repo = PlanRepository(session=db)
        plans: List[Plan] = plan_repo.get_all_plans()
        print(plans)
        return plans
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@plan_router.post(
    "",
    response_model=PlanCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_superuser)],
)
def create_plan(plan_in: PlanCreate, db: Session = Depends(get_db)):
    """Creates a new plan."""
    try:
        plan_repo = PlanRepository(session=db)
        plan: Plan = plan_repo.create(plan_in)
        return plan
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@plan_router.patch(
    "/{plan_id}",
    response_model=PlanUpdateResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_superuser)],
)
def update_plan(plan_id: int, plan_in: PlanUpdate, db: Session = Depends(get_db)):
    """Update a new plan."""
    try:
        plan_repo = PlanRepository(session=db)
        plan: Plan = plan_repo.update(object_id=plan_id, obj_in=plan_in)
        return plan
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@plan_router.delete(
    "/{plan_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_superuser)],
)
def update_plan(plan_id: int, db: Session = Depends(get_db)):
    """Update a new plan."""
    try:
        plan_repo = PlanRepository(session=db)
        plan_repo.delete(object_id=plan_id)
        return {"detail": "Plan deleted."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
