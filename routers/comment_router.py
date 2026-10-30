from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.comment import CommentCreate, CommentResponse
from services.comment_services import handle_create_comment, handle_get_comments
from dependencies.auth_dependencies import handle_get_user
from models.user import UserModel

router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["Comments"])

@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(task_id: int, comment: CommentCreate, current_user: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_create_comment(task_id=task_id, comment=comment, user_id=current_user["user_id"], db=db)

@router.get("", response_model=List[CommentResponse])
def get_comments(task_id: int, current_user: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_get_comments(task_id=task_id, user_id=current_user["user_id"], db=db)