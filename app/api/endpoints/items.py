from typing import List, Optional
from fastapi import APIRouter, HTTPException, status

from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()

# Simple in-memory items database
items_db = [
    {"id": 1, "name": "Item 1", "description": "This is item 1", "price": 50.0},
    {"id": 2, "name": "Item 2", "description": "This is item 2", "price": 30.0},
]

@router.get("/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 100):
    """
    Retrieve all items with pagination.
    """
    return items_db[skip : skip + limit]

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """
    Create a new item.
    """
    new_id = max([i.get("id", 0) for i in items_db]) + 1
    new_item = Item(id=new_id, **item.model_dump())
    items_db.append(new_item.model_dump())
    return new_item

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """
    Get a specific item by ID.
    """
    item = next((i for i in items_db if i.get("id") == item_id), None)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Item with ID {item_id} not found"
        )
    return item

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    """
    Update an existing item.
    """
    item_idx = next((idx for idx, i in enumerate(items_db) if i.get("id") == item_id), None)
    if item_idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Item with ID {item_id} not found"
        )
    
    update_data = item.model_dump(exclude_unset=True)
    current_item = items_db[item_idx]
    updated_item = {**current_item, **update_data}
    items_db[item_idx] = updated_item
    return updated_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    Delete an item.
    """
    item_idx = next((idx for idx, i in enumerate(items_db) if i.get("id") == item_id), None)
    if item_idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Item with ID {item_id} not found"
        )
    
    items_db.pop(item_idx)
    return None 