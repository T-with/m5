from fastapi import APIRouter, Query, HTTPException, status
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db

from app.models.booking_request import BookingRequestCreate, BookingRequestUpdate, BookingRequestResponse
from app.services.booking_request_service import BookingRequestService

router = APIRouter(
    prefix="/api/bookings",
    tags=["Booking Requests"]
)

# Temporary models for the route file
class AddonItem(BaseModel):
    name: str
    price: float

class BookingRequestCreate(BaseModel):
    listing_id: int
    requested_date: str
    requested_time: str = None
    location: str
    description: str = None
    selected_addons: List[AddonItem] = []
    client_budget: float = None

class BookingRequestUpdate(BaseModel):
    status: str = None
    freelancer_price: float = None

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_booking_request(
    request_data: BookingRequestCreate,
    client_role: str = Query(..., regex="^(job_seeker|evaluator)$"),
    client_id: int = Query(..., gt=0)
):
    """Create a new booking request"""
    return BookingRequestService.create_booking_request(
        request_data.listing_id, client_role, client_id, request_data.dict()
    )

@router.get("/freelancer/{freelancer_id}", response_model=List[dict])
async def get_freelancer_bookings(freelancer_id: int):
    """Get all booking requests for a freelancer"""
    return BookingRequestService.get_freelancer_bookings(freelancer_id)

@router.get("/client", response_model=List[dict])
async def get_client_bookings(
    client_role: str = Query(..., regex="^(job_seeker|evaluator)$"),
    client_id: int = Query(..., gt=0)
):
    """Get all booking requests made by a client"""
    return BookingRequestService.get_client_bookings(client_role, client_id)

@router.put("/{booking_id}", response_model=dict)
async def update_booking_request(
    booking_id: int,
    update_data: BookingRequestUpdate,
    freelancer_id: int = Query(None, gt=0),
    employer_id: int = Query(None, gt=0)
):
    """Update a booking request"""
    # If marking as completed, must be employer
    if update_data.status == 'completed':
        if not employer_id:
            raise HTTPException(
                status_code=403,
                detail='Only employers can mark bookings as complete'
            )
        
        # Verify employer owns this booking
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT br.*, l.freelancer_id 
                FROM booking_requests br
                JOIN listings l ON br.listing_id = l.id
                WHERE br.id = ? AND br.client_role = 'evaluator' AND br.client_id = ?
            """, (booking_id, employer_id))
            
            booking = cursor.fetchone()
            if not booking:
                raise HTTPException(
                    status_code=404,
                    detail='Booking not found or you are not authorized'
                )
            
            if booking['status'] != 'in_progress':
                raise HTTPException(
                    status_code=400,
                    detail=f'Cannot complete booking with status: {booking["status"]}'
                )
            
            # Update to completed
            cursor.execute("""
                UPDATE booking_requests 
                SET status = 'completed', updated_at = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), booking_id))
            
            conn.commit()
            
            # Create notification for freelancer
            from app.services.notification_service import NotificationService
            NotificationService.create_notification(
                user_role='job_seeker',
                user_id=booking['freelancer_id'],
                notification_type='booking_completed',
                title='Booking Completed',
                message='Client has marked your booking as complete!',
                related_id=booking_id,
                related_type='booking_request'
            )
            
            return {
                'success': True,
                'message': 'Booking marked as complete',
                'booking_id': booking_id
            }
    
    # Existing logic for freelancer updates
    if freelancer_id:
        return BookingRequestService.update_booking_status(
            booking_id, freelancer_id, update_data.dict(exclude_unset=True)
        )
    
    raise HTTPException(
        status_code=400,
        detail='Either freelancer_id or employer_id must be provided'
    )

@router.get("/{booking_id}", response_model=dict)
async def get_booking_request(booking_id: int):
    """Get details of a specific booking request"""
    return BookingRequestService.get_booking_by_id(booking_id)