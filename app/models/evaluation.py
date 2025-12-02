from pydantic import BaseModel, Field
from typing import Optional

class EvaluationCreate(BaseModel):
    evaluator_id: int = Field(..., gt=0)
    job_seeker_id: int = Field(..., gt=0)
    score: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class EvaluationResponse(BaseModel):
    id: int
    evaluator_id: int
    evaluator_name: str
    evaluator_company: Optional[str]
    job_seeker_id: int
    job_seeker_name: str
    score: int
    comment: Optional[str]
    evaluation_date: str
    average_score: Optional[float] = None