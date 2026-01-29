from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models import POI, User
from app.schemas import POICreate, POIUpdate


# --- helpers -------------------------------------------------

def _validate_lat_lng(lat: float, lng: float):
    if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
        raise HTTPException(400, "Invalid lat/lng")


def _get_poi_or_404(db: Session, poi_id: int) -> POI:
    poi = (
        db.query(POI)
        .filter(POI.id == poi_id, POI.is_deleted == False)  # noqa
        .first()
    )
    if not poi:
        raise HTTPException(404, "POI not found")
    return poi


# --- public API ----------------------------------------------

def create_poi(db: Session, data: POICreate, user: User) -> POI:
    _validate_lat_lng(data.lat, data.lng)

    poi = POI(
        name=data.name,
        lat=data.lat,
        lng=data.lng,
        description=data.description,
        tags=data.tags,
        media=[m.model_dump() for m in data.media],
        type=data.type,
        # user_id=user.id  ← cuando lo añadas
    )

    db.add(poi)
    db.commit()
    db.refresh(poi)
    return poi


def list_pois(
    db: Session,
    tag: Optional[str],
    poi_type: Optional[str],
    q: Optional[str],
    limit: int,
) -> List[POI]:
    query = db.query(POI).filter(POI.is_deleted == False)  # noqa

    if poi_type:
        query = query.filter(POI.type == poi_type)

    if q:
        query = query.filter(POI.name.ilike(f"%{q}%"))

    if tag:
        query = query.filter(POI.tags.contains([tag]))

    return query.order_by(POI.id.desc()).limit(limit).all()


def get_poi(db: Session, poi_id: int) -> POI:
    return _get_poi_or_404(db, poi_id)


def update_poi(
    db: Session,
    poi_id: int,
    data: POIUpdate,
    user: User,
) -> POI:
    poi = _get_poi_or_404(db, poi_id)

    payload = data.model_dump(exclude_unset=True)

    if "lat" in payload or "lng" in payload:
        _validate_lat_lng(
            payload.get("lat", poi.lat),
            payload.get("lng", poi.lng),
        )

    for field, value in payload.items():
        setattr(poi, field, value)

    db.commit()
    db.refresh(poi)
    return poi


def delete_poi(
    db: Session,
    poi_id: int,
    user: User,
) -> None:
    poi = _get_poi_or_404(db, poi_id)

    poi.is_deleted = True
    db.commit()
