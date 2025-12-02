import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.config import settings
from app.database import init_database

from app.routes.freelancers import router as freelancers_router
from app.routes.freelancer_auth import router as freelancer_auth_router
from app.routes.ratings import router as ratings_router
from app.routes.admin import router as admin_router
from app.routes.evaluators import router as evaluators_router
from app.routes.evaluations import router as evaluations_router
from app.routes.job_seekers import router as job_seekers_router
from app.routes.messages import router as messages_router
from app.routes.messages_page import router as messages_page_router
from app.routes.listings import router as listings_router
from app.routes import listings, create_listings
from app.routes.booking_request import router as booking_requests_router
from app.routes.notification import router as notifications_router

PORT = int(os.getenv('PORT', 8000))

app = FastAPI(
    title='Free Recruitment Market',
    description='Free Recruitment Market - a platform for job seekers and evaluators with booking requests',
    version='2.2.1',
    docs_url='/docs',
    redoc_url='/redoc'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Include existing routes
app.include_router(admin_router)
app.include_router(freelancers_router)
app.include_router(freelancer_auth_router)
app.include_router(ratings_router)
app.include_router(evaluators_router)
app.include_router(evaluations_router)
app.include_router(job_seekers_router)
app.include_router(messages_router)
app.include_router(messages_page_router)
app.include_router(listings_router)
app.include_router(listings.router)
app.include_router(create_listings.router)
app.include_router(booking_requests_router)
app.include_router(notifications_router)

@app.on_event('startup')
async def startup_event():
    init_database()
    print(f'✓ Free Recruitment Market v2.2.1 started successfully')
    print(f'✓ Bug fixes: Notifications display, Employer dashboard, Listings display')
    print(f'✓ Features: Booking Requests & Notifications')
    print(f'✓ Admin Panel: http://{settings.host}:{settings.port}/admin')
    print(f'✓ API Docs: http://{settings.host}:{settings.port}/docs')

@app.get('/', tags=['Root'])
async def root():
    return {
        'message': 'Free Recruitment Market API',
        'version': '2.2.1',
        'features': ['Freelancer Profiles', 'Service Listings', 'Messaging', 'Booking Requests', 'Notifications'],
        'admin': '/admin',
        'docs': '/docs'
    }

@app.get('/api/health', tags=['Health'])
async def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Free Recruitment Market',
        'version': '2.2.1',
        'features': ['booking_requests', 'notifications', 'messaging', 'ratings', 'freelancer_auth']
    }

# Add the new HTML routes
@app.get('/booking_dashboard.html')
async def booking_dashboard():
    """Booking dashboard for freelancers"""
    from fastapi.responses import FileResponse
    import os
    # Fix path - templates is at same level as main.py
    html_path = os.path.join(os.path.dirname(__file__), 'templates', 'booking_dashboard.html')
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail=f"File not found: {html_path}")
    return FileResponse(html_path)

@app.get('/notifications.html')
async def notifications_page():
    """Notifications page"""
    from fastapi.responses import FileResponse
    import os
    html_path = os.path.join(os.path.dirname(__file__), 'templates', 'notifications.html')
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail=f"File not found: {html_path}")
    return FileResponse(html_path)

@app.get('/employer_dashboard.html')
async def employer_dashboard():
    """Employer dashboard for viewing booking requests"""
    from fastapi.responses import FileResponse
    import os
    html_path = os.path.join(os.path.dirname(__file__), 'templates', 'employer_dashboard.html')
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail=f"File not found: {html_path}")
    return FileResponse(html_path)

@app.get('/employer_booking_dashboard.html')
async def employer_booking_dashboard_alias():
    """Redirect to employer_dashboard.html for backwards compatibility"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url='/employer_dashboard.html', status_code=301)

if __name__ == '__main__':
    if __name__ == '__main__':
        import uvicorn
        uvicorn.run(
            'app.main:app',
            host='0.0.0.0',  # Changed!
            port=PORT,       # Changed!
            reload=os.getenv('RENDER') is None
        )