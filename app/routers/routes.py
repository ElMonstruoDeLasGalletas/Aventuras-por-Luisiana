from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..deps import get_db, get_current_user, require_roles
from ..models import User
from ..schemas import RouteCreate, RouteOut, RouteImport, RouteUpdate
from ..services import route_service

router = APIRouter(prefix="/routes", tags=["routes"])

@router.post("", response_model=RouteOut)
def create_route(
    data: RouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return route_service.create_route(db, data)

@router.get("", response_model=List[RouteOut])
def list_routes(
    db: Session = Depends(get_db)
):
    return route_service.list_routes(db)

@router.get("/recommended", response_model=List[RouteOut])
def get_recommended_routes_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve rutas ordenadas por coincidencia con las preferencias del usuario.
    Las rutas con más tags coincidentes aparecen primero.
    Si el usuario no tiene preferencias, devuelve todas las rutas.
    """
    return route_service.get_recommended_routes(db, current_user.id)

@router.get("/{route_id}", response_model=RouteOut)
def get_route(
    route_id: int,
    db: Session = Depends(get_db)
):
    return route_service.get_route(db, route_id)

@router.post("/import", response_model=RouteOut)
def import_route(
    data: RouteImport,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return route_service.import_route(db, data, current_user)

@router.get("/{route_id}/export")
def export_route(
    route_id: int,
    db: Session = Depends(get_db)
):
    return route_service.export_route(db, route_id)

@router.put("/{route_id}", response_model=RouteOut)
def update_route(
    route_id: int,
    data: RouteUpdate,
    db: Session = Depends(get_db),
):
    return route_service.update_route(db, route_id, data)

@router.delete("/{route_id}", status_code=204)
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
):
    route_service.delete_route(db, route_id)
    return None
