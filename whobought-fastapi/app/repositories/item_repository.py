from typing import List, Optional, Dict, Any
from .generic_repository import GenericRepository
from .cosmosdb_repository import get_cosmos_manager
from ..models.entities.item import Item


class ItemRepository(GenericRepository[Item]):
    """Repository for Item operations in Cosmos DB"""
    
    def __init__(self):
        super().__init__(
            container_getter=get_cosmos_manager().get_items_container,
            entity_type=Item
        )
    
    async def find_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all items created by a specific user"""
        query = f"SELECT * FROM c WHERE c.purchasedBy = '{user_id}'"
        return await self.query(query)
    
    async def find_paid_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all items where a specific user is marked as 'paidFor'"""
        return await self.find_by_array_contains("paidFor", user_id)
    
    async def find_by_purchase_id(self, purchase_id: str) -> List[Dict[str, Any]]:
        """Find all items for a specific purchase"""
        return await self.find_by_field("purchase_id", purchase_id)
    
    async def find_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Find items by substring of name (case insensitive)"""
        return await self.find_by_contains_field("name", name)


def get_item_repository() -> ItemRepository:
    """Factory function for ItemRepository"""
    return ItemRepository() 