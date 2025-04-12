from dal.mongodb_dal import MongoDBDAL
from models.user import User
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError, PyMongoError

class UserDAL(MongoDBDAL):
    """Data Access Layer for users collection"""
    
    def __init__(self):
        super().__init__("users")
    
    async def setup_indexes(self):
        """Setup required indexes for the users collection"""
        await self.create_index([("email", 1)], unique=True)
    
    async def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users from the database"""
        return await self.find_all()
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find a user by email"""
        user = await self.find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found with the provided email."
            )
        return user
    
    async def create_user(self, user_data: User) -> Dict[str, Any]:
        """Create a new user in the database"""
        try:
            # Ensure email index exists
            await self.setup_indexes()
            
            # Convert pydantic model to dict
            user_dict = user_data.model_dump()
            
            # Insert the user
            inserted_user = await self.insert_one(user_dict)
            
            return {
                "data": inserted_user,
                "message": "User created successfully.",
                "status": status.HTTP_201_CREATED
            }
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already registered. Please use a different email."
            )
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while creating user: {str(e)}"
            )
    
    async def update_user(self, email: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a user by email"""
        result = await self.update_one({"email": email}, update_data)
        return {
            "data": result.get("document"),
            "message": "User updated successfully.",
            "status": status.HTTP_200_OK
        }
    
    async def delete_all_users(self) -> Dict[str, Any]:
        """Delete all users from the database"""
        result = await self.delete_many({})
        return {
            "data": f"Deleted {result['count']} users successfully.",
            "status": status.HTTP_200_OK,
            "message": "All users deleted successfully."
        } 