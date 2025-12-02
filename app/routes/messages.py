from typing import List, Optional
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Query, status, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

from app.models.message import (
    MessageCreate,
    MessageResponse,
    ConversationSummary,
    UserSearchResult,
    AttachmentResponse,
)
from app.services.message_service import MessageService

router = APIRouter(
    prefix="/api/messages",
    tags=["Messages"],
)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send a message",
    description="Send a message between a job seeker and an evaluator, optionally with a file attached.",
)

async def send_message(
    sender_role: str = Form(..., regex="^(job_seeker|evaluator)$"),
    sender_id: int = Form(..., gt=0),
    receiver_role: str = Form(..., regex="^(job_seeker|evaluator)$"),
    receiver_id: int = Form(..., gt=0),
    content: str = Form("", max_length=2000),
    files: List[UploadFile] = File(None),
):
    if not content and not files:
        raise HTTPException(
            status_code=400,
            detail="Message must have text or at least one attachment",
        )

    # Build MessageCreate from form fields
    payload = MessageCreate(
        sender_role=sender_role,
        sender_id=sender_id,
        receiver_role=receiver_role,
        receiver_id=receiver_id,
        content=content,
    )

    # Save uploaded files to disk
    upload_dir = Path("/app/data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []
    if files:
        for upload in files:
            # Generate unique filename to avoid collisions
            ext = Path(upload.filename).suffix
            unique_name = f"{uuid4().hex}{ext}"
            file_path = upload_dir / unique_name

            # Write file contents
            with file_path.open("wb") as f:
                f.write(await upload.read())

            size_bytes = file_path.stat().st_size
            mime_type = upload.content_type or "application/octet-stream"

            saved_files.append(
                {
                    "file_path": str(file_path),
                    "original_filename": upload.filename,
                    "mime_type": mime_type,
                    "size_bytes": size_bytes,
                }
            )

    # Store message + attachments in DB
    send_result = MessageService.send_message(payload, files=saved_files)

    # Fetch the newly created message as a full MessageResponse (with attachments)
    messages = MessageService.get_messages(send_result["conversation_id"])
    created = next(m for m in messages if m.id == send_result["message_id"])

    return created

@router.get(
    "/conversations",
    response_model=List[ConversationSummary],
    summary="List user conversations",
    description="List all conversations for a given user (job seeker or evaluator).",
)
async def list_conversations(
    user_role: str = Query(..., regex="^(job_seeker|evaluator)$"),
    user_id: int = Query(..., gt=0),
):
    return MessageService.list_conversations(user_role=user_role, user_id=user_id)


@router.get(
    "/conversations/{conversation_id}",
    response_model=List[MessageResponse],
    summary="Get conversation messages",
    description="Fetch full message history for a specific conversation.",
)
async def get_conversation_messages(conversation_id: str):
    return MessageService.get_messages(conversation_id=conversation_id)


@router.get(
    "/users/search",
    response_model=List[UserSearchResult],
    summary="Search users for messaging",
    description="Search job seekers and evaluators by name or email.",
)
async def search_users(
    q: str = Query(
        ...,
        min_length=1,
        description="Search term to match against name or email",
    )
):
    return MessageService.search_users(query=q)

@router.get(
    "/attachments/{attachment_id}",
    summary="Download a message attachment",
    description="Fetch a file that was attached to a message.",
)
async def download_attachment(attachment_id: int):
    """
    Return the attachment file for download/viewing.
    """
    info = MessageService.get_attachment(attachment_id)
    if info is None:
        raise HTTPException(status_code=404, detail="Attachment not found")

    file_path = Path(info["file_path"])
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=str(file_path),
        media_type=info["mime_type"],
        filename=info["original_filename"],
    )
