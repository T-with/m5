import json
from typing import List, Optional

from fastapi import APIRouter, Request, HTTPException, status
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


class ListingCreate(BaseModel):
    title: str
    description: str
    base_price: float
    tags: List[str]
    addons: Optional[List[AddonItem]] = []


# ---------- Page routes ----------

@router.get("/create-listing-page", response_class=HTMLResponse)
async def create_listing_page(request: Request):
    try:
        return templates.TemplateResponse("create_listings.html", {"request": request})
    except Exception as e:
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(f"Error loading template: {str(e)}", status_code=500)


@router.get("/create-listing.html", response_class=HTMLResponse)
async def create_listing_html(request: Request):
    try:
        return templates.TemplateResponse("create_listings.html", {"request": request})
    except Exception as e:
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(f"Error loading template: {str(e)}", status_code=500)


@router.get("/create_listings.html", response_class=HTMLResponse)
async def create_listings_html(request: Request):
    try:
        return templates.TemplateResponse("create_listings.html", {"request": request})
    except Exception as e:
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(f"Error loading template: {str(e)}", status_code=500)


# ---------- API routes ----------

@router.post(
    "/api/freelancers/{freelancer_id}/listings",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Create Listing for Freelancer",
    description="Create a new service listing for a specific freelancer"
)
async def create_listing(freelancer_id: int, listing: ListingCreate):
    """
    Create a new listing for a freelancer
    
    **Path Parameters:**
    - **freelancer_id**: The ID of the freelancer creating the listing
    
    **Required fields:**
    - **title**: Service title
    - **description**: Detailed description
    - **base_price**: Starting price
    - **tags**: List of tags for categorization
    
    **Optional fields:**
    - **addons**: List of add-on services with names and prices
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
        
        # Convert tags and addons to JSON strings for storage
        # Ensure tags is a list (can be empty)
        tags_list = listing.tags if listing.tags else []
        tags_json = json.dumps(tags_list)
        
        # Ensure addons is a list and convert to dict format
        addons_list = listing.addons if listing.addons else []
        addons_json = json.dumps([addon.dict() for addon in addons_list])
        
        # Insert listing
        cursor.execute('''
            INSERT INTO listings (
                freelancer_id, title, description, base_price, tags, addons
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            freelancer_id,
            listing.title,
            listing.description,
            listing.base_price,
            tags_json,
            addons_json
        ))
        
        conn.commit()
        listing_id = cursor.lastrowid
        
        return {
            "success": True,
            "message": "Listing created successfully",
            "listing_id": listing_id
        }


@router.put(
    "/api/listings/{listing_id}",
    response_model=dict,
    summary="Update Listing",
    description="Update an existing listing"
)
async def update_listing(listing_id: int, listing: ListingCreate):
    """
    Update an existing listing
    
    **Path Parameters:**
    - **listing_id**: The ID of the listing to update
    
    **Request body**: Same as create listing
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Check if listing exists
        cursor.execute('SELECT id FROM listings WHERE id = ?', (listing_id,))
        existing_listing = cursor.fetchone()
        
        if not existing_listing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Listing with id {listing_id} not found"
            )
        
        # Convert tags and addons to JSON strings for storage
        tags_json = json.dumps(listing.tags)
        addons_json = json.dumps([addon.dict() for addon in listing.addons])
        
        # Update listing
        cursor.execute('''
            UPDATE listings 
            SET title = ?, description = ?, base_price = ?, tags = ?, addons = ?
            WHERE id = ?
        ''', (
            listing.title,
            listing.description,
            listing.base_price,
            tags_json,
            addons_json,
            listing_id
        ))
        
        conn.commit()
        
        return {
            "success": True,
            "message": "Listing updated successfully",
            "listing_id": listing_id
        }


@router.delete(
    "/api/listings/{listing_id}",
    response_model=dict,
    summary="Delete Listing",
    description="Delete a specific listing"
)
async def delete_listing(listing_id: int):
    """
    Delete a listing
    
    **Path Parameters:**
    - **listing_id**: The ID of the listing to delete
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM listings WHERE id = ?', (listing_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Listing with id {listing_id} not found"
            )
        
        return {
            "success": True,
            "message": "Listing deleted successfully"
        }