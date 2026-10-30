from db.database import Base
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
class CommentModel(Base):
    __tablename__ = "comments"
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    task_id = Column(
        Integer,
        ForeignKey("research_tasks.id", ondelete="CASCADE"),
        nullable=False
    )
    author_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    content = Column(
        Text,
        nullable=False
    )
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )

    task = relationship("TaskModel", back_populates="comments")

    author = relationship("UserModel", back_populates="comments")