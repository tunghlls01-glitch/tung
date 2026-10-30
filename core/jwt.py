from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from datetime import datetime, timezone, timedelta
from typing import Optional
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALG = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

def create_access_token(user_id: int, email: str, role_user: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sup": user_id,
        "user_name": email,
        "role_account": role_user,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALG)

def create_refresh_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sup": user_id,
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALG)

def decode_token(token: str) -> Optional[dict]:
    try: 
        return jwt.decode(token, SECRET_KEY, algorithms=[ALG])
    except JWTError:
        return None
