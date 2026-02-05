from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

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
        orm_mode = True
    