from typing import Any, Dict, List
from models.user import User
from fastapi import HTTPException, status
from dal import user_dal


class UserService:
    """Service layer for user-related operations"""
    
    @staticmethod
    async def get_users() -> List[User]:
        """Get all users"""
        try:
            return await user_dal.get_all_users()
        except Exception as e:
            # The DAL already handles most exceptions, this is just for unexpected errors
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while fetching users: {str(e)}"
            )

    @staticmethod
    async def create_user(user_data: User) -> Dict[str, Any]:
        """Create a new user"""
        try:
            return await user_dal.create_user(user_data)
        except Exception as e:
            # The DAL already handles most exceptions, this is just for unexpected errors
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while creating user: {str(e)}"
            )

    @staticmethod
    async def get_user_by_email(email: str) -> Dict[str, Any]:
        """Get a user by email"""
        try:
            return await user_dal.get_user_by_email(email)
        except Exception as e:
            # The DAL already handles most exceptions, this is just for unexpected errors
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while fetching user: {str(e)}"
            )

    @staticmethod
    async def delete_users() -> Dict[str, Any]:
        """Delete all users"""
        try:
            return await user_dal.delete_all_users()
        except Exception as e:
            # The DAL already handles most exceptions, this is just for unexpected errors
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while deleting users: {str(e)}"
            )
