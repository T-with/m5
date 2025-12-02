from app.routes.freelancers import router as freelancers_router
from app.routes.ratings import router as ratings_router
from app.routes.admin import router as admin_router
from app.routes.evaluators import router as evaluators_router
from app.routes.evaluations import router as evaluations_router
from app.routes.job_seekers import router as job_seekers_router

freelancers = freelancers_router
ratings = ratings_router
admin = admin_router
evaluators = evaluators_router
evaluations = evaluations_router
job_seekers = job_seekers_router

__all__ = [
    'freelancers', 
    'ratings', 
    'admin', 
    'evaluators', 
    'evaluations',
    'job_seekers'
]