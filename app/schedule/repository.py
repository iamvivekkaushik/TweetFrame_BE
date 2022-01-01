from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_, true

from app.database.repository import BaseRepository
from app.enums import ScheduleStatus
from app.schedule.models import Schedule, ScheduleBase


class ScheduleRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Schedule, model_base=ScheduleBase)

    def all_active_schedules(self) -> List[Schedule]:
        query = self.session.query(Schedule).filter(
            or_(
                self.model.status == ScheduleStatus.CREATED.value,
                self.model.status == ScheduleStatus.IN_PROGRESS.value
            ),
            self.model.is_active == true())

        return query.all()
