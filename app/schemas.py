from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=6, max_length=128)

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
    
class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None, max_length=1000)

class ReviewOut(BaseModel):
    id: int
    user_id: int
    route_id: int
    rating: int
    content: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
    
class RouteCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    poi_ids: List[int] = Field(default_factory=list, min_length=1)
    
class RouteOut(BaseModel):
    id: int
    name: str
    dscription:  Optional[str]
    poi_ids: List[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class RouteImport(BaseModel):
    name: str
    description: Optional[str] = None
    poi_ids: List[str]
