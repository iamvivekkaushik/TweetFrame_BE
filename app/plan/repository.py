from sqlalchemy.orm import Session

from app.plan.models import Plan, PlanBase
from app.database.repository import BaseRepository


class PlanRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Plan, model_base=PlanBase)
