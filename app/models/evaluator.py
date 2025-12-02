from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EvaluatorCreate(BaseModel):
    name: str
    email: str
    password: str
    company: Optional[str] = None
    position: Optional[str] = None

class EvaluatorResponse(BaseModel):
    id: int
    name: str
    email: str
    company: Optional[str] = None
    position: Optional[str] = None
    evaluation_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True