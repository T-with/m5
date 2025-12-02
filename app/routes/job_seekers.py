from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.job_seeker import JobSeekerCreate, JobSeekerUpdate, JobSeekerResponse
from app.services.job_seeker_service import JobSeekerService

router = APIRouter(prefix="/api/job-seekers", tags=["Job Seekers"])

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_job_seeker(data: JobSeekerCreate):
    return JobSeekerService.create(data)

@router.get("", response_model=List[JobSeekerResponse])
async def list_job_seekers():
    return JobSeekerService.list_all()

@router.get("/{id}", response_model=JobSeekerResponse)
async def get_job_seeker(id: int):
    return JobSeekerService.get_by_id(id)

@router.get("/{id}/evaluations", response_model=List)
async def get_job_seeker_evaluations(id: int):
    from app.services.evaluation_service import EvaluationService
    return EvaluationService.get_by_job_seeker(id)

@router.put("/{id}", response_model=dict)
async def update_job_seeker(id: int, data: JobSeekerUpdate):
    return JobSeekerService.update(id, data)

@router.delete("/{id}", response_model=dict)
async def delete_job_seeker(id: int):
    return JobSeekerService.delete(id)