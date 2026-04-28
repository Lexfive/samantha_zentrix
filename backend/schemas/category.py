from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreate(BaseModel):
    name:  str = Field(min_length=1, max_length=100)
    color: str = Field(default="#6366f1", pattern=r"^#[0-9a-fA-F]{6}$")


class CategoryUpdate(BaseModel):
    name:  Optional[str] = Field(default=None, min_length=1, max_length=100)
    color: Optional[str] = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")


class CategoryResponse(BaseModel):
    id:      int
    name:    str
    color:   str
    user_id: int

    model_config = {"from_attributes": True}
