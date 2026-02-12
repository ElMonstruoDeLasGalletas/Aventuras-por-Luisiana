# app/services/auth_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import User
from ..security import create_access_token, hash_password, verify_password

def normalize_role_id(role_id: int | None) -> int:
    if role_id not in (1, 2):
        return 3
    return role_id

def register_user(db: Session, email: str, name: str, password: str, role_id: int):
    # Comprueba si ya existe
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    role_id = normalize_role_id(role_id)

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

def delete_user(db: Session, target_email: str, current_user: User):
    """
    Borra un usuario solo si:
    - current_user es admin, o
    - current_user.email == target_email
    """
    # Solo admin o el propio usuario
    if current_user.role.name.lower() != "admin" and current_user.email != target_email:
        raise HTTPException(status_code=403, detail="You don't have permissions to delete this user!")

    user = db.query(User).filter(User.email == target_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": f"User {target_email} deleted correctly"}