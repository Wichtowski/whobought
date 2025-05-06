from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class ItemCreateDto(BaseModel):
    """DTO for creating an item"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    purchasedBy: str
    amount: float = Field(..., gt=0)
    paidFor: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Groceries",
                "description": "Weekly shopping",
                "purchasedBy": "550e8400-e29b-41d4-a716-446655440000",
                "amount": 45.50,
                "paidFor": ["550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440001"]
            }
        }


class ItemUpdateDto(BaseModel):
    """DTO for updating an item"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    purchasedBy: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    paidFor: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Groceries",
                "amount": 50.75,
                "paidFor": ["550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440001"]
            }
        }


class ItemResponseDto(BaseModel):
    """DTO for item response"""
    id: str
    name: str
    description: Optional[str] = None
    purchasedBy: str
    amount: float
    paidFor: List[str]
    createdAt: str
    updatedAt: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Groceries",
                "description": "Weekly shopping",
                "purchasedBy": "550e8400-e29b-41d4-a716-446655440000",
                "amount": 45.50,
                "paidFor": ["550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440001"],
                "createdAt": "2023-04-01T00:00:00.000Z",
                "updatedAt": "2023-04-01T00:00:00.000Z"
            }
        } 