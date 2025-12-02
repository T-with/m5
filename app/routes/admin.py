#197d273c94a0b17226ba40905c4328817094769072e08ed71db8a640b5fd0a95
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import hashlib
import os

router = APIRouter(tags=['Pages'])  # ← MUST BE LINE 7!

# Get templates directory path
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '../templates')

# Admin password hash (SHA-256) - Password: CMPT276
ADMIN_PASSWORD_HASH = os.getenv(
    'ADMIN_PASSWORD_HASH',
    '197d273c94a0b17226ba40905c4328817094769072e08ed71db8a640b5fd0a95'
)

def verify_admin_password(password: str) -> bool:
    """Verify admin password using SHA-256 hash"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash == ADMIN_PASSWORD_HASH

class AdminLoginRequest(BaseModel):
    password: str

@router.post('/api/admin/verify')
async def verify_admin(request: AdminLoginRequest):
    """Verify admin password"""
    print(f"🔍 Received password verification request")
    print(f"🔍 Input hash: {hashlib.sha256(request.password.encode()).hexdigest()}")
    print(f"🔍 Expected hash: {ADMIN_PASSWORD_HASH}")
    
    if verify_admin_password(request.password):
        return {'success': True, 'message': 'Admin access granted'}
    else:
        raise HTTPException(status_code=401, detail='Invalid admin password')

@router.get('/', response_class=HTMLResponse)
async def home():
    """Home page"""
    html_path = os.path.join(TEMPLATES_DIR, 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@router.get('/admin', response_class=HTMLResponse)
async def admin_dashboard():
    """Admin panel"""
    html_path = os.path.join(TEMPLATES_DIR, 'admin.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@router.get('/job_seeker_register.html', response_class=HTMLResponse)
async def job_seeker_register():
    """Job seeker registration page"""
    html_path = os.path.join(TEMPLATES_DIR, 'job_seeker_register.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@router.get('/evaluator_register.html', response_class=HTMLResponse)
async def evaluator_register():
    """Evaluator registration page"""
    html_path = os.path.join(TEMPLATES_DIR, 'evaluator_register.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@router.get('/talent_market.html', response_class=HTMLResponse)
async def talent_market():
    """Talent market page"""
    html_path = os.path.join(TEMPLATES_DIR, 'talent_market.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@router.get('/index.html', response_class=HTMLResponse)
async def index_html():
    """Home page (alias)"""
    html_path = os.path.join(TEMPLATES_DIR, 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())
@router.get('/messages.html', response_class=HTMLResponse)
async def messages_page():
    """Messages page"""
    html_path = os.path.join(TEMPLATES_DIR, 'messages.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@router.get('/listings.html', response_class=HTMLResponse)
async def listings_page():
    """Listings page"""
    html_path = os.path.join(TEMPLATES_DIR, 'listings.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@router.get('/create_listings.html', response_class=HTMLResponse)
async def create_listings_page():
    """Create listings page"""
    html_path = os.path.join(TEMPLATES_DIR, 'create_listings.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@router.get('/sign_in.html', response_class=HTMLResponse)
async def sign_in_page():
    """Sign in page"""
    html_path = os.path.join(TEMPLATES_DIR, 'sign_in.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

