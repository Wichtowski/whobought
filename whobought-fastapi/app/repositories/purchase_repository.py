from typing import List, Optional, Dict, Any
from .generic_repository import GenericRepository
from .cosmosdb_repository import get_cosmos_manager
from ..models.entities.purchase import Purchase


class PurchaseRepository(GenericRepository[Purchase]):
    """Repository for Purchase operations in Cosmos DB"""
    
    def __init__(self):
        super().__init__(
            container_getter=get_cosmos_manager().get_purchases_container,
            entity_type=Purchase
        )
    
    async def find_by_group_id(self, group_id: str) -> List[Dict[str, Any]]:
        """Find all purchases in a specific group"""
        return await self.find_by_field("group_id", group_id)
    
    async def find_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        """Find all purchases made by a specific user"""
        return await self.find_by_field("user_id", user_id)
    
    async def find_by_group_and_timeframe(self, group_id: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Find purchases in a group within a specific timeframe"""
        query = f"""
        SELECT * FROM c 
        WHERE c.group_id = '{group_id}' 
        AND c.purchase_date >= '{start_date}' 
        AND c.purchase_date <= '{end_date}'
        """
        return await self.query(query)


def get_purchase_repository() -> PurchaseRepository:
    """Factory function for PurchaseRepository"""
    return PurchaseRepository() 