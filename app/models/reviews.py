from pydantic import BaseModel, Field
from datetime import datetime

class Review(BaseModel):
    content: str
    rating: int
    created_by_id: str
    book_id: str
    created_at: datetime
    updated_at: datetime