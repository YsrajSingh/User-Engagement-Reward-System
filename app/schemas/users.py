from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    username: str
    id: Optional[int] = None

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: Optional[str] = None 


class TokenData(BaseModel):
    username: str | None = None
    total_points: Optional[float] = None
