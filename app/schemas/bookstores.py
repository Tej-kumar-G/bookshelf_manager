from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas import CreateUpdateMixin

class CreateBookstore(BaseModel):
    name: str = Field(..., examples=["Barnes & Noble"])
    location: str = Field(..., examples=["New York, USA"])

class UpdateBookstore(BaseModel):
    name: Optional[str] = Field(None, examples=["Barnes & Noble Updated"])
    location: Optional[str] = Field(None, examples=["Los Angeles, USA"])

class BookstoreResponse(CreateUpdateMixin):
    name: str = Field(..., examples=["Barnes & Noble"])
    location: str = Field(..., examples=["New York, USA"])
    books: List[dict] = Field(default_factory=list, examples=[[{"id": "book_id", "name": "Book Title"}]])

class BaseBookstoreResponse(BaseModel):
    id: str = Field(..., examples=["60d0fe4f5311236168a109ca"])
    name: str = Field(..., examples=["Barnes & Noble"])
