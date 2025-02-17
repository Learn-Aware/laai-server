from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    profile_image: str
