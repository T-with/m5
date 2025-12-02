from fastapi import APIRouter, status
from typing import List  # add List 

# add RatingResponse 
from app.models.rating import RatingCreate, RatingDistribution, RatingResponse
from app.services.rating_service import RatingService

router = APIRouter(
    prefix="/api",
    tags=["Ratings"]
)


@router.post(
    "/ratings",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Rating",
    description="Submit a rating and review for a freelancer (1-5 stars)"
)
async def create_rating(rating: RatingCreate):
    """
    Submit a rating for a freelancer
    
    **Required fields:**
    - **freelancer_id**: ID of the freelancer being rated
    - **client_name**: Name of the client leaving the review
    - **rating**: Star rating (1-5)
    
    **Optional fields:**
    - **review_text**: Written review/feedback
    
    **Rating system:**
    - 5 stars: Excellent
    - 4 stars: Very Good
    - 3 stars: Good
    - 2 stars: Fair
    - 1 star: Poor
    """
    return RatingService.create_rating(rating)


@router.get(
    "/freelancers/{freelancer_id}/ratings",
    response_model=RatingDistribution,
    summary="Get Freelancer Ratings",
    description="Get all ratings and reviews for a specific freelancer"
)
async def get_freelancer_ratings(freelancer_id: int):
    """
    Get all ratings for a freelancer
    
    **Path Parameters:**
    - **freelancer_id**: Unique freelancer identifier
    
    **Returns:**
    - Average rating and total review count
    - Rating distribution (number of 1-5 star ratings)
    - All reviews in chronological order (newest first)
    """
    return RatingService.get_freelancer_ratings(freelancer_id)


@router.get(
    "/ratings/freelancer/{freelancer_id}",
    response_model=List[RatingResponse],
    summary="Get Freelancer Reviews List",
    description="Get list of reviews for a freelancer (Frontend compatibility)"
)
async def get_freelancer_reviews_list(freelancer_id: int):
    """
    Get raw list of reviews for a freelancer to match frontend expectations.
    Frontend expects an array of reviews, not a wrapped object.
    """
    data = RatingService.get_freelancer_ratings(freelancer_id)
    return data['reviews']


@router.get(
    "/freelancers/{freelancer_id}/rating-statistics",
    response_model=dict,
    summary="Get Rating Statistics",
    description="Get detailed rating statistics including percentages"
)
async def get_rating_statistics(freelancer_id: int):
    """
    Get detailed rating statistics
    
    **Path Parameters:**
    - **freelancer_id**: Unique freelancer identifier
    
    **Returns:**
    - Average rating and total reviews
    - Detailed breakdown with percentages for each star rating
    """
    return RatingService.get_rating_statistics(freelancer_id)