from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Group(BaseModel):
    """Group entity model"""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    member_ids: List[str]
    admin_ids: List[str]
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Roommates",
                "description": "Shared expenses for apartment",
                "member_ids": ["user1", "user2", "user3"],
                "admin_ids": ["user1"]
            }
        } 