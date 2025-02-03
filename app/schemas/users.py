from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., examples=["john_doe"])
    email: str = Field(..., examples=["john@example.com"])
    full_name: str = Field(..., examples=["John Doe"])
    password: str = Field(..., examples=["securepassword123"])

class UserUpdate(BaseModel):
    email: Optional[str] = Field(None, examples=["new_john@example.com"])
    full_name: Optional[str] = Field(None, examples=["John Doe"])

class UserResponse(BaseModel):
    id: str = Field(..., examples=["6769be7156ca61f944fa3f90"])
    username: str
    email: str
    full_name: str
