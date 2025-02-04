from pydantic import BaseModel, Field
from datetime import date, datetime

class Author(BaseModel):
    first_name: str
    last_name: str
    bio: str
    birth_date: date  # Keep this as date
    nationality: str

    def dict(self, *args, **kwargs):
        # Convert birth_date to string before saving to MongoDB
        data = super().dict(*args, **kwargs)
        data["birth_date"] = self.birth_date.isoformat()  # Convert to ISO string
        return data
