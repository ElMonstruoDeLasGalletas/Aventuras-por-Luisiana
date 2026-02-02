from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from ..deps import get_db, get_current_user
from ..schemas import FavouritesCreate, FavouritesOut
from ..models import User
from ..services import fav_service

router = APIRouter(prefix="/favs", tags=["favs"])


@router.post("", response_model=FavouritesOut)
def create_favourite(
    data: FavouritesCreate,
    db: Session = Depends(get_db),
    
):
    return fav_service.create_favourite(db, data)


@router.get("", response_model=List[FavouritesOut])
def list_favourites(
    db: Session = Depends(get_db),
    tag: Optional[str] = Query(default=None),
    fav_type: Optional[str] = Query(default=None, alias="type"),
    q: Optional[str] = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
):
    return fav_service.list_favourites(db, tag, fav_type, q, limit)


@router.delete("/{favourite_id}", status_code=204)
def delete_fav(
    favourite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    fav_service.delete_favourite(db, favourite_id, current_user)
    return None