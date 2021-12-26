from sqlalchemy.orm import Session

from app.schedule.models import Schedule, ScheduleBase
from app.database.repository import BaseRepository


class ScheduleRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Schedule, model_base=ScheduleBase)
