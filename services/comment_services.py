from models.comment import CommentModel
from models.task import TaskModel
from models.member import MemberModel
from schemas.comment import CommentCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
def handle_create_comment(task_id: int, comment: CommentCreate,user_id: int, db: Session):
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
    new_comment = CommentModel(
        task_id = task_id,
        author_id = user_id,
        content = comment.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def handle_get_comments(task_id: int, user_id: int, db: Session):
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
    return db.query(CommentModel).filter(CommentModel.task_id == task_id).all()