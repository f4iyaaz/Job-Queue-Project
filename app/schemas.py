from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobCreate(BaseModel):
    type: str
    payload: dict

class JobResponse(BaseModel):
    id: str
    type: str
    status: str
    created_at: datetime  # Change from str to datetime
    payload: dict
    result: Optional[dict] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None  # Add this
    completed_at: Optional[datetime] = None  # Add this
    
    class Config:
        from_attributes = True