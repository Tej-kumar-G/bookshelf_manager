# app/schemas/books.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas import CreateUpdateMixin

class CreateBook(BaseModel):
    name: str = Field(..., examples=["Harry Potter and the Chamber of Secrets"])
    description: str = Field(..., examples=["A magical adventure about Harry and his friends."])
    author_id: str = Field(..., examples=["67a5bcc7118d563cb5900e03"])
    category_id: str = Field(..., examples=["67a5bf89a6a8b01028544ca7"])
    publisher_id: Optional[str] = Field(None, examples=["67a5bd2c118d563cb5900e0a"])

class UpdateBook(BaseModel):
    name: Optional[str] = Field(None, examples=["Harry Potter and the Chamber of Secrets (Updated)"])
    description: Optional[str] = Field(None, examples=["An updated magical adventure."])
    author_id: Optional[str] = Field(None, examples=["67a5bcc7118d563cb5900e03"])
    category_id: Optional[str] = Field(None, examples=["67a5bf89a6a8b01028544ca7"])
    publisher_id: Optional[str] = Field(None, examples=["67a5bd2c118d563cb5900e0a"])

class BookResponse(CreateUpdateMixin):
    name: str = Field(..., examples=["Harry Potter and the Chamber of Secrets"])
    description: str = Field(..., examples=["A magical adventure about Harry and his friends."])
    author: dict = Field(..., examples=[{"id": "67a5bcc7118d563cb5900e03", "name": "James"}])
    category: dict = Field(..., examples=[{"id": "67a5bf89a6a8b01028544ca7", "name": "Fiction"}])
    publisher: Optional[dict] = Field(None, examples=[{"id": "67a5bd2c118d563cb5900e0a", "name": "Penguin Random House"}])
    is_published: bool = Field(..., examples=[True])
    average_rating: Optional[float] = Field(None, examples=[4.5])
    total_reviews: Optional[int] = Field(None, examples=[150])

class BaseBookResponse(BaseModel):
    id: str = Field(..., examples=["67a5f946ec61bfa6a3c2d7c7"])
    name: str = Field(..., examples=["Harry Potter and the Chamber of Secrets"])
