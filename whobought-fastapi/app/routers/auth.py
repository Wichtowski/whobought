from fastapi import APIRouter, HTTPException, Depends, status, Body, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict, Any

from ..models import UserCreate, Token, LoginRequest, User
from ..database import UsersDB
from ..auth import create_access_token, get_current_user
from ..responses import success_response, error_response, created_response

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register")
async def register(request: Request, user_data: UserCreate):
    """Register a new user"""
    try:
        # Create user in database
        user_dict = user_data.dict()
        created_user = await UsersDB.create_user(user_dict)
        
        # Check for errors
        if isinstance(created_user, dict) and "error" in created_user:
            return error_response(
                message=created_user["error"],
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        # Create token for the new user
        token_data = {
            "sub": created_user["id"],
            "username": created_user["username"],
            "email": created_user["email"]
        }
        
        access_token = create_access_token(data=token_data)
        
        # Return token and user data
        return created_response(
            data={
                "user": {
                    "id": created_user["id"],
                    "username": created_user["username"],
                    "email": created_user["email"]
                },
                "token": {
                    "access_token": access_token,
                    "token_type": "bearer"
                }
            },
            message="User registered successfully"
        )
    except Exception as e:
        return error_response(message=f"Registration failed: {str(e)}")

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 compatible token login, get an access token for future requests"""
    user = await UsersDB.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        return error_response(
            message="Incorrect username or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        
    # Create token for the user
    token_data = {
        "sub": user["id"],
        "username": user["username"],
        "email": user["email"]
    }
    
    access_token = create_access_token(data=token_data)
    
    return success_response(
        data={"access_token": access_token, "token_type": "bearer"}
    )

@router.post("/login")
async def login(login_data: LoginRequest):
    """Login and get an access token"""
    user = await UsersDB.authenticate_user(login_data.username, login_data.password)
    
    if not user:
        return error_response(
            message="Incorrect username or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        
    # Create token for the user
    token_data = {
        "sub": user["id"],
        "username": user["username"],
        "email": user["email"]
    }
    
    access_token = create_access_token(data=token_data)
    
    return success_response(
        data={
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"]
            },
            "token": {
                "access_token": access_token,
                "token_type": "bearer"
            }
        },
        message="Login successful"
    )

@router.get("/me")
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user information"""
    return success_response(
        data={
            "id": current_user["id"],
            "username": current_user["username"],
            "email": current_user["email"]
        }
    ) 