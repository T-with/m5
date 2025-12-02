from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class NotificationCreate(BaseModel):
    user_role: Literal['job_seeker', 'evaluator']
    user_id: int = Field(..., gt=0)
    type: Literal['booking_request', 'booking_accepted', 'booking_declined', 'booking_completed', 'new_message']
    title: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    related_id: Optional[int] = Field(None, description="ID of related booking/message")
    related_type: Optional[str] = Field(None, description="Type of related object")

class NotificationResponse(BaseModel):
    id: int
    user_role: str
    user_id: int
    type: str
    title: str
    message: str
    related_id: Optional[int]
    related_type: Optional[str]
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationUpdate(BaseModel):
    is_read: bool = True