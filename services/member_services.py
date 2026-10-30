from schemas.member import MemberCreate
from models.member import MemberModel
from models.project import ProjectModel
from models.user import UserModel
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def handle_add_member(member: MemberCreate,project_id: int,user_id: int, db: Session):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không có id {project_id} đề tài này"
        )
    if project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới có quyền thêm thành viên vào đề tài"
        )
    user = db.query(UserModel).filter(UserModel.id == member.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy user có id {member.user_id}"
        )
    check = db.query(MemberModel).filter(MemberModel.project_id == project_id, MemberModel.user_id == member.user_id).first()
    if check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User này đã là thành viên đề tài rồi"
        )
    
    new_member = MemberModel(
        project_id = project_id,
        user_id = member.user_id,
        role = member.role
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def handle_get_member_by_project_id(project_id: int,user_id: int, db: Session):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không có id {project_id} đề tài này"
        )
    is_member = db.query(MemberModel).filter(MemberModel.project_id == project_id, MemberModel.user_id == user_id).first()
    if is_member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem danh sách thành viên đề tài này",
        )
    member = db.query(MemberModel).filter(MemberModel.project_id == project_id).all()
    return member

def handle_delete_member(project_id: int, user_id_delete: int, user_id_current: int, db:Session):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không có id {project_id} đề tài này"
        )
    if project.owner_id != user_id_current:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới có quyền xóa thành viên"
        )
    if user_id_delete == project.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể xóa OWNER ra khỏi đề tài",
        )
    member = db.query(MemberModel).filter(MemberModel.project_id == project_id, MemberModel.user_id == user_id_delete).first()
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thành viên không tồn tại trong đề tài"
        )
    db.delete(member)
    db.commit()
    return True

