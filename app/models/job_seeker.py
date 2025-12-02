from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class JobSeekerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    location: str
    profile_picture: Optional[str] = None
    work_experience: str
    skills: Optional[str] = None
    job_type: str
    availability: str = "available"

class JobSeekerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    profile_picture: Optional[str] = None
    work_experience: Optional[str] = None
    skills: Optional[str] = None
    job_type: Optional[str] = None
    availability: Optional[str] = None

class JobSeekerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    location: str
    profile_picture: Optional[str]
    work_experience: str
    skills: Optional[str]
    job_type: str
    availability: str
    average_score: float = 0.0
    evaluation_count: int = 0
    created_at: str
    updated_at: str