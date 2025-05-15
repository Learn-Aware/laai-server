import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SECRET_KEY = os.getenv("JWT_SECRET")
SALT = os.getenv("JWT_SALT")
DOMAIN = os.getenv("DOMAIN")