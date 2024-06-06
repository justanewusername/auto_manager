from pydantic import BaseModel
from database_manager import DatabaseManager
from fastapi import status, HTTPException
from fastapi import APIRouter
from schemas import *

# class Item(BaseModel):
#     name: str

# class ItemNumber(BaseModel):
#     number: int

router = APIRouter(prefix="/favorites")

@router.get("/")
async def get_all_favorites():
    databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
    result = databaseManager.get_all_posts()
    return result


@router.post("/create")
async def create_item(item: ItemNumber):
    try:
        databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
        result = databaseManager.add_to_favorites(item.number)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return result


@router.post("/del")
async def create_item(item: ItemNumber):
    try:
        databaseManager = DatabaseManager("postgresql://user:qwerty@db:5432/mydbname")
        result = databaseManager.delete_from_favorites(item.number)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post found with id {item.number} in favorites")
    return result
