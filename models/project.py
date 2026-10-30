from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base

class ProjectModel(Base):
    __tablename__ = "research_projects"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    name = Column(
        String(200),
        nullable=False,
    )
    description = Column(
        Text,
        nullable=True,
    )
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    owner = relationship("UserModel", back_populates="owned_projects")

    members = relationship("MemberModel", back_populates="project", cascade="all, delete-orphan")

    tasks = relationship("TaskModel", back_populates="project", cascade="all, delete-orphan")