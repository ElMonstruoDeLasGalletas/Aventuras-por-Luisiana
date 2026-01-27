from typing import Optional, List
from pydantic import BaseModel

class RouteUpdate(BaseModel):
    name: Optional[str] =  None
    description: Optional[str] = None
    poi_ids: Optional[list] = None