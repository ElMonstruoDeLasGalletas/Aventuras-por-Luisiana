
from typing import Annotated, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import Route, User, UserFavs
from ..schemas import FavouritesCreate

def _get_favourites_or_404(db: Session, favourite_id: int) -> UserFavs:
    favourite = (
        db.query(UserFavs)
        .filter(UserFavs.id == favourite_id)  # noqa
        # .first()
    )
    if not favourite:
        raise HTTPException(404, "Favourite not found")
    return favourite

def create_favourite(db: Session, data: FavouritesCreate) -> UserFavs:
    favourite = UserFavs(
        user_id=data.user_id,
        route_id=data.route_id,
    )
    
    db.add(favourite)
    db.commit()
    db.refresh(favourite)
    return favourite


def list_favourites(db: Session, user_id: int) -> List[UserFavs]:
    favs = (
        db.query(UserFavs)
        .filter(UserFavs.user_id == user_id)
        .all()
    )
    return favs


def delete_favourite(
    db: Session,
    favourite_id: int
) -> UserFavs:
    favourite = _get_favourites_or_404(db, favourite_id)
    db.commit()
    return favourite
