from configs.mongo_config import users_collection
from models.user import User
from fastapi import HTTPException

class UserService:
    @staticmethod
    def get_users():
        try:
            users = list(users_collection.find())
            for user in users:
                user["_id"] = str(user["_id"])
            return users
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

    @staticmethod
    def create_user(user_data: User):
        try:
            user_dict = user_data.dict()
            result = users_collection.insert_one(user_dict)
            user_dict["_id"] = str(result.inserted_id)
            return user_dict
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}") 
    @staticmethod
    def get_user_by_email(email: str):
        try:
            user = users_collection.find_one({"email": email})
            if user:
                user["_id"] = str(user["_id"])
                return user
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")