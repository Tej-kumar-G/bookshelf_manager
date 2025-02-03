from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    full_name: str
    password: str  # Note: For real-world apps, hash passwords!
