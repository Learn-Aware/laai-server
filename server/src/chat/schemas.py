from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Request model to handle incoming chat messages
class ChatMessageModel(BaseModel):
    user_id: str
    topic_id: str
    message: str

# Response model for returning chat response
class ChatResponseModel(BaseModel):
    response: str
    timestamp: datetime
    session_id: Optional[str] = None  # If you're using session IDs to track conversations
