from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import User
from .security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials




security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    try:
        token = credentials.credentials
        payload = decode_token(token)
        email = payload.get("sub")
        if not email:
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
