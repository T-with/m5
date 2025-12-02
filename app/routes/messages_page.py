from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Pages"])


@router.get("/messages", response_class=HTMLResponse)
async def messages_page(
    request: Request,
    user_role: Optional[str] = None,
    user_id: Optional[int] = None,
    other_role: Optional[str] = None,
    other_id: Optional[int] = None,
):
    """
    Render the messaging UI.

    user_role / user_id: the currently signed-in user (if any).
    other_role / other_id: optional "target" user (e.g., from a job listing
    link) to jump straight into that conversation.
    """
    return templates.TemplateResponse(
        "messages.html",
        {
            "request": request,
            "user_role": user_role or "",
            "user_id": user_id or "",
            "other_role": other_role or "",
            "other_id": other_id or "",
        },
    )

