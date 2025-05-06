from azure.cosmos import CosmosClient, exceptions
import os
import logging
from datetime import datetime
import uuid
from functools import lru_cache
from typing import Optional, Dict, Any, List, Type, TypeVar, Generic, Callable


T = TypeVar('T')
logger = logging.getLogger(__name__)


class CosmosDBManager:
    """Singleton manager for Cosmos DB connections"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CosmosDBManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Load environment variables directly from Azure App Service settings
        self.connection_string = os.environ.get("COSMOS_CONNECTION_STRING")
        self.database_name = os.environ.get("COSMOS_DATABASE_NAME", "whobought")
        self.items_container_name = os.environ.get("COSMOS_CONTAINER_NAME", "items")
        self.users_container_name = os.environ.get("COSMOS_USER_CONTAINER_NAME", "users")
        
        # Initialize connections to None
        self.client = None
        self.database = None
        self.items_container = None
        self.users_container = None
        
        # Initialize connection at startup if environment variables are set
        if self.connection_string:
            try:
                self._initialize_connection()
            except Exception as e:
                logger.error(f"Failed to connect to Cosmos DB: {str(e)}")
                
        self._initialized = True
        
    def _initialize_connection(self):
        """Initialize connection to Cosmos DB"""
        if not self.client:
            logger.info("Initializing Cosmos DB connection...")
            self.client = CosmosClient.from_connection_string(self.connection_string)
            self.database = self.client.get_database_client(self.database_name)
            self.items_container = self.database.get_container_client(self.items_container_name)
            self.users_container = self.database.get_container_client(self.users_container_name)
            logger.info(f"Successfully connected to Cosmos DB database '{self.database_name}'")
    
    def get_items_container(self):
        """Get the items container client"""
        if not self.items_container:
            self._initialize_connection()
        return self.items_container
    
    def get_users_container(self):
        """Get the users container client"""
        if not self.users_container:
            self._initialize_connection()
        return self.users_container


@lru_cache()
def get_cosmos_manager():
    """Singleton factory function for CosmosDBManager"""
    return CosmosDBManager()


class BaseCosmosRepository(Generic[T]):
    """Base repository for Cosmos DB operations"""
    
    def __init__(self, container_getter: Callable):
        self.container_getter = container_getter
    
    async def get_all(self, query: str = "SELECT * FROM c") -> List[Dict[str, Any]]:
        """Get all documents"""
        try:
            container = self.container_getter()
            items = list(container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return items
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e
    
    async def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get document by ID"""
        try:
            container = self.container_getter()
            item = container.read_item(item=item_id, partition_key=item_id)
            return item
        except exceptions.CosmosResourceNotFoundError:
            return None
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e
    
    async def create(self, item_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new document"""
        try:
            container = self.container_getter()
            
            # Ensure the item has an ID
            if not item_dict.get("id"):
                item_dict["id"] = str(uuid.uuid4())
            
            # Add creation timestamp
            now = datetime.utcnow()
            item_dict["createdAt"] = now.isoformat()
            
            # If it's an updateable item, add updatedAt timestamp
            if "updatedAt" in item_dict:
                item_dict["updatedAt"] = now.isoformat()
            
            created_item = container.create_item(body=item_dict)
            return created_item
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e
    
    async def update(self, item_id: str, item_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing document"""
        try:
            container = self.container_getter()
            
            # Read existing item first
            try:
                existing_item = container.read_item(item=item_id, partition_key=item_id)
            except exceptions.CosmosResourceNotFoundError:
                return None
            
            # Preserve the id and createdAt
            item_dict["id"] = item_id
            if "createdAt" in existing_item:
                item_dict["createdAt"] = existing_item.get("createdAt")
            
            # Update updatedAt timestamp
            if "updatedAt" in existing_item or "updatedAt" in item_dict:
                item_dict["updatedAt"] = datetime.utcnow().isoformat()
            
            updated_item = container.replace_item(item=item_id, body=item_dict)
            return updated_item
        except exceptions.CosmosResourceNotFoundError:
            return None
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e
    
    async def delete(self, item_id: str) -> bool:
        """Delete a document"""
        try:
            container = self.container_getter()
            container.delete_item(item=item_id, partition_key=item_id)
            return True
        except exceptions.CosmosResourceNotFoundError:
            return False
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e
    
    async def query(self, query: str) -> List[Dict[str, Any]]:
        """Run a custom query"""
        try:
            container = self.container_getter()
            items = list(container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return items
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e 