from fastapi import APIRouter, status
from typing import List

from app.models.freelancer import (
    FreelancerCreate,
    FreelancerUpdate,
    FreelancerResponse,
    FreelancerListResponse
)
from app.services.freelancer_service import FreelancerService

router = APIRouter(
    prefix="/api/freelancers",
    tags=["Freelancers"]
)


@router.post(
    "",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Create Freelancer Profile",
    description="Create a new freelancer profile with customizable information"
)
async def create_freelancer(freelancer: FreelancerCreate):
    """
    Create a new freelancer profile
    
    **Required fields:**
    - **name**: Freelancer's full name
    - **email**: Unique email address
    
    **Optional fields:**
    - **profile_picture**: URL or Base64 encoded image
    - **about_me**: Personal introduction/bio
    - **availability**: Status (available/busy/unavailable)
    """
    return FreelancerService.create_freelancer(freelancer)


@router.get(
    "",
    response_model=List[FreelancerListResponse],
    summary="List All Freelancers",
    description="Get a list of all freelancers with their basic info and ratings"
)
async def list_freelancers():
    """
    Get all freelancer profiles
    
    Returns a list of all freelancers including:
    - Basic profile information
    - Average rating and total reviews
    """
    return FreelancerService.list_freelancers()


@router.get(
    "/{freelancer_id}",
    response_model=FreelancerResponse,
    summary="Get Freelancer Details",
    description="Get detailed information about a specific freelancer"
)
async def get_freelancer(freelancer_id: int):
    """
    Get detailed freelancer profile
    
    **Path Parameters:**
    - **freelancer_id**: Unique freelancer identifier
    
    **Returns:**
    - Complete profile information
    - Rating statistics
    - Recent 5 reviews
    """
    return FreelancerService.get_freelancer(freelancer_id, include_reviews=True)


@router.put(
    "/{freelancer_id}",
    response_model=dict,
    summary="Update Freelancer Profile",
    description="Update freelancer profile information"
)
async def update_freelancer(freelancer_id: int, freelancer: FreelancerUpdate):
    """
    Update freelancer profile
    
    **Path Parameters:**
    - **freelancer_id**: Unique freelancer identifier
    
    **Updatable fields:**
    - name
    - profile_picture
    - about_me
    - availability
    """
    return FreelancerService.update_freelancer(freelancer_id, freelancer)


@router.delete(
    "/{freelancer_id}",
    response_model=dict,
    summary="Delete Freelancer Profile",
    description="Delete a freelancer profile and all associated ratings"
)
async def delete_freelancer(freelancer_id: int):
    """
    Delete freelancer profile
    
    **Path Parameters:**
    - **freelancer_id**: Unique freelancer identifier
    
    **Warning:** This will also delete all ratings associated with this freelancer
    """
    return FreelancerService.delete_freelancer(freelancer_id)