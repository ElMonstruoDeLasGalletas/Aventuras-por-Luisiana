from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class RouteCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    poi_ids: List[int] = Field(default_factory=list, min_length=1)
    
class RouteOut(BaseModel):
    id: int
    name: str
    description:  Optional[str]
    poi_ids: List[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class RouteImport(BaseModel):
    name: str
    description: Optional[str] = None
    poi_ids: List[str]

class RouteUpdate(BaseModel):
    name: Optional[str] =  None
    description: Optional[str] = None
    poi_ids: Optional[list] = None