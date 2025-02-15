from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    id: int
    sender: str
    text: str
    time: str
    image: Optional[str] = None


class Conversation(BaseModel):
    id: str
    messages: List[Message]


class ConversationRequest(BaseModel):
    user_email: str
    conversations: List[Conversation]
