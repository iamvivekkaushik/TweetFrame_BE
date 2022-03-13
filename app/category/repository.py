from typing import Union, Dict, Any

from fastapi import Query
from sqlalchemy.orm import Session

from app.category.models import Category, CategoryBase, CategoryUpdate
from app.database.repository import BaseRepository
from app.file.repository import FileRepository


class CategoryRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Category, model_base=CategoryBase)

    def get_by_slug(self, category_slug: str) -> Category:
        query: Query = self.session.query(self.model)
        query = query.filter(self.model.slug == category_slug)
        return query.first()

    def update(
        self, *, object_id: int, obj_in: Union[CategoryUpdate, Dict[str, Any]]
    ) -> Category:
        db_obj = self.get(object_id)

        obj_data = db_obj.__dict__

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                # logger.debug(field, update_data[field])
                setattr(db_obj, field, update_data[field])

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)

        if db_obj.icon:
            icon_url = db_obj.icon
            file_repo = FileRepository(session=self.session)
            file_repo.set_to_inactive(url=icon_url)

        return db_obj
