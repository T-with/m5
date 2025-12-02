from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RatingCreate(BaseModel):
    freelancer_id: int
    evaluator_id: int
    rating: int
    review_text: Optional[str] = None

class RatingResponse(BaseModel):
    id: int
    freelancer_id: int
    evaluator_id: int
    rating: int
    review_text: Optional[str] = None
    created_at: datetime
    evaluator_name: str
    evaluator_company: Optional[str] = None
    job_seeker_name: str

    class Config:
        from_attributes = True

class FreelancerRating(BaseModel):
    id: int
    freelancer_id: int
    evaluator_id: int
    rating: int
    review_text: Optional[str] = None
    created_at: datetime
    evaluator_name: str
    evaluator_company: Optional[str] = None
    average_score: float

    class Config:
        from_attributes = True


class RatingDistribution(BaseModel):
    rating_info: dict  # Contains: average, count, total_reviews
    rating_distribution: dict  # Rating counts per star (1-5)
    reviews: List[RatingResponse]