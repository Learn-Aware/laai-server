from datetime import datetime
import json
import os
import shutil
from typing import List, Optional
from uuid import uuid4
from bson import ObjectId
from pymongo import MongoClient
import redis
from fastapi import HTTPException, UploadFile
from src.agent.service import AgentService
from ..config import db

# # Setup MongoDB connection
# client = MongoClient("mongodb://localhost:27017")
# db = client.chat_db
# chats_collection = db.chats
# users_collection = db.users
LOCAL_IMAGE_DIR = "../temp_db"
# # Setup Redis connection
# r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# create AgentService instance
agent_service = AgentService()

# Service to handle chat operations
class ChatService:
    def __init__(self):
        self.conversations_collection = db.get_collection("user_conversations")
        # self.chat_collection = db.get_collection("chats")
        self.topics_collection = db.get_collection("topics")
        # self.llm_responses_collection = db.get_collection("llm_responses")
        # self.images_collection = db.get_collection("conversation_image_metadata")

    async def store_image_locally(self, image: UploadFile, conversation_id: str) -> str:
        """
        Store the uploaded image locally and return the file path.
        """
        
        # Generate a unique file name to avoid collisions
        unique_filename = f"{uuid4().hex}_{image.filename}"
        # Save the image to the local storage directory
        image_path = os.path.join(LOCAL_IMAGE_DIR, unique_filename)

        
        # Save file asynchronously
        with open(image_path, 'wb') as f:
            shutil.copyfileobj(image.file, f)

        # Image metadata to store in MongoDB
        image_metadata = {
            "conversation_id": conversation_id,
            "image_path": image_path,
            "filename": image.filename,
            "content_type": image.content_type,
            "timestamp": datetime.utcnow()
        }

        # Save image metadata in MongoDB
        await self.images_collection.insert_one(image_metadata)

        # Cache the image metadata in Redis for fast access
        # await redis.set(f"image:{conversation_id}:{unique_filename}", json.dumps(image_metadata), ex=CACHE_EXPIRATION)

        return image_path

    async def get_image_metadata(self, conversation_id: str, filename: str) -> List[dict]:
        """
        Retrieve image metadata for a specific conversation from MongoDB.
        """
        # Check Redis cache for image metadata
        # image_metadata = await redis.get(f"image:{conversation_id}:{filename}")
        # if image_metadata:
        #     return json.loads(image_metadata)

        # If not found in Redis, get from MongoDB
        image_metadata = await self.images_collection.find_one({"conversation_id": conversation_id, "filename": filename})
        # if image_metadata:
        #     # Cache the image metadata in Redis
        #     await redis.set(f"image:{conversation_id}:{filename}", json.dumps(image_metadata), ex=CACHE_EXPIRATION)

        return image_metadata

    async def get_image_file(image_path: str):
        """
        Retrieve the image file from the local storage (file path).
        """
        with open(image_path, 'rb') as f:
            return f.read()  # Return the image binary data



    async def create_conversation(self, student_id: str, topic: Optional[str]) -> str:
        """
        Create a new conversation in MongoDB and cache it in Redis.
        """
        conversation_id = str(ObjectId())  # Generate unique conversation ID
        conversation_data = {
            "conversation_id": conversation_id,
            "student_id": student_id,
            "start_time": datetime.utcnow(),
            "end_time": None,
            "status": "active",
            "metadata": {
                "topic": topic,
                "session_id": str(uuid4()),
            }
        }

        # Store conversation in MongoDB
        await self.conversations_collection.insert_one(conversation_data)

        # Cache conversation metadata in Redis (for quick access)
        # await redis.set(conversation_id, json.dumps(conversation_data), ex=CACHE_EXPIRATION)
        
        return conversation_id

    async def add_user_message(self, conversation_id: str, message: str, image_id: Optional[UploadFile]):
        """
        Add a user message to MongoDB and cache it in Redis.
        """
        timestamp = datetime.utcnow()
        user_message_data = {
            "conversation_id": conversation_id,
            "message": message,
            "timestamp": timestamp,
            "image_id": image_id,
        }
        
        # Store the user message in MongoDB
        await self.user_messages_collection.insert_one(user_message_data)

        # Fetch existing conversation data from Redis and update it
        # conversation_data = await redis.get(conversation_id)
        # if conversation_data:
        #     conversation_data = json.loads(conversation_data)
        #     conversation_data['messages'] = conversation_data.get('messages', []) + [message]
        #     await redis.set(conversation_id, json.dumps(conversation_data), ex=CACHE_EXPIRATION)
        

    async def add_llm_response(self, conversation_id: str, response: str):
        """
        Add an LLM response to MongoDB and cache it in Redis.
        """
        timestamp = datetime.utcnow()
        llm_response_data = {
            "conversation_id": conversation_id,
            "response": response,
            "timestamp": timestamp
        }

        # Store the LLM response in MongoDB
        await self.llm_responses_collection.insert_one(llm_response_data)

        # Fetch existing conversation data from Redis and update it
        # conversation_data = await redis.get(conversation_id)
        # if conversation_data:
        #     conversation_data = json.loads(conversation_data)
        #     conversation_data['responses'] = conversation_data.get('responses', []) + [response]
        #     await redis.set(conversation_id, json.dumps(conversation_data), ex=CACHE_EXPIRATION)


    # async def get_chats(self, user_id: str, limit: int = 10, offset: int = 0) -> List[dict]:
    #     """
    #     Retrieve chat messages for a specific user from MongoDB.
    #     """
    #     chats = await self.chat_collection.find({"user_id": user_id}).skip(offset).limit(limit).to_list(length=limit)
    #     return chats

    # async def get_chat(self, user_id: str, section_id: str, )
    
    async def get_topic_documents(self, topic_id: str):
        topic = self.topics_collection.find_one({"topic_id": topic_id})
        if topic:
            return {"documents": topic["documents"]}
        else:
            raise HTTPException(status_code=404, detail="Topic not found")

    async def create_chat(self, user_id:str, topic_id:str, message:str):
        """
        Create a new chat session for a user.
        """
        conversation = {
            "user_id": user_id,
            "topic_id": topic_id,
            "conversation": [],
            "last_active": datetime.utcnow()
        }

        # Add the user's message to the conversation
        message = {
            "timestamp": datetime.utcnow(),
            "role": "assistant",
            "message": message,
        }

        conversation["conversation"].append(message)
        
        # Store the chat in MongoDB
        await self.conversations_collection.insert_one(conversation)
        
        return conversation
    
    async def chat(self, user_id: str, topic_id: str, message: str):
        """
        Handle the chat flow, including user messages and LLM responses.
        """
        # Find the conversation for the user and topic
        conversation = await self.conversations_collection.find_one({"user_id": user_id, "topic_id": topic_id})
        if not conversation:
            # If no conversation exists, create a new one
            conversation = await self.create_chat(user_id=user_id, topic_id=topic_id, message=message)
        else:
            # If conversation exists, add the user's message
            user_message = {
                "timestamp": datetime.utcnow(),
                "role": "user",
                "message": message,
            }
            conversation["conversation"].append(user_message)
            
            
            
            # feed conversation and topic to LLM to get a response
            response = await agent_service.generate_response(conversation, topic_id, message)
            llm_response = {
                "timestamp": datetime.utcnow(),
                "role": "assistant",
                "message": response,
            }
            conversation["conversation"].append(llm_response)

            return llm_response
            

        return conversation

    # async def get_conversation(self, conversation_id: str):
    #     """
    #     Retrieve a conversation from Redis or MongoDB if not in cache.
    #     """
    #     # First, try to get the conversation from Redis
    #     # conversation_data = await redis.get(conversation_id)
    #     # if conversation_data:
    #     #     return json.loads(conversation_data)
        
    #     # If not found in Redis, fetch from MongoDB
    #     conversation_data = await self.conversations_collection.find_one({"conversation_id": conversation_id})
    #     # if conversation_data:
    #     #     # Cache the conversation in Redis for future use
    #     #     await redis.set(conversation_id, json.dumps(conversation_data), ex=CACHE_EXPIRATION)
        
    #     return conversation_data
    

    # async def chat_flow(self, conversation_id: Optional[str], topic: Optional[str], student_id:str ,message: str, image_file: Optional[UploadFile]):
    #     """
    #     Main chat flow function to handle user messages and LLM responses.
    #     """
    #     if not conversation_id:
    #         # Create a new conversation if no ID is provided
    #         conversation_id = await self.create_conversation(student_id=student_id, topic=topic)
        
    #     # Check is the image is uploaded
    #     if image_file:
    #         # Store the image locally
    #         image_path = await self.store_image_locally(image_file, conversation_id)

    #     # Check conversation status
    #     conversation = await self.get_conversation(conversation_id)
    #     if not conversation:
    #         raise HTTPException(status_code=404, detail="Conversation not found")
    #     if conversation["status"] != "active":
            
        