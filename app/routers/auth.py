from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..deps import get_db, get_current_user
from ..models import User
from ..schemas import LoginResponse, RegisterRequest, LoginRequest, UserPublic
from ..security import verify_password, create_access_token
from ..services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(
        db,
        email=data.email,
        name=data.name,
        password=data.password,
        role_id=data.role_id
    )

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(db, email=data.email, password=data.password)

@router.get("/me", response_model=UserPublic)
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role.name  # <-- así solo devolvemos el string
    }

@router.delete("/user/{email}")
def delete_user(
    email: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # obtenemos al usuario que hace la petición
):
    return auth_service.delete_user(db, target_email=email, current_user=current_user)