from pydantic import BaseModel, Field
from datetime import datetime

class Category(BaseModel):
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
  