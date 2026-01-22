from typing import Optional, List
from pydantic import BaseModel

class POIUpdate(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    media: Optional[list] = None
    type: Optional[str] = None
