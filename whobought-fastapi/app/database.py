from azure.cosmos import CosmosClient, exceptions
import os
import logging
from datetime import datetime
import uuid
from functools import lru_cache
from typing import Optional, Dict, Any, List

from .utils import hash_password, verify_password

logger = logging.getLogger(__name__)

class CosmosDBManager:
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
        # These will be set in the App Service Configuration or during local development
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
                # Don't raise error here, let it be handled when used
                
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


class ItemsDB:
    @staticmethod
    async def get_all_items():
        try:
            cosmos = get_cosmos_manager()
            items_container = cosmos.get_items_container()
            
            items = list(items_container.query_items(
                query="SELECT * FROM c ORDER BY c.createdAt DESC",
                enable_cross_partition_query=True
            ))
            return items
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e

    @staticmethod
    async def get_item(item_id: str):
        try:
            cosmos = get_cosmos_manager()
            items_container = cosmos.get_items_container()
            
            item = items_container.read_item(item=item_id, partition_key=item_id)
            return item
        except exceptions.CosmosResourceNotFoundError:
            return None
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e

    @staticmethod
    async def create_item(item_dict: dict):
        try:
            cosmos = get_cosmos_manager()
            items_container = cosmos.get_items_container()
            
            if not item_dict.get("id"):
                item_dict["id"] = str(uuid.uuid4())
            
            now = datetime.utcnow()
            item_dict["createdAt"] = now.isoformat()
            item_dict["updatedAt"] = now.isoformat()
            
            created_item = items_container.create_item(body=item_dict)
            return created_item
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e

    @staticmethod
    async def update_item(item_id: str, item_dict: dict):
        try:
            cosmos = get_cosmos_manager()
            items_container = cosmos.get_items_container()
            
            existing_item = items_container.read_item(item=item_id, partition_key=item_id)
            
            # Preserve the id and createdAt
            item_dict["id"] = item_id
            item_dict["createdAt"] = existing_item.get("createdAt")
            item_dict["updatedAt"] = datetime.utcnow().isoformat()
            
            updated_item = items_container.replace_item(item=item_id, body=item_dict)
            return updated_item
        except exceptions.CosmosResourceNotFoundError:
            return None
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e

    @staticmethod
    async def delete_item(item_id: str):
        try:
            cosmos = get_cosmos_manager()
            items_container = cosmos.get_items_container()
            
            items_container.delete_item(item=item_id, partition_key=item_id)
            return True
        except exceptions.CosmosResourceNotFoundError:
            return False
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e


class UsersDB:
    @staticmethod
    async def get_all_users():
        try:
            cosmos = get_cosmos_manager()
            users_container = cosmos.get_users_container()
            
            users = list(users_container.query_items(
                query="SELECT * FROM c",
                enable_cross_partition_query=True
            ))
            return users
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e

    @staticmethod
    async def get_user(user_id: str):
        try:
            cosmos = get_cosmos_manager()
            users_container = cosmos.get_users_container()
            
            user = users_container.read_item(item=user_id, partition_key=user_id)
            return user
        except exceptions.CosmosResourceNotFoundError:
            return None
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e

    @staticmethod
    async def get_user_by_username(username: str):
        try:
            cosmos = get_cosmos_manager()
            users_container = cosmos.get_users_container()
            
            # Query for user by username
            query = f"SELECT * FROM c WHERE c.username = '{username}'"
            users = list(users_container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            
            if users:
                return users[0]
            return None
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e

    @staticmethod
    async def get_user_by_email(email: str):
        try:
            cosmos = get_cosmos_manager()
            users_container = cosmos.get_users_container()
            
            # Query for user by email
            query = f"SELECT * FROM c WHERE c.email = '{email}'"
            users = list(users_container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            
            if users:
                return users[0]
            return None
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e

    @staticmethod
    async def create_user(user_data: Dict[str, Any]):
        try:
            cosmos = get_cosmos_manager()
            users_container = cosmos.get_users_container()
            
            # Check if username already exists
            existing_user = await UsersDB.get_user_by_username(user_data.get("username", ""))
            if existing_user:
                return {"error": "Username already exists"}
            
            # Check if email already exists
            existing_email = await UsersDB.get_user_by_email(user_data.get("email", ""))
            if existing_email:
                return {"error": "Email already exists"}
            
            # Create new user with hashed password
            if not user_data.get("id"):
                user_data["id"] = str(uuid.uuid4())
            
            # Hash the password if provided
            if "password" in user_data:
                hashed_password = hash_password(user_data["password"])
                user_data["hashed_password"] = hashed_password
                # Remove plain password
                del user_data["password"]
            
            user_data["createdAt"] = datetime.utcnow().isoformat()
            
            created_user = users_container.create_item(body=user_data)
            return created_user
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB error: {str(e)}")
            raise e

    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user with username and password"""
        user = await UsersDB.get_user_by_username(username)
        
        if not user:
            return None
        
        # Verify password
        if not verify_password(password, user.get("hashed_password", "")):
            return None
        
        # Remove hashed password before returning
        user_data = {k: v for k, v in user.items() if k != "hashed_password"}
        return user_data 