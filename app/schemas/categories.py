from pydantic import BaseModel, Field
from typing import Optional
from app.schemas import CreateUpdateMixin

class CreateCategory(BaseModel):
    name: str = Field(..., examples=["Fiction"])
    description: str = Field(..., examples=["Fictional books and stories."])

class UpdateCategory(BaseModel):
    name: Optional[str] = Field(None, examples=["Non-Fiction"])
    description: Optional[str] = Field(None, examples=["Real stories and factual content."])

class CategoryResponse(CreateUpdateMixin):
    name: str = Field(..., examples=["Fiction"])
    description: str = Field(..., examples=["Fictional books and stories."])

class BaseCategoryResponse(BaseModel):
    id: str = Field(..., examples=["60d0fe4f5311236168a109ca"])
    name: str = Field(..., examples=["Fiction"])
