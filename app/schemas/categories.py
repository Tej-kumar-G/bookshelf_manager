from pydantic import BaseModel, Field
from typing import Optional

# Schema for creating a category
class CategoryCreate(BaseModel):
    name: str = Field(..., examples=["Fiction"])

# Schema for updating a category
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, examples=["Historical Fiction"])

# Schema for category response
class CategoryResponse(BaseModel):
    id: str = Field(..., examples=["6769be7156ca61f944fa3f90"])
    name: str = Field(..., examples=["Fiction"])
