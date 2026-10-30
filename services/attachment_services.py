from models.attachment import AttachmentModel
from models.task import TaskModel
from models.member import MemberModel
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
import uuid
import os
import shutil
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def handle_create_attachment(task_id: int, file: UploadFile, user_id: int, db:Session):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nhiệm vụ không tồn tại"
        )
    is_member = db.query(MemberModel).filter(MemberModel.project_id == task.project_id, MemberModel.user_id == user_id).first()
    if is_member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải là thành viên của đề tài chứa nhiệm vụ này"
        )
    original_file_name = file.filename
    unique_file_name = f"{uuid.uuid4()}_{original_file_name}"
    file_path = os.path.join(UPLOAD_DIR, unique_file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    file_url = f"/uploads/{unique_file_name}"

    new_attachment = AttachmentModel(
        task_id = task_id,
        uploaded_by=user_id,
        file_name = original_file_name,
        file_url = file_url
    )
    db.add(new_attachment)
    db.commit()
    db.refresh(new_attachment)
    return new_attachment

def handle_get_attachment(task_id: int, user_id: int, db: Session):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nhiệm vụ không tồn tại"
        )
    is_member = db.query(MemberModel).filter(MemberModel.project_id == task.project_id, MemberModel.user_id == user_id).first()
    if is_member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải là thành viên của đề tài chứa nhiệm vụ này"
        )
    return db.query(AttachmentModel).filter(AttachmentModel.task_id == task_id).all()