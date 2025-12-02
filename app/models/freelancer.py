from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class FreelancerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  # NEW: Added password field
    phone: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    skills: Optional[str] = None
    about_me: Optional[str] = None
    work_experience: Optional[str] = None
    availability: str = 'available'
    profile_picture: Optional[str] = None

class FreelancerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # NEW: Added password field for updates
    phone: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    skills: Optional[str] = None
    about_me: Optional[str] = None
    work_experience: Optional[str] = None
    availability: Optional[str] = None
    profile_picture: Optional[str] = None

class FreelancerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    skills: Optional[str] = None
    about_me: Optional[str] = None
    work_experience: Optional[str] = None
    availability: str
    profile_picture: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class FreelancerWithRating(FreelancerResponse):
    rating_info: dict

    class Config:
        from_attributes = True

class FreelancerListResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    skills: Optional[str] = None
    about_me: Optional[str] = None
    work_experience: Optional[str] = None
    availability: str
    profile_picture: Optional[str] = None
    created_at: datetime
    average_score: float = 0.0
    evaluation_count: int = 0
    rating_info: dict

    class Config:
        from_attributes = True