from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from ..models import Route, POI, User
from ..schemas import RouteCreate, RouteImport

def _validate_poi_ids(db: Session, poi_ids: list[int]) -> None:
    if not poi_ids:
        raise HTTPException(status_code=400, detail="Poi ids cannot be empty")

    existing = (
        db.query(POI.id)
        .filter(POI.id.in_(poi_ids), POI.is_deleted == False)  # noqa
        .all()
    )

    existing_ids = {row[0] for row in existing}
    missing = [pid for pid in poi_ids if pid not in existing_ids]

    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"POI ids not found: {missing}"
        )

def create_route(
    db: Session,
    data: RouteCreate,
    current_user: User
) -> Route:
    _validate_poi_ids(db, data.poi_ids)

    route = Route(
        name=data.name,
        description=data.description,
        poi_ids=data.poi_ids,
        is_deleted=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(route)
    db.commit()
    db.refresh(route)

    return route

def list_routes(db: Session):
    return (
        db.query(Route)
        .filter(Route.is_deleted == False)  # noqa
        .order_by(Route.id.desc())
        .limit(200)
        .all()
    )

def get_route(db: Session, route_id: int) -> Route:
    route = (
        db.query(Route)
        .filter(Route.id == route_id, Route.is_deleted == False)  # noqa
        .first()
    )

    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    return route

def import_route(
    db: Session,
    data: RouteImport,
    current_user: User
) -> Route:
    _validate_poi_ids(db, data.poi_ids)

    route = Route(
        name=data.name,
        description=data.description,
        poi_ids=data.poi_ids,
        is_deleted=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(route)
    db.commit()
    db.refresh(route)

    return route

def export_route(db: Session, route_id: int):
    route = (
        db.query(Route)
        .filter(Route.id == route_id, Route.is_deleted == False)  # noqa
        .first()
    )

    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    return {
        "id": route.id,
        "name": route.name,
        "description": route.description,
        "poi_ids": route.poi_ids,
        "created_at": route.created_at,
        "updated_at": route.updated_at,
    }
