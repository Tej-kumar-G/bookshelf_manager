from pydantic import BaseModel, Field
from datetime import datetime

class Publisher(BaseModel):
    name: str
    location: str
    created_at: datetime
    updated_at: datetime
