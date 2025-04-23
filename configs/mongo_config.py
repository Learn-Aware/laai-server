import os
import logging
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, OperationFailure

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mongodb")

load_dotenv()

# Get connection details from environment variables
DB_USERNAME = os.getenv("MONGO_USERNAME", "")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", "")
DB_CLUSTER = os.getenv("MONGO_CLUSTER", "")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "")

# Format the URI using the MongoDB Atlas connection string format
MONGO_URI = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_CLUSTER}/?retryWrites=true&w=majority&appName=Cluster0"

# Default settings for connection pooling
DEFAULT_MAX_POOL_SIZE = 10
DEFAULT_MIN_POOL_SIZE = 1
DEFAULT_MAX_IDLE_TIME_MS = 10000  # 10 seconds
DEFAULT_CONNECT_TIMEOUT_MS = 30000  # 30 seconds
DEFAULT_SERVER_SELECTION_TIMEOUT_MS = 30000  # 30 seconds

class MongoDBSingleton:
    _instance = None
    client = None
    db = None
    is_connected = False
    auth_failed = False
    connection_error = None
    db_initialized = False
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def initialize(self, 
                  uri=MONGO_URI, 
                  db_name=MONGO_DB_NAME,
                  max_pool_size=DEFAULT_MAX_POOL_SIZE,
                  min_pool_size=DEFAULT_MIN_POOL_SIZE,
                  max_idle_time_ms=DEFAULT_MAX_IDLE_TIME_MS,
                  connect_timeout_ms=DEFAULT_CONNECT_TIMEOUT_MS,
                  server_selection_timeout_ms=DEFAULT_SERVER_SELECTION_TIMEOUT_MS):
        """Initialize the MongoDB connection with pooling"""
        try:
            logger.info("Initializing MongoDB connection pool...")
            # Create the client using the Atlas connection string format
            self.client = MongoClient(
                uri,
                maxPoolSize=max_pool_size,
                minPoolSize=min_pool_size,
                maxIdleTimeMS=max_idle_time_ms,
                connectTimeoutMS=connect_timeout_ms,
                serverSelectionTimeoutMS=server_selection_timeout_ms
            )
            
            # Test connection to server to confirm successful connection
            try:
                # Just get the server status - this will test basic connectivity
                self.client.admin.command('ping')
                self.is_connected = True
                self.auth_failed = False
                self.connection_error = None
                logger.info("Pinged your deployment. Successfully connected to MongoDB!")
                
                # Now try to access the actual database
                try:
                    self.db = self.client[db_name]
                    # Count documents in a collection to verify database access
                    collections = self.db.list_collection_names()
                    self.db_initialized = True
                    logger.info(f"Successfully connected to database: {db_name} with collections: {collections}")
                except OperationFailure as e:
                    # We can connect but auth failed for the specific database
                    logger.warning(f"Connected to MongoDB server but database access failed: {e}")
                    self.auth_failed = True
                    self.connection_error = str(e)
                    self.db_initialized = False
                    # Still return True since basic connectivity works
                    return True
                
            except Exception as e:
                logger.error(f"Could not connect to MongoDB server: {e}")
                self.is_connected = False
                self.connection_error = str(e)
                self.db_initialized = False
                return False
                
            return True
        except Exception as e:
            logger.error(f"Unexpected error initializing MongoDB connection: {e}")
            self.is_connected = False
            self.connection_error = str(e)
            self.db_initialized = False
            return False
    
    def get_status(self):
        """Get the current status of the MongoDB connection"""
        status = {
            "is_connected": self.is_connected,
            "auth_failed": self.auth_failed,
            "db_initialized": self.db_initialized,
            "connection_error": self.connection_error
        }
        
        # Try to get server info if connected
        if self.is_connected and self.client:
            try:
                status["server_info"] = self.client.admin.command('ping')
            except Exception as e:
                status["server_info_error"] = str(e)
                
        return status
    
    def close(self):
        """Close the MongoDB connection"""
        if self.client:
            self.client.close()
            self.is_connected = False
            self.db_initialized = False
            logger.info("MongoDB connection closed")

# Create a singleton instance
mongodb = MongoDBSingleton.get_instance()

# Legacy support - maintain backward compatibility with existing code
# We'll initialize these in the startup event of the FastAPI app
client = None  
db = None
users_collection = None
conversation_collection = None

def setup_legacy_clients():
    """Setup the legacy client variables after initialization"""
    global client, db, users_collection, conversation_collection
    if not mongodb.is_connected:
        return False
    
    client = mongodb.client
    
    # Don't use boolean check on mongodb.db which causes NotImplementedError
    if mongodb.db_initialized and mongodb.db is not None:
        db = mongodb.db
        users_collection = db["users"]
        conversation_collection = db["conversations"]
        return True
    return False
