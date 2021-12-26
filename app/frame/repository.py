from sqlalchemy.orm import Session

from app.frame.models import Frame, FrameBase
from app.database.repository import BaseRepository


class FrameRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Frame, model_base=FrameBase)
