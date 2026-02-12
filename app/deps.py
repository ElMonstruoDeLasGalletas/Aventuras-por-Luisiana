from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload

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

    user = db.query(User)\
            .options(joinedload(User.role))\
            .filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Crea una función decoradora para no tener que romper el código que hemos hecho,
# simplemente añadir el decorador como @require_roles("maquetador", "admin")
# def require_roles(*allowed_roles):
#     def decorator(func):
#         async def wrapper(user = Depends(get_current_user), *args, **kwargs):
#             if user.role.name not in allowed_roles:
#                 raise HTTPException(status_code=403, detail="No tienes permisos")
#             return await func(*args, **kwargs)
#         return wrapper
#     return decorator

def require_roles(*allowed_roles):
    allowed_roles_lower = [role.lower() for role in allowed_roles]

    def dependency(current_user: User = Depends(get_current_user)):
        print("ROL DE USUARIO:", current_user.role.name)
        print("ROLES PERMITIDOS:", allowed_roles_lower)
        if not current_user.role or current_user.role.name.lower() not in allowed_roles_lower:
            raise HTTPException(status_code=403, detail="No tienes permisos")
        return current_user
    
    return dependency