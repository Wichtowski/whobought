from typing import Dict, Any, Optional, List
from .generic_repository import GenericRepository
from .cosmosdb_repository import get_cosmos_manager
from ..models.entities.user import User


class UserRepository(GenericRepository[User]):
    """Repository for User operations in Cosmos DB"""
    
    def __init__(self):
        super().__init__(
            container_getter=get_cosmos_manager().get_users_container,
            entity_type=User
        )
    
    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a user by their email address"""
        query = f"SELECT * FROM c WHERE c.email = '{email}'"
        result = await self.query(query)
        return result[0] if result else None
    
    async def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        return await self.find_one_by_field("username", username)


def get_user_repository() -> UserRepository:
    """Factory function for UserRepository"""
    return UserRepository() 