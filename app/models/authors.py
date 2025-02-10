# app/models/authors.py
from pydantic import BaseModel, Field
from datetime import datetime

class Author(BaseModel):
    name: str
    age: int
    gender: str
    # password: str  # if needed, otherwise omit this field for authors
    # In many cases you may want to include additional fields like biography, etc.
    created_at: datetime
    updated_at: datetime