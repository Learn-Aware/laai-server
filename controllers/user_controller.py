from fastapi import APIRouter, HTTPException
from models.user import User
from services.user_service import UserService

router = APIRouter()

@router.get("/users")
async def get_users():
    return UserService.get_users()

@router.post("/register")
async def create_user(user: User):
    return UserService.create_user(user)

@router.get("/users/{email}")
async def get_user_by_email(email: str):
    return UserService.get_user_by_email(email)
