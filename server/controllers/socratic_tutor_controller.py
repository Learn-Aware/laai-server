from typing import Optional
from core.logic.conversation_flowv2 import main_chat_flowv2
from fastapi import APIRouter, UploadFile, Form
from schemas.socratic_tutor_schemas import QuestionResponse

router = APIRouter()

SESSION_FILE = "temp_db/conversation_db_v3.json"


@router.post("/v2/chat", response_model=QuestionResponse)
async def chat_flow(
    user_request: str = Form(...),
    session_id: Optional[str] = Form(None),
    image: Optional[UploadFile] = None,
):
    return main_chat_flowv2(user_request, SESSION_FILE, session_id, image)
