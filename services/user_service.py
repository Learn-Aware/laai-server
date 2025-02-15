from typing import Any, Dict, List
from configs.mongo_config import users_collection
from models.user import User
from fastapi import HTTPException, status
from pymongo.errors import PyMongoError, DuplicateKeyError


class UserService:
    @staticmethod
    async def get_users() -> List[User]:
        try:
            users = list(users_collection.find())
            for user in users:
                user["_id"] = str(user["_id"])
            return users
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while fetching users.",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while fetching users.",
            )

    @staticmethod
    async def create_user(user_data: User) -> Dict[str, Any]:
        try:
            user_dict = user_data.model_dump()
            users_collection.create_index([("email", 1)], unique=True)
            result = users_collection.insert_one(user_dict)
            user_dict["_id"] = str(result.inserted_id)
            return {
                "data": user_dict,
                "message": "User created successfully.",
                "status": status.HTTP_201_CREATED,
            }
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email is already registered. Please use a different email.",
            )
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We encountered an issue while creating your account. Please try again later.",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}. Please try again later.",
            )

    @staticmethod
    async def get_user_by_email(email: str) -> User:
        user = users_collection.find_one({"email": email})

        if user:
            user["_id"] = str(user["_id"])
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found with the provided email.",
            )

    @staticmethod
    async def delete_users() -> Dict[str, Any]:
        try:
            result = users_collection.delete_many({})
            return {
                "data": f"Deleted {result.deleted_count} users successfully.",
                "status": status.HTTP_200_OK,
                "message": "All users deleted successfully.",
            }
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while deleting users from the database.",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}. Please try again later.",
            )
