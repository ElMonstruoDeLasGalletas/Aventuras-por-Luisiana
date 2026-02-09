import json
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models import POI, User
from app.schemas import POICreate, POIImport, POIUpdate


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

def create_pois(db: Session, pois: list[POI], user: User) -> list[POI]:
    db_pois = []

    for poi in pois:
        db_poi = POI(
            **poi.model_dump()
        )
        db.add(db_poi)
        db_pois.append(db_poi)

    db.commit()

    for poi in db_pois:
        db.refresh(poi)

    return db_pois

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

def export_pois(db: Session, as_list=False):
    """
    Devuelve todos los POIs de la base de datos en formato lista de diccionarios,
    lista para ser enviada como JSON en un endpoint.

    Params:
    -------
    db : Session
        Sesión de SQLAlchemy conectada a la base de datos.
    as_list : bool, opcional (por defecto True)
        Determina el formato de salida:
        - False: devuelve una lista de diccionarios lista para enviar como JSON a la app.
        - True: devuelve un string JSON serializado, listo para guardar en un archivo.

    """
    pois = db.query(POI).all()
    data = []
    for poi in pois:
        data.append({
            "id": poi.id,
            "name": poi.name,
            "lat": poi.lat,
            "lng": poi.lng,
            "description": poi.description,
            "tags": poi.tags if hasattr(poi, "tags") else [],
            # "tags": [t.name for t in poi.tags],
            "media": poi.media,
            "type": poi.type,
            "is_deleted": poi.is_deleted,
            "created_at": poi.created_at.isoformat(),
            "updated_at": poi.updated_at.isoformat()
        })
    if as_list:
        return data
    return json.dumps(data, ensure_ascii=False, indent=2)

def import_pois(db: Session, pois: List[POIImport]):
    """
    Recibe una lista de POIs en formato JSON y los añade a la base de datos.
    Los tags se guardan como lista de strings por ahora.
    """
    for poi in pois:
        existing = db.query(POI).filter_by(id=poi.id).first() if poi.id else None

        if existing:
            # update
            for field, value in poi.model_dump().items():
                setattr(existing, field, value)
            existing.updated_at = datetime.now(timezone.utc)
        else:
            db.add(POI(**poi.model_dump()))

    db.commit()