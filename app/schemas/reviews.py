from pydantic import BaseModel, Field
from typing import Optional

class ReviewCreate(BaseModel):
    content: str = Field(..., examples=["A captivating story with deep symbolism."])
    rating: int = Field(..., examples=[5])

class ReviewUpdate(BaseModel):
    content: Optional[str] = Field(None, examples=["An exceptional novel with rich storytelling."])
    rating: Optional[int] = Field(None, examples=[4])

class ReviewResponse(BaseModel):
    id: str = Field(..., examples=["9876fd7156ca61f944fa3f91"])
    book_id: str = Field(..., examples=["6769be7156ca61f944fa3f90"])
    content: str = Field(..., examples=["A captivating story with deep symbolism."])
    rating: int = Field(..., examples=[5])
