from pymongo.errors import ServerSelectionTimeoutError, OperationFailure, ConnectionFailure
from configs.mongo_config import mongodb, MONGO_DB_NAME
from typing import Dict, Any


class HealthDAL:
    """Data Access Layer for health checks"""
    
    @staticmethod
    async def check_database_health() -> Dict[str, Any]:
        """
        Check if the MongoDB database connection is healthy.
        Returns a status object with different values depending on the connection state.
        """
        # Get the MongoDB connection status
        mongo_status = mongodb.get_status()
        
        # If not connected at all
        if not mongo_status["is_connected"]:
            return {
                "status": "disconnected",
                "message": "Database connection is not established",
                "error": mongo_status.get("connection_error"),
                "action_needed": "Application restart may be required"
            }
        
        # If connected but authentication failed
        if mongo_status["auth_failed"]:
            return {
                "status": "partial",
                "message": "Connected to MongoDB server but authentication failed",
                "error": mongo_status.get("connection_error"),
                "server_info": mongo_status.get("server_info", {})
            }
        
        # Check if we can access the database
        try:
            # Try a simple operation
            client = mongodb.client
            
            # Skip any DB-level operations that might cause boolean check issues
            try:
                server_info = client.admin.command('ping')
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Failed to ping MongoDB server: {str(e)}",
                    "recoverable": True
                }
            
            return {
                "status": "healthy",
                "message": "Database connection is healthy",
                "server": server_info.get("ok", 1) == 1,
                "db_accessible": mongodb.db_initialized
            }
        except ConnectionFailure:
            return {
                "status": "error",
                "message": "Failed to connect to MongoDB server",
                "recoverable": True
            }
        except ServerSelectionTimeoutError:
            return {
                "status": "error",
                "message": "Database server not reachable - timed out while selecting server",
                "recoverable": True
            }
        except OperationFailure as e:
            # Handle auth failure specifically
            if "auth" in str(e).lower():
                return {
                    "status": "partial",
                    "message": "Connected to MongoDB server but authentication failed",
                    "error": str(e)
                }
            # Other operation failures
            return {
                "status": "error",
                "message": f"Database operation failed: {str(e)}",
                "recoverable": True
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error checking database health: {str(e)}",
                "recoverable": False
            } 