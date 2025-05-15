import os
from typing import Optional
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
# Load environment variables from .env file
# load_dotenv()

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    
    MONGO_CONNECTION_STRING: str
    MONGO_DB_NAME: str  
    MONGO_DB_PASSWORD: str

    SECRET_KEY: str
    SALT: str

    JWT_SECRET: str
    JWT_ALGORITHM: str

    REDIS_URL: str

    DOMAIN: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_FROM_EMAIL: str
    MAIL_FROM: Optional[EmailStr] = None  # Optional field with default None
    MAIL_FROM_NAME: str
    
    MAIL_STARTTLS:bool = True
    MAIL_SSL_TLS:bool = False
    USE_CREDENTIALS:bool = True
    VALIDATE_CERTS:bool = True


# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# SECRET_KEY = os.getenv("JWT_SECRET")
# SALT = os.getenv("JWT_SALT")
# DOMAIN = os.getenv("DOMAIN")

# MONGO_URI = os.getenv("MONGO_URI")
# MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

Config = Settings()

client = AsyncIOMotorClient(Config.MONGO_CONNECTION_STRING)
db = client.get_database(Config.MONGO_DB_NAME)

