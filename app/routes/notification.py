from fastapi import APIRouter, Query, HTTPException, status
from typing import List
from pydantic import BaseModel

from app.models.notification import NotificationResponse, NotificationUpdate
from app.services.notification_service import NotificationService

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)

class NotificationUpdate(BaseModel):
    is_read: bool = True

@router.get("", response_model=List[dict])
async def get_user_notifications(
    user_role: str = Query(..., regex="^(job_seeker|evaluator)$"),
    user_id: int = Query(..., gt=0),
    unread_only: bool = Query(False, description="Get only unread notifications")
):
    """
    Get notifications for a user
    
    **Query Parameters:**
    - **user_role**: Role of the user (job_seeker or evaluator)
    - **user_id**: ID of the user
    - **unread_only**: If true, return only unread notifications
    
    **Returns:**
    - List of notifications for the user
    """
    return NotificationService.get_user_notifications(user_role, user_id, unread_only)

@router.get("/unread-count", response_model=dict)
async def get_unread_count(
    user_role: str = Query(..., regex="^(job_seeker|evaluator)$"),
    user_id: int = Query(..., gt=0)
):
    """
    Get count of unread notifications for a user
    
    **Query Parameters:**
    - **user_role**: Role of the user (job_seeker or evaluator)
    - **user_id**: ID of the user
    
    **Returns:**
    - Count of unread notifications
    """
    count = NotificationService.get_unread_count(user_role, user_id)
    return {"unread_count": count}

@router.put("/{notification_id}/read", response_model=dict)
async def mark_notification_read(
    notification_id: int,
    user_id: int = Query(..., gt=0)
):
    """
    Mark a notification as read
    
    **Path Parameters:**
    - **notification_id**: ID of the notification to mark as read
    
    **Query Parameters:**
    - **user_id**: ID of the user (for authorization)
    
    **Returns:**
    - Success message
    """
    return NotificationService.mark_notification_read(notification_id, user_id)

@router.put("/read-all", response_model=dict)
async def mark_all_notifications_read(
    user_role: str = Query(..., regex="^(job_seeker|evaluator)$"),
    user_id: int = Query(..., gt=0)
):
    """
    Mark all notifications as read for a user
    
    **Query Parameters:**
    - **user_role**: Role of the user (job_seeker or evaluator)
    - **user_id**: ID of the user
    
    **Returns:**
    - Success message
    """
    return NotificationService.mark_all_notifications_read(user_role, user_id)

@router.delete("/{notification_id}", response_model=dict)
async def delete_notification(
    notification_id: int,
    user_id: int = Query(..., gt=0)
):
    """
    Delete a notification
    
    **Path Parameters:**
    - **notification_id**: ID of the notification to delete
    
    **Query Parameters:**
    - **user_id**: ID of the user (for authorization)
    
    **Returns:**
    - Success message
    """
    return NotificationService.delete_notification(notification_id, user_id)