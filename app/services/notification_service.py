from sqlalchemy.orm import Session
from datetime import datetime, timezone, date
from math import radians, sin, cos, sqrt, atan2

from ..models import DeviceToken, Geofence, NotificationLog


# Fórmula Haversine: calcula la distancia en metros entre dos coordenadas
def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371000  # Radio de la Tierra en metros
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lng2 - lng1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


# Registra o actualiza el token FCM de un dispositivo
def register_device_token(db: Session, user_id: int, token: str) -> DeviceToken:
    existing = db.query(DeviceToken).filter(DeviceToken.token == token).first()
    if existing:
        existing.user_id = user_id
        existing.is_active = True
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(existing)
        return existing

    device_token = DeviceToken(user_id=user_id, token=token)
    db.add(device_token)
    db.commit()
    db.refresh(device_token)
    return device_token


# Devuelve las geofences activas que el usuario aún no ha recibido hoy
def get_triggered_geofences(db: Session, user_id: int, lat: float, lng: float) -> list[Geofence]:
    geofences = db.query(Geofence).filter(Geofence.is_deleted == False).all()
    triggered = []

    for geofence in geofences:
        distance = haversine_distance(lat, lng, geofence.lat, geofence.lng)
        if distance <= geofence.radius_meters:
            # Comprueba si ya se envió esta notificación hoy
            already_sent = db.query(NotificationLog).filter(
                NotificationLog.user_id == user_id,
                NotificationLog.geofence_id == geofence.id,
                NotificationLog.sent_at >= datetime.now(timezone.utc).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
            ).first()

            if not already_sent:
                triggered.append(geofence)

    return triggered


# Registra en el log que se envió la notificación
def log_notification(db: Session, user_id: int, geofence_id: int) -> NotificationLog:
    log = NotificationLog(user_id=user_id, geofence_id=geofence_id)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


# Crea una nueva geofence
def create_geofence(db: Session, name: str, message: str, lat: float, lng: float,
                    radius_meters: float, poi_id: int | None, route_id: int | None) -> Geofence:
    geofence = Geofence(
        name=name,
        message=message,
        lat=lat,
        lng=lng,
        radius_meters=radius_meters,
        poi_id=poi_id,
        route_id=route_id
    )
    db.add(geofence)
    db.commit()
    db.refresh(geofence)
    return geofence