from fastapi import APIRouter, status, Depends
from schemas.member import MemberCreate, MemberResponse
from sqlalchemy.orm import Session
from db.database import get_db
from dependencies.auth_dependencies import handle_get_user
from services.member_services import handle_add_member, handle_get_member_by_project_id, handle_delete_member
router = APIRouter(prefix="/research-projects/{project_id}/members", tags=["MEMBERS"])

@router.post("", response_model=MemberResponse, status_code=status.HTTP_201_CREATED, summary="Thêm thành viên")
def create_member(member: MemberCreate,project_id: int,user_data: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_add_member(member=member, project_id=project_id, user_id=user_data["user_id"], db=db)

@router.get("", response_model=list[MemberResponse], status_code=status.HTTP_200_OK, summary="Danh sách thành viên")
def get_member_all(project_id: int,user_data: dict = Depends(handle_get_user), db: Session = Depends(get_db)):
    return handle_get_member_by_project_id(project_id=project_id, user_id= user_data["user_id"], db=db)

@router.delete("", status_code=status.HTTP_204_NO_CONTENT, summary="Xóa thành viên")
def delete_member(project_id: int, user_id_delete: int, user_data: dict = Depends(handle_get_user), db:Session = Depends(get_db)):
    return handle_delete_member(project_id=project_id, user_id_delete=user_id_delete, user_id_current=user_data["user_id"], db=db)
