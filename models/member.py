from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from db.database import Base
from .enums import MemberRole

class MemberModel(Base):
    __tablename__ = "research_members"
    project_id = Column(
        Integer,
        ForeignKey("research_projects.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    role = Column(
        Enum(MemberRole),
        default=MemberRole.MEMBER,
        nullable=False,
    )
    joined_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    project = relationship("ProjectModel", back_populates="members")

    user = relationship("UserModel", back_populates="memberships")