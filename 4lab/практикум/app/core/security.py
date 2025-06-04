from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.db.database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
from app.core.password import get_password_hash, verify_password

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

class TokenPayload(BaseModel):
    sub: str
    exp: int

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": user.email}


def get_user_by_email(db: Session, email: str):
    from app.cruds.user import get_user_by_email as user_get_by_email
    return user_get_by_email(db, email)