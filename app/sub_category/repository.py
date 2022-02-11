from typing import Dict, Any, Union

from fastapi import Query
from sqlalchemy.orm import Session

from app.database.repository import BaseRepository
from app.file.repository import FileRepository
from app.sub_category.models import SubCategoryBase, SubCategory, SubCategoryUpdate


class SubCategoryRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=SubCategory, model_base=SubCategoryBase)

    def get_by_category_id(self, category_id: int) -> list:
        query: Query = self.session.query(self.model)
        query = query.filter(self.model.category_id == category_id)
        return query.all()

    def update(
        self, *, object_id: int, obj_in: Union[SubCategoryUpdate, Dict[str, Any]]
    ) -> SubCategory:
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
