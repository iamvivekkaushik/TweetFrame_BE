from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import Query
from sqlalchemy import true

from app.plan.repository import PlanRepository
from app.user.models import User
from app.purchase.models import Purchase, PurchaseBase, PurchaseCreate
from app.database.repository import BaseRepository


class PurchaseRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Purchase, model_base=PurchaseBase)

    def get_active_purchase(self, user: User) -> Purchase:
        query: Query = self.session.query(self.model).filter(
            self.model.user_id == user.id, self.model.is_active == true()
        )
        return query.first()

    def set_free_plan(self, user: User) -> Purchase:
        plan_repo = PlanRepository(self.session)

        plan = plan_repo.get_free_plan()
        if plan is None:
            raise Exception("Plan not found")

        purchase_create = PurchaseCreate(
            name=plan.name,
            remaining_custom_frames=plan.max_custom_frames,
            remaining_frame_usage=plan.max_frame_usage,
            remaining_active_schedules=plan.max_active_schedules,
            start_date=datetime.now(),
            end_date=None,
            start_time="",
            end_time=None,
            user_id=user.id,
            plan_id=plan.id,
            payment_id=user.account_id,
            amount_paid=0.0,
            currency="USD",
        )
        purchase = self.create(purchase_create)
        return purchase
