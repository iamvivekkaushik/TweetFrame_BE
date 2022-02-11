from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from starlette import status

from app.database.core import get_db
from app.purchase.models import (
    PurchaseResponse,
    PurchaseUpdate,
)
from app.purchase.repository import PurchaseRepository
from app.user.jwt import get_current_user, get_current_superuser
from app.user.models import User

purchase_router = APIRouter()


@purchase_router.get("", response_model=List[PurchaseResponse])
def get_all_purchases(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Returns all the Purchases available for a user."""
    purchase_repo = PurchaseRepository(session=db)
    purchase_list = purchase_repo.get_all(user=user)
    return purchase_list


@purchase_router.get("/active", response_model=PurchaseResponse)
def get_active_purchase(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get current active purchase for the user."""
    purchase_repo = PurchaseRepository(session=db)
    purchase = purchase_repo.get_active_purchase(user=user)

    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have an active purchase.",
        )
    return purchase


@purchase_router.get("/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get a single Purchase using Object ID."""
    try:
        purchase_repo = PurchaseRepository(session=db)
        purchase = purchase_repo.get(purchase_id, user=user)
        return purchase
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have access to this purchase.",
        )


@purchase_router.post("/freePlan", response_model=PurchaseResponse)
def set_free_plan(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create a new Purchase."""
    purchase_repo = PurchaseRepository(db)
    active_plan = purchase_repo.get_active_purchase(user)

    if active_plan:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have an active plan.",
        )

    purchase = purchase_repo.set_free_plan(user=user)
    return purchase


@purchase_router.patch(
    "/{purchase_id}",
    response_model=PurchaseResponse,
    dependencies=[Depends(get_current_superuser)],
)
def update_purchase(
    purchase_id: int, purchase_in: PurchaseUpdate, db: Session = Depends(get_db)
):
    """Update a Purchase."""
    try:
        purchase_repo = PurchaseRepository(db)
        purchase = purchase_repo.update(object_id=purchase_id, obj_in=purchase_in)
        return purchase
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid purchase id.",
        )
