from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    """User entity model"""
    id: Optional[str] = None
    username: str
    email: str
    hashed_password: Optional[str] = None
    createdAt: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "johndoe",
                "email": "john@example.com",
                "createdAt": "2023-04-01T00:00:00.000Z"
            }
        } 