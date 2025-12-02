from fastapi import APIRouter, status, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.models.evaluator import EvaluatorCreate, EvaluatorResponse
from app.services.evaluator_service import EvaluatorService
from app.database import get_db
import hashlib

router = APIRouter(
    prefix='/api/evaluators',
    tags=['Evaluators']
)

class PasswordVerifyRequest(BaseModel):
    email: Optional[str] = None
    evaluator_id: Optional[int] = None
    password: str

class PasswordVerifyResponse(BaseModel):
    success: bool
    evaluator_id: int
    name: str
    company: Optional[str] = None

@router.post('', response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_evaluator(data: EvaluatorCreate):
    return EvaluatorService.create(data)

@router.get('', response_model=List[EvaluatorResponse])
async def list_evaluators():
    return EvaluatorService.list_all()

@router.get('/{id}', response_model=EvaluatorResponse)
async def get_evaluator(id: int):
    return EvaluatorService.get_by_id(id)

@router.post('/verify-password', response_model=PasswordVerifyResponse)
async def verify_password(data: PasswordVerifyRequest):
    """
    Verify evaluator's password
    
    Can verify by either email or evaluator_id
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Build query based on provided identifier
        if data.email:
            cursor.execute(
                'SELECT id, name, email, password, company FROM evaluators WHERE email = ?',
                (data.email,)
            )
        elif data.evaluator_id:
            cursor.execute(
                'SELECT id, name, email, password, company FROM evaluators WHERE id = ?',
                (data.evaluator_id,)
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
        
        # Verify password (check both hashed and plain text for backwards compatibility)
        password_hash = hashlib.sha256(data.password.encode()).hexdigest()
        
        if evaluator['password'] != password_hash and evaluator['password'] != data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )
        
        return PasswordVerifyResponse(
            success=True,
            evaluator_id=evaluator['id'],
            name=evaluator['name'],
            company=evaluator['company']
        )

@router.get('/check-email/{email}')
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