from fastapi import APIRouter, status, Depends, Query
from services.task_services import handle_post_task, handle_get_task_by_project_id, handle_get_by_id, handle_update_task, handle_delete_task
from schemas.task import TaskResponse, TaskUpdate, TaskCreate
from sqlalchemy.orm import Session
from db.database import get_db
from dependencies.auth_dependencies import handle_get_user
from typing import Optional
from models.enums import TaskStatus, TaskPriority
router = APIRouter(tags=["TASKS"])

@router.post("/research-projects/{project_id}/research-tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Tạo nhiệm vụ nghiên cứu")
def create_task(project_id: int, task: TaskCreate,user_data: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_post_task(project_id=project_id, task=task, user_id=user_data["user_id"], db=db)

@router.get("/research-projects/{project_id}/research-tasks", response_model=list[TaskResponse], status_code=status.HTTP_200_OK, summary="List/filter/search nhiệm vụ nghiên cứu")
def get_all_task(project_id: int ,search: Optional[str] = Query(None), status_filter: Optional[TaskStatus] = Query(None, alias="status"), priority_filter: Optional[TaskPriority] = Query(None, alias="priority"), skip: Optional[int] = Query(0, ge=0), limit: Optional[int] = Query(10, ge=1, le=100), assignee_id: Optional[int]= Query(None),user_data: dict = Depends(handle_get_user), db:Session = Depends(get_db)):
    return handle_get_task_by_project_id(project_id=project_id, search=search, status_filter=status_filter, assignee_id=assignee_id, priority_filter=priority_filter, skip=skip, limit=limit, user_id=user_data["user_id"], db=db)

@router.get("/research-tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK, summary="Chi tiết nhiệm vụ nghiên cứu")
def get_task_by_id(task_id: int, user_data: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_get_by_id(task_id=task_id, user_id=user_data["user_id"], db = db)

@router.patch("/research-tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK, summary="Cập nhật nhiệm vụ nghiên cứu")
def update_task(task_id:int, task_new: TaskUpdate, user_data:dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_update_task(task_id=task_id, task_new=task_new, user_id=user_data["user_id"], db=db)

@router.delete("/research-tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Xóa nhiệm vụ nghiên cứu")
def delete_task(task_id: int, user_data: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_delete_task(task_id=task_id, user_id=user_data["user_id"], db=db)