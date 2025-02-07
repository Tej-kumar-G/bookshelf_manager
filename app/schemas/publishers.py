from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas import CreateUpdateMixin

class CreatePublisher(BaseModel):
    name: str = Field(..., examples=["Penguin Random House"])
    location: str = Field(..., examples=["New York, USA"])

class UpdatePublisher(BaseModel):
    name: Optional[str] = Field(None, examples=["Penguin Random House"])
    location: Optional[str] = Field(None, examples=["Los Angeles, USA"])

class PublisherResponse(CreateUpdateMixin):
    name: str = Field(..., examples=["Penguin Random House"])
    location: str = Field(..., examples=["New York, USA"])
    books: List[dict] = Field(default_factory=list, examples=[[{"id": "book_id", "name": "Book Title"}]])

class BasePublisherResponse(BaseModel):
    id: str = Field(..., examples=["60d0fe4f5311236168a109ca"])
    name: str = Field(..., examples=["Penguin Random House"])
