from sqlalchemy import ForeignKey, Column, Integer

from app.database.core import Base


# Associative table between Workspace <-> User
class AssocTagFrames(Base):
    tag_id = Column(
        Integer,
        ForeignKey(
            "tag.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    frames_id = Column(
        Integer,
        ForeignKey(
            "frame.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
