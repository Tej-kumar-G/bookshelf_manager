from pydantic import BaseModel

class Review(BaseModel):
    book_id: str
    content: str
    rating: int
