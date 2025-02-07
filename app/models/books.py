# app/models/books.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Book(BaseModel):
    name: str
    description: str
    author_id: str
    category_id: str
    publisher_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
