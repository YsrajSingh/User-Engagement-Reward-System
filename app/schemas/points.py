from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class PointsCreate(BaseModel):
    points: float
    description: Optional[str] = None

class PointsResponse(BaseModel):
    id: int
    points: float
    description: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

class PointBase(BaseModel):
    name: str
    x: float
    y: float
    description: Optional[str] = None

class PointCreate(PointBase):
    pass  # Can add extra validation or attributes for creation if necessary

class PointUpdate(PointBase):
    pass  # Can add extra fields for update (e.g., making fields optional)

class PointInDB(PointBase):
    id: int

    class Config:
        orm_mode = True  # Allows the model to work with SQLAlchemy ORM objects


class PointOut(BaseModel):
    id: int
    user_id: int
    points: float
    description: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
