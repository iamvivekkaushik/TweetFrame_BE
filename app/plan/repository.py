from typing import List

from fastapi import Query
from sqlalchemy import true
from sqlalchemy.orm import Session

from app.database.repository import BaseRepository
from app.plan.models import Plan, PlanBase


class PlanRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Plan, model_base=PlanBase)

    def get_all_plans(self, skip=0, limit=100) -> List[Plan]:
        """Returns all the available Plans"""
        query: Query = (
            self.session.query(self.model)
            .filter(self.model.is_active == true())
            .offset(skip)
            .limit(limit)
        )
        return query.all()
