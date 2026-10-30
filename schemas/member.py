from pydantic import BaseModel, ConfigDict
from typing import Optional
from models.enums import MemberRole
from datetime import datetime

class MemberBase(BaseModel):
    role: Optional[MemberRole] = MemberRole.MEMBER

class MemberCreate(MemberBase):
    project_id: int
    user_id: int

class MemberUpdate(BaseModel):
    role: MemberRole

class MemberResponse(MemberBase):
    project_id: int
    user_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)