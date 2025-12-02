from typing import List, Dict, Any, Optional

from app.models.message import (
    MessageCreate,
    MessageResponse,
    ConversationSummary,
    UserSearchResult,
)
from app.repositories.message_repository import MessageRepository


class MessageService:
    @staticmethod
    def send_message(
        payload: MessageCreate,
        files: Optional[List[Dict[str, Any]]] = None,
        base_url: str = "",
    ) -> Dict[str, Any]:
        """
        Send a message and optionally attach files.

        `files` is expected to be a list of dicts with keys:
            - file_path (server-side path, e.g. /app/data/uploads/uuid.png)
            - original_filename
            - mime_type
            - size_bytes

        `base_url` is an optional prefix used to build public URLs for attachments,
        e.g. base_url='/api/attachments'.
        """
        conversation_id = MessageRepository.build_conversation_id(
            sender_role=payload.sender_role,
            sender_id=payload.sender_id,
            receiver_role=payload.receiver_role,
            receiver_id=payload.receiver_id,
        )

        message_id = MessageRepository.insert_message(
            conversation_id=conversation_id,
            sender_role=payload.sender_role,
            sender_id=payload.sender_id,
            receiver_role=payload.receiver_role,
            receiver_id=payload.receiver_id,
            content=payload.content,
        )
        
        attachment_dicts: List[Dict[str, Any]] = []
        if files:
            for f in files:
                attachment_id = MessageRepository.add_attachment(
                    message_id=message_id,
                    file_path=f["file_path"],
                    original_filename=f["original_filename"],
                    mime_type=f["mime_type"],
                    size_bytes=f["size_bytes"]
                )

                # Build a URL the frontend can use
                # Example: f"{base_url}/{attachment_id}" if base_url='/api/attachments'
                url = f"{base_url}/{attachment_id}" if base_url else str(attachment_id)

                attachment_dicts.append(
                    {
                        "id": attachment_id,
                        "message_id": message_id,
                        "url": url,
                        "original_filename": f["original_filename"],
                        "mime_type": f["mime_type"],
                        "size_bytes": f["size_bytes"],
                        # created_at will be filled in when you fetch via get_messages,
                        # so we leave it out here for the lightweight send response.
                    }
                )



        # BUG FIX #8: Create notification for receiver
        try:
            from app.services.notification_service import NotificationService
            from app.database import get_db
            
            # Get sender name for notification message
            with get_db() as conn:
                cursor = conn.cursor()
                if payload.sender_role == 'job_seeker':
                    cursor.execute('SELECT name FROM freelancers WHERE id = ?', (payload.sender_id,))
                else:
                    cursor.execute('SELECT name FROM evaluators WHERE id = ?', (payload.sender_id,))
                sender = cursor.fetchone()
                sender_name = sender['name'] if sender else 'Someone'
            
            # Create notification
            NotificationService.create_notification(
                user_role=payload.receiver_role,
                user_id=payload.receiver_id,
                notification_type='new_message',
                title='New Message',
                message=f'You have a new message from {sender_name}',
                related_id=message_id,
                related_type='message'
            )
        except Exception as e:
            # Don't fail message send if notification fails
            print(f"Warning: Failed to create message notification: {e}")

        return {
            "message_id": message_id,
            "conversation_id": conversation_id,
            "sender_role": payload.sender_role,
            "sender_id": payload.sender_id,
            "receiver_role": payload.receiver_role,
            "receiver_id": payload.receiver_id,
            "content": payload.content,
            "attachments": attachment_dicts,
        }

    @staticmethod
    def list_conversations(user_role: str, user_id: int) -> List[ConversationSummary]:
        rows = MessageRepository.list_conversations_for_user(user_role, user_id)
        return [ConversationSummary(**row) for row in rows]

    @staticmethod
    def get_messages(conversation_id: str) -> List[MessageResponse]:
        rows = MessageRepository.get_conversation_messages(conversation_id)
        return [MessageResponse(**row) for row in rows]

    @staticmethod
    def search_users(query: str) -> List[UserSearchResult]:
        rows = MessageRepository.search_users(query)
        return [UserSearchResult(**row) for row in rows]
    
    @staticmethod
    def get_attachment(attachment_id: int) -> Dict[str, Any] | None:
        return MessageRepository.get_attachment(attachment_id)