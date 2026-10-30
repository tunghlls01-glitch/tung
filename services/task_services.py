from models.task import TaskModel
from sqlalchemy.orm import Session
from schemas.task import TaskCreate, TaskUpdate
from models.project import ProjectModel
from models.member import MemberModel
from models.user import UserModel
from fastapi import HTTPException, status

def handle_post_task(project_id: int, task: TaskCreate,user_id: int, db: Session):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tồn tại đề tài có id {project_id}"
        )
    user_is_member = db.query(MemberModel).filter(MemberModel.project_id == project_id, MemberModel.user_id == user_id).first()
    if user_is_member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ thành viên của đề tài mới có quyền tạo nhiệm vụ"
        )
    if task.assignee_id is not None:
        assignee = db.query(UserModel).filter(UserModel.id == task.assignee_id).first()
        if assignee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tồn tại user có id {task.assignee_id}",
            )
        assignee = db.query(MemberModel).filter(MemberModel.project_id == project_id, MemberModel.user_id == task.assignee_id).first()
        if assignee is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Người được giao việc (assignee) phải là thành viên trong đề tài",
            )
    new_task = TaskModel(
        project_id = project_id,
        title = task.title,
        description = task.description,
        assignee_id = task.assignee_id,
        status = task.status,
        priority = task.priority,
        due_date = task.due_date,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def handle_get_task_by_project_id(project_id: int,user_id: int,search: str,status_filter: str, priority_filter: str, skip: int, limit: int, assignee_id: int, db:Session):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Không tồn tại đề tài có id {project_id}"
        )
    member = db.query(MemberModel).filter(MemberModel.project_id == project_id, MemberModel.user_id == user_id).first()
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem nhiệm vụ của đề tài này",
        )
    query = db.query(TaskModel).filter(TaskModel.project_id == project_id)
    if search and search.strip():
        query = query.filter(TaskModel.title.ilike(f"%{search.strip()}%"))
    if status_filter:
        query = query.filter(TaskModel.status == status_filter)
    if priority_filter:
        query = query.filter(TaskModel.priority == priority_filter)
    if assignee_id:
        query = query.filter(TaskModel.assignee_id == assignee_id)
    return query.offset(skip).limit(limit).all()

def handle_get_by_id(task_id: int, user_id: int, db: Session):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Không tồn tại nhiệm vụ đề tài có id {task_id}"
        )
    member = db.query(MemberModel).filter(MemberModel.project_id == task.project_id, MemberModel.user_id == user_id).first()
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem nhiệm vụ của đề tài này"
        )
    
    return task

def handle_update_task(task_id:int, task_new: TaskUpdate, user_id:int, db: Session):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tồn tại nhiệm vụ đề tài có id {task_id} cần cập nhật"
        )
    project = db.query(ProjectModel).filter(ProjectModel.id == task.project_id).first()
    is_owner = project.owner_id == user_id
    is_assignee = task.assignee_id == user_id
    if not (is_owner or is_assignee):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER đề tài hoặc người được giao việc mới có quyền cập nhật nhiệm vụ này",
        )
    if task_new.assignee_id is not None:
        if not is_owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Chỉ OWNER mới có quyền chuyển giao nhiệm vụ cho người khác"
            )
        assingnee_is_member = db.query(MemberModel).filter(MemberModel.project_id == task.project_id, MemberModel.user_id == task_new.assignee_id).first()
        if assingnee_is_member is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Người được giao việc phải là thành viên trong đề tài",
            )
        task.assignee_id = task_new.assignee_id
    if task_new.title is not None:
        task.title = task_new.title
    if task_new.description is not None:
        task.description = task_new.description
    if task_new.status is not None:
        task.status = task_new.status
    if task_new.priority is not None:
        task.priority = task_new.priority
    if task_new.due_date is not None:
        task.due_date = task_new.due_date
    db.commit()
    db.refresh(task)
    return task

def handle_delete_task(task_id: int, user_id: int, db: Session):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tồn tại nhiệm vụ đề tài có id {task_id} để xóa"
        )
    project = db.query(ProjectModel).filter(ProjectModel.id == task.project_id).first()
    is_owner = project.owner_id == user_id
    is_assignee = task.assignee_id == user_id
    if not (is_owner or is_assignee):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER đề tài hoặc người được giao việc mới có quyền xóa nhiệm vụ này",
        )
    db.delete(task)
    db.commit()
    return True