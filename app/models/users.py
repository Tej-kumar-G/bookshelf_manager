# app/models/users.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class User(BaseModel):
    name: str
    email: EmailStr
    gender: str
    phone_number: str
    age: int
    password: str  # In production, store hashed passwords instead.
    total_reviews: int = 0
    created_at: datetime
    updated_at: datetime
