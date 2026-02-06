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
    print(f"create\ndb: {db}\ndata: {data}")
    return fav_service.create_favourite(db, data)


# @router.get("/all", response_model=List[FavouritesOut])
# def list_all_favourites(
#     db: Session = Depends(get_db),
# ):
#     user: User = get_current_user()
#     print(user)
#     return fav_service.list_favourites(db, user.id)

@router.get("", response_model=List[FavouritesOut])
def list_favourites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return fav_service.list_favourites(db, current_user.id)


@router.delete("/{favourite_id}", status_code=204)
def delete_fav(
    favourite_id: int,
    db: Session = Depends(get_db)
):
    fav_service.delete_favourite(db, favourite_id)
    return None