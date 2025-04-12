from typing import Any, Dict, List, Optional, TypeVar, Generic
from pymongo.collection import Collection
from pymongo.errors import PyMongoError, DuplicateKeyError, OperationFailure
from fastapi import HTTPException, status
from bson import ObjectId
from configs.mongo_config import mongodb

T = TypeVar('T')

class MongoDBDAL(Generic[T]):
    """Base Data Access Layer for MongoDB collections"""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self._collection = None
    
    @property
    def collection(self) -> Collection:
        """Get the MongoDB collection, with validation checks"""
        # First, check connection status
        if not mongodb.is_connected:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection is not available. Please try again later."
            )
        
        # Then check if the db is initialized
        if not mongodb.db_initialized:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database is not properly initialized. Please try again later."
            )
        
        # If collection hasn't been initialized yet, initialize it
        if self._collection is None:
            if mongodb.db is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database reference is not available."
                )
            self._collection = mongodb.db[self.collection_name]
        
        return self._collection
    
    async def find_all(self) -> List[Dict[str, Any]]:
        """Retrieve all documents from the collection"""
        try:
            result = list(self.collection.find())
            # Convert ObjectId to string for JSON serialization
            for item in result:
                if "_id" in item and isinstance(item["_id"], ObjectId):
                    item["_id"] = str(item["_id"])
            return result
        except OperationFailure as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed: {str(e)}"
            )
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while retrieving documents: {str(e)}"
            )
    
    async def find_all_filtered(self, filter_dict: Dict[str, Any], projection: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Find all documents matching the filter criteria"""
        try:
            if projection:
                result = list(self.collection.find(filter_dict, projection))
            else:
                result = list(self.collection.find(filter_dict))
                
            # Convert ObjectId to string for JSON serialization
            for item in result:
                if "_id" in item and isinstance(item["_id"], ObjectId):
                    item["_id"] = str(item["_id"])
            return result
        except OperationFailure as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed: {str(e)}"
            )
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while retrieving filtered documents: {str(e)}"
            )
    
    async def find_one(self, filter_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document by filter criteria"""
        try:
            result = self.collection.find_one(filter_dict)
            if result and "_id" in result and isinstance(result["_id"], ObjectId):
                result["_id"] = str(result["_id"])
            return result
        except OperationFailure as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed: {str(e)}"
            )
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while finding document: {str(e)}"
            )
    
    async def insert_one(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a single document into the collection"""
        try:
            result = self.collection.insert_one(document)
            # Return the document with the new id
            document["_id"] = str(result.inserted_id)
            return document
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A document with this key already exists."
            )
        except OperationFailure as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed: {str(e)}"
            )
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while inserting document: {str(e)}"
            )
    
    async def update_one(self, filter_dict: Dict[str, Any], update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a single document in the collection"""
        try:
            result = self.collection.update_one(filter_dict, {"$set": update_data})
            if result.modified_count == 0:
                if result.matched_count == 0:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Document not found."
                    )
                # Document found but not modified (already has the same values)
                return {"matched": True, "modified": False}
            
            # Get the updated document
            updated_doc = self.collection.find_one(filter_dict)
            if updated_doc and "_id" in updated_doc:
                updated_doc["_id"] = str(updated_doc["_id"])
            
            return {"matched": True, "modified": True, "document": updated_doc}
        except OperationFailure as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed: {str(e)}"
            )
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while updating document: {str(e)}"
            )
    
    async def delete_one(self, filter_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Delete a single document from the collection"""
        try:
            result = self.collection.delete_one(filter_dict)
            if result.deleted_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Document not found."
                )
            
            return {"deleted": True, "count": result.deleted_count}
        except OperationFailure as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed: {str(e)}"
            )
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while deleting document: {str(e)}"
            )
    
    async def delete_many(self, filter_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Delete multiple documents from the collection"""
        try:
            result = self.collection.delete_many(filter_dict)
            return {"deleted": True, "count": result.deleted_count}
        except OperationFailure as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed: {str(e)}"
            )
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while deleting documents: {str(e)}"
            )
    
    async def create_index(self, keys_list, **kwargs):
        """Create an index on the collection"""
        try:
            return self.collection.create_index(keys_list, **kwargs)
        except OperationFailure as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed: {str(e)}"
            )
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while creating index: {str(e)}"
            ) 