from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, ExpiredSignatureError, JWTError
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALG = os.getenv("ALGORITHM")

security_token = HTTPBearer()
def handle_get_user(credentials: HTTPAuthorizationCredentials = Depends(security_token)):
    token = credentials.credentials
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALG])
        user_name = payload.get("user_name")
        role_name = payload.get("role_account")
        user_id = payload.get("sup")
        if not user_id or not role_name:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không chứa đủ thông tin xác thực"
            )
        return {
            "username": user_name,
            "role_name": role_name,
            "user_id": user_id,
        }
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ"
        )

class RoleCheck: 
    def __init__(self, allow_roles: list[str]):
        self.allow_roles = allow_roles

    def __call__(self, user_data: dict = Depends(handle_get_user)) -> dict:
        user_role_name = user_data.get("role_name")
        if user_role_name not in self.allow_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Quyền '{user_role_name}' không được phép thực hiện hành động này",
            )
        return user_data
