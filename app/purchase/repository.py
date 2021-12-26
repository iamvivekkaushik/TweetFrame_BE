from sqlalchemy.orm import Session

from app.purchase.models import Purchase, PurchaseBase
from app.database.repository import BaseRepository


class PurchaseRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Purchase, model_base=PurchaseBase)
