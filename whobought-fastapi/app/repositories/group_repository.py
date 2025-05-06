from typing import List, Dict, Any, Optional
from .generic_repository import GenericRepository
from .cosmosdb_repository import get_cosmos_manager
from ..models.entities.group import Group


class GroupRepository(GenericRepository[Group]):
    """Repository for Group operations in Cosmos DB"""
    
    def __init__(self):
        super().__init__(
            container_getter=get_cosmos_manager().get_groups_container,
            entity_type=Group
        )
    
    async def find_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all groups a user belongs to"""
        query = f"SELECT * FROM c WHERE ARRAY_CONTAINS(c.member_ids, '{user_id}')"
        return await self.query(query)
    
    async def find_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Find groups by partial name match (case insensitive)"""
        query = f"SELECT * FROM c WHERE CONTAINS(LOWER(c.name), LOWER('{name}'))"
        return await self.query(query)


def get_group_repository() -> GroupRepository:
    """Factory function for GroupRepository"""
    return GroupRepository() 