from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Purchase(BaseModel):
    """Purchase entity model"""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    user_id: str
    group_id: str
    purchase_date: datetime
    total_amount: float
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Night Hangout",
                "description": "Pub Crawl",
                "user_id": "user1",
                "group_id": "group1",
                "purchase_date": "2023-04-01T12:00:00.000Z",
                "total_amount": 87.50
            }
        } 