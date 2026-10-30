from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from db.database import Base
from .enums import UserRole

class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    password_hash = Column(
        String(225),
        nullable=False,
    )
    full_name = Column(
        String(100),
        nullable=False,
    )
    role = Column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False,
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    owned_projects = relationship("ProjectModel", back_populates="owner", cascade="all, delete-orphan")

    memberships = relationship("MemberModel", back_populates="user", cascade="all, delete-orphan")

    assigned_tasks = relationship("TaskModel", back_populates="assignee")

    comments = relationship("CommentModel", back_populates="author")

    attachments = relationship("AttachmentModel", back_populates="uploader")