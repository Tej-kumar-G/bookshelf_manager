from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class Bookstore(BaseModel):
    name: str
    location: str
    book_ids: List[str] = []  # store only book ids
    created_at: datetime
    updated_at: datetime