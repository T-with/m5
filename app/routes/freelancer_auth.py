from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.services.freelancer_service import FreelancerService

router = APIRouter(
    prefix="/api/freelancers",
    tags=["Freelancer Authentication"]
)

class PasswordVerificationRequest(BaseModel):
    email: Optional[str] = None
    freelancer_id: Optional[int] = None
    password: str

class PasswordVerificationResponse(BaseModel):
    success: bool
    freelancer_id: int
    name: str
    email: str

@router.post("/verify-password", response_model=PasswordVerificationResponse)
async def verify_freelancer_password(request: PasswordVerificationRequest):
    """
    Verify freelancer password for authentication
    
    Can verify by either email or freelancer_id
    """
    if request.email:
        result = FreelancerService.verify_password(request.email, request.password)
    elif request.freelancer_id:
        # Get freelancer by ID and verify password
        freelancer = FreelancerService.get_freelancer(request.freelancer_id)
        result = FreelancerService.verify_password(freelancer['email'], request.password)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either email or freelancer_id must be provided"
        )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    return PasswordVerificationResponse(**result)

@router.get("/check-email/{email}")
async def check_freelancer_email(email: str):
    """
    Check if a freelancer exists with the given email
    """
    from app.database import get_db
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email FROM freelancers WHERE email = ?', (email,))
        freelancer = cursor.fetchone()
        
        if freelancer:
            return {
                "exists": True,
                "freelancer_id": freelancer['id'],
                "name": freelancer['name'],
                "email": freelancer['email']
            }
        else:
            return {"exists": False}