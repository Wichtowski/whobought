from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Item(BaseModel):
    """Item entity model"""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    purchasedBy: str
    amount: float
    paidFor: List[str]
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Groceries",
                "description": "Weekly shopping",
                "purchasedBy": "user1",
                "amount": 45.50,
                "paidFor": ["user1", "user2"]
            }
        } 