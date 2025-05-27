from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShanyrakCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    location: str

class ShanyrakUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None

class ShanyrakOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    location: str
    created_at: datetime

    class Config:
        orm_mode = True

