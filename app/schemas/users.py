# app/schemas/users.py
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from app.schemas import CreateUpdateMixin

class CreateUser(BaseModel):
    name: str = Field(..., examples=["Alice Smith"])
    email: EmailStr = Field(..., examples=["alice.smith@example.com"])
    gender: str = Field(..., examples=["Female"])
    phone_number: str = Field(..., examples=["+12345678901"])
    age: int = Field(..., examples=[28])
    password: str = Field(..., examples=["strongpassword123"])

class UserResponse(CreateUpdateMixin):
    name: str = Field(..., examples=["Alice Smith"])
    email: EmailStr = Field(..., examples=["alice.smith@example.com"])
    gender: str = Field(..., examples=["Female"])
    phone_number: str = Field(..., examples=["+12345678901"])
    age: int = Field(..., examples=[28])
    total_reviews: int = Field(0, examples=[5])

class UpdateUser(BaseModel):
    name: Optional[str] = Field(None, examples=["Alice Smith"])
    email: Optional[EmailStr] = Field(None, examples=["alice.new@example.com"])
    gender: Optional[str] = Field(None, examples=["Female"])
    phone_number: Optional[str] = Field(None, examples=["+12345678902"])
    age: Optional[int] = Field(None, examples=[29])

class BaseUserResponse(BaseModel):
    id: str = Field(..., examples=["60d0fe4f5311236168a109ca"])
    name: str = Field(..., examples=["Alice Smith"])
