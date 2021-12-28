from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database.core import get_db
from app.plan.models import PlanCreate, PlanCreateResponse, Plan
from app.plan.repository import PlanRepository
from app.user.jwt import get_current_superuser

plan_router = APIRouter()


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
