from app.models import CreateUpdateMixin
from datetime import date, datetime

class User(CreateUpdateMixin):
    name: str
    email: str
    gender: str
    phone_number: str
    age: int
    password: str

