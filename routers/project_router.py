from fastapi import APIRouter, status, Depends, Query
from schemas.project import ProjectResponse, ProjectCreate, ProjectUpdate
from sqlalchemy.orm import Session
from db.database import get_db
from services.project_services import handle_create_project, handle_get_project, handle_get_project_by_id, handle_update_project, handle_delete_project
from dependencies.auth_dependencies import handle_get_user
from typing import Optional
router = APIRouter(prefix="/research-projects", tags=["PROJECTS"])

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED,summary="Tạo đề tài nghiên cứu")
def create_project(project: ProjectCreate,user_data: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_create_project(project=project, user_id=user_data["user_id"], db=db)

@router.get("", response_model=list[ProjectResponse], status_code=status.HTTP_200_OK, summary="Danh sách đề tài nghiên cứu của tôi")
def get_project_all(search: Optional[str] = None,skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100),user_data: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_get_project(search=search, skip=skip, limit=limit, user_id=user_data["user_id"], db=db)

@router.get("/{project_id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK, summary="Chi tiết đề tài nghiên cứu")
def get_project_id(project_id: int, user_data:dict = Depends(handle_get_user), db:Session = Depends(get_db)):
    return handle_get_project_by_id(project_id=project_id, user_id=user_data["user_id"], db=db)

@router.patch("/{project_id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK, summary="Cập nhật đề tài nghiên cứu")
def update_project(project_id: int, project_new:ProjectUpdate,  user_data: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_update_project(project_id=project_id, project_new=project_new, user_id=user_data["user_id"], db=db)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Xóa đề tài nghiên cứu")
def delete_project(project_id: int, user_data: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_delete_project(project_id=project_id, user_id=user_data["user_id"], db=db)