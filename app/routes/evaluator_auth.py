# Add this route to your existing app/routes/evaluators.py file

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import sqlite3
from app.database import get_db

# Add this route class to your existing evaluators.py
class PasswordVerificationRequest(BaseModel):
    email: Optional[str] = None
    evaluator_id: Optional[int] = None
    password: str

class PasswordVerificationResponse(BaseModel):
    success: bool
    evaluator_id: int
    name: str
    company: Optional[str] = None

# Add this route function to your existing router
@router.post("/verify-password", response_model=PasswordVerificationResponse)
async def verify_evaluator_password(request: PasswordVerificationRequest):
    """
    Verify evaluator password for authentication
    
    Can verify by either email or evaluator_id
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Build query based on provided identifier
        if request.email:
            cursor.execute(
                'SELECT id, name, email, password, company FROM evaluators WHERE email = ?',
                (request.email,)
            )
        elif request.evaluator_id:
            cursor.execute(
                'SELECT id, name, email, password, company FROM evaluators WHERE id = ?',
                (request.evaluator_id,)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either email or evaluator_id must be provided"
            )
        
        evaluator = cursor.fetchone()
        
        if not evaluator:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evaluator not found"
            )
        
        # Verify password
        if evaluator['password'] != request.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )
        
        return PasswordVerificationResponse(
            success=True,
            evaluator_id=evaluator['id'],
            name=evaluator['name'],
            company=evaluator['company']
        )

@router.get("/check-email/{email}")
async def check_evaluator_email(email: str):
    """
    Check if an evaluator exists with the given email
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, company FROM evaluators WHERE email = ?', (email,))
        evaluator = cursor.fetchone()
        
        if evaluator:
            return {
                "exists": True,
                "evaluator_id": evaluator['id'],
                "name": evaluator['name'],
                "company": evaluator['company']
            }
        else:
            return {"exists": False}