# app/schemas/reviews.py
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas import CreateUpdateMixin

class CreateReview(BaseModel):
    content: str = Field(..., examples=["An outstanding work of literature!"])
    rating: int = Field(..., examples=[5])
    created_by_id: str = Field(..., examples=["67a62fab1c388e002d06805d"])  # sample user id
    book_id: str = Field(..., examples=["67a5c096118d563cb5900e18"])        # sample book id

class UpdateReview(BaseModel):
    content: Optional[str] = Field(None, examples=["A timeless classic that leaves a lasting impression."])
    rating: Optional[int] = Field(None, examples=[5])

class ReviewResponse(CreateUpdateMixin):
    content: str = Field(..., examples=["An outstanding work of literature!"])
    rating: int = Field(..., examples=[5])
    created_by: dict = Field(..., examples=[{"id": "67a62fab1c388e002d06805d", "name": "John Doe"}])
    book: dict = Field(..., examples=[{"id": "67a5c096118d563cb5900e18", "name": "Harry Potter and the Chamber of Secrets"}])

class BaseReviewResponse(BaseModel):
    id: str = Field(..., examples=["67a5c0b0118d563cb5900e1a"])
    content: str = Field(..., examples=["An outstanding work of literature!"])
