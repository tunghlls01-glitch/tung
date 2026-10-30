from fastapi import APIRouter, Depends, status
from db.database import get_db
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from schemas.auth_schemas import LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse
from services.auth_services import handle_register_services, handle_login_service, handle_refresh_service
router = APIRouter(prefix="/auth", tags=["AUTHENTICATION"])

@router.post("/register", response_model= UserResponse)
def register(account_user: UserCreate, db: Session = Depends(get_db)):
    return handle_register_services(account_user=account_user, db=db)

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(user_account: LoginRequest, db: Session = Depends(get_db)):
    return handle_login_service(user_account=user_account, db=db)

@router.post("/refresh",response_model=RefreshTokenResponse,status_code=status.HTTP_200_OK,)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    return handle_refresh_service(refresh_token=payload.refresh_token, db=db)
