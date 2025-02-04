from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class AuthorCreate(BaseModel):
    first_name: str = Field(..., examples=["George"])
    last_name: str = Field(..., examples=["Orwell"])
    bio: Optional[str] = Field(None, examples=["British writer famous for '1984' and 'Animal Farm'."])
    birth_date: Optional[date] = Field(None, examples=["1903-06-25"])
    nationality: Optional[str] = Field(None, examples=["British"])

class AuthorUpdate(BaseModel):
    first_name: Optional[str] = Field(None, examples=["George"])
    last_name: Optional[str] = Field(None, examples=["Orwell"])
    bio: Optional[str] = Field(None, examples=["British writer famous for '1984' and 'Animal Farm'."])
    birth_date: Optional[date] = Field(None, examples=["1903-06-25"])
    nationality: Optional[str] = Field(None, examples=["British"])

class AuthorResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    bio: Optional[str]
    birth_date: Optional[date]
    nationality: Optional[str]
