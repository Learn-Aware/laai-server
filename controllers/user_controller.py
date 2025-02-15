from fastapi import APIRouter
from typing import List, Dict, Any
from models.user import User
from services.user_service import UserService

router = APIRouter()


@router.get("/users", response_model=List[Dict[str, Any]])
async def get_users():
    return await UserService.get_users()


@router.post("/register", response_model=Dict[str, Any])
async def create_user(user: User):
    return await UserService.create_user(user)


@router.get("/users/{email}", response_model=Dict[str, Any])
async def get_user_by_email(email: str):
    return await UserService.get_user_by_email(email)


@router.delete("/users")
async def delete_users():
    return await UserService.delete_users()
