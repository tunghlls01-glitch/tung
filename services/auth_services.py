from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.jwt import create_access_token, create_refresh_token, decode_token
from core.password import check_password, handle_hash_password
from models.enums import UserRole
from models.user import UserModel
from schemas.auth_schemas import LoginRequest
from schemas.user import UserCreate

def handle_register_services(account_user: UserCreate, db: Session):
    user = (db.query(UserModel).filter(UserModel.email == account_user.email).first())
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên tài khoản hoặc email đã tồn tại",
        )
    hash_password = handle_hash_password(account_user.password)
    new_account = UserModel(
        email=account_user.email,
        password_hash=hash_password,
        full_name=account_user.full_name,
        role=UserRole.USER,
        is_active=True,
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

def handle_login_service(user_account: LoginRequest, db: Session):
    user = (db.query(UserModel).filter(UserModel.email == user_account.email).first())
    if not user or not check_password(password=user_account.password, hash_password=user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mật khẩu hoặc tài khoản của bạn sai",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản đã bị vô hiệu hóa hoặc bị khóa",
        )
    role_val = (user.role.value if hasattr(user.role, "value") else str(user.role))
    access_token = create_access_token(user_id=user.id, email=user.email, role_user=role_val)
    refresh_token = create_refresh_token(user_id=user.id)
    return {
        "message": "Đăng nhập thành công",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

def handle_refresh_service(refresh_token: str, db: Session):
    payload = decode_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token không hợp lệ hoặc đã hết hạn",
        )

    user_id = payload.get("sup")
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản đã bị vô hiệu hóa hoặc bị khóa",
        )

    role_val = (
        user.role.value if hasattr(user.role, "value") else str(user.role)
    )

    new_access_token = create_access_token(
        user_id=user.id, email=user.email, role_user=role_val
    )

    return {"access_token": new_access_token, "token_type": "bearer"}