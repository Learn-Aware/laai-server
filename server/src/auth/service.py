
from fastapi import HTTPException

from src.auth.utils import generate_passwd_hash
from ..config import db
from .schemas import ParentModel, StudentModel



class UserService:
    def __init__(self):
        self.student_collection = db.get_collection("students")
        self.parent_collection = db.get_collection("parents")
        
    async def get_user_by_email(self, email: str):
        if (
            user := await self.student_collection.find_one({"email": email})
        ) is not None:
            return user
        
        return None
        
    async def user_exists(self, email: str):
        """
        Check if the user exists in the database.
        """
        user = await self.get_user_by_email(email)
        return True if user is not None else False
    
    async def create_student(self, student: StudentModel):
        """
        Create a new student account.
        """
        # generate hash for password
        student.password = generate_passwd_hash(student.password)

        new_student = await self.student_collection.insert_one(student.dict())
        created_student = await self.student_collection.find_one({"_id": new_student.inserted_id})
        return created_student
    
    async def create_parent(self, parent: ParentModel):
        """
        Create a new student account.
        """
        # generate hash for password
        parent.password = generate_passwd_hash(parent.password)

        new_parent = await self.parent_collection.insert_one(parent.dict())
        created_parent = await self.parent_collection.find_one({"_id": new_parent.inserted_id})
        return created_parent