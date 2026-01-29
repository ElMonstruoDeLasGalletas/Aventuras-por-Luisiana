from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from ..deps import get_db, get_current_user
from ..models import UserPreferences
from ..schemas import UserPreferencesCreate, UserPreferencesOut

router = APIRouter(prefix="/preferences", tags=["preferences"])

# Dependency para obtener el usuario actual autenticado
CurrentUser = Annotated[dict, Depends(get_current_user)]
DbSession = Annotated[Session, Depends(get_db)]


# Endpoint para crear o actualizar las preferencias del usuario
@router.post("/", response_model=UserPreferencesOut, status_code=status.HTTP_201_CREATED)
def set_user_preferences(
    preferences_data: UserPreferencesCreate,
    current_user: CurrentUser,
    db: DbSession
):
    """
    Guarda las preferencias del usuario (tags que le interesan).
    Si ya tiene preferencias, las actualiza. Si no, las crea.
    """
    user_id = current_user["id"]
    
    # Buscamos si ya tiene preferencias guardadas
    existing = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
    
    if existing:
        # Actualizar preferencias existentes
        existing.preferred_tags = preferences_data.preferred_tags
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Crear nuevas preferencias
        new_prefs = UserPreferences(
            user_id=user_id,
            preferred_tags=preferences_data.preferred_tags
        )
        db.add(new_prefs)
        db.commit()
        db.refresh(new_prefs)
        return new_prefs


# Endpoint para obtener las preferencias del usuario actual
@router.get("/", response_model=UserPreferencesOut)
def get_user_preferences(
    current_user: CurrentUser,
    db: DbSession
):
    """
    Devuelve las preferencias del usuario autenticado.
    Si no tiene preferencias, devuelve error 404.
    """
    user_id = current_user["id"]
    
    prefs = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
    
    if not prefs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no tiene preferencias configuradas"
        )
    
    return prefs