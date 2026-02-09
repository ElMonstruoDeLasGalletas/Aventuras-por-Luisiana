from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List

from ..deps import get_db, get_current_user
from ..models import Tag, User, UserPreferredTag
from ..schemas import TagOut, TagCreate, UserPreferencesAdd, UserPreferencesRemove, UserPreferencesOut

router = APIRouter(prefix="/preferences", tags=["preferences"])

# Dependency para obtener el usuario actual autenticado
# CurrentUser = Annotated[dict, Depends(get_current_user)]
# DbSession = Annotated[Session, Depends(get_db)]


# Obtener todos los tags disponibles en el catálogo
@router.get("/tags", response_model=List[TagOut])
def get_all_tags(db: Session = Depends(get_db)):
    """
    Devuelve todos los tags disponibles en el catálogo.
    No requiere autenticación.
    """
    tags = db.query(Tag).all()
    return tags


# Crear un nuevo tag en el catálogo (normalmente solo admin)
@router.post("/tags", response_model=TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crea un nuevo tag en el catálogo.
    Si el tag ya existe, devuelve error 400.
    """
    # Verificar si el tag ya existe
    existing = db.query(Tag).filter(Tag.name == tag_data.name.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tag '{tag_data.name}' ya existe"
        )
    
    # Crear nuevo tag
    new_tag = Tag(name=tag_data.name.lower())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


# Obtener las preferencias del usuario (tags que le gustan)
@router.get("/", response_model=UserPreferencesOut)
def get_user_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Devuelve los tags que le gustan al usuario autenticado.
    """
    user_id = current_user.id
    
    # Obtener todas las relaciones user_preferred_tags del usuario
    user_tags = db.query(UserPreferredTag).filter(UserPreferredTag.user_id == user_id).all()
    
    # Obtener los tags completos
    tag_ids = [ut.tag_id for ut in user_tags]
    tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    
    return {"tags": tags}


# Añadir tags a las preferencias del usuario
@router.post("/user-tags", response_model=UserPreferencesOut, status_code=status.HTTP_201_CREATED)
def add_user_preferences(
    preferences_data: UserPreferencesAdd,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Añade tags a las preferencias del usuario.
    Si un tag ya está en las preferencias, lo ignora (no duplica).
    """
    user_id = current_user.id
    
    # Verificar que todos los tag_ids existen
    existing_tags = db.query(Tag).filter(Tag.id.in_(preferences_data.tag_ids)).all()
    existing_tag_ids = {tag.id for tag in existing_tags}
    
    invalid_ids = set(preferences_data.tag_ids) - existing_tag_ids
    if invalid_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tags con IDs {list(invalid_ids)} no existen"
        )
    
    # Obtener tags que ya tiene el usuario
    current_prefs = db.query(UserPreferredTag).filter(UserPreferredTag.user_id == user_id).all()
    current_tag_ids = {pref.tag_id for pref in current_prefs}
    
    # Añadir solo los tags que no tiene
    new_tag_ids = existing_tag_ids - current_tag_ids
    
    for tag_id in new_tag_ids:
        new_pref = UserPreferredTag(user_id=user_id, tag_id=tag_id)
        db.add(new_pref)
    
    db.commit()
    
    # Devolver las preferencias actualizadas
    all_user_tags = db.query(UserPreferredTag).filter(UserPreferredTag.user_id == user_id).all()
    tag_ids = [ut.tag_id for ut in all_user_tags]
    tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    
    return {"tags": tags}


# Eliminar un tag específico de las preferencias del usuario
@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user_preference(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Elimina un tag específico de las preferencias del usuario.
    Si el tag no está en las preferencias, devuelve error 404.
    """
    user_id = current_user.id
    
    # Buscar la relación user_preferred_tag
    pref = db.query(UserPreferredTag).filter(
        UserPreferredTag.user_id == user_id,
        UserPreferredTag.tag_id == tag_id
    ).first()
    
    if not pref:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag con ID {tag_id} no está en las preferencias del usuario"
        )
    
    db.delete(pref)
    db.commit()
    
    return None


# Eliminar múltiples tags de las preferencias del usuario
@router.delete("/tags", status_code=status.HTTP_204_NO_CONTENT)
def remove_user_preferences(
    preferences_data: UserPreferencesRemove,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Elimina múltiples tags de las preferencias del usuario.
    """
    user_id = current_user.id
    
    # Eliminar todas las relaciones que coincidan
    db.query(UserPreferredTag).filter(
        UserPreferredTag.user_id == user_id,
        UserPreferredTag.tag_id.in_(preferences_data.tag_ids)
    ).delete(synchronize_session=False)
    
    db.commit()
    
    return None


# Eliminar una tag existente
@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def remove_tags(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
):
    """
    Elimina un tag del catálogo.
    Si el tag no existe, devuelve error 404.
    """
    # Verificar si el tag existe
    existing = db.query(Tag).filter(Tag.name == tag_data.name.lower()).first()
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag '{tag_data.name}' no existe"
        )
    
    # Elimina el tag
    tag = existing
    db.delete(tag)
    db.commit()
    return tag