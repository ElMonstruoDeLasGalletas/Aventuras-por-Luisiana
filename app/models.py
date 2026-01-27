from datetime import datetime, timezone
from sqlalchemy import ForeignKey, UniqueConstraint, String, Integer, DateTime, Float, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from .db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

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

class Review(Base):
    __tablename__ = "reviews"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    poi_id: Mapped[int] = mapped_column(ForeignKey("pois.id"), nullable=False, index=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False, index=True) #1..5
    content: Mapped[str] = mapped_column(String(1000), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), on_update=lambda: datetime.now(timezone.utc), nullable=False)
    # TODO: photo
    
    __table_args__ = (
        UniqueConstraint("user_id", "poi_id", name="uq_user_poi_review"), #Permitir una única review por POI
        CheckConstraint("rating >= 1 AND rating <= 5", name="rating_range")
    )
    
class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    # ID único de la preferencia
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Usuario al que pertenecen estas preferencias (solo puede tener unas preferencias)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True, index=True)
    
    # Lista de tags que le gustan al usuario (ej: ["nature", "kayak", "photo"])
    # Se guarda como JSON en la BD para poder meter varios tags
    preferred_tags: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    
    # Fecha en la que se crearon las preferencias (primera vez que configura el onboarding)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Fecha de última actualización (por si el usuario cambia sus preferencias más adelante)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), on_update=lambda: datetime.now(timezone.utc), nullable=False)