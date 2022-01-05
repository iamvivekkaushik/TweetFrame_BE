from sqlalchemy.orm import Session

from app.database.repository import BaseRepository
from app.file.models import File, FileBase


class FileRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=File, model_base=FileBase)
