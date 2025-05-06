from typing import List, Dict, Any, Optional
from .generic_repository import GenericRepository
from .cosmosdb_repository import get_cosmos_manager
from ..models.entities.payment import Payment


class PaymentRepository(GenericRepository[Payment]):
    """Repository for Payment operations in Cosmos DB"""
    
    def __init__(self):
        super().__init__(
            container_getter=get_cosmos_manager().get_payments_container,
            entity_type=Payment
        )
    
    async def find_by_group_id(self, group_id: str) -> List[Dict[str, Any]]:
        """Get all payments for a group"""
        return await self.find_by_field("group_id", group_id)
    
    async def find_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all payments for a user"""
        return await self.find_by_field("user_id", user_id)


def get_payment_repository() -> PaymentRepository:
    """Factory function for PaymentRepository"""
    return PaymentRepository() 