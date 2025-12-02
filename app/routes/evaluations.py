from fastapi import APIRouter, status
from typing import List
from app.services.evaluation_service import EvaluationService
router = APIRouter(
    prefix='/api/evaluations',
    tags=['Evaluations']
)

@router.get('', response_model=List)
async def list_evaluations():
    return EvaluationService.list_all()