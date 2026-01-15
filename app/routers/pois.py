from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from ..deps import get_db, get_current_user
from ..models import POI, User
from ..schemas import POICreate, POIOut

router = APIRouter(prefix="/pois", tags=["pois"])

@router.post("", response_model=POIOut)
def create_poi(
    data: POICreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # protegido
):
    if not (-90 <= data.lat <= 90) or not (-180 <= data.lng <= 180):
        raise HTTPException(status_code=400, detail="Invalid lat/lng")

    poi = POI(
        name=data.name,
        lat=data.lat,
        lng=data.lng,
        description=data.description,
        tags=data.tags,
        media=[m.model_dump() for m in data.media],
        type=data.type,
    )
    db.add(poi)
    db.commit()
    db.refresh(poi)
    return poi

@router.get("", response_model=List[POIOut])
def list_pois(
    db: Session = Depends(get_db),
    tag: Optional[str] = Query(default=None),
    poi_type: Optional[str] = Query(default=None, alias="type"),
    q: Optional[str] = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
):
    query = db.query(POI).filter(POI.is_deleted == False)  # noqa

    if poi_type:
        query = query.filter(POI.type == poi_type)

    if q:
        query = query.filter(POI.name.ilike(f"%{q}%"))

    if tag:
        # JSONB tags contiene [tag]
        query = query.filter(POI.tags.contains([tag]))

    return query.order_by(POI.id.desc()).limit(limit).all()

@router.get("/{poi_id}", response_model=POIOut)
def get_poi(poi_id: int, db: Session = Depends(get_db)):
    poi = db.query(POI).filter(POI.id == poi_id, POI.is_deleted == False).first()  # noqa
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")
    return poi
