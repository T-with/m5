from datetime import datetime
from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    """
    Represents a new message being sent in a conversation.
    The client provides who is sending, who is receiving, and the content.
    The backend will compute a consistent conversation_id based on the two parties.
    """
    sender_role: Literal["job_seeker", "evaluator"] = Field(
        ...,
        description="Role of the sender"
    )
    sender_id: int = Field(
        ...,
        gt=0,
        description="ID of the sender (job seeker or evaluator)"
    )
    receiver_role: Literal["job_seeker", "evaluator"] = Field(
        ...,
        description="Role of the receiver"
    )
    receiver_id: int = Field(
        ...,
        gt=0,
        description="ID of the receiver (job seeker or evaluator)"
    )
    content: str = Field(
        "",
        min_length=0,
        max_length=2000,
        description="Message body text (May be empty if only attachments)"
    )

class AttachmentResponse(BaseModel):
    '''
    represents a file attatched to a message.
    '''

    id: int
    message_id: int
    file_path: str
    original_filename: str
    mime_type: str
    size_bytes: int
    created_at: datetime
    
    

class MessageResponse(BaseModel):
    """
    Represents a message returned to the client.
    Includes party names and IDs so the frontend can display conversations cleanly.
    """
    id: int
    conversation_id: str
    sender_role: Literal["job_seeker", "evaluator"]
    sender_id: int
    sender_name: Optional[str] = None
    receiver_role: Literal["job_seeker", "evaluator"]
    receiver_id: int
    receiver_name: Optional[str] = None
    content: str
    created_at: datetime

    #appending to add attatchment functionality

    attachments: List[AttachmentResponse] = Field(
        default_factory=list,
        description="files attatched to this message (images, PDF's, audio, etc)"\
    )
    
    


class ConversationSummary(BaseModel):
    """
    A summary of a conversation for the conversation list.
    Shows the other party and the latest message preview.
    """
    conversation_id: str
    other_party_role: Literal["job_seeker", "evaluator"]
    other_party_id: int
    other_party_name: Optional[str] = None
    last_message: str
    last_message_time: datetime

    #Displaying summary if attatchments were sent
    has_attachments: bool = Field(
        default=False,
        description="Whether the latest message in this conversation has any file attachments"
    )


class UserSearchResult(BaseModel):
    """
    Result row when searching for users to start a conversation with.
    """
    role: Literal["job_seeker", "evaluator"]
    id: int
    name: str
    email: str
