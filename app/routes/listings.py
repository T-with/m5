import json
from typing import List, Optional

from fastapi import APIRouter, Query, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

from app.database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


# ---------- Pydantic models ----------

class AddonItem(BaseModel):
    name: str
    price: float


class ListingResponse(BaseModel):
    id: int
    freelancer_id: int
    freelancer_name: str
    title: str
    description: str
    base_price: float
    tags: List[str]
    addons: List[AddonItem]
    created_at: str

    class Config:
        from_attributes = True


# ---------- Page routes ----------

@router.get("/listings-page", response_class=HTMLResponse)
async def listings_page(request: Request):
    try:
        return templates.TemplateResponse("listings.html", {"request": request})
    except Exception as e:
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(f"Error loading template: {str(e)}", status_code=500)


@router.get("/listings.html", response_class=HTMLResponse)
async def listings_html(request: Request):
    try:
        return templates.TemplateResponse("listings.html", {"request": request})
    except Exception as e:
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(f"Error loading template: {str(e)}", status_code=500)


# ---------- API routes ----------

@router.get(
    "/api/listings",
    response_model=List[ListingResponse],
    summary="Get All Listings",
    description="Get all service listings with optional filtering"
)
async def get_all_listings(
    title_search: Optional[str] = Query(None, description="Search by title"),
    freelancer_search: Optional[str] = Query(None, description="Search by freelancer name"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter by")
):
    """
    Get all listings with optional filtering
    
    **Query Parameters:**
    - **title_search**: Filter by title (case-insensitive)
    - **freelancer_search**: Filter by freelancer name (case-insensitive)
    - **tags**: Comma-separated list of tags to filter by
    
    **Returns:**
    - List of all listings matching the criteria
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                l.id,
                l.freelancer_id,
                f.name as freelancer_name,
                l.title,
                l.description,
                l.base_price,
                l.tags,
                l.addons,
                l.created_at
            FROM listings l
            JOIN freelancers f ON l.freelancer_id = f.id
            WHERE 1=1
        '''
        
        params = []
        
        # Add title search filter
        if title_search:
            query += ' AND LOWER(l.title) LIKE ?'
            params.append(f'%{title_search.lower()}%')
        
        # Add freelancer search filter
        if freelancer_search:
            query += ' AND LOWER(f.name) LIKE ?'
            params.append(f'%{freelancer_search.lower()}%')
        
        query += ' ORDER BY l.created_at DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        listings = []
        for row in rows:
            tags_list = json.loads(row['tags'])
            addons_list = json.loads(row['addons']) if row['addons'] else []
            
            # Filter by tags if specified
            if tags:
                requested_tags = [t.strip().lower() for t in tags.split(',')]
                row_tags_lower = [t.lower() for t in tags_list]
                
                # Check if any requested tag is in the listing's tags
                if not any(tag in row_tags_lower for tag in requested_tags):
                    continue
            
            listing = ListingResponse(
                id=row['id'],
                freelancer_id=row['freelancer_id'],
                freelancer_name=row['freelancer_name'],
                title=row['title'],
                description=row['description'],
                base_price=row['base_price'],
                tags=tags_list,
                addons=addons_list,
                created_at=row['created_at']
            )
            listings.append(listing)
        
        return listings


# FIX FOR BUG #3: Add alias endpoint for /api/listings/all
@router.get(
    "/api/listings/all",
    response_model=List[ListingResponse],
    summary="Get All Listings (Alias)",
    description="Alias endpoint for getting all service listings - redirects to /api/listings"
)
async def get_all_listings_alias(
    title_search: Optional[str] = Query(None, description="Search by title"),
    freelancer_search: Optional[str] = Query(None, description="Search by freelancer name"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter by")
):
    """
    Alias endpoint that calls the main get_all_listings function.
    This fixes the bug where frontend calls /api/listings/all instead of /api/listings
    """
    return await get_all_listings(title_search, freelancer_search, tags)


@router.get(
    "/api/freelancers/{freelancer_id}/listings",
    response_model=List[ListingResponse],
    summary="Get Freelancer's Listings",
    description="Get all listings for a specific freelancer"
)
async def get_freelancer_listings(freelancer_id: int):
    """
    Get all listings for a specific freelancer
    
    **Path Parameters:**
    - **freelancer_id**: The ID of the freelancer
    
    **Returns:**
    - List of all listings for this freelancer
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Verify freelancer exists
        cursor.execute('SELECT id, name FROM freelancers WHERE id = ?', (freelancer_id,))
        freelancer = cursor.fetchone()
        
        if not freelancer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Freelancer with id {freelancer_id} not found"
            )
        
        cursor.execute('''
            SELECT 
                l.id,
                l.freelancer_id,
                f.name as freelancer_name,
                l.title,
                l.description,
                l.base_price,
                l.tags,
                l.addons,
                l.created_at
            FROM listings l
            JOIN freelancers f ON l.freelancer_id = f.id
            WHERE l.freelancer_id = ?
            ORDER BY l.created_at DESC
        ''', (freelancer_id,))
        
        rows = cursor.fetchall()
        
        listings = []
        for row in rows:
            listing = ListingResponse(
                id=row['id'],
                freelancer_id=row['freelancer_id'],
                freelancer_name=row['freelancer_name'],
                title=row['title'],
                description=row['description'],
                base_price=row['base_price'],
                tags=json.loads(row['tags']),
                addons=json.loads(row['addons']) if row['addons'] else [],
                created_at=row['created_at']
            )
            listings.append(listing)
        
        return listings


@router.get(
    "/api/listings/{listing_id}",
    response_model=ListingResponse,
    summary="Get Single Listing",
    description="Get details of a specific listing"
)
async def get_listing(listing_id: int):
    """
    Get a single listing by ID
    
    **Path Parameters:**
    - **listing_id**: The ID of the listing
    
    **Returns:**
    - Listing details
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                l.id,
                l.freelancer_id,
                f.name as freelancer_name,
                l.title,
                l.description,
                l.base_price,
                l.tags,
                l.addons,
                l.created_at
            FROM listings l
            JOIN freelancers f ON l.freelancer_id = f.id
            WHERE l.id = ?
        ''', (listing_id,))
        
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Listing with id {listing_id} not found"
            )
        
        listing = ListingResponse(
            id=row['id'],
            freelancer_id=row['freelancer_id'],
            freelancer_name=row['freelancer_name'],
            title=row['title'],
            description=row['description'],
            base_price=row['base_price'],
            tags=json.loads(row['tags']),
            addons=json.loads(row['addons']) if row['addons'] else [],
            created_at=row['created_at']
        )
        
        return listing