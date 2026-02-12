from datetime import datetime, timezone
from sqlalchemy import ForeignKey, UniqueConstraint, String, Integer, DateTime, Float, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from .db import Base

class UserRole(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True) # 'user', 'ld', 'admin'

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), default=3)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    favourites = relationship("UserFavs", back_populates="user")
    role = relationship("UserRole")

class POI(Base):
    __tablename__ = "pois"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)

    description: Mapped[str | None] = mapped_column(String, nullable=True)

    # tags[] y media[] en Postgres como JSONB (ideal para rapidez y flexibilidad)
    tags: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    media: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)  # [{type,url,title?}]

    type: Mapped[str | None] = mapped_column(String(60), nullable=True, index=True)

    # para sync y borrado suave
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

class Route(Base):
    __tablename__ = "routes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    poi_ids: Mapped[list] = mapped_column(JSONB, nullable=False)
    is_deleted: Mapped[Boolean] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False) 

    favourited_by = relationship("UserFavs", back_populates="route")
    

class Review(Base):
    __tablename__ = "reviews"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"), nullable=False, index=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False, index=True) #1..5
    content: Mapped[str] = mapped_column(String(1000), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    # TODO: photo
    
    __table_args__ = (
        UniqueConstraint("user_id", "route_id", name="uq_user_poi_review"), #Permitir una única review por POI
        CheckConstraint("rating >= 1 AND rating <= 5", name="rating_range")
    )

# Catálogo de tags disponibles en la aplicación
class Tag(Base):
    __tablename__ = "tags"
    
    # ID único del tag
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Nombre del tag (ej: "nature", "kayak", "photo")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    
    # Fecha de creación del tag
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

# Tabla intermedia: relación muchos a muchos entre User y Tag
class UserPreferredTag(Base):
    __tablename__ = "user_preferred_tags"
    
    # ID único de la relación
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Usuario que tiene esta preferencia
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    
    # Tag que le gusta al usuario
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=False, index=True)
    
    # Fecha en que añadió esta preferencia
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    __table_args__ = (
        # Un usuario no puede tener el mismo tag duplicado
        UniqueConstraint("user_id", "tag_id", name="uq_user_tag"),
    )

    
# Ya no necesitamos esta tabla, pero la dejamos vacía para mantener compatibilidad temporal
class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    
class UserFavs(Base):
    __tablename__ = "user_favs"
    __table_args__ = (UniqueConstraint("user_id", "route_id", name="uq_user_route"),)
   
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    user = relationship("User", back_populates="favourites")
    route = relationship("Route", back_populates="favourited_by")
    
    # Token FCM del dispositivo del usuario (para enviar notificaciones push)
class DeviceToken(Base):
    __tablename__ = "device_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Usuario al que pertenece este dispositivo
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    # Token FCM que proporciona Firebase al dispositivo Android
    token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Para desactivar tokens caducados sin borrarlos
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User")


# Zona geográfica que dispara una notificación al entrar
class Geofence(Base):
    __tablename__ = "geofences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Nombre descriptivo de la zona (ej: "Entrada al Barrio Francés")
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # Mensaje que recibirá el usuario al entrar en la zona
    message: Mapped[str] = mapped_column(String(500), nullable=False)

    # Centro de la zona geográfica
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)

    # Radio en metros que define el área de la zona
    radius_meters: Mapped[float] = mapped_column(Float, nullable=False, default=200.0)

    # POI o ruta asociada (opcionales)
    poi_id: Mapped[int | None] = mapped_column(ForeignKey("pois.id"), nullable=True, index=True)
    route_id: Mapped[int | None] = mapped_column(ForeignKey("routes.id"), nullable=True, index=True)

    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    poi = relationship("POI")
    route = relationship("Route")


# Registro de notificaciones enviadas (para no repetir la misma al usuario)
class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    geofence_id: Mapped[int] = mapped_column(ForeignKey("geofences.id"), nullable=False, index=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User")
    geofence = relationship("Geofence")