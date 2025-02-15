from typing import Any, Dict, List
from fastapi import APIRouter
from services.conversation_service import ConversationService
from models.conversation import ConversationRequest

router = APIRouter()


@router.post("")
async def save_conversations(request: ConversationRequest):
    return await ConversationService.save_conversations(
        request.user_email, request.conversations
    )


@router.get("/{user_email}")
async def get_session_ids(user_email: str):
    return await ConversationService.get_session_ids(user_email)


@router.get("/{user_email}/{session_id}")
async def get_conversation(user_email: str, session_id: str):
    return await ConversationService.get_conversation(user_email, session_id)

@router.delete("/{user_email}/{session_id}")
async def delete_conversation(user_email: str, session_id: str):
    return await ConversationService.delete_conversation(user_email, session_id)
