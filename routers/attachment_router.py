from typing import List
from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.attachment import AttachmentResponse
from services.attachment_services import handle_create_attachment, handle_get_attachment
from dependencies.auth_dependencies import handle_get_user
from models.user import UserModel

router = APIRouter(prefix="/tasks/{task_id}/attachments", tags=["Attachments"])

@router.post("", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
def create_attachment(task_id: int, file: UploadFile = File(...), current_user: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_create_attachment(task_id=task_id, file=file, user_id=current_user["user_id"], db=db)

@router.get("", response_model=List[AttachmentResponse])
def get_attachments(task_id: int, current_user: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_get_attachment(task_id=task_id, user_id=current_user["user_id"], db=db)