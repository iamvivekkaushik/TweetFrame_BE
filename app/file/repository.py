from sqlalchemy.orm import Session
from fastapi import Query
from app.database.repository import BaseRepository
from app.file.models import File, FileBase


class FileRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=File, model_base=FileBase)

    def get_by_url(self, url) -> File:
        query: Query = self.session.query(self.model)
        query = query.filter(self.model.url == url)
        return query.first()

    def set_to_inactive(self, url) -> None:
        query: Query = self.session.query(self.model)
        query = query.filter(self.model.url == url)
        file: File = query.first()

        if file:
            file.is_active = False
            self.session.add(file)
            self.session.commit()
