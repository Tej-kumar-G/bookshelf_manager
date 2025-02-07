# app/schemas/__init__.py
from pydantic import BaseModel, Field
from datetime import datetime

class CreateUpdateMixin(BaseModel):
    id: str = Field(..., examples=['60d0fe4f5311236168a109ca'])
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
