from schemas.project import ProjectCreate, ProjectUpdate
from sqlalchemy.orm import Session
from models.member import MemberModel, MemberRole
from models.project import ProjectModel
from fastapi import HTTPException, status
def handle_create_project(project: ProjectCreate,user_id: int, db: Session):
    new_project = ProjectModel(
        name = project.name,
        description = project.description,
        owner_id = user_id
    )
    db.add(new_project)
    db.flush()

    new_member = MemberModel(
        project_id = new_project.id,
        user_id = user_id,
        role = MemberRole.OWNER
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_project) 
    return new_project

def handle_get_project(search: str,user_id: int,skip: int, limit: int, db: Session):
    query = db.query(ProjectModel).join(MemberModel, ProjectModel.id == MemberModel.project_id).filter(MemberModel.user_id == user_id)
    if search and search.strip():
        query = query.filter(ProjectModel.name.ilike(f"%{search.strip()}%"))
    return query.offset(skip).limit(limit).all()

def handle_get_project_by_id(project_id: int, user_id:int, db:Session):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy đề tài có id {project_id}"
        )
    is_member = db.query(MemberModel).filter(MemberModel.project_id == project_id, MemberModel.user_id == user_id).first()
    if is_member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không là thành viên đề tài này"
        )
    return project

def handle_update_project(project_id: int, project_new:ProjectUpdate,  user_id: int, db: Session):
    project = db.query(ProjectModel).filter(project_id == ProjectModel.id).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy đề tài có id {project_id} cần cập nhật"
        )
    if project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới có quyền cập nhật đề tài"
        )
    if project_new.name is not None:
        project.name = project_new.name
    if project_new.description is not None:
        project.description = project_new.description
    db.commit()
    db.refresh(project)
    return project

def handle_delete_project(project_id: int, user_id: int, db: Session):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy đề tài có id {project_id} cần xóa"
        )
    if project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới có quyền xóa đề tài"
        )
    db.query(MemberModel).filter(MemberModel.project_id == project_id).delete()
    db.delete(project)
    db.commit()
    return True
