from typing import List

from fastapi import Query
from sqlalchemy import true
from sqlalchemy.orm import Session

from app.database.repository import BaseRepository
from app.plan.models import Plan, PlanBase, PlanCreate


class PlanRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Plan, model_base=PlanBase)

    def get_free_plan(self) -> Plan:
        """Returns a Plan by name"""
        try:
            query: Query = (
                self.session.query(self.model)
                .filter(self.model.name == "Free")
                .filter(self.model.is_active == true())
            )
            return query.one()
        except Exception as e:
            plan_create = PlanCreate(
                name="Free",
                price=0,
                max_frame_usage=50,
                max_custom_frames=3,
                max_active_schedules=2,
            )
            return self.create(object_in=plan_create)

    def get_plan_by_name(self, name: str) -> Plan:
        """Returns a Plan by name"""
        query: Query = (
            self.session.query(self.model)
            .filter(self.model.name == name)
            .filter(self.model.is_active == true())
        )
        return query.first()

    def get_all_plans(self, skip=0, limit=100) -> List[Plan]:
        """Returns all the available Plans"""
        query: Query = (
            self.session.query(self.model)
            .filter(self.model.is_active == true())
            .offset(skip)
            .limit(limit)
        )
        return query.all()
