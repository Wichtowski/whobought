from typing import TypeVar, Generic, Dict, Any, List, Optional, Callable, Type
from .cosmosdb_repository import BaseCosmosRepository, get_cosmos_manager

T = TypeVar('T')

class GenericRepository(BaseCosmosRepository[T]):
    """Generic repository pattern implementation for CosmosDB"""
    
    def __init__(self, container_getter: Callable, entity_type: Type[T]):
        super().__init__(container_getter=container_getter)
        self.entity_type = entity_type
    
    async def find_by_field(self, field_name: str, value: Any) -> List[Dict[str, Any]]:
        """Generic method to find items by a specific field value"""
        query = f"SELECT * FROM c WHERE c.{field_name} = '{value}'"
        return await self.query(query)
    
    async def find_one_by_field(self, field_name: str, value: Any) -> Optional[Dict[str, Any]]:
        """Generic method to find one item by a specific field value"""
        results = await self.find_by_field(field_name, value)
        return results[0] if results else None
    
    async def find_by_contains_field(self, field_name: str, value: Any) -> List[Dict[str, Any]]:
        """Generic method to find items by a field containing a value (case insensitive)"""
        query = f"SELECT * FROM c WHERE CONTAINS(LOWER(c.{field_name}), LOWER('{value}'))"
        return await self.query(query)
    
    async def find_by_array_contains(self, array_field: str, value: Any) -> List[Dict[str, Any]]:
        """Generic method to find items where an array field contains a value"""
        query = f"SELECT * FROM c WHERE ARRAY_CONTAINS(c.{array_field}, '{value}')"
        return await self.query(query) 