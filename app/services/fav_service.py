from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import UserFavs
#from ..models import UserFavs as Favourite
from ..schemas import FavouritesCreate

def _get_favourites_or_404(db: Session, favourite_id: int) -> UserFavs:
    favourite = (
        db.query(UserFavs)
        .filter(UserFavs.id == favourite_id, UserFavs.is_deleted == False)  # noqa
        .first()
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


def list_favourites(
    user_id: int,
    db: Session,
):
    return (
            db.query(UserFavs)
            .filter(UserFavs.user_id == user_id, UserFavs.is_deleted == False) #noqa
            .order_by(UserFavs.id.desc())
            .limit(200)
            .all()
        )

def delete_favourite(
    db: Session,
    favourite_id: int,
) -> None:
    favourite = _get_favourites_or_404(db, favourite_id)

    favourite.is_deleted = True
    db.commit()
