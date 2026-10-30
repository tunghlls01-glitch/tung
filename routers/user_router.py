from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from db.database import get_db
from dependencies.auth_dependencies import RoleCheck, handle_get_user
from schemas.user import UserResponse, UserUpdate
from services.user_services import get_user_token, hanlde_get_role_admin

router = APIRouter(prefix="/users", tags=["USERS"])

@router.get("/me",response_model=UserResponse,status_code=status.HTTP_200_OK,summary="Xem thông tin cá nhân")
def get_me(user_data: dict = Depends(handle_get_user),db: Session = Depends(get_db)):
    return get_user_token(user_id=user_data["user_id"], db=db)
    
@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK, summary="Danh sách user (ADMIN)")
def get_users(search: Optional[str] = Query(None), is_active: Optional[bool] = Query(None), skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), user_data: dict = Depends(RoleCheck(["ADMIN"])), db: Session = Depends(get_db)):
    return hanlde_get_role_admin(search=search, is_active=is_active, skip=skip, limit=limit, db=db)

