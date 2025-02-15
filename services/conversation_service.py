from typing import Dict, Any, List
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError
from configs.mongo_config import conversation_collection
from models.conversation import Conversation, Message
from fastapi.encoders import jsonable_encoder


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

            conversation_docs = [
                {
                    "user_email": user_email,
                    "session_id": conversation.id,
                    "messages": [msg.model_dump() for msg in conversation.messages],
                }
                for conversation in conversations
            ]

            result = conversation_collection.insert_many(conversation_docs)

            return {
                "message": f"Conversations for {user_email} saved successfully",
                "inserted_count": len(result.inserted_ids),
                "inserted_ids": [str(_id) for _id in result.inserted_ids],
            }

        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def get_session_ids(user_email: str) -> List[str]:
        try:
            conversation_docs = conversation_collection.find(
                {"user_email": user_email}, {"session_id": 1}
            )

            return [doc["session_id"] for doc in conversation_docs]

        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def get_conversation(user_email: str, session_id: str) -> dict:
        try:
            conversation_doc = conversation_collection.find_one(
                {"user_email": user_email, "session_id": session_id}
            )

            if not conversation_doc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation with session_id {session_id} not found",
                )

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

        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def delete_conversation(user_email: str, session_id: str) -> Dict[str, Any]:
        try:
            result = conversation_collection.delete_one(
                {"user_email": user_email, "session_id": session_id}
            )

            if not result.deleted_count:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation with session_id {session_id} not found",
                )

            return {
                "message": f"Conversation with session_id {session_id} deleted successfully"
            }

        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
