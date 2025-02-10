from typing import Optional, List, Any
from pydantic import BaseModel, Field

from app.schemas import CreateUpdateMixin


class CreateUser(BaseModel):
    name :str = Field(...,examples=["uday kiran reddy"])
    email: str = Field(..., examples = ["uday@zysec.ai"])
    gender: str  = Field(...,examples = ['udayreddy_26'])
    phone_number: str  = Field(...,examples = ['udayreddy_26'])
    age: int = Field(...,examples = [24])
    password: str = Field(...,examples = ['strongpassword123'])
    
class UserResponse(CreateUpdateMixin):
    name :str = Field(...,examples=["uday kiran reddy"])
    email: str = Field(..., examples = ["uday@zysec.ai"])
    gender: str  = Field(...,examples = ['udayreddy_26'])
    phone_number: str  = Field(...,examples = ['udayreddy_26'])
    age: int = Field(...,examples = [24])
    total_reviews: int = Field(0)


class UpdateUser(BaseModel):
    name :Optional[str] = Field(...,examples=["uday kiran reddy"])
    email: Optional[str] = Field(..., examples = ["uday@zysec.ai"])
    gender: Optional[str]  = Field(...,examples = ['udayreddy_26'])
    age: Optional[int] = Field(...,examples = [24])
    phone_number: Optional[str]  = Field(...,examples = ['udayreddy_26'])

class BaseUserResponse(BaseModel):
    id: str = Field(...)
    name: str = Field(...)






