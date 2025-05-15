import os
from dotenv import load_dotenv
# from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# client = MongoClient(MONGO_URI)
# Create a MongoDB client
client = AsyncIOMotorClient(CONNECTION_STRING)
# db = client[MONGO_DB_NAME]
db = client.get_database(MONGO_DB_NAME)

student_collection = db.get_collection("students")
# conversation_collection = db["conversations"]
