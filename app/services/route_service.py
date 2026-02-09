from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from ..models import Route, POI, User
from ..schemas import RouteCreate, RouteImport, RouteUpdate


def _get_route_or_404(db: Session, route_id: int) -> Route:
    route = (
        db.query(Route)
        .filter(Route.id == route_id, Route.is_deleted == False)  # noqa
        .first()
    )
    if not route:
        raise HTTPException(404, "Route not found")
    return route


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

def update_route(
    db: Session,
    route_id: int,
    data: RouteUpdate,
) -> Route:
    route = _get_route_or_404(db, route_id)

    payload = data.model_dump(exclude_unset=True)

    for field, value in payload.items():
        setattr(route, field, value)

    db.commit()
    db.refresh(route)
    return route


def delete_route(
    db: Session,
    route_id: int,
) -> None:
    route = _get_route_or_404(db, route_id)

    route.is_deleted = True
    db.commit()


# Rutas recomendadas
def get_recommended_routes(db: Session, user_id: int):
    """
    Devuelve rutas ordenadas por coincidencia con las preferencias del usuario.
    Si el usuario no tiene preferencias, devuelve todas las rutas sin orden especial.
    """
    from ..models import UserPreferredTag, Tag, POI
    
    # Obtener los tag_ids que le gustan al usuario
    user_tag_ids = (
        db.query(UserPreferredTag.tag_id)
        .filter(UserPreferredTag.user_id == user_id)
        .all()
    )
    user_tag_ids = [row[0] for row in user_tag_ids]
    
    # Si no tiene preferencias, devolver todas las rutas
    if not user_tag_ids:
        return list_routes(db)
    
    # Obtener los nombres de los tags del usuario
    user_tags = (
        db.query(Tag.name)
        .filter(Tag.id.in_(user_tag_ids))
        .all()
    )
    user_tag_names = {row[0] for row in user_tags}
    
    # Obtener todas las rutas activas
    routes = (
        db.query(Route)
        .filter(Route.is_deleted == False)  # noqa
        .all()
    )
    
    # Calcular score para cada ruta
    routes_with_score = []
    for route in routes:
        # Obtener los POIs de la ruta
        pois = (
            db.query(POI)
            .filter(POI.id.in_(route.poi_ids), POI.is_deleted == False)  # noqa
            .all()
        )
        
        # Recopilar todos los tags de los POIs de esta ruta
        route_tags = set()
        for poi in pois:
            if poi.tags:  # poi.tags es una lista JSONB
                route_tags.update(poi.tags)
        
        # Calcular coincidencias
        matches = len(user_tag_names & route_tags)
        
        routes_with_score.append({
            "route": route,
            "score": matches
        })
    
    # Ordenar por score descendente
    routes_with_score.sort(key=lambda x: x["score"], reverse=True)
    
    # Devolver solo las rutas (sin el score)
    return [item["route"] for item in routes_with_score]