from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..deps import get_db, get_current_user
from ..models import Route, POI, User
from ..schemas import RouteCreate, RouteOut, RouteImport

router = APIRouter(prefix="/routes", tags=["routes"])

def _validate_poi_ids(db: Session, poi_ids: list[int]) -> None:
    if not poi_ids:
        raise HTTPException(status_code=400, detail="Poi ids cannot be empty")
    
    # POIs existentes (y no borrados)
    existing = (
        db.query(POI.id)
        .filter(POI.id.in_(poi_ids), POI.is_deleted == False) #noqa
        .all()
    )
    existing_ids = {row[0] for row in existing}
    missing = [pid for pid in poi_ids if pid not in existing_ids]
    if missing:
        raise HTTPException(status_code=400, detail=f"POI ids not found: {missing}")
    
@router.post("", response_model=RouteOut)
def create_route(
    data: RouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _validate_poi_ids(db, data.poi_ids)
    
    route = Route(
        name=data.name,
        description=data.description,
        poi_ids=data.poi_ids,
        is_deleted=False,
    )
    db.add(route)
    db.commit()
    db.refresh(route)
    return route

@router.get("", response_model=List[RouteOut])
def list_routes(db: Session = Depends(get_db)):
    return (
        db.query(Route)
        .filter(Route.is_deleted == False) #noqa
        .order_by(Route.id.desc())
        .limit(200)
        .all()
    )
    
@router.get("/{route_id}", response_model=RouteOut)
def get_route(route_id: int, db: Session = Depends(get_db)):
    route = (
        db.query(Route)
        .filter(Route.id == route_id, Route.is_deleted == False) #noqa
        .first()
    )
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.post("/import", response_model=RouteOut)
def import_route(
    data: RouteImport,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    _validate_poi_ids(db, data.poi_ids)
    
    route = Route(
        name=data.name,
        description=data.description,
        poi_ids=data.poi_ids,
        is_deleted=False
    )
    db.add(route)
    db.commit()
    db.refresh(route)
    return route
@router.get("/{route_id}/export")
def export_route(route_id: int, db: Session = Depends(get_db)):
    route = (
        db.query(Route)
        .filter(Route.id == route_id, Route.is_deleted == False) #noqa
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
        "updated_at": route.updated_at
    }
    
    