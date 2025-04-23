from typing import Dict, Any, List
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError
from models.conversation import Conversation, Message
from fastapi.encoders import jsonable_encoder
from dal import conversation_dal


class ConversationService:

    @staticmethod
    async def save_conversations(
        user_email: str, conversations: List[Conversation]
    ) -> Dict[str, Any]:
        try:
            if not conversations:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No conversations provided",
                )

            inserted_count = 0
            updated_count = 0

            for conversation in conversations:
                # Try to find existing conversations with this session_id
                filter_dict = {"user_email": user_email, "session_id": conversation.id}
                existing_conversations = await conversation_dal.find_all_filtered(filter_dict)
                
                if existing_conversations:
                    # Update the existing conversation
                    existing_conv = existing_conversations[0]  # Take the first one if multiple
                    update_data = {
                        "messages": [msg.model_dump() for msg in conversation.messages]
                    }
                    
                    result = await conversation_dal.update_one(
                        {"_id": existing_conv["_id"]},
                        update_data
                    )
                    if result.get("modified", False):
                        updated_count += 1
                else:
                    # Insert a new conversation
                    conversation_doc = {
                        "user_email": user_email,
                        "session_id": conversation.id,
                        "messages": [msg.model_dump() for msg in conversation.messages],
                    }
                    await conversation_dal.insert_one(conversation_doc)
                    inserted_count += 1

            return {
                "message": f"Conversations for {user_email} processed successfully",
                "inserted_count": inserted_count,
                "updated_count": updated_count,
            }

        except Exception as e:
            # The DAL already handles most exceptions, this is just for unexpected errors
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while saving conversations: {str(e)}"
            )

    @staticmethod
    async def get_session_ids(user_email: str) -> List[str]:
        try:
            return await conversation_dal.get_conversations_by_email(user_email)
        except Exception as e:
            # The DAL already handles most exceptions, this is just for unexpected errors
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while fetching session IDs: {str(e)}"
            )

    @staticmethod
    async def get_conversation(user_email: str, session_id: str) -> dict:
        try:
            # Try to find the conversation
            filter_dict = {"user_email": user_email, "session_id": session_id}
            conversations = await conversation_dal.find_all_filtered(filter_dict)

            if not conversations:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation with session_id {session_id} not found",
                )

            conversation_doc = conversations[0]  # Take the first one if multiple
            
            conversation = Conversation(
                id=conversation_doc["session_id"],
                messages=[
                    Message(**msg) for msg in conversation_doc.get("messages", [])
                ],
            )

            return {
                "user_email": user_email,
                "conversation": jsonable_encoder(conversation),
            }

        except Exception as e:
            # The DAL already handles most exceptions, this is just for unexpected errors
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while fetching conversation: {str(e)}"
            )

    @staticmethod
    async def delete_conversation(user_email: str, session_id: str) -> Dict[str, Any]:
        try:
            filter_dict = {"user_email": user_email, "session_id": session_id}
            result = await conversation_dal.delete_many(filter_dict)

            if result["count"] == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation with session_id {session_id} not found",
                )

            return {
                "message": f"Conversation with session_id {session_id} deleted successfully"
            }

        except Exception as e:
            # The DAL already handles most exceptions, this is just for unexpected errors
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while deleting conversation: {str(e)}"
            )

    @staticmethod
    async def update_conversation(
        user_email: str, session_id: str, conversations: List[Conversation]
    ) -> Dict[str, Any]:
        try:
            if not conversations:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No conversations provided",
                )

            # Check if the conversation exists
            filter_dict = {"user_email": user_email, "session_id": session_id}
            existing_conversations = await conversation_dal.find_all_filtered(filter_dict)

            if not existing_conversations:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation with session_id {session_id} not found",
                )

            # Update the conversation
            update_data = {
                "messages": [msg.model_dump() for msg in conversations[0].messages]
            }
            
            await conversation_dal.update_one(filter_dict, update_data)

            return {
                "message": f"Conversation with session_id {session_id} updated successfully"
            }

        except Exception as e:
            # The DAL already handles most exceptions, this is just for unexpected errors
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while updating conversation: {str(e)}"
            )
