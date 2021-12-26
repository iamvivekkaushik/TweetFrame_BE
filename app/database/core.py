import functools
import re
import traceback
from datetime import datetime

import databases
from loguru import logger
from sqlalchemy import create_engine, Column, Boolean, DateTime, MetaData
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.config import DATABASE_URL

database = databases.Database(DATABASE_URL)

# Use check same thread for sqlite only
# engine = create_engine(str(DATABASE_URL))

# Use for some other database (ex. postgresql)
engine = create_engine(str(DATABASE_URL), pool_pre_ping=True)

SessionLocal: sessionmaker = sessionmaker(bind=engine)


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)  # noqa
    return "_".join([x.lower() for x in names if x])


def resolve_attr(obj, attr, default=None):
    """Attempts to access attr via dotted notation, returns none if attr does
    not exist."""
    try:
        return functools.reduce(getattr, attr.split("."), obj)
    except AttributeError:
        return default


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class CustomBase(object):
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)


Base = declarative_base(cls=CustomBase)
Base.metadata = MetaData(naming_convention=naming_convention)
Base.metadata.create_all(engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error(traceback.print_exc())
    finally:
        db.close()
