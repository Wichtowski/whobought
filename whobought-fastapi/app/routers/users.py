from fastapi import APIRouter, HTTPException, Depends, status, Body, Request
from typing import List
from fastapi.responses import JSONResponse

from ..models import User
from ..database import UsersDB
from ..dependencies import get_db
from ..responses import success_response, error_response, not_found_response, created_response

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_users(request: Request, db=Depends(get_db)):
    try:
        users = await UsersDB.get_all_users()
        return success_response(data=users)
    except Exception as e:
        return error_response(message=f"Database error: {str(e)}")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db=Depends(get_db)):
    try:
        created_user = await UsersDB.create_user(user.dict())
        return created_response(data=created_user)
    except Exception as e:
        return error_response(message=f"Database error: {str(e)}")

@router.get("/{user_id}")
async def get_user(user_id: str, db=Depends(get_db)):
    user = await UsersDB.get_user(user_id)
    if not user:
        return not_found_response(message="User not found")
    return success_response(data=user) 