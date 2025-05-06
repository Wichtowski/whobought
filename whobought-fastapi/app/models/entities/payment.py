from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Payment(BaseModel):
    """Payment entity model"""
    id: Optional[str] = None
    user_id: str
    group_id: str
    amount: float
    description: Optional[str] = None
    payment_date: datetime
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user1",
                "group_id": "group1",
                "amount": 45.50,
                "description": "Repayment for groceries",
                "payment_date": "2023-04-05T15:30:00.000Z"
            }
        } 