from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class AddonItem(BaseModel):
    name: str
    price: float

class BookingRequestCreate(BaseModel):
    listing_id: int = Field(..., gt=0, description="ID of the listing being booked")
    requested_date: str = Field(..., description="Date in YYYY-MM-DD format")
    requested_time: Optional[str] = Field(None, description="Time in HH:MM format")
    location: str = Field(..., min_length=1, description="Location for the service")
    description: Optional[str] = Field(None, description="Additional details from client")
    selected_addons: List[AddonItem] = Field(default=[], description="Selected add-ons with prices")
    client_budget: Optional[float] = Field(None, gt=0, description="Client's proposed budget")

class BookingRequestUpdate(BaseModel):
    status: Optional[Literal['pending', 'accepted', 'declined', 'in_progress', 'completed', 'cancelled']] = None
    freelancer_price: Optional[float] = Field(None, gt=0, description="Freelancer's counter-offer price")

class BookingRequestResponse(BaseModel):
    id: int
    listing_id: int
    listing_title: str
    freelancer_id: int
    freelancer_name: str
    client_role: str
    client_id: int
    client_name: str
    requested_date: str
    requested_time: Optional[str]
    location: str
    description: Optional[str]
    selected_addons: List[AddonItem]
    client_budget: Optional[float]
    freelancer_price: Optional[float]
    price_difference_percent: Optional[float]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookingRequestSummary(BaseModel):
    id: int
    listing_title: str
    client_name: str
    freelancer_name: str
    requested_date: str
    status: str
    client_budget: Optional[float]
    freelancer_price: Optional[float]
    created_at: datetime