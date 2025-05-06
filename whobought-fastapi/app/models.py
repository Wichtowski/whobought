from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Generic, TypeVar, Any
from datetime import datetime
import uuid


class Item(BaseModel):
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


class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    createdAt: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com"
            }
        }


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "securepassword123"
            }
        }


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepassword123"
            }
        }


T = TypeVar('T')

class ApiResponse(Generic[T]):
    """Standard API response format for the entire application"""
    def __init__(
        self,
        data: Optional[T] = None,
        message: str = "Success",
        success: bool = True,
        status_code: int = 200,
        errors: Optional[List[str]] = None
    ):
        self.data = data
        self.message = message
        self.success = success
        self.status_code = status_code
        self.errors = errors or []
        self.timestamp = datetime.utcnow().isoformat()

    def dict(self):
        """Convert response to dictionary"""
        return {
            "data": self.data,
            "message": self.message,
            "success": self.success,
            "statusCode": self.status_code,
            "errors": self.errors,
            "timestamp": self.timestamp
        }


class ResponseModel(BaseModel):
    """Pydantic model for API responses"""
    data: Optional[Any] = None
    message: str = "Success"
    success: bool = True
    statusCode: int = 200
    errors: List[str] = []
    timestamp: str 