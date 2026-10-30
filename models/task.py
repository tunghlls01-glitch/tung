from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from .enums import TaskStatus, TaskPriority
class TaskModel(Base):
    __tablename__ = "research_tasks"
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    project_id = Column(
        Integer,
        ForeignKey("research_projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(
        String(200),
        nullable=False,
    )
    description = Column(
        Text,
        nullable=True,
    )
    assignee_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.TODO,
        nullable=False,
    )
    priority = Column(
        Enum(TaskPriority),
        default=TaskPriority.MEDIUM,
        nullable=False,
    )
    due_date = Column(
        DateTime,
        nullable=True,
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    
    project = relationship("ProjectModel", back_populates="tasks")

    assignee = relationship("UserModel", back_populates="assigned_tasks")

    comments = relationship("CommentModel", back_populates="task")

    attachments = relationship("AttachmentModel", back_populates="task")