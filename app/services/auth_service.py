# app/services/auth_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import User
from ..security import create_access_token, hash_password, verify_password

def register_user(db: Session, email: str, name: str, password: str, role_id: int):
    # Comprueba si ya existe
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crear el usuario
    user = User(
        email=email,
        name=name,
        password_hash=hash_password(password),
        role_id=role_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Devolver dict listo para response_model
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role.name
    }

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(subject=user.email)
    
    # Devolver dict listo para response_model
    return {"access_token": token}