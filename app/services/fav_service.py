
from typing import Annotated, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models import Route, User, UserFavs
from ..schemas import FavouritesCreate

def _get_favourites_or_404(db: Session, favourite_id: int) -> UserFavs:
    favourite = (
        db.query(UserFavs)
        .filter(UserFavs.id == favourite_id)  # noqa
        .first()
    )
    if not favourite:
        raise HTTPException(404, "Favourite not found")
    return favourite


def create_favourite(db: Session, user_id: int, route_id: int) -> UserFavs:
    favourite = UserFavs(
        user_id=user_id,
        route_id=route_id,
    )

    try:
        db.add(favourite)
        db.commit()
        db.refresh(favourite)
        return favourite
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Route already in favourites"
        )
    


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
    db.delete(favourite)
    db.commit()
    db.refresh(favourite)
    return favourite
