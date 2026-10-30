from sqlalchemy.orm import Session
from models.user import UserModel
from fastapi import HTTPException, status

def get_user_token(user_id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản đã bị vô hiệu hóa",
        )
    return user

def hanlde_get_role_admin(search: str, is_active: bool, skip: int, limit: int, db: Session):
    query = db.query(UserModel)
    if search:
        query = query.filter(UserModel.full_name.ilike(f"%{search}%") | UserModel.email.ilike(f"%{search}%"))
    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)
    return query.offset(skip).limit(limit).all()
