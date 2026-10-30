from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AttachmentResponse(BaseModel):
    id: int
    task_id: int
    uploaded_by: int
    file_name: str
    file_url: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
