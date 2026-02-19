from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=6, max_length=128)
    role_id: int

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str

    class Config:
        from_attributes = True

class MediaItem(BaseModel):
    type: str = Field(pattern="^(image|audio|video)$")
    url: str
    title: Optional[str] = None

class POICreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    lat: float
    lng: float
    description: Optional[str] = None
    tags: List[str] = []
    media: List[MediaItem] = []
    type: Optional[str] = Field(default=None, max_length=60)

class POIOut(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    description: Optional[str]
    tags: List[str]
    media: List[MediaItem]
    type: Optional[str]

    class Config:
        from_attributes = True
    
class POIUpdate(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    media: Optional[list] = None
    type: Optional[str] = None

class RouteCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    poi_ids: List[int] = Field(default_factory=list, min_length=1)
    image_url: Optional[str] = None 
    
class RouteOut(BaseModel):
    id: int
    name: str
    description:  Optional[str]
    poi_ids: List[int]
    created_at: datetime
    updated_at: datetime
    image_url: Optional[str]
    
    class Config:
        from_attributes = True
        
class RouteImport(BaseModel):
    name: str
    description: Optional[str] = None
    poi_ids: List[str]
    image_url: Optional[str] = None

class RouteUpdate(BaseModel):
    name: Optional[str] =  None
    description: Optional[str] = None
    poi_ids: Optional[list] = None
    image_url: Optional[str] = None
    
class ReviewCreate(BaseModel):
    route_id: int
    rating: int = Field(ge=1, le=5)
    content: Optional[str] = Field(default=None, max_length=1000)

class ReviewOut(BaseModel):
    id: int
    route_id: int
    rating: int
    content: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class ReviewUpdate(BaseModel):
    rating: int = Field(ge=1, le=5)
    content: Optional[str] = Field(default=None, max_length=1000)

# Schema para un Tag individual (solo lectura)
class TagOut(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True


# Schema para crear un nuevo tag en el catálogo (solo admin, normalmente)
class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)

class TagDelete(BaseModel):
    name: str

# Schema para añadir tags a las preferencias del usuario (lo que manda el frontend)
class UserPreferencesAdd(BaseModel):
    # Lista de IDs de tags que quiere añadir (ej: [1, 3, 5])
    tag_ids: List[int] = Field(default=[])


# Schema para eliminar tags de las preferencias del usuario
class UserPreferencesRemove(BaseModel):
    # Lista de IDs de tags que quiere eliminar (ej: [2, 4])
    tag_ids: List[int] = Field(default=[])


# Schema para cuando el backend devuelve las preferencias (lo que recibe el frontend)
class UserPreferencesOut(BaseModel):
    # Lista de tags completos con su ID y nombre
    tags: List[TagOut]
    
    class Config:
        from_attributes = True
        
class FavouritesCreate(BaseModel):
    route_id: int

class FavouritesOut(BaseModel):
    id: int
    route_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
# No hay update de favoritos porque al eliminar se quita de fav y al crearlo se pone.

# Schema para registrar el token FCM del dispositivo
class DeviceTokenCreate(BaseModel):
    token: str

class DeviceTokenOut(BaseModel):
    id: int
    user_id: int
    token: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Schema para recibir la ubicación del usuario
class LocationCheck(BaseModel):
    lat: float
    lng: float


# Schema para crear una geofence
class GeofenceCreate(BaseModel):
    name: str
    message: str
    lat: float
    lng: float
    radius_meters: float = 200.0
    poi_id: int
    route_id: int | None = None


# Schema para devolver una geofence
class GeofenceOut(BaseModel):
    id: int
    name: str
    message: str
    lat: float
    lng: float
    radius_meters: float
    poi_id: int | None
    route_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


# Schema para devolver las geofences que se han disparado
class TriggeredGeofencesOut(BaseModel):
    triggered: List[GeofenceOut]