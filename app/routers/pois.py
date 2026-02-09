from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List

from ..deps import get_db, get_current_user
from ..schemas import POICreate, POIImport, POIOut
from ..models import User
from ..services import poi_service
from ..schemas import POIUpdate

router = APIRouter(prefix="/pois", tags=["pois"])


@router.post("", response_model=POIOut)
def create_poi(
    data: POICreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return poi_service.create_poi(db, data, current_user)

@router.post("/bulk", response_model=list[POIOut])
def create_pois(
    data: List[POICreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return poi_service.create_pois(db, data, current_user)

@router.post("/import")
def import_pois(
    pois: List[POIImport],
    db: Session = Depends(get_db)
):
    """
    Recibe una lista de POIs desde la app y los importa a la base de datos.
    - Si el POI tiene id y existe -> se actualiza  
    - Si no tiene id -> se crea un nuevo POI
    """
    poi_service.import_pois(db, pois)
    return {"message": "POIs imported successfully"}

@router.get("/export")
def export_pois(
    db: Session = Depends(get_db),
    as_list: bool = True
):
    data = poi_service.export_pois(db, as_list=as_list)
    return JSONResponse(content=data)

@router.get("", response_model=List[POIOut])
def list_pois(
    db: Session = Depends(get_db),
    tag: Optional[str] = Query(default=None),
    poi_type: Optional[str] = Query(default=None, alias="type"),
    q: Optional[str] = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
):
    return poi_service.list_pois(db, tag, poi_type, q, limit)


@router.get("/{poi_id}", response_model=POIOut)
def get_poi(
    poi_id: int,
    db: Session = Depends(get_db),
):
    return poi_service.get_poi(db, poi_id)

@router.put("/{poi_id}", response_model=POIOut)
def update_poi_endpoint(
    poi_id: int,
    data: POIUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return poi_service.update_poi(db, poi_id, data, current_user)


@router.delete("/{poi_id}", status_code=204)
def delete_poi_endpoint(
    poi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    poi_service.delete_poi(db, poi_id, current_user)
    return None