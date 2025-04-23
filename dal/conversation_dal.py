from dal.mongodb_dal import MongoDBDAL
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError

class ConversationDAL(MongoDBDAL):
    """Data Access Layer for conversations collection"""
    
    def __init__(self):
        super().__init__("conversations")
    
    async def setup_indexes(self):
        """Setup required indexes for the conversations collection"""
        await self.create_index([("user_email", 1)])
        await self.create_index([("session_id", 1)])
    
    async def get_all_conversations(self) -> List[Dict[str, Any]]:
        """Get all conversations from the database"""
        return await self.find_all()
    
    async def get_conversations_by_email(self, user_email: str) -> List[Dict[str, Any]]:
        """Find conversations by user email"""
        try:
            # Get distinct session_ids for this user
            filter_dict = {"user_email": user_email}
            conversations = await self.find_all_filtered(filter_dict)
            
            # Extract unique session IDs
            session_ids = set()
            for conversation in conversations:
                if "session_id" in conversation:
                    session_ids.add(conversation["session_id"])
            
            return list(session_ids)
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while retrieving conversations: {str(e)}"
            )
    
    async def get_conversation_by_session_id(self, session_id: str) -> List[Dict[str, Any]]:
        """Find all conversations for a specific session ID"""
        try:
            filter_dict = {"session_id": session_id}
            conversations = await self.find_all_filtered(filter_dict)
            
            if not conversations:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No conversations found for session ID: {session_id}"
                )
                
            return conversations
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while retrieving conversation: {str(e)}"
            )
    
    async def create_conversation(self, conversation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new conversation in the database"""
        try:
            # Ensure indexes exist
            await self.setup_indexes()
            
            # Insert the conversation
            inserted_conversation = await self.insert_one(conversation_data)
            
            return {
                "data": inserted_conversation,
                "message": "Conversation created successfully.",
                "status": status.HTTP_201_CREATED
            }
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while creating conversation: {str(e)}"
            )
    
    async def delete_conversations_by_session_id(self, session_id: str) -> Dict[str, Any]:
        """Delete all conversations for a specific session ID"""
        try:
            filter_dict = {"session_id": session_id}
            result = await self.delete_many(filter_dict)
            
            if result["count"] == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No conversations found for session ID: {session_id}"
                )
                
            return {
                "data": f"Deleted {result['count']} conversations successfully.",
                "status": status.HTTP_200_OK,
                "message": f"All conversations for session ID {session_id} deleted successfully."
            }
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while deleting conversations: {str(e)}"
            ) 