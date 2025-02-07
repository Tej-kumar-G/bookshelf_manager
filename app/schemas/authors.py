# app/schemas/authors.py
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas import CreateUpdateMixin

class CreateAuthor(BaseModel):
    name: str = Field(..., examples=["Mark Twain"])
    age: int = Field(..., examples=[45])
    gender: str = Field(..., examples=["Male"])
    # You can include additional fields if required (e.g., biography)

class AuthorResponse(CreateUpdateMixin):
    name: str = Field(..., examples=["Mark Twain"])
    age: int = Field(..., examples=[45])
    gender: str = Field(..., examples=["Male"])
    latest_books: List[dict] = Field(default_factory=list, examples=[[{"id": "bookid1", "name": "Book Title"}]])
    total_published: int = Field(0, examples=[10])

class UpdateAuthor(BaseModel):
    name: Optional[str] = Field(None, examples=["Samuel Clemens"])
    age: Optional[int] = Field(None, examples=[46])
    gender: Optional[str] = Field(None, examples=["Male"])

class BaseAuthorResponse(BaseModel):
    id: str = Field(..., examples=["60d0fe4f5311236168a109ca"])
    name: str = Field(..., examples=["Mark Twain"])
