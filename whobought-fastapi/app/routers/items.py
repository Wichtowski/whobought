from fastapi import APIRouter, HTTPException, Depends, status, Body, Request
from typing import List
from fastapi.responses import JSONResponse

from ..models import Item
from ..database import ItemsDB
from ..dependencies import get_db
from ..responses import success_response, error_response, not_found_response, created_response

router = APIRouter(
    prefix="/api/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_items(request: Request, db=Depends(get_db)):
    try:
        items = await ItemsDB.get_all_items()
        return success_response(data=items)
    except Exception as e:
        return error_response(message=f"Database error: {str(e)}")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item, db=Depends(get_db)):
    try:
        created_item = await ItemsDB.create_item(item.dict())
        return created_response(data=created_item)
    except Exception as e:
        return error_response(message=f"Database error: {str(e)}")

@router.get("/{item_id}")
async def get_item(item_id: str, db=Depends(get_db)):
    item = await ItemsDB.get_item(item_id)
    if not item:
        return not_found_response(message="Item not found")
    return success_response(data=item)

@router.put("/{item_id}")
async def update_item(item_id: str, item: Item, db=Depends(get_db)):
    updated_item = await ItemsDB.update_item(item_id, item.dict())
    if not updated_item:
        return not_found_response(message="Item not found")
    return success_response(
        data=updated_item,
        message="Item updated successfully"
    )

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_item(item_id: str, db=Depends(get_db)):
    success = await ItemsDB.delete_item(item_id)
    if not success:
        return not_found_response(message="Item not found")
    return success_response(message="Item deleted successfully") 