from typing import Optional
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base item schema with common attributes."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)


class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)


class Item(ItemBase):
    """Schema for a complete item with ID."""
    id: int
    
    class Config:
        from_attributes = True 