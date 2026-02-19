from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..deps import get_db, get_current_user, require_roles
from ..models import User
from ..schemas import DeviceTokenCreate, DeviceTokenOut, LocationCheck, GeofenceCreate, GeofenceOut, TriggeredGeofencesOut
from ..services import notification_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


# El dispositivo Android registra su token FCM
@router.post("/device-token", response_model=DeviceTokenOut)
def register_device_token(
    data: DeviceTokenCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_service.register_device_token(db, current_user.id, data.token)


# El front manda las coordenadas y el back devuelve las geofences que se han disparado
@router.post("/check-location", response_model=TriggeredGeofencesOut)
def check_location(
    data: LocationCheck,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    triggered = notification_service.get_triggered_geofences(db, current_user.id, data.lat, data.lng)

    # Registra en el log cada geofence disparada
    for geofence in triggered:
        notification_service.log_notification(db, current_user.id, geofence.id)

    return TriggeredGeofencesOut(triggered=triggered)


# Un admin crea una nueva geofence
@router.post("/geofences", response_model=GeofenceOut)
def create_geofence(
    data: GeofenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "ld")),
):
    return notification_service.create_geofence(
        db,
        name=data.name,
        message=data.message,
        lat=data.lat,
        lng=data.lng,
        radius_meters=data.radius_meters,
        poi_id=data.poi_id,
        route_id=data.route_id,
    )