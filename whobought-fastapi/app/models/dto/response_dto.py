from pydantic import BaseModel, Field
from typing import Optional, List, Any, Generic, TypeVar
from datetime import datetime


T = TypeVar('T')

class ApiResponseDto(BaseModel, Generic[T]):
    """Standard API response DTO"""
    data: Optional[T] = None
    message: str = ""
    statusCode: int = 200
    errors: List[str] = []
    timestamp: str

    class Config:
        json_schema_extra = {
            "example": {
                "data": None,
                "message": "Success",
                "statusCode": 200,
                "errors": [],
                "timestamp": "2023-04-01T00:00:00.000Z"
            }
        } 