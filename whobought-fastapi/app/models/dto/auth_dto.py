from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreateDto(BaseModel):
    """DTO for user registration"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "securepassword123"
            }
        }


class UserResponseDto(BaseModel):
    """DTO for user response"""
    id: str
    username: str
    email: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "johndoe",
                "email": "john@example.com"
            }
        }


class LoginRequestDto(BaseModel):
    """DTO for login request"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepassword123"
            }
        }


class TokenDto(BaseModel):
    """DTO for token response"""
    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenPayloadDto(BaseModel):
    """DTO for token payload data"""
    sub: str
    username: str
    email: str
    exp: Optional[int] = None
    iat: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "sub": "550e8400-e29b-41d4-a716-446655440000",
                "username": "johndoe",
                "email": "john@example.com",
                "exp": 1617235200,
                "iat": 1617148800
            }
        }


class AuthResponseDto(BaseModel):
    """DTO for authentication response containing user and token"""
    user: UserResponseDto
    token: TokenDto

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "username": "johndoe",
                    "email": "john@example.com"
                },
                "token": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer"
                }
            }
        } 