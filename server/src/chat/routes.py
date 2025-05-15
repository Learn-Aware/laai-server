from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

# from server.schemas.models.user import User
from src.auth.dependencies import get_current_user
from src.auth.schemas import StudentModel
from src.chat.schemas import ChatMessageModel
from src.chat.service import ChatService


chat_router = APIRouter()

@chat_router.post(
    "/chat",
    response_description="Ask a question to the chat service",
    # response_model=ChatResponseModel,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False)
async def chat(
    chat_message: ChatMessageModel,
    current_user: StudentModel = Depends(get_current_user),
):
    user_id = current_user['_id']
    message = chat_message.message
    topic_id = chat_message.topic_id
    # Assuming you have a chat service that handles the logic
    chat_service = ChatService()

    llm_response = await chat_service.chat(
        user_id=user_id,
        message=message,
        topic_id=topic_id,)
    # print(current_user)

    # await chat_service.save_message(
    #     user_id=user_id,
    #     message=message,
    #     session_id=session_id,
    #     timestamp=timestamp,
    # )
    
    # await chat_service.cache_recent_chat(
    #     user_id=user_id,
    #     message=message,
    #     session_id=session_id,
    #     timestamp=timestamp,
    # )

    # recent_chat_history = await chat_service.get_recent_chat_from_cache(
    #     user_id=user_id,
    #     session_id=session_id,
    # )

    # response = await chat_service.generate_response(
    #     user_id=user_id,
    #     message=message,
    #     session_id=session_id,
    #     recent_chat_history=recent_chat_history,
    # )

    # await chat_service.save_message(
    #     user_id=user_id,
    #     message=response,
    #     session_id=session_id,
    #     timestamp=timestamp,
    # )

    return JSONResponse(
        content={
            "message": "Chat response generated successfully",
            # "response": llm_response,
            # "response": current_user,

        },
        status_code=status.HTTP_200_OK,
    )