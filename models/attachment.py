from datetime import datetime, timezone
from db.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class AttachmentModel(Base):
    __tablename__ = "attachments"

    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True, 
        index=True
    )
    task_id = Column(
        Integer,
        ForeignKey("research_tasks.id", ondelete="CASCADE"),
        nullable=False,
    )
    uploaded_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    file_name = Column(
        String(255), 
        nullable=False
    )
    file_url = Column(
        Text, 
        nullable=False
    )
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    task = relationship("TaskModel", back_populates="attachments")

    uploader = relationship("UserModel", back_populates="attachments")